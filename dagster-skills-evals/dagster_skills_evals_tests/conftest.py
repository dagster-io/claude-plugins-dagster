from pathlib import Path

import pytest
from dagster_shared.serdes import deserialize_value, serialize_value
from dagster_skills_evals.execution import ClaudeExecutionResultSummary


class BaselineManager:
    """Manages performance baselines with simple JSON storage."""

    def __init__(self, baseline_dir: Path, test_name: str, update_mode: bool = False):
        self.baseline_dir = baseline_dir
        self.test_name = test_name
        self.update_mode = update_mode
        self.baseline_dir.mkdir(exist_ok=True)

    @property
    def baseline_path(self) -> Path:
        return self.baseline_dir / f"{self.test_name}.json"

    @property
    def baseline(self) -> ClaudeExecutionResultSummary | None:
        if not self.baseline_path.exists():
            return None
        with self.baseline_path.open() as f:
            return deserialize_value(f.read(), ClaudeExecutionResultSummary)

    def save_baseline(self, summary: ClaudeExecutionResultSummary) -> None:
        with self.baseline_path.open("w") as f:
            f.write(serialize_value(summary))

    def _assert_improvement(
        self,
        old: ClaudeExecutionResultSummary | None,
        new: ClaudeExecutionResultSummary,
    ) -> None:
        """Assert that the new summary is an improvement over the old summary."""
        if old is None:
            return
        assert new.input_tokens <= old.input_tokens
        assert new.output_tokens <= old.output_tokens
        assert new.execution_time_ms <= old.execution_time_ms

    def assert_improved(self, summary: ClaudeExecutionResultSummary) -> None:
        if self.update_mode:
            self.save_baseline(summary)

        self._assert_improvement(self.baseline, summary)


def pytest_addoption(parser):
    parser.addoption(
        "--snapshot-update",
        action="store_true",
        default=False,
        help="Update baseline snapshots instead of comparing against them",
    )


@pytest.fixture
def baseline_manager(request) -> BaselineManager:
    """Provides baseline management with --snapshot-update support."""
    baseline_dir = Path(__file__).parent / "__baselines__"
    update_mode = request.config.getoption("--snapshot-update")
    return BaselineManager(
        baseline_dir, test_name=request.node.name, update_mode=update_mode
    )
