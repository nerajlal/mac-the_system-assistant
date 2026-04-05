document.addEventListener('DOMContentLoaded', () => {
    const powerToggle = document.getElementById('power-toggle');
    const powerLabel = document.getElementById('power-label');
    const micIndicator = document.getElementById('mic-indicator');
    const statusBadge = document.getElementById('status-badge');
    const logStream = document.getElementById('log-stream');

    let isPolling = false;

    // Helper: Add a log entry
    function addLog(message, type = 'system') {
        const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'});
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        entry.innerHTML = `<span class="time">${time}</span> ${message}`;
        logStream.appendChild(entry);
        
        // Auto scroll to bottom
        logStream.scrollTop = logStream.scrollHeight;
    }

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
            addLog(`System ${isActive ? 'activated. Now listening.' : 'deactivated. Sleeping.'}`);
        } catch (error) {
            console.error("Failed to toggle:", error);
            // Revert UI on failure
            e.target.checked = !isActive;
            addLog("Error communicating with the assistant.", "system");
        }
    });

    // Update UI based on remote state
    function updateUI(state) {
        if (state.is_active) {
            powerLabel.textContent = "System Active";
            powerLabel.className = "power-label active";
            micIndicator.className = "mic-icon waiting";
            statusBadge.textContent = "Waiting";
            statusBadge.style.color = "var(--accent)";
            statusBadge.style.borderColor = "var(--accent)";
        } else {
            powerLabel.textContent = "System Inactive";
            powerLabel.className = "power-label inactive";
            micIndicator.className = "mic-icon disabled";
            statusBadge.textContent = "Offline";
            statusBadge.style.color = "var(--text-muted)";
            statusBadge.style.borderColor = "var(--panel-border)";
        }
    }

    // Poll status periodically (Optional polish: can be expanded later to stream logs real-time)
    async function pollStatus() {
        if (isPolling) return;
        isPolling = true;
        
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            // Only update toggle UI if they don't match (prevents jitter)
            if (powerToggle.checked !== data.is_active) {
                powerToggle.checked = data.is_active;
                updateUI(data);
            }
        } catch (error) {
            console.error("Polling error:", error);
        } finally {
            isPolling = false;
            setTimeout(pollStatus, 2000); // Poll every 2 seconds
        }
    }

    // Initial state check
    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            powerToggle.checked = data.is_active;
            updateUI(data);
            pollStatus();
        })
        .catch(err => {
            console.error(err);
            addLog("Could not connect to assistant backend.", "danger");
        });
});
