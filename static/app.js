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

    let isPolling = false;

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

    function updateUI(state) {
        if (state.is_active) {
            body.classList.remove('system-offline');
            body.classList.add('system-active');

            powerLabel.textContent = "System Active";
            powerLabel.className = "power-text active";
            
            micIndicator.className = "mic-core waiting";
            statusBadge.className = "status-pill status-waiting";
            statusText.textContent = "Standing By";
        } else {
            body.classList.remove('system-active');
            body.classList.add('system-offline');

            powerLabel.textContent = "System Offline";
            powerLabel.className = "power-text inactive";
            
            micIndicator.className = "mic-core disabled";
            statusBadge.className = "status-pill status-offline";
            statusText.textContent = "Offline";
        }
    }

    async function pollStatus() {
        if (isPolling) return;
        isPolling = true;
        
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (powerToggle.checked !== data.is_active) {
                powerToggle.checked = data.is_active;
                updateUI(data);
            }

            // Pseudo-log for demo if something's happening in backend
            // In a real app we'd fetch actual logs from a /api/logs endpoint.
            
        } catch (error) {
            console.error("Polling error:", error);
        } finally {
            isPolling = false;
            setTimeout(pollStatus, 2000);
        }
    }

    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            powerToggle.checked = data.is_active;
            updateUI(data);
            pollStatus();
        })
        .catch(err => {
            console.error(err);
            addLog("Could not connect to assistant backend.", "system");
        });
});
