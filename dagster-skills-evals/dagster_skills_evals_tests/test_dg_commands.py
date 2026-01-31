import subprocess
import tempfile
from pathlib import Path

from dagster_skills_evals.execution import execute_prompt
from dagster_skills_evals_tests.conftest import BaselineManager
from dagster_skills_evals_tests.utils import unset_virtualenv


def test_create_dagster_project(baseline_manager: BaselineManager):
    project_name = "acme_co_dataeng"
    prompt = f"Create a new Dagster project named {project_name}"

    # Run with skills enabled
    with unset_virtualenv(), tempfile.TemporaryDirectory() as tmp_dir:
        result = execute_prompt(prompt, tmp_dir)
        print(result.conversation_summary())

        # make sure the skill was used
        assert "dagster-skills:dg" in result.summary.skills_used

        # make sure the generated project is valid
        project_dir = Path(tmp_dir) / project_name

        subprocess.run(["uv", "run", "dg", "list", "projects"], cwd=project_dir, check=True)
        subprocess.run(["uv", "run", "dg", "list", "defs"], cwd=project_dir, check=True)

        baseline_manager.assert_improved(result.summary)


def test_scaffold_asset(baseline_manager: BaselineManager):
    project_name = "acme_co_dataeng"
    asset_name = "dwh_asset"
    prompt = f"Add a new asset with an empty body named '{asset_name}'"

    # Run with skills enabled
    with unset_virtualenv(), tempfile.TemporaryDirectory() as tmp_dir:
        subprocess.run(
            ["uvx", "create-dagster", "project", project_name, "--uv-sync"],
            cwd=tmp_dir,
            check=False,
        )
        project_dir = Path(tmp_dir) / project_name
        result = execute_prompt(prompt, project_dir.as_posix())
        print(result.conversation_summary())

        # make sure the skill was used
        assert "dagster-skills:dg" in result.summary.skills_used

        # make sure the asset was scaffolded
        defs_result = subprocess.run(
            ["uv", "run", "dg", "list", "defs"],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        assert asset_name in defs_result.stdout

        baseline_manager.assert_improved(result.summary)
