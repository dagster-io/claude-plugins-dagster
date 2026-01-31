import json
import subprocess
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any

from dagster_shared.record import record
from dagster_shared.serdes import whitelist_for_serdes

_PLUGINS_DIR = Path(__file__).parent.parent.parent.parent / "skills"
assert _PLUGINS_DIR.exists()


@whitelist_for_serdes
@record
class ClaudeExecutionResultSummary:
    input_tokens: int
    output_tokens: int
    execution_time_ms: int
    tools_used: list[str]
    skills_used: list[str]


@dataclass
class ClaudeExecutionResult:
    cli_result: subprocess.CompletedProcess[str]

    @cached_property
    def summary(self) -> ClaudeExecutionResultSummary:
        return ClaudeExecutionResultSummary(
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
            execution_time_ms=self.execution_time_ms,
            tools_used=[tool["name"] for tool in self.tool_usages],
            skills_used=[skill["skill"] for skill in self.skill_usages],
        )

    @property
    def stdout(self) -> str:
        return self.cli_result.stdout

    @property
    def stderr(self) -> str:
        return self.cli_result.stderr

    @property
    def return_code(self) -> int:
        return self.cli_result.returncode

    @cached_property
    def _json_output(self) -> list[dict[str, Any]]:
        return json.loads(self.stdout)

    @cached_property
    def _result_event(self) -> dict[str, Any]:
        """Get the final result event from the execution."""
        for event in reversed(self._json_output):
            if event.get("type") == "result":
                return event
        raise ValueError("No result event found in execution output")

    @property
    def execution_time_ms(self) -> int:
        return self._result_event["duration_ms"]

    @property
    def input_tokens(self) -> int:
        return self._result_event["usage"]["input_tokens"]

    @property
    def output_tokens(self) -> int:
        return self._result_event["usage"]["output_tokens"]

    @property
    def tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @cached_property
    def messages(self) -> list[dict[str, Any]]:
        """Extract all messages without extra metadata.

        Returns a list of simplified message objects with role and content.
        """
        result = []
        for event in self._json_output:
            if event.get("type") in ("assistant", "user") and "message" in event:
                msg = event["message"]
                result.append({"role": msg.get("role"), "content": msg.get("content", [])})
        return result

    @cached_property
    def tool_usages(self) -> list[dict[str, Any]]:
        """Extract all tool usage objects from the execution.

        Returns a list of tool usage objects with id, name, and input.
        """
        result = []
        for event in self._json_output:
            if event.get("type") in ("assistant", "user") and "message" in event:
                msg = event["message"]
                content = msg.get("content", [])
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "tool_use":
                        result.append(
                            {
                                "id": item.get("id"),
                                "name": item.get("name"),
                                "input": item.get("input", {}),
                            }
                        )
        return result

    @cached_property
    def skill_usages(self) -> list[dict[str, Any]]:
        result = []
        for tool_usage in self.tool_usages:
            if tool_usage["name"] == "Skill":
                result.append(tool_usage["input"])
        return result

    def conversation_summary(self) -> str:
        return "\n".join([json.dumps(message, indent=2) for message in self.messages])


def run_claude_headless(
    prompt: str, target_dir: str, plugins_dir: str | None, timeout: int = 300
) -> ClaudeExecutionResult:
    """Run Claude CLI in headless mode in a specified working directory."""

    cmd = [
        "claude",
        "--print",
        "--output-format",
        "json",
        "--no-session-persistence",
        "--dangerously-skip-permissions",
        "--verbose",
        "--model",
        "sonnet",
    ]

    if plugins_dir:
        for subdir in Path(plugins_dir).iterdir():
            cmd.extend(["--plugin-dir", str(subdir)])

    result = subprocess.run(
        cmd,
        cwd=target_dir,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )

    return ClaudeExecutionResult(cli_result=result)


def execute_prompt(
    prompt: str, target_dir: str, include_plugins: bool = True
) -> ClaudeExecutionResult:
    plugins_dir = str(_PLUGINS_DIR) if include_plugins else None
    return run_claude_headless(prompt=prompt, target_dir=target_dir, plugins_dir=plugins_dir)
