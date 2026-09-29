#!/usr/bin/env python3
"""agent-writing-studio — doctor · install · update · uninstall.

Chạy bằng Python 3.10 trở lên, **chỉ thư viện chuẩn**, trên Windows và macOS (Linux cũng được):

    python studio.py doctor              # kiểm, không sửa gì
    python studio.py install [--station PATH] [--host claude] [--dry-run]
    python studio.py update  [--yes]     # git pull --ff-only, từ chối khi checkout có sửa dở
    python studio.py uninstall [--host claude]

Repo này không có engine: skill là văn bản agent đọc, script trong `shared/` và `skills/*/scripts/`
chỉ là lớp kiểm chứng. Vì vậy bộ vòng đời cố ý mỏng:

- **install** chỉ dựng thư mục dữ liệu (workspace `.work/` trong repo, hoặc station ngoài repo khi
  có `WRITING_STUDIO_DATA` / `--station`) rồi **in** lệnh đăng ký plugin cho host. Nó không tự sửa
  cấu hình của Claude, Codex hay Antigravity — người dùng hoặc agent chạy lệnh in ra, sau khi đọc.
- **uninstall** chỉ in lệnh gỡ plugin. Nó **không bao giờ xoá dữ liệu**: `.work/`, station và kho
  tri thức là của người dùng.
- **doctor** báo từng dòng `PASS` / `WARN` / `FAIL` / `NOT_CHECKED`. Thiếu thư viện tuỳ chọn là
  `WARN`, không phải `FAIL`; thứ không kiểm được thì nói `NOT_CHECKED`, không tô xanh.

Mã thoát: 0 = không có `FAIL` · 1 = có `FAIL` · 2 = từ chối làm (tham số sai, checkout có sửa dở,
đích ghi nằm trong cây source).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "agent-writing-studio"
MIN_PYTHON = (3, 10)

STATION_ENV = "WRITING_STUDIO_DATA"
KNOWLEDGE_ENV = "WRITING_STUDIO_KNOWLEDGE"
LEGACY_KNOWLEDGE_ENV = "OPCOS_BRAIN_PATH"  # đường lùi cho máy dựng trước 0.3.0, bỏ ở 0.4

WORKSPACE = ROOT / ".work"
STATION_DIRS = ("work", "out", "corpus")

AXES = ("01-context-architect", "02-cowriter", "03-critique", "04-humanizer", "05-forensics")
SUB_SKILLS = ("05a-reading", "05b-scoring", "05c-reporting", "05d-calibration")
COMMANDS = ("01-context", "02-draft", "03-critique", "04-humanize", "05-audit", "deliver-docx", "list")
GENRE_COUNT = 9

VERSION_FILES = (".claude-plugin/plugin.json", ".codex-plugin/plugin.json")
MARKETPLACE = ".claude-plugin/marketplace.json"
CITATION = "CITATION.cff"

OPTIONAL_LIBS = (
    ("jsonschema", "jsonschema", "kiểm schema của samples/ và test"),
    ("yaml", "PyYAML", "đọc hồ sơ thể loại, dựng hồ sơ giọng"),
    ("underthesea", "underthesea", "tách từ tiếng Việt cho bộ đếm (thiếu thì đo ở mức âm tiết)"),
    ("docx", "python-docx", "giao bản .docx"),
)

HOSTS = ("claude", "codex", "antigravity", "claude-desktop")

EXIT_OK, EXIT_FAIL, EXIT_REFUSED = 0, 1, 2
PASS, WARN, FAIL, NOT_CHECKED = "PASS", "WARN", "FAIL", "NOT_CHECKED"


# ── phân giải đường dữ liệu ─────────────────────────────────────────────────────────────

def env_path(name: str) -> Path | None:
    value = (os.environ.get(name) or "").strip()
    return Path(value).expanduser() if value else None


def resolve_data(station_arg: str | None = None) -> tuple[str, Path]:
    """(chế độ, gốc dữ liệu). Thứ tự: --station → WRITING_STUDIO_DATA → workspace `.work/` trong repo.

    Không có mặc định nào đoán trong thư mục home: không đặt gì là workspace trong repo.
    """
    if station_arg:
        return "station", Path(station_arg).expanduser()
    station = env_path(STATION_ENV)
    if station:
        return "station", station
    return "workspace", WORKSPACE


def resolve_knowledge() -> tuple[str | None, Path | None]:
    for name in (KNOWLEDGE_ENV, LEGACY_KNOWLEDGE_ENV):
        path = env_path(name)
        if path:
            return name, path
    return None, None


def inside_source_tree(path: Path) -> bool:
    """Đích ghi nằm trong cây source mà không phải workspace `.work/` ⇒ từ chối."""
    try:
        resolved = path.resolve()
        resolved.relative_to(ROOT)
    except ValueError:
        return False
    try:
        resolved.relative_to(WORKSPACE.resolve())
        return False
    except ValueError:
        return True


# ── doctor ──────────────────────────────────────────────────────────────────────────────

def manifest_versions(root: Path = ROOT) -> dict[str, str | None]:
    found: dict[str, str | None] = {}
    for rel in VERSION_FILES:
        found[rel] = json.loads((root / rel).read_text(encoding="utf-8")).get("version")
    market = json.loads((root / MARKETPLACE).read_text(encoding="utf-8"))
    for plugin in market.get("plugins") or []:
        found[f"{MARKETPLACE}#{plugin.get('name')}"] = plugin.get("version")
    match = re.search(r"(?m)^version:\s*\"?([^\"\s]+)\"?\s*$",
                      (root / CITATION).read_text(encoding="utf-8"))
    found[CITATION] = match.group(1) if match else None
    return found


def check_python():
    ok = sys.version_info[:2] >= MIN_PYTHON
    version = ".".join(map(str, sys.version_info[:3]))
    return (PASS if ok else FAIL, "python",
            version if ok else f"{version} — cần {MIN_PYTHON[0]}.{MIN_PYTHON[1]} trở lên")


def check_layout():
    missing = [f"skills/{a}/SKILL.md" for a in AXES if not (ROOT / "skills" / a / "SKILL.md").is_file()]
    missing += [f"skills/05-forensics/{s}/SKILL.md" for s in SUB_SKILLS
                if not (ROOT / "skills" / "05-forensics" / s / "SKILL.md").is_file()]
    missing += [f"commands/{c}.md" for c in COMMANDS if not (ROOT / "commands" / f"{c}.md").is_file()]
    if missing:
        return FAIL, "repo", "thiếu " + ", ".join(missing)
    return PASS, "repo", f"{len(AXES) + len(SUB_SKILLS)} skill · {len(COMMANDS)} lệnh"


def check_manifests():
    try:
        found = manifest_versions()
    except (OSError, ValueError) as error:
        return FAIL, "manifest", f"không đọc được: {error}"
    values = set(found.values())
    if None in values or len(values) != 1:
        return FAIL, "manifest", "phiên bản lệch: " + json.dumps(found, ensure_ascii=False)
    return PASS, "manifest", f"{values.pop()} ở {len(found)} chỗ khai"


def check_genres():
    genres = sorted(p for p in (ROOT / "shared" / "genres").glob("*.md") if not p.name.startswith("_"))
    if len(genres) != GENRE_COUNT:
        return FAIL, "genres", f"có {len(genres)} hồ sơ, cần {GENRE_COUNT}"
    if importlib.util.find_spec("yaml") is None:
        return NOT_CHECKED, "genres", f"{len(genres)} hồ sơ; chưa có PyYAML nên chưa đọc thử khối yaml"
    import yaml

    broken = []
    for path in genres:
        blocks = re.findall(r"(?ms)^```yaml\r?\n(.*?)^```", path.read_text(encoding="utf-8"))
        try:
            if not blocks:
                raise ValueError("không có khối yaml")
            for block in blocks:
                yaml.safe_load(block)
        except (ValueError, yaml.YAMLError):
            broken.append(path.name)
    if broken:
        return FAIL, "genres", "khối yaml hỏng: " + ", ".join(broken)
    return PASS, "genres", f"{len(genres)} hồ sơ đọc được"


def check_samples():
    folder = ROOT / "samples"
    pairs = (("context.json", "context.schema.json"), ("critique.expected.json", "critique.schema.json"))
    missing = [name for name, _ in pairs if not (folder / name).is_file()]
    if missing or not (folder / "bai-mau.md").is_file():
        return FAIL, "samples", "thiếu " + ", ".join(missing or ["bai-mau.md"])
    if importlib.util.find_spec("jsonschema") is None:
        return NOT_CHECKED, "samples", "chưa có jsonschema nên chưa kiểm schema"
    from jsonschema import Draft202012Validator

    problems = []
    for name, schema_name in pairs:
        schema = json.loads((ROOT / "shared" / "schemas" / schema_name).read_text(encoding="utf-8"))
        data = json.loads((folder / name).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(data))
        if errors:
            problems.append(f"{name}: {errors[0].message[:80]}")
    if problems:
        return FAIL, "samples", "; ".join(problems)
    return PASS, "samples", "bài mẫu + context + critique kỳ vọng hợp lệ theo schema (offline)"


def check_data():
    mode, root = resolve_data()
    if mode == "workspace":
        return PASS, "data", f"workspace {root} (mặc định; Git bỏ qua) — đặt {STATION_ENV} nếu muốn station riêng"
    if not root.is_dir():
        return WARN, "data", f"station {STATION_ENV}={root} chưa tồn tại — chạy `python studio.py install`"
    missing = [d for d in STATION_DIRS if not (root / d).is_dir()]
    if missing:
        return WARN, "data", f"station {root} thiếu {', '.join(missing)} — chạy `python studio.py install`"
    return PASS, "data", f"station {root}"


def check_knowledge():
    name, path = resolve_knowledge()
    if not name:
        return NOT_CHECKED, "knowledge", f"không có kho tri thức (tuỳ chọn; đặt {KNOWLEDGE_ENV} nếu có)"
    if not path.is_dir():
        return WARN, "knowledge", f"{name} trỏ tới thư mục không tồn tại"
    if name == LEGACY_KNOWLEDGE_ENV:
        return WARN, "knowledge", f"đang đọc tên biến cũ — đặt {KNOWLEDGE_ENV} (tên cũ bỏ ở 0.4)"
    return PASS, "knowledge", f"{KNOWLEDGE_ENV} đã đặt"


def check_optional_libs():
    rows = []
    for module, package, purpose in OPTIONAL_LIBS:
        if importlib.util.find_spec(module) is None:
            rows.append((WARN, f"lib:{package}", f"chưa cài — tuỳ chọn, dùng để {purpose}"))
        else:
            rows.append((PASS, f"lib:{package}", "có"))
    return rows


def check_claude_plugin():
    """Đọc sổ plugin của Claude Code (chỉ đọc). Không có sổ ⇒ NOT_CHECKED, không đoán."""
    ledger = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
    if not ledger.is_file():
        return NOT_CHECKED, "host:claude", "chưa thấy Claude Code trên máy này"
    try:
        data = json.loads(ledger.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return NOT_CHECKED, "host:claude", "không đọc được sổ plugin của Claude Code"
    plugins = data.get("plugins", data) if isinstance(data, dict) else {}
    installs = [entry for key, entries in plugins.items() if key.split("@")[0] == NAME
                for entry in (entries if isinstance(entries, list) else [entries])]
    if not installs:
        return NOT_CHECKED, "host:claude", "plugin chưa cài cho Claude Code — xem `python studio.py install`"
    wanted = manifest_versions()[VERSION_FILES[0]]
    have = sorted({str(entry.get("version")) for entry in installs if isinstance(entry, dict)})
    if have == [wanted]:
        return PASS, "host:claude", f"plugin {wanted}"
    return WARN, "host:claude", (f"plugin đang ở {', '.join(have)}, repo ở {wanted} — "
                                 f"chạy `claude plugin update {NAME}@{NAME}`")


def doctor_rows():
    rows = [check_python(), check_layout(), check_manifests(), check_genres(), check_samples(),
            check_data(), check_knowledge()]
    rows += check_optional_libs()
    rows.append(check_claude_plugin())
    rows.append((NOT_CHECKED, "host:codex", "kiểm bằng lệnh plugin của Codex đang cài (xem hosts/codex)"))
    return rows


def cmd_doctor(args) -> int:
    rows = doctor_rows()
    if args.json:
        print(json.dumps([{"status": s, "check": c, "detail": d} for s, c, d in rows],
                         ensure_ascii=False, indent=2))
    else:
        for status, check, detail in rows:
            print(f"{status:<12} {check:<22} {detail}")
    return EXIT_FAIL if any(status == FAIL for status, _, _ in rows) else EXIT_OK


# ── lệnh host (chỉ in, không chạy) ──────────────────────────────────────────────────────

def host_steps(host: str, action: str) -> list[str]:
    market = NAME
    ref = f"{NAME}@{market}"
    if host == "claude":
        return {
            "install": [
                "# Cài cố định (nạp từ GitHub, bản đã phát hành):",
                f"claude plugin marketplace add ducnguyen221/{NAME}",
                f"claude plugin install {ref}",
                "# Hoặc chạy thẳng từ checkout này, mỗi phiên một lần:",
                f'claude --plugin-dir "{ROOT}"',
            ],
            "update": [f"claude plugin marketplace update {market}", f"claude plugin update {ref}"],
            "uninstall": [f"claude plugin uninstall {ref}"],
        }[action]
    if host == "codex":
        return [
            "# Codex đọc .codex-plugin/plugin.json (skills: ./skills/).",
            "# Lệnh plugin khác nhau theo bản Codex — xem `codex plugin --help`, rồi làm theo hosts/codex/README.md.",
        ]
    if host == "antigravity":
        return ["# Antigravity: mở chính thư mục repo; agent đọc GEMINI.md → AGENTS.md → skills/<trục>/SKILL.md."]
    return ["# Claude Desktop (tab chat) không nạp skill từ repo — dùng Claude Code, Codex hoặc Antigravity."]


def cmd_install(args) -> int:
    mode, root = resolve_data(args.station)
    if mode == "station" and inside_source_tree(root):
        print(f"Từ chối: station {root} nằm trong cây source của repo. Chọn thư mục ngoài repo, "
              f"hoặc bỏ --station để dùng workspace {WORKSPACE}.", file=sys.stderr)
        return EXIT_REFUSED
    targets = [root] if mode == "workspace" else [root / d for d in STATION_DIRS]
    print(f"Dữ liệu: {mode} {root}")
    for target in targets:
        if target.is_dir():
            print(f"  giữ nguyên  {target}")
        elif args.dry_run:
            print(f"  sẽ tạo      {target}")
        else:
            target.mkdir(parents=True, exist_ok=True)
            print(f"  đã tạo      {target}")
    print(f"\nĐăng ký với {args.host} — chạy các lệnh dưới (installer không tự sửa cấu hình host):")
    for line in host_steps(args.host, "install"):
        print(f"  {line}")
    print("\nKiểm lại: python studio.py doctor")
    return EXIT_OK


def git(*argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(ROOT), *argv], capture_output=True, text=True,
                          encoding="utf-8")


def cmd_update(args) -> int:
    if not (ROOT / ".git").exists():
        print("Không phải bản checkout git — cập nhật qua plugin của host:", file=sys.stderr)
        for line in host_steps("claude", "update"):
            print(f"  {line}", file=sys.stderr)
        return EXIT_REFUSED
    status = git("status", "--porcelain", "--untracked-files=no")
    if status.returncode != 0:
        print(f"git status lỗi: {status.stderr.strip()}", file=sys.stderr)
        return EXIT_REFUSED
    if status.stdout.strip():
        print("Từ chối cập nhật: checkout có sửa dở chưa commit. Không reset, không stash thay bạn —"
              " commit hoặc cất thay đổi rồi chạy lại.", file=sys.stderr)
        return EXIT_REFUSED
    if not args.yes:
        print("Sẽ chạy: git pull --ff-only (thêm --yes để chạy). Sau đó cập nhật plugin của host:")
        for line in host_steps("claude", "update"):
            print(f"  {line}")
        return EXIT_OK
    pulled = git("pull", "--ff-only")
    print(pulled.stdout.strip() or pulled.stderr.strip())
    if pulled.returncode != 0:
        return EXIT_FAIL
    print("Tiếp theo — cập nhật plugin của host rồi mở phiên mới:")
    for line in host_steps("claude", "update"):
        print(f"  {line}")
    return EXIT_OK


def cmd_uninstall(args) -> int:
    print(f"Gỡ khỏi {args.host} — chạy các lệnh dưới:")
    for line in host_steps(args.host, "uninstall"):
        print(f"  {line}")
    mode, root = resolve_data()
    print(f"\nDữ liệu KHÔNG bị đụng: {mode} {root}"
          + (f"; kho tri thức {resolve_knowledge()[1]}" if resolve_knowledge()[0] else "")
          + ". Muốn xoá dữ liệu thì tự xoá, sau khi đã sao lưu.")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="studio.py", description="agent-writing-studio lifecycle")
    sub = parser.add_subparsers(dest="command", required=True)
    doctor = sub.add_parser("doctor", help="kiểm, không sửa gì")
    doctor.add_argument("--json", action="store_true", help="in dạng JSON cho máy đọc")
    install = sub.add_parser("install", help="dựng thư mục dữ liệu + in lệnh đăng ký host")
    install.add_argument("--station", help=f"station ngoài repo (mặc định: ${STATION_ENV}, rồi .work/)")
    install.add_argument("--host", choices=HOSTS, default="claude")
    install.add_argument("--dry-run", action="store_true", help="chỉ in, không tạo gì")
    update = sub.add_parser("update", help="git pull --ff-only khi checkout sạch")
    update.add_argument("--yes", action="store_true", help="chạy thật thay vì chỉ in")
    uninstall = sub.add_parser("uninstall", help="in lệnh gỡ plugin; không xoá dữ liệu")
    uninstall.add_argument("--host", choices=HOSTS, default="claude")
    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as exit_:
        return EXIT_REFUSED if exit_.code else EXIT_OK
    return {"doctor": cmd_doctor, "install": cmd_install, "update": cmd_update,
            "uninstall": cmd_uninstall}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
