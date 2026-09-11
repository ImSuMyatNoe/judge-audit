"""judge-audit: check whether your LLM judge is measuring anything.

Companion code for the talk "LLM-as-a-Judge Is Probably Lying to You".

    from judge_audit import simulate, metrics
    data = simulate.build_dataset()
    print(metrics.stability(data["trace"]))

The metrics work on any judge trace, real or simulated. The simulator ships
synthetic data only, so the demo runs offline with no API keys.
"""

__version__ = "0.1.0"

from . import metrics, simulate  # noqa: F401

__all__ = ["metrics", "simulate", "__version__"]
