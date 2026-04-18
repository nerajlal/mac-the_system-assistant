document.addEventListener('DOMContentLoaded', () => {
    // Prevent multiple definitions or listeners just in case
    if (window.macooInitialized) return;
    window.macooInitialized = true;

    const powerToggle = document.getElementById('power-toggle');
    const powerLabel = document.getElementById('power-label');
    const micIndicator = document.getElementById('mic-indicator');
    const statusBadge = document.getElementById('status-badge');
    const statusText = document.getElementById('status-text');
    const logStream = document.getElementById('log-stream');
    const body = document.body;

    const snoozeBtn = document.getElementById('snooze-btn');
    const snoozeText = document.getElementById('snooze-text');
    let snoozeTimer = null;
    let isPolling = false;
    let lastHeardProcessed = "";
    let lastSpokenProcessed = "";
    let lastMemoriesSync = "";
    let lastTasksSync = "";

    // Helper: Add a log entry
    function addLog(message, type = 'system') {
        const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'});
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        
        let prefix = '[SYS]';
        if (type === 'user') prefix = '[USR]';
        if (type === 'assistant') prefix = '[MAC]';

        entry.innerHTML = `<span class="time">${prefix} ${time}</span> <span class="msg">${message}</span>`;
        logStream.appendChild(entry);
        
        // Auto scroll to bottom
        logStream.scrollTop = logStream.scrollHeight;
    }

    // Interactive mouse glow for premium cards
    document.querySelectorAll('.group-hover-effect').forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });

    // Toggle assistant state
    powerToggle.addEventListener('change', async (e) => {
        const isActive = e.target.checked;
        
        try {
            const response = await fetch('/api/toggle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ is_active: isActive })
            });
            const data = await response.json();
            
            updateUI(data);
            addLog(`System ${isActive ? 'activated. Protocols engaged.' : 'deactivated. Going into stasis.'}`, 'system');
        } catch (error) {
            console.error("Failed to toggle:", error);
            e.target.checked = !isActive;
            addLog("Error communicating with kernel.", "system");
        }
    });

    // Snooze Logic
    snoozeBtn.addEventListener('click', async () => {
        if (snoozeTimer) return; // Already snoozing

        try {
            const response = await fetch('/api/snooze', { method: 'POST' });
            const data = await response.json();
            
            addLog("Snooze engaged. Silence for 5 minutes.", "system");
            startSnoozeCountdown(data.duration_minutes * 60);
        } catch (error) {
            console.error("Snooze failed:", error);
        }
    });

    function startSnoozeCountdown(seconds) {
        snoozeBtn.classList.add('active');
        let remaining = seconds;
        
        updateSnoozeUI(remaining);
        
        snoozeTimer = setInterval(() => {
            remaining--;
            if (remaining <= 0) {
                clearInterval(snoozeTimer);
                snoozeTimer = null;
                snoozeBtn.classList.remove('active');
                snoozeText.textContent = "Snooze";
                
                // Automatically re-enable system
                fetch('/api/toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ is_active: true })
                }).then(res => res.json()).then(data => updateUI(data));

                addLog("Snooze expired. System returning to stand-by.", "system");
            } else {
                updateSnoozeUI(remaining);
            }
        }, 1000);
    }

    function updateSnoozeUI(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        snoozeText.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    function updateUI(state) {
        if (state.is_active) {
            body.classList.remove('system-offline');
            body.classList.add('system-active');
            powerToggle.checked = true;
            powerLabel.textContent = "System Active";
            powerLabel.className = "power-text active";
            
            micIndicator.className = "mic-core waiting";
            statusBadge.className = "status-pill status-waiting";
            statusText.textContent = "Standing By";
            
            if (snoozeTimer) {
                clearInterval(snoozeTimer);
                snoozeTimer = null;
                snoozeBtn.classList.remove('active');
                snoozeText.textContent = "Snooze";
            }
        } else {
            body.classList.remove('system-active');
            body.classList.add('system-offline');
            powerToggle.checked = false;
            powerLabel.textContent = "System Offline";
            powerLabel.className = "power-text inactive";
            
            micIndicator.className = "mic-core disabled";
            statusBadge.className = "status-pill status-offline";
            statusText.textContent = state.last_heard === "SNOOZE_ENGAGED" ? "Snoozing" : "Offline";
        }
    }

    async function pollStatus() {
        if (isPolling) return;
        isPolling = true;
        
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            updateUI(data);
            
            // Activity Sync - Realtime Logs
            if (data.last_heard && data.last_heard !== lastHeardProcessed && data.last_heard !== "SNOOZE_ENGAGED") {
                addLog(data.last_heard, 'user');
                lastHeardProcessed = data.last_heard;
            }
            if (data.last_spoken && data.last_spoken !== lastSpokenProcessed) {
                addLog(data.last_spoken, 'assistant');
                lastSpokenProcessed = data.last_spoken;
            }
            
            // Handle the API Badge state dynamically
            const apiBadge = document.getElementById('api-status-badge');
            const apiPill = document.getElementById('api-pulse-dot');
            const apiText = document.getElementById('api-status-text');
            
            if (data.api_active) {
                apiBadge.style.background = 'rgba(60, 255, 120, 0.1)';
                apiBadge.style.borderColor = 'rgba(60, 255, 120, 0.3)';
                apiPill.style.background = 'rgb(60, 255, 120)';
                apiText.style.color = 'rgb(120, 255, 150)';
                apiText.textContent = 'API Live (Gemini)';
            } else {
                apiBadge.style.background = 'rgba(255, 60, 60, 0.1)';
                apiBadge.style.borderColor = 'rgba(255, 60, 60, 0.3)';
                apiPill.style.background = 'rgb(255, 60, 60)';
                apiText.style.color = 'rgb(255, 100, 100)';
                apiText.textContent = 'API Offline (Regex)';
            }
            
            // Sync Memories & Tasks
            fetchMemories();
            fetchTasks();
            
        } catch (error) {
            console.error("Polling error:", error);
        } finally {
            isPolling = false;
            setTimeout(pollStatus, 2000);
        }
    }

    // ── Memory Vault Logic ─────────────────────────────────────────────── #
    async function fetchMemories() {
        try {
            const response = await fetch('/api/memories');
            const memories = await response.json();
            renderMemories(memories);
        } catch (error) {
            console.error("Failed to fetch memories:", error);
        }
    }

    function renderMemories(memories) {
        const memoryList = document.getElementById('memory-list');
        const keys = Object.keys(memories);
        
        // Optimize: Only render if data has changed
        const currentState = JSON.stringify(memories);
        if (currentState === lastMemoriesSync) return;
        lastMemoriesSync = currentState;

        if (keys.length === 0) {
            memoryList.innerHTML = `
                <div class="empty-memory">
                    No memories saved yet. Ask Macoo something like "My favorite color is blue".
                </div>`;
            return;
        }

        memoryList.innerHTML = '';
        keys.forEach(key => {
            const item = document.createElement('div');
            item.className = 'memory-item';
            item.innerHTML = `
                <div class="memory-content">
                    <span class="memory-key">${key.replace(/_/g, ' ')}</span>
                    <span class="memory-val">${memories[key]}</span>
                </div>
                <button class="delete-memory-btn" data-key="${key}" title="Forget this memory">
                    <span class="delete-icon">✕</span>
                </button>
            `;
            memoryList.appendChild(item);
        });

        // Attach delete listeners
        document.querySelectorAll('.delete-memory-btn').forEach(btn => {
            btn.onclick = async (e) => {
                e.stopPropagation();
                const key = btn.getAttribute('data-key');
                await deleteMemory(key);
            };
        });
    }

    async function deleteMemory(key) {
        try {
            const response = await fetch(`/api/memories/${key}`, { method: 'DELETE' });
            if (response.ok) {
                await fetchMemories();
                addLog(`Memory deleted: ${key}`, "system");
            }
        } catch (error) {
            console.error("Delete failed:", error);
        }
    }

    // ── Scheduled Tasks Logic ────────────────────────────────────────── #
    async function fetchTasks() {
        try {
            const response = await fetch('/api/tasks');
            const tasks = await response.json();
            renderTasks(tasks);
        } catch (error) {
            console.error("Failed to fetch tasks:", error);
        }
    }

    function renderTasks(tasks) {
        const taskList = document.getElementById('task-list');
        
        // Optimize: Only render if data has changed
        const currentState = JSON.stringify(tasks);
        if (currentState === lastTasksSync) return;
        lastTasksSync = currentState;

        if (tasks.length === 0) {
            taskList.innerHTML = `
                <div class="empty-tasks">
                    No active tasks. Try "Remind me to drink water in 15 minutes".
                </div>`;
            return;
        }

        taskList.innerHTML = '';
        const now = new Date();

        tasks.forEach(task => {
            const item = document.createElement('div');
            item.className = `task-item ${task.type}`;
            
            let timeStr = "";
            let countdownStr = "";
            
            if (task.due_datetime) {
                const due = new Date(task.due_datetime);
                timeStr = due.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                
                const diffMs = due - now;
                const diffMins = Math.round(diffMs / 60000);
                
                if (diffMins > 0) {
                    if (diffMins < 60) {
                        countdownStr = `in ${diffMins}m`;
                    } else if (diffMins < 1440) {
                        countdownStr = `in ${Math.floor(diffMins/60)}h`;
                    } else {
                        countdownStr = `in ${Math.floor(diffMins/1440)}d`;
                    }
                } else {
                    countdownStr = "due now";
                }
            }

            item.innerHTML = `
                <div class="task-meta">
                    <span class="task-type">${task.type}</span>
                    <span class="task-content">${task.content}</span>
                    <span class="task-due">${timeStr} ${countdownStr ? '• ' + countdownStr : ''}</span>
                </div>
                <button class="done-btn" data-id="${task.id}" title="Mark as done">
                    <span class="check-icon">✓</span>
                </button>
            `;
            taskList.appendChild(item);
        });

        // Attach completion listeners
        document.querySelectorAll('.done-btn').forEach(btn => {
            btn.onclick = async (e) => {
                e.stopPropagation();
                const id = btn.getAttribute('data-id');
                await markTaskDone(id);
            };
        });
    }

    async function markTaskDone(id) {
        try {
            const response = await fetch(`/api/tasks/done/${id}`, { method: 'POST' });
            if (response.ok) {
                await fetchTasks();
                addLog("Task completed and archived.", "system");
            }
        } catch (error) {
            console.error("Completion failed:", error);
        }
    }

    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            updateUI(data);
            pollStatus();
        })
        .catch(err => {
            console.error(err);
            addLog("Could not connect to assistant backend.", "system");
        });
});
