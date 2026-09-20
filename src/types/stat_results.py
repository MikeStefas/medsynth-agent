from pydantic import BaseModel


class KSResult(BaseModel):
    statistic: float                  # D-statistic in [0, 1] (closer to 0 is better)
    p_value: float                    # p >= 0.05 means distributions match
    passed: bool                      # True if p_value >= 0.05


class TVDResult(BaseModel):
    distance: float                   # TVD in [0, 1] (closer to 0 is better)
    passed: bool                      # True if distance <= 0.10
