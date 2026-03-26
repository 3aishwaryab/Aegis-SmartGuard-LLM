# Aegis LLM Guardrail System - PPT Content

## Slide 1: Title
- **Aegis LLM Guardrail System**
- A Research-Grade LLM Firewall for Real-Time Threat Detection.
- [Your Name/Team]

## Slide 2: Problem Statement
- LLMs are vulnerable to:
  - **Jailbreaks**: Bypassing safety filters.
  - **Prompt Injections**: Malicious code or commands.
  - **Toxicity**: Hateful or harmful content.
  - **PII Extraction**: Stealing personal data.
- Need for a lightweight, CPU-friendly, and robust guardrail system.

## Slide 3: Core Objective
- Build an LLM firewall system that:
  - Classifies prompts as SAFE or UNSAFE.
  - Categorizes unsafe prompts into specific threat types.
  - Provides a confidence score for each verdict.
  - Runs with low latency on standard CPUs.

## Slide 4: System Architecture
- **Backend**:
  - Dataset generation (Synthetic + Manual + Public).
  - Dual-model approach: Baseline vs. Trained.
  - Evaluation and research analysis.
- **Frontend**:
  - React-based dashboard for real-time monitoring.
  - Detailed analysis and research insights.

## Slide 5: Dataset Creation
- **Total Samples**: 500+
- **Sources**:
  - Manual (Human-written).
  - Synthetic (Gemini 2.0 Flash).
  - Public (Do-not-answer dataset).
- **Split**: 70% Train, 15% Validation, 15% Test.

## Slide 6: Model Design
- **Baseline**: TF-IDF + Logistic Regression.
- **Trained Model**: Fine-tuned DistilBERT-base-uncased.
- **Optimization**: CPU-friendly, sub-50ms inference.
- **Training**: Early stopping, dropout, fixed random seed.

## Slide 7: Evaluation Results
- **Accuracy**: ~96% (Trained) vs. ~82% (Baseline).
- **F1 Score**: ~0.95 (Trained) vs. ~0.81 (Baseline).
- **Latency (P95)**: ~45ms (Trained) vs. ~5ms (Baseline).
- **Confusion Matrix**: High precision across all threat categories.

## Slide 8: Research Insights
- **Error Analysis**: False positives on security discussions.
- **Overfitting**: Prevented by early stopping at epoch 5.
- **Comparison**: DistilBERT significantly outperforms the baseline in subtle jailbreak detection.
- **Insights**: Pattern recognition of "DAN" style jailbreaks is highly effective.

## Slide 9: Demo & UI
- Dark cybersecurity theme.
- Real-time inference with adjustable threshold.
- Activity logs and metrics dashboard.
- Detailed analysis and research explorer.

## Slide 10: Conclusion
- Aegis provides a production-quality, reproducible, and research-grade solution for LLM security.
- Future work: Expanding the dataset and exploring more lightweight architectures (e.g., MobileBERT).
