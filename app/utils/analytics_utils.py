"""Analytics helpers using Pandas and NumPy."""
from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd
import numpy as np


def calculate_task_analytics(task_dicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute task analytics from a list of task dictionaries."""
    df = pd.DataFrame(task_dicts)

    if df.empty:
        return {
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "completion_percentage": 0.0,
            "priority_distribution": {},
        }

    total_tasks = int(len(df))
    completed_tasks = int((df["status"] == "completed").sum())
    pending_tasks = int((df["status"] != "completed").sum())

    completion_percentage = float(
        np.round((completed_tasks / total_tasks) * 100, 2)
    )
    priority_distribution = df["priority"].value_counts().to_dict()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_percentage": completion_percentage,
        "priority_distribution": priority_distribution,
    }
