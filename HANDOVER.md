# Handover entry point

Read AGENTS.md, constitution.md and README.md before resuming work. Preserve existing project-specific handover history and entry points.

## Handover format

Append one entry per completed bounded work package; do not invent current project status.

- Timestamp: ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`).
- Ticket and executor.
- Changes: concrete files and resulting behavior.
- Verification: exact command, exit status and evidence path.
- Open issues and next action.
- Local publication policy: `github_existing`.

Live portfolio status is generated in `C:/MyCodes/company/reports/project-standards.json`.


<!-- company-project-standard:v1 -->
## Company documentation standard

Read [PROJECT_STANDARDS.md](C:/MyCodes/company/docs/PROJECT_STANDARDS.md) for shared file formats and new-project templates.
Existing project requirements, storage contracts and model policies remain authoritative;
this reference does not migrate domain data or change those requirements.
Read AGENTS.md, constitution.md and HANDOVER.md before working. Record handovers with
evidence and UTC timestamps. Do not publish or create a remote for a local-only project.
<!-- /company-project-standard -->

## 2026-09-29T20:37:14Z — T-0059 (Codex)

Owner-authorized local generation policy migration: general summaries/answers now default to `gemma4:26b`; explicit allowed alternatives are validated by `C:/MyCodes/company/runner/local_ai_policy.py` before inference. Legacy arbitrary environment/model overrides fail closed. Shared policy availability is required; no independent fallback or package dependency was added.

Verification: `C:/MyCodes/reader/.venv/Scripts/python.exe tests/test_local_policy.py` from reader: 5 offline boundary tests PASS, exit 0, including this project. Reader `tests/test_stages.py`: 19 checks PASS, exit 0; `tests/run_golden.py`: 31/31 (100%), exit 0. No local inference executed. Initial check with Hermes environment failed because trafilatura was unavailable; rerun in reader project environment passed.

Preserved: embeddings, ASR, rerankers, pricing, measured history and upstream checkouts. Next action: owner/root review T-0059; live Gemma output quality and performance remain unmeasured in this change. No commit, push or publication.
