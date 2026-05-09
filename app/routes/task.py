"""Task management REST API endpoints."""
from __future__ import annotations

from flask import Blueprint, request, jsonify, session

from app import db, socketio
from app.models import Task
from app.routes.auth import login_required

task_bp = Blueprint("task", __name__, url_prefix="/api/tasks")

ALLOWED_PRIORITIES = {"low", "medium", "high"}
ALLOWED_STATUSES = {"pending", "completed"}


@task_bp.get("/")
@login_required
def get_tasks():
    """Return all tasks for the logged-in user."""
    tasks = (
        Task.query.filter_by(user_id=session["user_id"])
        .order_by(Task.created_date.desc())
        .all()
    )
    return jsonify({"success": True, "tasks": [task.to_dict() for task in tasks]})


@task_bp.get("/<int:task_id>")
@login_required
def get_task(task_id: int):
    """Return a single task by ID."""
    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first()
    if not task:
        return jsonify({"success": False, "error": "Task not found"}), 404
    return jsonify({"success": True, "task": task.to_dict()})


@task_bp.post("/")
@login_required
def create_task():
    """Create a new task for the logged-in user."""
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip() or None
    priority = str(data.get("priority", "medium")).strip().lower()
    status = str(data.get("status", "pending")).strip().lower()

    if not title:
        return jsonify({"success": False, "error": "Title is required"}), 400
    if priority not in ALLOWED_PRIORITIES:
        return jsonify({"success": False, "error": "Invalid priority"}), 400
    if status not in ALLOWED_STATUSES:
        return jsonify({"success": False, "error": "Invalid status"}), 400

    task = Task(
        title=title,
        description=description,
        priority=priority,
        status=status,
        user_id=session["user_id"],
    )
    db.session.add(task)
    db.session.commit()

    socketio.emit(
        "task_updated",
        {"action": "created", "task": task.to_dict()},
        skip_sid=False
    )

    return jsonify({"success": True, "task": task.to_dict()}), 201


@task_bp.put("/<int:task_id>")
@login_required
def update_task(task_id: int):
    """Update an existing task by ID."""
    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first()
    if not task:
        return jsonify({"success": False, "error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    if "title" in data:
        title = str(data.get("title", "")).strip()
        if not title:
            return jsonify({"success": False, "error": "Title is required"}), 400
        task.title = title

    if "description" in data:
        task.description = str(data.get("description", "")).strip() or None

    if "priority" in data:
        priority = str(data.get("priority", "")).strip().lower()
        if priority not in ALLOWED_PRIORITIES:
            return jsonify({"success": False, "error": "Invalid priority"}), 400
        task.priority = priority

    if "status" in data:
        status = str(data.get("status", "")).strip().lower()
        if status not in ALLOWED_STATUSES:
            return jsonify({"success": False, "error": "Invalid status"}), 400
        task.status = status

    db.session.commit()

    socketio.emit(
        "task_updated",
        {"action": "updated", "task": task.to_dict()},
        skip_sid=False
    )

    return jsonify({"success": True, "task": task.to_dict()})


@task_bp.delete("/<int:task_id>")
@login_required
def delete_task(task_id: int):
    """Delete a task by ID."""
    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first()
    if not task:
        return jsonify({"success": False, "error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    socketio.emit(
        "task_updated",
        {"action": "deleted", "task_id": task_id},
        skip_sid=False
    )

    return jsonify({"success": True, "message": "Task deleted"})
