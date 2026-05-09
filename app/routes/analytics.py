"""Analytics API endpoint using Pandas and NumPy."""
from __future__ import annotations

from flask import Blueprint, jsonify, session

from app.models import Task
from app.routes.auth import login_required
from app.utils.analytics_utils import calculate_task_analytics

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.get("/")
@login_required
def get_analytics():
    """Return analytics for the logged-in user's tasks."""
    tasks = Task.query.filter_by(user_id=session["user_id"]).all()
    task_dicts = [task.to_dict() for task in tasks]

    analytics = calculate_task_analytics(task_dicts)

    return jsonify({"success": True, "analytics": analytics})
