# Mimir v0  
### Evaluating Structured Diagnostic Reasoning in LLM-Based Incident Analysis

## Overview

Mimir v0 is a small, controlled research prototype that investigates the following question:

> Does enforcing a structured diagnostic reasoning schema in large language models (LLMs) reduce hallucinations and improve root-cause accuracy in log-based incident analysis, compared to free-form generation — with and without retrieval?

This repository contains a **research artifact**, not a production system.  
The goal is to validate methodology and reasoning behavior, not to build a full SRE agent.

---

## Research Scope

### Included
- Log-based incident diagnosis
- Kubernetes-style service failures
- One LLM backbone
- Prompt-level control of reasoning structure
- Optional lightweight retrieval (RAG)

### Explicitly Excluded
- Agents or tool execution
- Real-time systems
- Dashboards or UI
- Production infrastructure
- Multi-model ensembles

Scope constraints are intentional to preserve experimental control.

---

## Experimental Design

### Diagnostic Reasoning Schema

Structured outputs are constrained to the following schema:

1. Symptom Identification  
2. Hypothesis Generation (1–3 plausible causes)  
3. Verification Checks (evidence for or against each hypothesis)  
4. Root Cause Conclusion  
5. Safe Mitigation Suggestion (non-destructive)

The schema constrains output structure and reasoning order, not the model’s internal chain-of-thought.

---

### Experimental Conditions

All experiments are run under four conditions:

1. Free-form generation (no RAG)  
2. Free-form generation + RAG  
3. Structured reasoning (no RAG)  
4. Structured reasoning + RAG  

All conditions use the same LLM backbone and decoding parameters.

---

## Dataset

- 5–20 manually curated synthetic incidents
- Each incident includes:
  - incident description
  - log snippets
  - ground-truth root cause
  - supporting evidence
- Dataset is frozen prior to experimentation

Dataset quality is prioritized over size.

---

## Evaluation Methodology

### Primary Metrics
- Root-cause accuracy (correct / partial / incorrect)
- Hallucination rate:
  - unsupported claims
  - invented services or components
- Reasoning completeness

### Evaluation Process
- Raw LLM outputs are saved verbatim
- Evaluation is performed manually
- Outputs are reviewed without condition labels
- Subjectivity is acknowledged and documented

---

## Repository Structure
```
mimir-v0/
├── data/
│ ├── incidents/ # frozen incident definitions
│ └── outputs/ # raw LLM outputs
├── prompts/ # prompt templates (experimental conditions)
├── inference/ # scripts to run experiments
├── eval/ # evaluation templates and analysis
├── experiments/ # aggregated results
├── RESULTS.md # findings and observations
└── README.md
```


---

## Running Experiments

1. Install dependencies  
2. Ensure API key is available via environment variable  
3. Run inference script to generate outputs  
4. Perform manual evaluation using evaluation templates  
5. Aggregate results and write findings in `RESULTS.md`

Exact commands are documented in the respective scripts.

---

## Limitations

- Small dataset size
- Manual evaluation introduces subjectivity
- Single LLM backbone
- Synthetic incidents may not reflect full production complexity

These limitations are intentional and appropriate for v0.

---

## Status

Mimir v0 is a **completed research prototype** intended to:
- validate structured reasoning as a diagnostic tool
- inform future system design
- serve as a foundation for larger-scale studies

---

## License / Usage

This repository is intended for research and educational purposes.