"""Generate the worked example: a photo-refund agent, judged.

The story: a customer photographs the meal that arrived, says it is wrong or
damaged, and asks for a refund. An agent looks at the photo, checks the order,
and decides -- refund, reject, or escalate to a human. Then an LLM judge reads
the whole trace and scores the decision out of ten.

That judge is the thing this repository is about.

Everything here is SYNTHETIC. No real orders, no real photos, no real model
output. The underlying trace comes from judge_audit.simulate, whose parameters
are calibrated to published effect sizes (docs/calibration.md), so the audits
below produce exactly the numbers quoted in the talk. Re-running this script
reproduces the same files: the seeds are fixed.

    python examples/photo_refund/make_data.py
"""

from __future__ import annotations

import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from judge_audit import simulate as S  # noqa: E402

HERE = pathlib.Path(__file__).parent

DISHES = [
    "chicken rice", "laksa", "char kway teow", "nasi lemak", "bak chor mee",
    "roti prata", "hokkien mee", "satay set", "carrot cake", "fish soup",
    "mee goreng", "chai tow kway", "wanton mee", "curry puff", "kaya toast",
]
COMPLAINTS = [
    "wrong item", "spilled in transit", "missing side", "cold on arrival",
    "looks nothing like the photo", "wrong size", "packaging crushed",
]
DECISIONS = ["refund", "reject", "escalate"]


def build(n_items: int = 600, seed: int = 20260911) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (traces, judged) -- one row per order, and one per judge pass."""
    data = S.build_dataset(n_items=n_items, seed=seed)
    items, trace = data["items"], data["trace"]
    rng = np.random.default_rng(seed)

    order_ids = [f"ORD-{40000 + i * 7}" for i in range(len(items))]
    id_map = dict(zip(items["item_id"], order_ids))

    traces = pd.DataFrame({
        "order_id": order_ids,
        "dish": rng.choice(DISHES, len(items)),
        "complaint": rng.choice(COMPLAINTS, len(items)),
        "photo": [f"photos/{o.lower()}.jpg" for o in order_ids],
        # What the agent decided. Escalation is the safe middle; the judge has
        # opinions about when it was warranted, which is where it gets messy.
        "agent_decision": np.where(
            items["fluent_but_wrong"], "refund",
            np.where(items["latent_quality"] > 0.62, "refund",
                     np.where(items["latent_quality"] > 0.4, "escalate", "reject"))),
        "refund_amount_sgd": (rng.uniform(4, 28, len(items))).round(2),
        # Two separate human judgements, as everywhere in this repo: was the
        # decision well handled, and was it actually the right call?
        "human_score": items["human_score"].to_numpy(),
        "human_correct": items["human_correct"].to_numpy(),
        "confusing_photo": items["difficulty_stratum"].astype(str).to_numpy(),
        "fluent_but_wrong": items["fluent_but_wrong"].to_numpy(),
    })

    judged = trace.rename(columns={"item_id": "order_id"}).copy()
    judged["order_id"] = judged["order_id"].map(id_map)
    judged = judged[[
        "order_id", "run", "judge_score", "judge_score_recovered", "was_blank",
        "equivalent", "human_score", "human_correct", "difficulty_stratum",
        "fluent_but_wrong", "system",
    ]].rename(columns={
        "difficulty_stratum": "photo_clarity",
        "system": "agent_version",
        "equivalent": "right_call",
    })
    judged["agent_version"] = judged["agent_version"].replace(
        {"model-A": "agent-v2.3", "model-B": "agent-v2.2"})
    # The simulator's difficulty quartiles, said in the language of the domain:
    # how readable the customer's photo is.
    clarity = {
        "Q1 clearest": "clear photo",
        "Q2": "mostly clear",
        "Q3": "hard to read",
        "Q4 most ambiguous": "barely readable",
    }
    judged["photo_clarity"] = judged["photo_clarity"].map(clarity)
    traces["confusing_photo"] = traces["confusing_photo"].map(clarity)
    return traces, judged


def main() -> int:
    traces, judged = build()
    traces.to_csv(HERE / "traces.csv", index=False)
    judged.to_csv(HERE / "judged.csv", index=False)
    print(f"wrote traces.csv   {len(traces):>5} orders")
    print(f"wrote judged.csv   {len(judged):>5} rows  "
          f"({judged['run'].nunique()} judge passes per order)")
    print(f"blank judge scores {int(judged['judge_score'].isna().sum()):>5}  "
          f"({judged['judge_score'].isna().mean():.1%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
