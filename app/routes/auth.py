"""Authentication and page routes."""
from __future__ import annotations

from functools import wraps

from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template

from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


def login_required(view):
    """Require a logged-in user for JSON API routes."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return (
                jsonify({"success": False, "error": "Authentication required"}),
                401,
            )
        return view(*args, **kwargs)

    return wrapped


@auth_bp.get("/")
def index():
    """Redirect users to the correct landing page."""
    if "user_id" in session:
        return redirect(url_for("auth.dashboard"))
    return redirect(url_for("auth.login_page"))


@auth_bp.get("/login")
def login_page():
    """Render the login page."""
    return render_template("login.html")


@auth_bp.get("/register")
def register_page():
    """Render the registration page."""
    return render_template("register.html")


@auth_bp.get("/dashboard")
def dashboard():
    """Render the dashboard for authenticated users."""
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("dashboard.html")


@auth_bp.post("/auth/register")
def register():
    """Register a new user with username, email, and password."""
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", "")).strip()

    if not username or not email or not password:
        return (
            jsonify({"success": False, "error": "All fields are required"}),
            400,
        )

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        return (
            jsonify({"success": False, "error": "User already exists"}),
            409,
        )

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Log the user in after registration
    session.clear()
    session["user_id"] = user.id
    session["username"] = user.username

    return jsonify({"success": True, "user": user.to_dict()}), 201


@auth_bp.post("/auth/login")
def login():
    """Authenticate a user and create a session."""
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", "")).strip()

    if not email or not password:
        return (
            jsonify({"success": False, "error": "Email and password are required"}),
            400,
        )

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return (
            jsonify({"success": False, "error": "Invalid credentials"}),
            401,
        )

    session.clear()
    session["user_id"] = user.id
    session["username"] = user.username

    return jsonify({"success": True, "user": user.to_dict()})


@auth_bp.post("/auth/logout")
def logout():
    """Log out the current user."""
    session.clear()
    return jsonify({"success": True, "message": "Logged out"})
