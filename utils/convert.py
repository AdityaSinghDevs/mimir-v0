import json
import re
from pathlib import Path
from typing import Dict, Any, List


def clean_markdown(text: str) -> str:
    """
    Clean and normalize LLM output while preserving markdown structure.
    """
    if not text:
        return ""

    text = text.replace("\r\n", "\n").strip()

    # Normalize headings (### -> ### with spacing consistency)
    text = re.sub(r"^(#{1,6})(\S)", r"\1 \2", text, flags=re.MULTILINE)

    # Ensure spacing before headings
    text = re.sub(r"\n(#{1,6})", r"\n\n\1", text)

    # Normalize bullet points
    text = re.sub(r"\n\s*-\s*", "\n- ", text)

    # Normalize numbered lists
    text = re.sub(r"\n\s*(\d+)\.\s*", r"\n\1. ", text)

    return text.strip()


def format_run(run: Dict[str, Any]) -> str:
    run_id = run.get("run_id", "N/A")
    response = clean_markdown(run.get("response", ""))

    return f"## Run {run_id}\n\n{response}\n"


def format_incident(data: Dict[str, Any]) -> str:
    incident_id = data.get("incident_id", "N/A")
    title = data.get("title", "N/A")
    root_cause = data.get("ground_truth_root_cause", "").strip()

    output = [
        f"# Incident: {incident_id}",
        "",
        "## Title",
        title,
        "",
        "## Ground Truth Root Cause",
        root_cause,
        "",
        "---",
        ""
    ]

    responses: List[Dict[str, Any]] = data.get("responses", [])

    for run in responses:
        output.append(format_run(run))

    return "\n".join(output).strip()


def process_file(input_path: Path, output_path: Path):
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        formatted_text = format_incident(data)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(formatted_text)

        print(f"[✓] {input_path.name} → {output_path.name}")

    except Exception as e:
        print(f"[✗] Failed: {input_path.name} | {e}")


def process_directory(input_dir: str, output_dir: str):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    output_path.mkdir(parents=True, exist_ok=True)

    json_files = list(input_path.glob("*.json"))

    if not json_files:
        print("[!] No JSON files found.")
        return

    for file in json_files:
        out_file = output_path / (file.stem + ".md")
        process_file(file, out_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert JSON → Markdown")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    input_path = Path(args.input)

    if input_path.is_file():
        process_file(input_path, Path(args.output))
    else:
        process_directory(args.input, args.output)