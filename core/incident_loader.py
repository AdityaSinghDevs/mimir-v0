import yaml
from typing import List, Dict

from core.paths import INCIDENTS


def get_incident_ids() -> List[str]:

    ids = []

    for p in INCIDENTS.iterdir():
        if p.is_dir():
            ids.append(p.name)

    ids.sort()

    return ids

def load_incident(incident_id: str) -> Dict:

    incident_path = INCIDENTS / incident_id

    yaml_path = incident_path / "incident.yaml"
    logs_path = incident_path / "logs.txt"

    with open(yaml_path, "r", encoding="utf-8") as f:
        meta = yaml.safe_load(f)

    with open(logs_path, "r", encoding="utf-8") as f:
        logs = []

        for line in f.readlines():
            cleaned = line.strip()

            if cleaned:
                logs.append(cleaned)

    incident = {
        "id": incident_id,
        "description": meta["description"],
        "logs": logs,
        "title": meta["metadata"]["title"],
        "ground_truth_root_cause": meta["ground_truth"]["root_cause"],
        "ambiguity_level" : meta["metadata"]["amiguity_level"],
    }

    return incident