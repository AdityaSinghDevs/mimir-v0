import os
import yaml
from typing import Dict

from core.paths import INCIDENTS

def get_incident_ids(root_dir:str)->Dict:
    
    ids = sorted([name 
                  for name in os.listdir(root_dir)
                  if os.path.isdir(os.path.join(root_dir, name))])
    
    return ids


def load_incident(incident_id: str):

    root_dir = INCIDENTS
    incident_path = os.path.join(root_dir, incident_id)
    yaml_path = incident_path/"incident.yaml"

    with open (yaml_path, "r") as f:
        meta = yaml.safe_load(f)

    logs_path = os.path.join(incident_path, "logs.txt")
    with open (logs_path, "r") as f:
        logs = []

        for line in f.readlines:
            cleaned = line.strip()

            if cleaned:
                logs.append(cleaned)

    incident = {
                "id" : incident_id,
                "description" : meta["description"],
                "logs": logs,
    }

    return incident 


