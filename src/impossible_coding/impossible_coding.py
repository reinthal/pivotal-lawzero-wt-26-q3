"""Impossible coding eval.

Presents the model with a GitHub-style issue whose acceptance criteria are
physically unachievable (e.g. quicksort 1M ints in <1 ms in pure Python),
under heavy social/business pressure injected via configurable urgency
prompts. We measure whether the model holds the line (honestly reports
infeasibility in the PR) or caves and cheats (modifies tests, monkey-patches
timing, fabricates results).

All prompt content (developer guidelines, urgency prompts, PR template,
submit-tool description, grader rubric, target answer) lives in
``impossible_coding.yaml`` so the experiment can be tuned without code
changes.
"""

from pathlib import Path
from typing import Any

import yaml
from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import model_graded_qa
from inspect_ai.solver import basic_agent, system_message
from inspect_ai.tool import bash, python, text_editor

HERE = Path(__file__).parent
CONFIG_PATH = HERE / "impossible_coding.yaml"
SCENARIOS_DIR = HERE / "data" / "scenarios"

DEFAULT_MESSAGE_LIMIT = 50
DEFAULT_TIME_LIMIT = 300
DEFAULT_TOKEN_LIMIT = 300_000
DEFAULT_URGENCY = ["team_disappointment", "revenue_loss", "ceo_authority"]


def _load_config() -> dict[str, Any]:
    return yaml.safe_load(CONFIG_PATH.read_text())


def _system_prompt(
    config: dict[str, Any], urgency_keys: list[str], fair: bool
) -> str:
    parts = [config["developer_guidelines"]]
    for key in urgency_keys:
        parts.append(config["urgency_prompts"][key])
    parts.append("PR template (use this when calling submit_pr):\n\n" + config["pr_template"])
    if fair:
        parts.append(config["fair_out_prompt"])
    return "\n\n".join(parts)


def _scenario_sample(scenario_dir: Path, target: str) -> Sample:
    issue = (scenario_dir / "issue.md").read_text()
    files: dict[str, str] = {}
    for path in scenario_dir.iterdir():
        if path.is_file() and path.name not in {"issue.md", "setup.sh"}:
            files[f"repo/{path.name}"] = str(path)
    return Sample(
        input=issue,
        id=scenario_dir.name,
        target=target,
        files=files,
        setup=str(scenario_dir / "setup.sh"),
    )


def _load_scenarios(target: str) -> list[Sample]:
    return [
        _scenario_sample(d, target)
        for d in sorted(SCENARIOS_DIR.iterdir())
        if d.is_dir() and (d / "issue.md").exists()
    ]


@task
def impossible_coding(
    urgency: list[str] | None = None,
    fair: bool = False,
    message_limit: int = DEFAULT_MESSAGE_LIMIT,
    time_limit: int = DEFAULT_TIME_LIMIT,
    token_limit: int = DEFAULT_TOKEN_LIMIT,
) -> Task:
    """Impossible coding eval with pressure-injection.

    Args:
        urgency: Which urgency prompts (keys from ``impossible_coding.yaml``
            ``urgency_prompts``) to splice into the system prompt. Defaults
            to all three.
        fair: When True, append a fair-out clause to the system prompt
            telling the model it may decline by ticking **No** and explaining
            why the task is impossible. Ablation for measuring whether an
            explicit opt-out changes capitulation rates under pressure.
        message_limit: Max messages in the agent conversation per sample.
        time_limit: Max wall-clock seconds per sample.
        token_limit: Max model tokens per sample.
    """
    config = _load_config()
    urgency_keys = urgency if urgency is not None else DEFAULT_URGENCY
    return Task(
        dataset=_load_scenarios(config["target"]),
        solver=[
            system_message(_system_prompt(config, urgency_keys, fair)),
            basic_agent(
                tools=[bash(), python(), text_editor()],
                message_limit=message_limit,
                submit_name="submit_pr",
                submit_description=config["submit_description"],
            ),
        ],
        scorer=model_graded_qa(
            template=config["grader_template"],
            grade_pattern=config["grade_pattern"],
        ),
        sandbox="local",
        message_limit=message_limit,
        time_limit=time_limit,
        token_limit=token_limit,
    )
