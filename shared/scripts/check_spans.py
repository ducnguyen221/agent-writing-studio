#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_spans.py — CỔNG 0-TOKEN: bản tự khai của trục 2 có còn trỏ đúng câu không?

Không gọi mô hình, không sửa file, không in nội dung ra ngoài trừ trích ngắn để người đọc định vị.

VÌ SAO CÓ FILE NÀY. `draft.schema.json` chỉ kiểm HÌNH DẠNG của `machine_written_spans[]`: mỗi phần tử
có `sentence_id` và `origin`. Nó không biết `sentence_id` ấy có tồn tại trong văn bản cuối hay không.
Hai đường hỏng đã gặp thật:

  1. **Sửa sau khi đã ghi meta.** Người dùng xin đổi hai đoạn, `sentence_id` từ chỗ đó trở đi dịch
     hết. Bản tự khai vẫn "hợp lệ" mà trỏ sai câu (ghi chú thực thi Phase 5, mục "chỗ trục 2 dễ quên
     tự khai nhất").
  2. **Bộ tách câu nuốt câu.** Ca `.work/cot-b-ai-baitap`: ngưỡng `min_chars=15` bỏ hai câu hỏi tu từ
     ngắn, nên bản tự khai phủ 45/47 câu và con số "45/45 do máy viết" là con số của script chứ không
     phải của văn bản (docs/results/self-audit-cot-B.md §2.1).

Cách chạy:

    python check_spans.py --meta .work/case/draft.meta.json --text .work/case/polished.md \
        [--sentences .work/case/sentences.json] [--strict]

`--sentences` (tuỳ chọn): so luôn file index trên đĩa với bản sinh lại từ `--text`. Lệch nghĩa là
index đã cũ, và mọi trục đọc nó đang trỏ sai.

`--strict`: coi câu CHƯA KHAI là lệch. Dùng khi bài được khai là 100% do máy viết. Mặc định KHÔNG
bật: câu không nằm trong `machine_written_spans[]` đọc là "do người viết", đó là trạng thái hợp lệ
của bài viết chung tay, không phải lỗi.

Mã thoát: 0 = khớp · 1 = có lệch (id không tồn tại, id trùng, index trên đĩa đã cũ, hoặc `--strict`
mà còn câu chưa khai).

VÙNG MÙ ĐÃ BIẾT: script so ID, không so nội dung. Nếu văn bản bị sửa mà số câu không đổi thì mọi ID
vẫn tồn tại và script báo khớp, trong khi bản tự khai đã trỏ sang câu khác. Chặn được chuyện đó cần
`draft.meta.json` giữ hash của văn bản tại lúc khai — chưa có trong schema, ghi lại ở đây để không ai
đọc "khớp" thành "đã chứng minh là đúng".
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTRACT_PATH = ROOT / "skills/05-forensics/scripts/extract.py"

EXIT_OK, EXIT_DRIFT = 0, 1


def load_extract(path=EXTRACT_PATH):
    spec = importlib.util.spec_from_file_location("forensics_extract", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Không nạp được extract.py bắt buộc: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def declared_spans(meta):
    """[(sentence_id, quote)] theo đúng thứ tự khai. Không im lặng bỏ qua khoá thiếu."""
    spans = meta.get("machine_written_spans")
    if spans is None:
        raise ValueError(
            "draft.meta.json thiếu `machine_written_spans` — trường này BẮT BUỘC CÓ MẶT, "
            "được phép rỗng. Rỗng là một khẳng định, vắng mặt là một chỗ trống."
        )
    if not isinstance(spans, list):
        raise ValueError("`machine_written_spans` phải là mảng.")
    out = []
    for item in spans:
        if not isinstance(item, dict) or "sentence_id" not in item:
            raise ValueError(f"Phần tử machine_written_spans không có sentence_id: {item!r}")
        out.append((item["sentence_id"], item.get("quote")))
    return out


def _looks_like_a_stale_index(declared_ids, sentences, undeclared):
    """Cảnh báo cho vùng mù: id còn đủ nhưng bản tự khai là của một index CŨ.

    Dấu hiệu: id đã khai là đúng khúc ĐẦU của index hiện tại, và mọi câu chưa khai nằm gọn ở khúc
    CUỐI. Khi bộ tách câu chèn thêm câu ở giữa (ca `.work/cot-b-ai-baitap`: hai câu hỏi tu từ ngắn
    được trả lại), mọi id từ chỗ chèn trở đi dịch đi — không id nào biến mất, nên phép so tập ID báo
    'khớp' trong khi từng nhãn đã trỏ sang câu bên cạnh.
    """
    if not undeclared or not declared_ids:
        return False
    all_ids = [item["id"] for item in sentences]
    prefix = all_ids[: len(declared_ids)]
    tail = set(all_ids[len(declared_ids):])
    return declared_ids == prefix and {item["id"] for item in undeclared} == tail


def compare(spans, sentences):
    """Đối chiếu id đã khai với index câu sinh lại từ văn bản đích."""
    index = {item["id"]: item for item in sentences}
    declared_ids = [sentence_id for sentence_id, _ in spans]
    seen, duplicates = set(), []
    for sentence_id in declared_ids:
        if sentence_id in seen:
            duplicates.append(sentence_id)
        seen.add(sentence_id)
    unknown = [sentence_id for sentence_id in declared_ids if sentence_id not in index]
    undeclared = [item for item in sentences if item["id"] not in seen]
    # `quote` là tuỳ chọn trong draft.schema.json; khai thì đối chiếu được nội dung, không chỉ ID.
    quote_mismatch = []
    for sentence_id, quote in spans:
        if not quote or sentence_id not in index:
            continue
        if quote.strip() not in index[sentence_id]["text"]:
            quote_mismatch.append(
                {"id": sentence_id, "declared": quote[:60], "actual": index[sentence_id]["text"][:60]}
            )
    return {
        "sentences_total": len(sentences),
        "declared_total": len(declared_ids),
        "unknown_ids": unknown,
        "duplicate_ids": duplicates,
        "quote_mismatch": quote_mismatch,
        "stale_index_suspected": _looks_like_a_stale_index(declared_ids, sentences, undeclared),
        "undeclared": [
            {
                "id": item["id"],
                "short": bool(item.get("short")),
                "quote": item["text"][:80],
            }
            for item in undeclared
        ],
    }


def compare_disk_index(sentences, disk):
    """Index trên đĩa so với bản sinh lại: số câu, id và nội dung phải trùng."""
    problems = []
    if len(disk) != len(sentences):
        problems.append(
            f"sentences.json trên đĩa có {len(disk)} câu, sinh lại từ văn bản đích ra "
            f"{len(sentences)} câu — index đã cũ, mọi trục đang đọc id sai."
        )
        return problems
    for fresh, old in zip(sentences, disk):
        if fresh["id"] != old.get("id") or fresh["text"] != old.get("text"):
            problems.append(
                f"Câu {fresh['id']} khác bản trên đĩa ({old.get('id')}): index đã cũ."
            )
            break
    return problems


def render(result, problems, strict):
    lines = ["== check_spans · cổng 0-token, chỉ đối chiếu ID ==", ""]
    lines.append(f"Câu trong văn bản đích : {result['sentences_total']}")
    lines.append(f"Câu đã khai machine    : {result['declared_total']}")
    lines.append(f"ID khai mà không có    : {len(result['unknown_ids'])}")
    lines.append(f"ID khai trùng nhau     : {len(result['duplicate_ids'])}")
    lines.append(f"Câu CHƯA KHAI          : {len(result['undeclared'])}")
    lines.append("")
    if result["unknown_ids"]:
        lines.append(
            "[LỆCH] Bản tự khai trỏ tới id không có trong văn bản đích: "
            + ", ".join(result["unknown_ids"][:20])
        )
        lines.append(
            "       Nguyên nhân hay gặp: văn bản đã sửa sau khi ghi meta. Sinh lại "
            "sentences.json rồi khai lại theo id mới, đừng sửa tay từng số."
        )
    if result["duplicate_ids"]:
        lines.append("[LỆCH] ID khai hai lần: " + ", ".join(result["duplicate_ids"][:20]))
    for item in result["quote_mismatch"]:
        lines.append(
            f"[LỆCH] {item['id']} khai trích dẫn không có trong câu đó. "
            f"Khai: {item['declared']!r} · Thực tế: {item['actual']!r}"
        )
    if result["stale_index_suspected"]:
        lines.append(
            "[NGHI INDEX CŨ] Id đã khai phủ đúng khúc ĐẦU của index và mọi câu chưa khai nằm gọn ở "
            "khúc CUỐI. Dáng này là dáng của bản tự khai viết theo một index cũ hơn: câu được chèn "
            "thêm ở giữa đẩy mọi id phía sau dịch đi, nên từng nhãn có thể đang trỏ sang câu bên "
            "cạnh dù không id nào biến mất. Sinh lại sentences.json rồi khai lại, đừng đọc con số "
            "'chưa khai' bên trên như thể chỉ thiếu mấy câu cuối."
        )
    if result["undeclared"]:
        head = "[LỆCH]" if strict else "[CHƯA KHAI]"
        lines.append(
            f"{head} {len(result['undeclared'])} câu không có trong machine_written_spans[]. "
            "Mặc định đọc là 'do người viết'; bài khai 100% do máy thì đây là câu bị bỏ sót."
        )
        for item in result["undeclared"][:20]:
            mark = " (câu ngắn)" if item["short"] else ""
            lines.append(f"       · {item['id']}{mark}: {item['quote']}")
    for problem in problems:
        lines.append(f"[LỆCH] {problem}")
    clean = (
        not problems
        and not result["unknown_ids"]
        and not result["duplicate_ids"]
        and not result["quote_mismatch"]
    )
    if clean and not result["undeclared"]:
        lines.append("Khớp: mọi id đã khai đều có thật, và mọi câu đều được khai.")
    lines.append("")
    lines.append(
        "Script so ID, không so nội dung: 'khớp' nghĩa là không phát hiện lệch, không phải "
        "đã chứng minh bản tự khai đúng."
    )
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Đối chiếu machine_written_spans[] với sentences.json sinh lại từ văn bản đích"
    )
    parser.add_argument("--meta", required=True, help="draft.meta.json của trục 2")
    parser.add_argument("--text", required=True, help="văn bản đích (draft.md hoặc polished.md)")
    parser.add_argument("--sentences", help="sentences.json trên đĩa; có thì so với bản sinh lại")
    parser.add_argument("--strict", action="store_true", help="câu chưa khai cũng tính là lệch")
    parser.add_argument("--out", help="ghi kết quả đối chiếu ra file JSON")
    args = parser.parse_args(argv)

    extract = load_extract()
    meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
    text = Path(args.text).read_text(encoding="utf-8")
    sentences = extract.sentences(text)
    result = compare(declared_spans(meta), sentences)

    problems = []
    if args.sentences:
        disk = json.loads(Path(args.sentences).read_text(encoding="utf-8"))
        problems += compare_disk_index(sentences, disk)

    drift = bool(
        result["unknown_ids"] or result["duplicate_ids"] or result["quote_mismatch"] or problems
    )
    if args.strict and result["undeclared"]:
        drift = True

    if args.out:
        payload = dict(result)
        payload["disk_index_problems"] = problems
        payload["strict"] = bool(args.strict)
        payload["drift"] = drift
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(render(result, problems, args.strict))
    return EXIT_DRIFT if drift else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
