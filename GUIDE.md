# Guide: one case through all five axes

**English** · [Tiếng Việt](GUIDE.vi.md)

This page walks **one piece of writing from start to finish**: context → draft → critique → humanize →
Word delivery → audit. Not installed yet? See [`INSTALL.md`](INSTALL.md). Want a ten-minute trial with a
ready-made sample first? See [`START-HERE.md`](START-HERE.md).

You **talk to the agent in plain Vietnamese** (the studio writes and reviews Vietnamese); the agent picks
the axis. Each step lists a sample request and the equivalent single-step command
(`/agent-writing-studio:<command>` in Claude Code; in other hosts, ask the agent to *read
`commands/<command>.md` and follow it*).

## 0. The case folder

Each piece gets a **case folder** with a short ASCII name, e.g. `bai-luan-ai`. It lives in:

- `workspace/bai-luan-ai/` inside the folder you opened — the default, no configuration, ignored by Git;
- or `$WRITING_STUDIO_DATA/work/bai-luan-ai/` if you set up a separate station.

The five axes talk **through the files in this folder**, never through chat memory — you can stop
halfway, open a new session tomorrow, or switch hosts without losing anything.

## 1. Context — `01-context` (axis Y1)

> *"Tôi cần viết một bài luận về việc dùng AI khi làm bài tập về nhà, cho giảng viên chấm. Dựng bối cảnh
> giúp tôi trước đã. Ca tên `bai-luan-ai`."* (I need an essay on using AI for homework, graded by a
> lecturer. Build the context first. Case name `bai-luan-ai`.)

The agent interviews you: the real brief, your thesis, the reader, the grader and rubric, the evidence
at hand. It reads section §1 of the genre profile (`shared/genres/essay.md`). With a personal knowledge
base (`WRITING_STUDIO_KNOWLEDGE`) it **points** to relevant documents; it never copies them.

**Writes:** `context.json`. **Gate:** open questions → the agent **stops and asks**; no step 2.

## 2. Draft — `02-draft` (axis Y2)

> *"Đã có `context.json` ở ca `bai-luan-ai`. Dựng dàn ý rồi viết nháp."*

The agent builds a **three-layer outline** and **waits for your approval**. Revise it as often as you
like; prose comes only after you agree. Every machine-written sentence is declared in
`draft.meta.json` — the provenance self-declaration that follows the text all the way to delivery.

**Writes:** `draft.md`, `draft.meta.json`, `sentences.json` (the shared sentence numbering).

## 3. Critique — `03-critique` (axis Y3)

> *"Chấm bản nháp ca `bai-luan-ai` theo hồ sơ `essay`, chỉ chỗ lập luận hổng."*

Each criterion is scored **separately** against the rubric in §3 of the genre profile, with fallacy
checks, a source-attribution check, and quoted evidence. **No total score.** `must_fix[]` says who fixes
what — you, or axis 4.

**Writes:** `critique.json`. Fix the substance (arguments, evidence) yourself here; axis 4 won't.

## 4. Humanize — `04-humanize` (axis Y4)

> *"Biên tập bản nháp ca `bai-luan-ai` về phía giọng của tôi, giữ nguyên số liệu và trích dẫn."*

The agent edits toward **your own voice** (your voice profile if you have one) and is forbidden to add
or drop facts or change claim strength. Three output modes: pasted text (signals → edited text → diff),
file (target file + diff beside it), embedded in a task. **Gate:** a fact added or dropped → the original
is returned.

**Writes:** `polished.md`, `polish.diff.json`, `polished.provenance.json` (travels with the delivery).

## 5. Deliver as Word — `deliver-docx`

> *"Giao bản docx của ca `bai-luan-ai` vào thư mục D:/bai-nop."*

The default delivery is `.docx` in standard Vietnamese document format (Times New Roman 13, 1.5 spacing,
margins 2/2/3/2 cm), written **exactly to the folder you name**, with the provenance file beside it.
Needs `python-docx`; if missing, the agent prints the install command. Markdown tables are not yet
converted to Word tables.

## 6. Audit — `05-audit` (axis Y5)

> *"Giám định ca `bai-luan-ai`."*

For text produced by the studio the default is **`audit`** mode: blind reading first, locked, then the
`draft.meta.json` self-declaration is checked against the text — the right question is *does the
declaration match*, not *can a machine guess*. **`blind`** mode (`--blind`) is for outside documents
with no declaration, and for calibration.

**Writes:** `evidence.json`, `report.md` — every finding with a counter-explanation and a verification
question. **No output is enough to accuse anyone**; the reasoning is in [README.vi.md §5](README.vi.md).

## Tips and limits

- **You rarely need all five axes.** Reviewing someone else's text: axis 3 (or 5) only. Already have
  your own draft: start at axis 3.
- **Missing input file:** the command says which file is missing and which command produces it; it does
  not re-run the chain on its own.
- **Genres:** `essay`, `research`, `blog`, `journalism`, `novel` (all five axes); `commentary`,
  `thesis-proposal`, `internship-report`, `teaching-initiative` (axis 5 only). New genre: [`docs/GENRES.md`](docs/GENRES.md).
- **Trouble:** `python studio.py doctor` (macOS: `python3.12`), then [`docs/troubleshooting.md`](docs/troubleshooting.md).
- List every command any time: `/agent-writing-studio:list`.
