"""Tests for UserPromptSubmit field-name compatibility.

Claude Code's UserPromptSubmit hook payload puts the user's text under
the key `prompt`, not `user_prompt`. Before the field-name fix, any rule
with `field: user_prompt` silently never fired because the engine
called `input_data.get("user_prompt", "")` and got an empty string.

These tests pin the contract:
- A rule with `field: user_prompt` must fire when input_data has `prompt`
- A rule with `field: prompt` must fire when input_data has `prompt`
- A rule with `field: user_prompt` must still fire when input_data has
  the legacy `user_prompt` key (backwards compat)
"""

from core.config_loader import Condition, Rule
from core.rule_engine import RuleEngine


def _make_rule(field: str) -> Rule:
    return Rule(
        name=f"warn-on-url-{field}",
        enabled=True,
        event="prompt",
        conditions=[Condition(field=field, operator="regex_match", pattern=r"https?://\S+")],
        action="warn",
        message="URL detected",
    )


def test_user_prompt_field_matches_prompt_key():
    """Rule with field=user_prompt fires when payload has key=prompt (Claude Code's actual key)."""
    rule = _make_rule("user_prompt")
    engine = RuleEngine()
    result = engine.evaluate_rules(
        [rule],
        {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "Check out https://arxiv.org/abs/2604.15597",
        },
    )
    assert "URL detected" in result.get("systemMessage", ""), (
        f"Expected URL rule to fire but got: {result}"
    )


def test_prompt_field_matches_prompt_key():
    """Rule with field=prompt fires when payload has key=prompt."""
    rule = _make_rule("prompt")
    engine = RuleEngine()
    result = engine.evaluate_rules(
        [rule],
        {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "Check out https://arxiv.org/abs/2604.15597",
        },
    )
    assert "URL detected" in result.get("systemMessage", ""), (
        f"Expected URL rule to fire but got: {result}"
    )


def test_user_prompt_field_matches_user_prompt_key_backcompat():
    """Rule with field=user_prompt still fires when payload uses legacy user_prompt key."""
    rule = _make_rule("user_prompt")
    engine = RuleEngine()
    result = engine.evaluate_rules(
        [rule],
        {
            "hook_event_name": "UserPromptSubmit",
            "user_prompt": "Check out https://arxiv.org/abs/2604.15597",
        },
    )
    assert "URL detected" in result.get("systemMessage", ""), (
        f"Expected URL rule to fire (backcompat path) but got: {result}"
    )


def test_no_match_when_no_url_in_prompt():
    """Sanity check: rule should NOT fire when prompt has no URL."""
    rule = _make_rule("user_prompt")
    engine = RuleEngine()
    result = engine.evaluate_rules(
        [rule],
        {
            "hook_event_name": "UserPromptSubmit",
            "prompt": "Just a regular message with no link",
        },
    )
    # No systemMessage / no warning should be present
    msg = result.get("systemMessage", "") or ""
    assert "URL detected" not in msg, f"URL rule fired on a no-URL prompt: {result}"
