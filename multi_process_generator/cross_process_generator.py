import pandas as pd
from typing import Dict
from .config import MULTI_PROCESS_CONFIGS, MultiProcessType

class CrossProcessGenerator:
    def __init__(self, process_type: MultiProcessType):
        self.config = MULTI_PROCESS_CONFIGS.get(process_type)

    def generate(self, num_cases: int):
        rows = []
        chain = "→".join(self.config["process_chain"])
        for i in range(num_cases):
            rows.append({
                "case_id": i+1,
                "process_chain": chain,
                "success_rate": sum(self.config.get("process_weights", [])) / max(1, len(self.config.get("process_weights", [])))
            })
        return pd.DataFrame(rows)

def calculate_cross_process_metrics(events_df: pd.DataFrame) -> Dict:
    return {
        "total_cases": len(events_df),
        "unique_chains": int(events_df["process_chain"].nunique()) if "process_chain" in events_df.columns else 0,
    }

def create_cross_process_summary(events_df: pd.DataFrame) -> pd.DataFrame:
    if "process_chain" not in events_df.columns:
        return pd.DataFrame()
    return events_df.groupby("process_chain").size().reset_index(name="count")
