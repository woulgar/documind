# PDM benchmark — task "rerank" — run the remaining agents (claude attempt already done).
# Criterion: work/token = assessed quality (0..1) / dev agent tokens.
# Each agent gets its own git worktree off the SAME baseline (v1, 5dc0116).
# PDM never runs the agents — you run each one in its worktree, then measure.
#
# Run this from the project root:  C:\MyCodes\pdm-pilots\rag-tutorial-v2
$ErrorActionPreference = "Stop"
$BASE  = "5dc01161e1d668b7cf5bb056544489415571b0bd"   # v1 baseline
$FLOW  = "C:/MyCodes/pdm/scripts/pdm_flow.py"
$INSTR = @'
[PDM benchmark task — frozen]
Add a new box `rerank` between Retrieve and Generate in the Query & answer pipeline.
- retriever.py::rerank(query, docs) -> docs : reorder retrieved chunks so the most
  on-topic chunk leads the prompt. Deterministic, cheap.
- Wire into pipeline.py::answer after retrieve, before generate.
- Add the box to .pdm/flow.json (parent query, connector retrieve, map retriever.py::rerank)
  with a deterministic test. Do not change any other box.
Done = flow.json has the rerank box, the fixed query still answers correctly with a
citation, and pdm_driver.run() measures clean.
'@

function New-Attempt($agent) {
  $dir = "../rag-tutorial-v2-$agent"
  git worktree add $dir -b "attempt/$agent" $BASE
  Write-Host "`n=== worktree ready: $dir (branch attempt/$agent) ===" -ForegroundColor Cyan
  Write-Host "Now open '$agent' IN THAT FOLDER and give it this instruction:`n" -ForegroundColor Yellow
  Write-Host $INSTR
  Write-Host "`nAfter the agent finishes + you commit in the worktree, measure it:" -ForegroundColor Yellow
  Write-Host "  python $FLOW $dir rerank@$agent pdm_driver run --out ./.pdm/traces`n"
}

# --- the three remaining contenders ---------------------------------------
# codex             : VS Code Codex
# opencode-qwen3:4b : opencode CLI with local qwen3:4b as the coding model
# claude-haiku-4.5  : Claude Code with model = claude-haiku-4.5
New-Attempt "codex"
New-Attempt "opencode-qwen3-4b"
New-Attempt "claude-haiku-4-5"

Write-Host "All worktrees created. Implement rerank in each, commit, then run the measure" -ForegroundColor Green
Write-Host "line printed above for each. Traces land in ./.pdm/traces as rerank@<agent>.json" -ForegroundColor Green
Write-Host "and show up side-by-side in the PDM Benchmark view next to rerank@claude." -ForegroundColor Green
Write-Host "`nCleanup when done:  git worktree remove ../rag-tutorial-v2-<agent>" -ForegroundColor DarkGray
