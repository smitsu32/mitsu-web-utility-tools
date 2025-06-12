class TimerStopwatchApp {
    constructor() {
        this.stopwatchInterval = null;
        this.timerInterval = null;
        this.currentTab = 'stopwatch';
        
        this.initializeElements();
        this.bindEvents();
        this.updateDisplay();
    }

    initializeElements() {
        // Tab elements
        this.stopwatchTab = document.getElementById('stopwatch-tab');
        this.timerTab = document.getElementById('timer-tab');
        this.stopwatchSection = document.getElementById('stopwatch-section');
        this.timerSection = document.getElementById('timer-section');

        // Stopwatch elements
        this.stopwatchDisplay = document.getElementById('stopwatch-display');
        this.stopwatchMs = document.getElementById('stopwatch-ms');
        this.stopwatchStart = document.getElementById('stopwatch-start');
        this.stopwatchStop = document.getElementById('stopwatch-stop');
        this.stopwatchLap = document.getElementById('stopwatch-lap');
        this.stopwatchReset = document.getElementById('stopwatch-reset');
        this.lapList = document.getElementById('lap-list');

        // Timer elements
        this.hoursInput = document.getElementById('hours');
        this.minutesInput = document.getElementById('minutes');
        this.secondsInput = document.getElementById('seconds');
        this.timerDisplay = document.getElementById('timer-display');
        this.timerStart = document.getElementById('timer-start');
        this.timerPause = document.getElementById('timer-pause');
        this.timerReset = document.getElementById('timer-reset');
        this.progressCircle = document.getElementById('progress-circle');
        this.timerFinished = document.getElementById('timer-finished');
    }

    bindEvents() {
        // Tab switching
        this.stopwatchTab.addEventListener('click', () => this.switchTab('stopwatch'));
        this.timerTab.addEventListener('click', () => this.switchTab('timer'));

        // Stopwatch controls
        this.stopwatchStart.addEventListener('click', () => this.startStopwatch());
        this.stopwatchStop.addEventListener('click', () => this.stopStopwatch());
        this.stopwatchLap.addEventListener('click', () => this.lapStopwatch());
        this.stopwatchReset.addEventListener('click', () => this.resetStopwatch());

        // Timer controls
        this.timerStart.addEventListener('click', () => this.startTimer());
        this.timerPause.addEventListener('click', () => this.pauseTimer());
        this.timerReset.addEventListener('click', () => this.resetTimer());

        // Timer input changes
        [this.hoursInput, this.minutesInput, this.secondsInput].forEach(input => {
            input.addEventListener('change', () => this.updateTimerDisplay());
        });

        // Close timer finished modal
        this.timerFinished.addEventListener('click', () => {
            this.timerFinished.classList.remove('show');
        });
    }

    switchTab(tab) {
        this.currentTab = tab;
        
        if (tab === 'stopwatch') {
            this.stopwatchTab.classList.add('active');
            this.timerTab.classList.remove('active');
            this.stopwatchSection.classList.add('active');
            this.timerSection.classList.remove('active');
        } else {
            this.timerTab.classList.add('active');
            this.stopwatchTab.classList.remove('active');
            this.timerSection.classList.add('active');
            this.stopwatchSection.classList.remove('active');
        }
    }

    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        const ms = Math.floor((seconds % 1) * 1000);

        if (hours > 0) {
            return {
                display: `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`,
                ms: `.${ms.toString().padStart(3, '0')}`
            };
        } else {
            return {
                display: `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`,
                ms: `.${ms.toString().padStart(3, '0')}`
            };
        }
    }

    // Stopwatch methods
    async startStopwatch() {
        try {
            const response = await fetch('/api/stopwatch/start', { method: 'POST' });
            const data = await response.json();
            
            if (data.running) {
                this.stopwatchStart.disabled = true;
                this.stopwatchStop.disabled = false;
                this.stopwatchLap.disabled = false;
                this.startStopwatchInterval();
            }
        } catch (error) {
            console.error('Error starting stopwatch:', error);
        }
    }

    async stopStopwatch() {
        try {
            const response = await fetch('/api/stopwatch/stop', { method: 'POST' });
            const data = await response.json();
            
            this.stopwatchStart.disabled = false;
            this.stopwatchStop.disabled = true;
            this.stopwatchLap.disabled = true;
            this.stopStopwatchInterval();
        } catch (error) {
            console.error('Error stopping stopwatch:', error);
        }
    }

    async lapStopwatch() {
        try {
            const response = await fetch('/api/stopwatch/lap', { method: 'POST' });
            const data = await response.json();
            
            if (data.status === 'lap_added') {
                this.addLapToDisplay(data.lap);
            }
        } catch (error) {
            console.error('Error adding lap:', error);
        }
    }

    async resetStopwatch() {
        try {
            const response = await fetch('/api/stopwatch/reset', { method: 'POST' });
            const data = await response.json();
            
            this.stopwatchStart.disabled = false;
            this.stopwatchStop.disabled = true;
            this.stopwatchLap.disabled = true;
            this.stopStopwatchInterval();
            this.stopwatchDisplay.textContent = '00:00:00';
            this.stopwatchMs.textContent = '.000';
            this.lapList.innerHTML = '';
        } catch (error) {
            console.error('Error resetting stopwatch:', error);
        }
    }

    startStopwatchInterval() {
        this.stopwatchInterval = setInterval(() => {
            this.updateStopwatchDisplay();
        }, 10);
    }

    stopStopwatchInterval() {
        if (this.stopwatchInterval) {
            clearInterval(this.stopwatchInterval);
            this.stopwatchInterval = null;
        }
    }

    async updateStopwatchDisplay() {
        try {
            const response = await fetch('/api/stopwatch/status');
            const data = await response.json();
            
            const timeFormatted = this.formatTime(data.time);
            this.stopwatchDisplay.textContent = timeFormatted.display;
            this.stopwatchMs.textContent = timeFormatted.ms;
        } catch (error) {
            console.error('Error updating stopwatch display:', error);
        }
    }

    addLapToDisplay(lap) {
        const lapElement = document.createElement('div');
        lapElement.className = 'lap-item';
        
        const timeFormatted = this.formatTime(lap.time);
        
        lapElement.innerHTML = `
            <div class="lap-number">Lap ${lap.lap}</div>
            <div class="lap-time">${timeFormatted.display}${timeFormatted.ms}</div>
            <div class="lap-timestamp">${lap.timestamp}</div>
        `;
        
        this.lapList.insertBefore(lapElement, this.lapList.firstChild);
    }

    // Timer methods
    async startTimer() {
        const hours = parseInt(this.hoursInput.value) || 0;
        const minutes = parseInt(this.minutesInput.value) || 0;
        const seconds = parseInt(this.secondsInput.value) || 0;
        const totalSeconds = hours * 3600 + minutes * 60 + seconds;

        if (totalSeconds <= 0) {
            alert('Please set a valid time!');
            return;
        }

        try {
            const response = await fetch('/api/timer/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ duration: totalSeconds })
            });
            const data = await response.json();
            
            if (data.running) {
                this.timerStart.disabled = true;
                this.timerPause.disabled = false;
                this.startTimerInterval();
            }
        } catch (error) {
            console.error('Error starting timer:', error);
        }
    }

    async pauseTimer() {
        try {
            const response = await fetch('/api/timer/pause', { method: 'POST' });
            const data = await response.json();
            
            this.timerStart.disabled = false;
            this.timerPause.disabled = true;
            this.stopTimerInterval();
        } catch (error) {
            console.error('Error pausing timer:', error);
        }
    }

    async resetTimer() {
        try {
            const response = await fetch('/api/timer/reset', { method: 'POST' });
            const data = await response.json();
            
            this.timerStart.disabled = false;
            this.timerPause.disabled = true;
            this.stopTimerInterval();
            this.updateTimerDisplay();
            this.updateProgressRing(0);
            this.timerFinished.classList.remove('show');
        } catch (error) {
            console.error('Error resetting timer:', error);
        }
    }

    startTimerInterval() {
        this.timerInterval = setInterval(() => {
            this.updateTimerDisplayFromServer();
        }, 100);
    }

    stopTimerInterval() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    async updateTimerDisplayFromServer() {
        try {
            const response = await fetch('/api/timer/status');
            const data = await response.json();
            
            const timeFormatted = this.formatTime(data.remaining);
            this.timerDisplay.textContent = timeFormatted.display;
            
            if (data.total > 0) {
                const progress = (data.total - data.remaining) / data.total;
                this.updateProgressRing(progress);
            }
            
            if (data.finished) {
                this.stopTimerInterval();
                this.timerStart.disabled = false;
                this.timerPause.disabled = true;
                this.showTimerFinished();
            }
        } catch (error) {
            console.error('Error updating timer display:', error);
        }
    }

    updateTimerDisplay() {
        const hours = parseInt(this.hoursInput.value) || 0;
        const minutes = parseInt(this.minutesInput.value) || 0;
        const seconds = parseInt(this.secondsInput.value) || 0;
        const totalSeconds = hours * 3600 + minutes * 60 + seconds;

        const timeFormatted = this.formatTime(totalSeconds);
        this.timerDisplay.textContent = timeFormatted.display;
        this.updateProgressRing(0);
    }

    updateProgressRing(progress) {
        const circumference = 2 * Math.PI * 90;
        const offset = circumference - (progress * circumference);
        this.progressCircle.style.strokeDashoffset = offset;
    }

    showTimerFinished() {
        this.timerFinished.classList.add('show');
        
        // Play sound (if supported)
        const audio = document.getElementById('timer-sound');
        if (audio) {
            audio.play().catch(e => console.log('Could not play sound:', e));
        }
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.timerFinished.classList.remove('show');
        }, 5000);
    }

    updateDisplay() {
        this.updateTimerDisplay();
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TimerStopwatchApp();
});