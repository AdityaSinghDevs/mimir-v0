# Ambiguity Metric Specification
Version: v1.0
Project: Synthetic Incident Log Ambiguity Evaluation Framework

---

# 1. Purpose

This document defines the formal ambiguity scoring methodology used to classify synthetic incidents into LOW, MODERATE, or HIGH ambiguity categories.

Ambiguity is defined as:

> The degree to which multiple root cause hypotheses remain structurally plausible and competitively ranked after model-based reasoning over logs.

This metric ensures:
- Reproducibility
- Cross-incident comparability
- Model evaluation consistency
- Research-grade rigor

---

# 2. Evaluation Protocol

For each incident:

1. Run LLM analysis **3 independent times** (temperature fixed).
2. Extract:
   - Top 3 hypotheses
   - Confidence percentages
   - Rank ordering
3. Compute ambiguity metrics defined below.

---

# 3. Core Ambiguity Components

Ambiguity score is composed of 4 structural dimensions:

---

## A. Confidence Spread (CS)

Measures how dominant the top hypothesis is.

Formula:

CS = H1_confidence - H2_confidence


Interpretation:
- Large spread → low ambiguity
- Small spread → high ambiguity

---

## B. Hypothesis Entropy (HE)

Measures distributional uncertainty.

Using normalized entropy over top 3 hypotheses:


HE = - Σ (p_i * log2(p_i))


Where p_i = normalized confidence (H1, H2, H3).

Higher entropy → more ambiguity.

Max entropy (3 equal hypotheses ≈ 33% each) ≈ 1.585  
Lower entropy (< 1.0) indicates dominance.

---

## C. Rank Stability (RS)

Measures consistency of top hypothesis across runs.


RS = (# runs where same hypothesis ranked #1) / 3


Interpretation:
- 1.0 → fully stable
- 0.66 → moderate instability
- <0.66 → high ambiguity

---

## D. Structural Fork Count (SFC)

Manual structural signal metric:

Count of independent, log-supported causal narratives that:
- Have direct log evidence
- Do not depend on the top hypothesis

Example structural forks:
- Split-brain evidence
- Replication corruption
- Deployment crash signals
- Storage corruption
- Human intervention traces

Scale:
- 1 → Linear causal chain
- 2 → One competing structural branch
- ≥3 → Multiple independent narratives

---

# 4. Composite Ambiguity Score (CAS)

We compute:


CAS = (Normalized HE * 0.4)
+ (1 - Normalized CS * 0.3)
+ ((1 - RS) * 0.2)
+ (Normalized SFC * 0.1)


Where:

- Normalized HE = HE / 1.585
- Normalized CS = CS / 100
- Normalized SFC = min(SFC / 3, 1)

CAS ∈ [0,1]

Higher CAS → higher ambiguity

---

# 5. Ambiguity Classification Thresholds

| CAS Range | Classification |
|-----------|---------------|
| 0.00 – 0.30 | LOW |
| 0.31 – 0.60 | MODERATE |
| 0.61 – 1.00 | HIGH |

---

# 6. Application to Current Incidents

---

## Incident 01 — HIGH

Observed Pattern:
- H1 ≈ 45–55%
- H2 ≈ 30–35%
- H3 ≈ 15–20%
- Rank instability observed
- ≥3 structural forks

Metrics:
- CS ≈ 15–20
- HE ≈ 1.45
- RS ≈ 0.66
- SFC ≥ 3

CAS ≈ 0.72–0.80

Classification: **HIGH**

---

## Incident 02 — MODERATE

Observed Pattern:
- H1 ≈ 52%
- H2 ≈ 32%
- H3 ≈ 16%
- Stable top hypothesis
- 2 structural forks

Metrics:
- CS ≈ 20
- HE ≈ 1.35
- RS = 1.0
- SFC = 2

CAS ≈ 0.48–0.55

Classification: **MODERATE**

---

## Incident 03 (Derived) — HIGH

Observed Pattern:
- H1 ≈ 52–58%
- H2 ≈ 30–33%
- H3 ≈ 10–15%
- Catalog corruption + split-brain + WAL gap
- ≥3 structural forks

Metrics:
- CS ≈ 20
- HE ≈ 1.38
- RS ≈ 0.66–1.0
- SFC ≥ 3

CAS ≈ 0.63–0.70

Classification: **HIGH**

---

## Incident 04 — LOW

Observed Pattern:
- H1 ≈ 65%
- H2 ≈ 25%
- H3 ≈ 10%
- Stable ranking across runs
- Single linear infra failure narrative

Metrics:
- CS ≈ 40
- HE ≈ 1.15
- RS = 1.0
- SFC = 1

CAS ≈ 0.22–0.28

Classification: **LOW**

---

# 7. Interpretation Guidelines

LOW:
- One dominant hypothesis
- Linear causal chain
- Competing hypotheses weak and dependent

MODERATE:
- Two structurally plausible narratives
- Stable ranking
- Evidence overlaps

HIGH:
- ≥3 structurally independent narratives
- Small confidence spread
- Possible rank instability
- Structural forks present

---

# 8. Important Research Note

Ambiguity is not noise.

Ambiguity is engineered through:
- Structural fork insertion
- Log-level symmetry
- Competing causal evidence
- Observability constraints

This metric quantifies that engineering discipline.

---

# 9. Future Extensions

Potential improvements:

- Cross-model ambiguity agreement score
- Hypothesis textual divergence metric
- Temporal reasoning difficulty score
- Counterfactual resilience testing

---

# 10. Conclusion

This framework provides a:

- Reproducible
- Quantifiable
- Scalable
- Model-evaluable

ambiguity scoring system for synthetic SRE incident datasets.