/* Global helpers for API calls and UI feedback */
const API = {
  login: "/auth/login",
  register: "/auth/register",
  logout: "/auth/logout",
  tasks: "/api/tasks",
  analytics: "/analytics",
};

const messageBox = document.getElementById("message");

function showMessage(text, type = "success") {
  if (!messageBox) return;
  messageBox.textContent = text;
  messageBox.className = `message ${type}`;
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    ...options,
  });

  let data = {};
  try {
    data = await response.json();
  } catch (e) {
    console.error("Failed to parse JSON:", e);
    data = {};
  }

  if (!response.ok) {
    const errorMsg = data.error || `HTTP ${response.status}: ${response.statusText}`;
    throw new Error(errorMsg);
  }
  return data;
}

/* Login page logic */
const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value.trim();

    try {
      await requestJson(API.login, {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      window.location.href = "/dashboard";
    } catch (error) {
      showMessage(error.message, "error");
    }
  });
}

/* Register page logic */
const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const username = document.getElementById("register-username").value.trim();
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value.trim();

    try {
      await requestJson(API.register, {
        method: "POST",
        body: JSON.stringify({ username, email, password }),
      });
      window.location.href = "/dashboard";
    } catch (error) {
      showMessage(error.message, "error");
    }
  });
}

/* Dashboard logic */
const taskForm = document.getElementById("task-form");
const taskTableBody = document.getElementById("task-table-body");
const cancelEditBtn = document.getElementById("cancel-edit-btn");
const formTitle = document.getElementById("form-title");
const saveTaskBtn = document.getElementById("save-task-btn");
let editingTaskId = null;

function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleString();
}

function resetForm() {
  if (!taskForm) return;
  taskForm.reset();
  document.getElementById("task-priority").value = "medium";
  document.getElementById("task-status").value = "pending";
  editingTaskId = null;
  formTitle.textContent = "Add Task";
  saveTaskBtn.textContent = "Save Task";
  cancelEditBtn.classList.add("hidden");
}

async function loadTasks() {
  if (!taskTableBody) return;
  try {
    const data = await requestJson(API.tasks);
    renderTasks(data.tasks || []);
  } catch (error) {
    console.error("Error loading tasks:", error);
  }
}

function renderTasks(tasks) {
  taskTableBody.innerHTML = "";
  if (!tasks.length) {
    const row = document.createElement("tr");
    row.innerHTML =
      '<td colspan="6" class="muted">No tasks found. Add one above.</td>';
    taskTableBody.appendChild(row);
    return;
  }

  tasks.forEach((task) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${task.title}</td>
      <td>${task.description || "-"}</td>
      <td><span class="badge ${task.priority}">${task.priority}</span></td>
      <td><span class="badge ${task.status}">${task.status}</span></td>
      <td>${formatDate(task.created_date)}</td>
      <td>
        <button class="btn outline edit-btn" data-id="${task.id}">Edit</button>
        <button class="btn outline delete-btn" data-id="${task.id}">Delete</button>
      </td>
    `;
    taskTableBody.appendChild(row);
  });

  document.querySelectorAll(".edit-btn").forEach((button) => {
    button.addEventListener("click", () => {
      const taskId = button.getAttribute("data-id");
      const task = tasks.find((item) => String(item.id) === taskId);
      if (!task) return;
      editingTaskId = task.id;
      document.getElementById("task-title").value = task.title;
      document.getElementById("task-description").value = task.description || "";
      document.getElementById("task-priority").value = task.priority;
      document.getElementById("task-status").value = task.status;
      formTitle.textContent = "Edit Task";
      saveTaskBtn.textContent = "Update Task";
      cancelEditBtn.classList.remove("hidden");
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  document.querySelectorAll(".delete-btn").forEach((button) => {
    button.addEventListener("click", async () => {
      const taskId = button.getAttribute("data-id");
      if (!confirm("Are you sure you want to delete this task?")) return;
      try {
        await requestJson(`${API.tasks}/${taskId}`, { method: "DELETE" });
        showMessage("✅ Task deleted successfully!", "success");
        await loadTasks();
        await loadAnalytics();
        setTimeout(() => (messageBox.textContent = ""), 3000);
      } catch (error) {
        showMessage("❌ " + error.message, "error");
      }
    });
  });
}

async function loadAnalytics() {
  const total = document.getElementById("total-tasks");
  if (!total) return;
  try {
    const data = await requestJson(API.analytics);
    const analytics = data.analytics || {};
    document.getElementById("total-tasks").textContent =
      analytics.total_tasks ?? 0;
    document.getElementById("completed-tasks").textContent =
      analytics.completed_tasks ?? 0;
    document.getElementById("pending-tasks").textContent =
      analytics.pending_tasks ?? 0;
    document.getElementById("completion-rate").textContent =
      `${analytics.completion_percentage ?? 0}%`;

    const dist = analytics.priority_distribution || {};
    const distText = Object.keys(dist).length
      ? Object.entries(dist)
          .map(([key, value]) => `${key}: ${value}`)
          .join(", ")
      : "No data";
    document.getElementById("priority-distribution").textContent = distText;
  } catch (error) {
    console.error("Error loading analytics:", error);
  }
}

if (taskForm) {
  taskForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const title = document.getElementById("task-title").value.trim();
    const description = document.getElementById("task-description").value.trim();
    const priority = document.getElementById("task-priority").value;
    const status = document.getElementById("task-status").value;

    try {
      if (editingTaskId) {
        await requestJson(`${API.tasks}/${editingTaskId}`, {
          method: "PUT",
          body: JSON.stringify({ title, description, priority, status }),
        });
        showMessage("✅ Task updated successfully!", "success");
      } else {
        await requestJson(API.tasks, {
          method: "POST",
          body: JSON.stringify({ title, description, priority, status }),
        });
        showMessage("✅ Task created successfully!", "success");
      }
      resetForm();
      await loadTasks();
      await loadAnalytics();
      setTimeout(() => (messageBox.textContent = ""), 3000);
    } catch (error) {
      showMessage("❌ " + error.message, "error");
    }
  });
}

if (cancelEditBtn) {
  cancelEditBtn.addEventListener("click", () => resetForm());
}

const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    try {
      await requestJson(API.logout, { method: "POST" });
      window.location.href = "/login";
    } catch (error) {
      showMessage(error.message, "error");
    }
  });
}

/* WebSocket live updates */
if (document.body.dataset.page === "dashboard" && window.io) {
  const socket = io();
  socket.on("task_updated", () => {
    loadTasks();
    loadAnalytics();
  });
}

// Load initial dashboard data
if (document.body.dataset.page === "dashboard") {
  loadTasks();
  loadAnalytics();
}
