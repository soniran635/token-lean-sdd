import os
import sys

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from src.models import PRDiffPayload
from src.pruner import SmartContextPruner
from src.preflight_gate import LocalPreflightGate

st.set_page_config(page_title="Token-Lean-SDD | DevEx Optimization", layout="wide", page_icon="⚡")

st.title("⚡ Token-Lean-SDD: Cost-Efficient AI Gating & Context Pruner")
st.markdown("**Local Open-Source Pre-Flight Gating | 70% Token Reduction | Zero Cloud Waste** | *100% Free & Open-Source*")

pruner = SmartContextPruner()
gate = LocalPreflightGate()

tab1, tab2 = st.tabs(["✂️ Smart Diff Pruner & Pre-Flight Gate", "💰 Enterprise Token FinOps Calculator"])

# ----------------- TAB 1: PRUNER & PRE-FLIGHT GATE -----------------
with tab1:
    st.subheader("1. Ingest PR Diff & Acceptance Criteria")
    st.caption("Prune noise and evaluate spec conformance locally on your laptop before calling expensive cloud models.")

    col1, col2 = st.columns(2)

    with col1:
        pr_id = st.text_input("Pull Request ID", "PR-STREAM-409")
        title = st.text_input("Feature Title", "Implement Player Buffer Auto-Flush")
        criteria_text = st.text_area(
            "Target Spec Acceptance Criteria (1 per line)",
            "Buffer flushes automatically when size reaches 50 items\n"
            "Buffer flushes if 5 seconds elapse on timer\n"
            "Exponential backoff retry on HTTP 5xx errors",
            height=100
        )

        sample_diff = (
            "diff --git a/player/buffer.py b/player/buffer.py\n"
            "index 84a1e9..2c99b1 100644\n"
            "--- a/player/buffer.py\n"
            "+++ b/player/buffer.py\n"
            "@@ -10,6 +10,14 @@\n"
            "// Standard boilerplate comments that blow up context limits\n"
            "// More license headers\n"
            "+ class BufferManager:\n"
            "+     def __init__(self, max_size=50, interval_sec=5.0):\n"
            "+         self.queue = []\n"
            "+         self.max_size = max_size\n"
            "+         self.interval = interval_sec\n"
            "+\n"
            "+     def push(self, event):\n"
            "+         self.queue.append(event)\n"
            "+         if len(self.queue) >= self.max_size:\n"
            "+             self.flush()\n"
        )
        raw_diff_input = st.text_area("Raw Git Diff Input", sample_diff, height=220)
        run_btn = st.button("🚀 Prune Context & Run Local Pre-Flight Gate", type="primary", use_container_width=True)

    with col2:
        if run_btn:
            crit_list = [c.strip() for c in criteria_text.split("\n") if c.strip()]
            payload = PRDiffPayload(
                pr_id=pr_id,
                feature_title=title,
                target_spec_criteria=crit_list,
                raw_diff_text=raw_diff_input
            )

            # Step 1: Prune
            report = pruner.prune_diff(raw_diff_input)
            
            st.subheader("2. Context Pruning Analytics")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Context Size Reduction", f"{report.reduction_percentage}%", delta="Tokens Saved")
            with m2:
                st.metric("Tokens Conserved", f"{report.tokens_conserved_estimate:,}")
            with m3:
                st.metric("Character Footprint", f"{report.pruned_char_count} chars", delta=f"-{report.original_char_count - report.pruned_char_count}")

            st.markdown("**Pruned Functional Delta (Sent to Model):**")
            st.code(report.pruned_context_text, language="python")

            st.divider()

            # Step 2: Local Pre-flight Gate
            st.subheader("3. Local Pre-Flight Gating Verdict ($0 Cost)")
            with st.spinner("Auditing against acceptance criteria via local Ollama..."):
                gate_result = gate.evaluate_preflight(payload, report)

            if gate_result.gate_verdict == "LOCAL_PASS_READY_FOR_PR":
                st.success("### ✅ VERDICT: LOCAL PASS (Ready for PR & Review)")
            else:
                st.warning("### ⚠️ VERDICT: LOCAL REJECT (Missing Criteria Detected)")

            st.markdown(f"**Gating Feedback:** {gate_result.developer_actionable_feedback}")

            if gate_result.missing_criteria:
                st.error("**Missing Acceptance Criteria:**")
                for m in gate_result.missing_criteria:
                    st.markdown(f"- ❌ {m}")

            st.info(f"💡 **FinOps Efficiency:** Avoided **${gate_result.cloud_cost_saved_usd:.4f}** in cloud API waste on this single run.")

# ----------------- TAB 2: FINOPS CALCULATOR -----------------
with tab2:
    st.subheader("Enterprise FinOps Savings Simulator")
    st.caption("Model the organizational dollar savings of local pre-flight pruning across engineering squads.")

    c1, c2 = st.columns(2)
    with c1:
        engineers_count = st.slider("Number of Active Engineers Using AI Agents", min_value=10, max_value=500, value=100, step=10)
        prs_per_day = st.slider("Average PRs / Commits per Engineer per Day", min_value=1, max_value=8, value=3)
        cloud_token_rate = st.selectbox("Cloud Model Tier ($ / 1M Tokens)", [15.0, 10.0, 5.0, 3.0], index=0)

    with c2:
        # Calculate monthly savings
        total_monthly_prs = engineers_count * prs_per_day * 22  # 22 working days
        avg_tokens_saved_per_pr = 2500  # average pruning savings
        total_tokens_saved = total_monthly_prs * avg_tokens_saved_per_pr
        monthly_dollars_saved = (total_tokens_saved / 1_000_000) * cloud_token_rate

        st.markdown("### Projected Monthly Enterprise Savings")
        st.metric(label="Monthly Cloud API Spend Avoided", value=f"${monthly_dollars_saved:,.2f}", delta="68% Budget Conservation")
        st.metric(label="Monthly Tokens Pruned", value=f"{total_tokens_saved / 1_000_000:.1f} Million Tokens")
        st.success(f"By filtering noise and running pre-flight gates locally with open-source models, an organization of **{engineers_count} engineers** saves **${monthly_dollars_saved:,.2f} every month**.")
