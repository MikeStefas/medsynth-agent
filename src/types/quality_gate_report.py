from typing import List
from pydantic import BaseModel, Field


class QualityGateReport(BaseModel):
    # Pillar 1: Statistical Fidelity
    mean_ks_statistic: float                 # Target: < 0.12
    mean_ks_pass_rate: float                 # Ratio of continuous columns passing p >= 0.05
    mean_tvd_score: float                    # Target: <= 0.10
    dpcm_corr_mae: float                     # Target: <= 0.10
    beta_recall: float                       # Target: >= 0.80 (Anti-mode-collapse)

    # Pillar 2: Clinical Hard Rules
    cvr: float                               # Constraint Violation Rate (MUST BE 0.0%)
    violation_details: List[str] = Field(default_factory=list)

    # Pillar 3: Privacy
    min_dcr: float                           # Distance to Closest Record (MUST BE > 0.0)
    median_dcr: float

    # Global Verdict
    all_passed: bool                         # True if CVR == 0.0, min_dcr > 0.0, and beta_recall >= 0.80
