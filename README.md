# Mimir v0
### Evaluating Structured Diagnostic Reasoning in LLM-Based Incident Analysis

---

## The Question

Does enforcing a structured diagnostic reasoning schema reduce hallucinations and improve root-cause accuracy in LLM-based log analysis — and does input ambiguity moderate that effect?

This is a **research artifact**, not a production system. The goal is to understand reasoning behavior under controlled conditions, not to build a deployable SRE agent.

---

## Note:
This is an early-stage study.\
v0 covers 4 incidents, 2 conditions, 3 runs each — 24 trials total.
 
Results are directional and 
exploratory, not statistically conclusive. More incidents are being 
added in the next phase. Treat the findings below as hypotheses 
worth investigating further, not conclusions worth generalizing from.


## What This Found

Across 24 controlled trials (4 incidents × 2 conditions × 3 runs):

> n=24 across 4 incidents. Patterns are consistent but not stable.
> at this scale. Interpret accordingly.

| Condition | Accuracy | Hallucination Rate | Reasoning Quality |
|-----------|----------|-------------------|-------------------|
| Freeform | 25% | 33% | 1.17 / 2 |
| Structured | 17% | 33% | 1.58 / 2 |

Overall hallucination rate was identical. Structured prompting traded accuracy for reasoning quality.

**The more interesting finding was ambiguity as a moderating variable:**

| Ambiguity | Condition | Accuracy | Hallucination |
|-----------|-----------|----------|---------------|
| Low | Freeform | 100% | 33% |
| Low | Structured | 0% | **0%** |
| High | Freeform | 0% | 33% |
| High | Structured | 33% | **50%** |

Same intervention. Reversed outcomes depending on input ambiguity.

On low-ambiguity incidents, structured reasoning eliminates hallucination — but over-constrains the reasoning path, causing the model to miss the correct root cause entirely.

On high-ambiguity incidents, structured prompting worsens hallucination while slightly improving accuracy — forcing structure onto genuinely unclear inputs appears to produce confidently-reasoned but partially fabricated conclusions.

**Documented failure modes:**
- Over-constrained reasoning paths on low-ambiguity inputs
- Premature hypothesis fixation under structured prompting

**Edge case noted:** Two trials produced accuracy=1 and hallucination=1 simultaneously — the model reached the correct conclusion while hallucinating supporting evidence. This raises a real question about what these metrics are independently capturing.

---

## Model & Setup

- **Model:** Qwen 2.5-3B — chosen for local reproducibility and controlled, deterministic inference
- **Evaluation:** Manual, blind to condition labels, with formalized grading criteria
- **Dataset:** Synthetic incidents constructed from real outage patterns (GitHub, Cloudflare, GitLab), with varying causal chain complexity and ambiguity levels. Frozen before experimentation.

---

## Experimental Design

### Reasoning Conditions

**Freeform:** No structural constraints on output. Model responds directly to incident description.

**Structured:** Output constrained to a five-stage diagnostic schema:
1. Symptom Identification
2. Hypothesis Generation (1–3 plausible causes)
3. Verification Checks (evidence for/against each hypothesis)
4. Root Cause Conclusion
5. Safe Mitigation Suggestion (non-destructive)

The schema constrains reasoning *order and structure*, not the model's internal chain-of-thought.

### Evaluation Metrics

| Metric | Scale | Description |
|--------|-------|-------------|
| Accuracy | 0 / 1 | Correct root cause identified |
| Hallucination | 0 / 1 | Unsupported claims or invented components present |
| Evidence Grounding | 0 – 2 | How well conclusions are tied to log evidence |
| Reasoning Quality | 0 – 2 | Coherence and completeness of diagnostic chain |

### What's Explicitly Out of Scope

- Agents or tool execution
- Real-time or production systems
- Multi-model comparisons
- UI or dashboards

Scope constraints are intentional. Experimental control over breadth.

---

## Repository Structure

```
mimir-v0/
├── data/
│   ├── incidents/          # frozen incident definitions
│   └── outputs/            # raw LLM outputs, saved verbatim
├── prompts/                # prompt templates per condition
├── inference/              # scripts to run experiments
├── eval/                   # evaluation templates and grading criteria
├── experiments/            # aggregated results and trial logs
├── RESULTS.md              # findings, observations, failure modes
└── README.md
```

---

## Running Experiments

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
export OPENAI_API_KEY=your_key_here  # or equivalent

# 3. Run inference
python inference/run_experiments.py --condition structured --incident incident_01

# 4. Evaluate outputs manually using eval/grading_template.md

# 5. Aggregate results
python eval/aggregate.py
```

Full parameter documentation is in each script's header.

---

## Limitations

- Small dataset (4 incidents, 3 runs per condition) — findings are directional, not statistically conclusive
- Manual evaluation introduces subjectivity despite blind review protocol
- Single model backbone — generalizability untested
- Synthetic incidents approximate but don't fully replicate production complexity

These are appropriate limitations for v0. The goal was methodology validation, not scale.

---

## Status & Next Steps

**v0 — Completed.** Structured vs. freeform comparison across 4 incidents, ambiguity analysis, failure mode documentation.

**Next:** RAG extension — does retrieval-augmented generation change how ambiguity interacts with structured reasoning, or does it shift the failure modes elsewhere?

---

## Citation

If you reference this work:

```
Singh, A. P. (2025). Mimir v0: Evaluating Structured Diagnostic Reasoning 
in LLM-Based Incident Analysis. GitHub. 
https://github.com/[your-username]/mimir-v0
```

---

*Research artifact. Built for understanding, not deployment.*