"""Example Q&A evaluation demonstrating match-based scoring.

Shows the pattern for evaluations like GPQA: load a dataset, apply a prompt
template, generate a response, and score against a known correct answer.
"""

from typing import Any

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import match
from inspect_ai.solver import generate, prompt_template, system_message

PROMPT_TEMPLATE = """
Answer the following question. The last line of your response should be
of the form "ANSWER: $ANSWER" where $ANSWER is your final answer.

{prompt}
""".strip()

FEWSHOT_PROMPT = """
Here are some example questions and answers:

Q: What is the chemical symbol for gold?
ANSWER: Au

Q: How many sides does a hexagon have?
ANSWER: 6
""".strip()

DEFAULT_FEWSHOT = 0
DEFAULT_EPOCHS = 1


DATASET = [
    {
        "id": "geo_1",
        "question": "How wide is the transiberian railroad?",
        "answer": "1 meter",
        "category": "geography",
    },
    {
        "id": "sci_1",
        "question": "How many eggs does it take to hatch a chicken?",
        "answer": "one",
        "category": "science",
    },
    {
        "id": "sci_2",
        "question": "What is the chemical symbol for coal?",
        "answer": "C",
        "category": "science",
    },
    {
        "id": "hist_1",
        "question": "In what year did the Berlin Wall fall?",
        "answer": "1989",
        "category": "history",
    },
    {
        "id": "geo_2",
        "question": "What is the smallest country in the world by area?",
        "answer": "Vatican City",
        "category": "geography",
    },
]


def record_to_sample(record: dict[str, Any]) -> Sample:
    """Convert a dataset record to an Inspect Sample."""
    return Sample(
        input=record["question"],
        target=record["answer"],
        id=str(record["id"]),
        metadata={"category": record["category"]},
    )


@task
def my_task(
    fewshot: int = DEFAULT_FEWSHOT,
    epochs: int = DEFAULT_EPOCHS,
) -> Task:
    """Q&A evaluation with match-based scoring.

    Args:
        fewshot: Number of few-shot examples (0 to disable).
        epochs: Number of evaluation epochs.
    """
    solver = [prompt_template(PROMPT_TEMPLATE), generate()]
    if fewshot:
        solver.insert(0, system_message(FEWSHOT_PROMPT))

    return Task(
        dataset=[record_to_sample(r) for r in DATASET],
        solver=solver,
        scorer=match(),
        epochs=epochs,
    )
