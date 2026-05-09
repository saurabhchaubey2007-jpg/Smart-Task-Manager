"""WebSocket event registrations for live task updates."""
from __future__ import annotations

from flask_socketio import emit


def register_socketio_events(socketio):
    """Register Socket.IO event handlers."""

    @socketio.on("connect")
    def handle_connect():
        # Notify the client that the socket is ready
        emit("task_updated", {"action": "connected"})

    @socketio.on("disconnect")
    def handle_disconnect():
        # Server-side hook for disconnect events (kept for clarity)
        return None
