from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class PRDiffPayload(BaseModel):
    pr_id: str
    feature_title: str
    target_spec_criteria: List[str]
    raw_diff_text: str

class PruningReport(BaseModel):
    original_char_count: int
    pruned_char_count: int
    tokens_conserved_estimate: int
    reduction_percentage: float
    pruned_context_text: str

class PreflightGateResult(BaseModel):
    pr_id: str
    gate_verdict: str  # 'LOCAL_PASS_READY_FOR_PR' or 'LOCAL_REJECT_FIX_REQUIRED'
    passed_criteria: List[str]
    missing_criteria: List[str]
    cloud_cost_saved_usd: float
    developer_actionable_feedback: str
