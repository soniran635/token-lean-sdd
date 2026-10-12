# ⚡ Token-Lean-SDD: Cost-Efficient AI Gating & Context Pruner

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
  <img src="https://img.shields.io/badge/Focus-AI_FinOps_%26_DevEx-blue?style=for-the-badge" alt="FinOps & DevEx" />
</p>

> An open-source pre-flight filtering engine for Specification-Driven Development (SDD) that prunes git diff context noise by 60%+ and gates pull request acceptance criteria locally using open-source models at $0 cost.

---

## 📌 The Problem: The AI Token Cost Explosion

In Specification-Driven Development (SDD), breaking features into atomic component cards accelerates velocity but results in **3x to 5x more pull requests**. When developers blindly dump full files or 40,000+ tokens of repository context into cloud AI coding agents (Cursor, Devin, Copilot, Claude Code) for small PR reviews:

1. **Context Window Waste:** 60% to 80% of prompt tokens are consumed by license headers, boilerplate comments, and unchanged lines.
2. **Exponential Cloud Spend:** Organizations burn tens of thousands of dollars monthly paying frontier model API rates for mundane syntax and formatting checks.
3. **Review Gridlock:** Incomplete PRs missing basic acceptance criteria reach senior human reviewers or trigger costly multi-turn cloud agent loops.

---

## 💡 The Solution: Local Pre-Flight Pruning & Gating

**Token-Lean-SDD** acts as a local, zero-cost developer proxy:

```mermaid
flowchart TD
    A[Raw Git Diff + Acceptance Criteria] --> B[Smart Context & Diff Pruner]

    subgraph Local_Processing [Local Zero-Cost Processing]
        B --> C[Pruned Functional Delta: 60-80% Smaller]
        C --> D[Local Pre-Flight Gate: Ollama / Llama 3.2]
        D --> E{Pre-Flight Verdict}
    end

    E -->|Criteria Missing| F[❌ Local Reject: Actionable Fix Feedback - Zero Cost]
    E -->|Criteria Satisfied| G[✅ Local Pass: Ready for PR & Cloud Review]
    G --> H[Enterprise Token FinOps Dashboard: Savings Logged]


    -------------------------
    ##⚙️ Core Architectural Capabilities
1. Smart Context & Diff Pruner (SmartContextPruner)
Ingests raw git diffs and extracts only the functional code delta (interfaces, business logic, and test assertions), stripping out git headers, whitespace, and comment noise to reduce payload size by 60% to 80%.

2. Local Pre-Flight Spec Gate (LocalPreflightGate)
Audits the pruned diff against Component Card acceptance criteria locally on the developer's laptop using open-source models (via Ollama) at $0 cost, catching omissions before triggering expensive cloud tokens or human review loops.

3. Enterprise FinOps Savings Calculator
Quantifies the exact tokens saved and cloud API dollars avoided per PR and across engineering squads.

## 🛠️ Tech Stack
Engine: Python 3.9+, Pydantic v2, Pandas

Local AI Inference: Ollama (llama3.2:3b)

Interactive Dashboard: Streamlit

License: MIT License

## 🚀 Quickstart
1. Clone & Set Up
git clone [https://github.com/soniran635/token-lean-sdd.git](https://github.com/soniran635/token-lean-sdd.git)
cd token-lean-sdd

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

2. Launch the Dashboard
streamlit run ui/app.py
Open http://localhost:8501 to test diff pruning, run local pre-flight gates, and simulate enterprise monthly token savings

📂 Repository Structure
token-lean-sdd/
├── src/
│   ├── models.py          # Pydantic schemas (PRDiffPayload, PruningReport, GateResult)
│   ├── pruner.py          # Smart Context & Diff Pruning engine
│   └── preflight_gate.py  # Local Ollama pre-flight gating engine
├── ui/
│   └── app.py             # Streamlit interactive dashboard & FinOps calculator
├── requirements.txt
└── README.md

📄 License
MIT License. Open source and free for the community.
---

