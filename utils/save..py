import json
import os

from core.paths import RESULTS


def save_results(
    incident_id: str,
    results: dict,
    prompt_type: str,
    rag: str = "no_rag"
) -> None:

    filename = f"{incident_id}_{prompt_type}_{rag}.json"

    output_path = os.path.join(RESULTS, filename)

    os.makedirs(RESULTS, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)