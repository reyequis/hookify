# Changelog

## v0.2.1 — 2026-05-05

### Fixed
- Bug #4: `UserPromptSubmit` rules with `field: user_prompt` now fire.
  Claude Code's hook payload uses key `prompt`, but the engine was
  reading `input_data["user_prompt"]` and silently returning empty
  string. Field extraction now accepts both `prompt` and `user_prompt`
  field names, preferring the actual Claude Code key. Discovered and
  fixed by [@adelaidasofia](https://github.com/adelaidasofia) in #2.

### Internal
- pytest test suite grew to 71 tests (4 new contract tests for the
  field-name fix).
- CI: `claude-review` workflow now skips on fork PRs (GitHub strips
  `id-token: write` from forks, so OIDC-based authentication can't
  succeed there).

## v0.2.0 — 2026-05-03

Initial fork of Anthropic's hookify with bug fixes and JSON cache.

### Fixed
- Bug #2: Rules in `~/.claude/` now load regardless of CWD. Project
  rules override global by name; disabled project rules suppress
  matching global rules. Fixes upstream issues #309, #503, #1294,
  #1444 on `anthropics/claude-plugins-official`.
- Bug #3: `event: file` rules now fire on Write operations. Field
  extraction falls back from `new_string` to `content`.

### Added
- JSON rule cache (mtime-invalidated). Reduces redundant YAML
  parsing on every hook event. Set `HOOKIFY_NO_CACHE=1` to disable.
- `not_regex_match` operator.
- `value` key as an alias for `pattern` in conditions.
- `read` event type for Read/Glob/Grep/LS tools.
- `Update` tool support in file-event mapping.
- `permissionDecisionReason` in block-rule output (Claude sees why
  it was blocked).
- Windows path quoting in `hooks.json`.
- `version` field in `plugin.json` (was missing upstream).
- `.claude-plugin/marketplace.json` for self-marketplacing.

### Internal
- pytest test suite (67 tests; none in upstream).
- ruff lint + format.
- GitHub Actions CI on Python 3.10, 3.11, 3.12.
- Apache 2.0 license preserved from upstream.
