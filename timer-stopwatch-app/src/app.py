from flask import Flask, render_template, jsonify, request
import time
import threading
from datetime import datetime

app = Flask(__name__, static_folder='../static', template_folder='../templates')

class TimerStopwatch:
    def __init__(self):
        self.stopwatch_start_time = None
        self.stopwatch_elapsed = 0
        self.stopwatch_running = False
        self.stopwatch_lap_times = []
        
        self.timer_duration = 0
        self.timer_start_time = None
        self.timer_running = False
        self.timer_paused_time = 0

timer_sw = TimerStopwatch()
1
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stopwatch/start', methods=['POST'])
def stopwatch_start():
    if not timer_sw.stopwatch_running:
        timer_sw.stopwatch_start_time = time.time() - timer_sw.stopwatch_elapsed
        timer_sw.stopwatch_running = True
    return jsonify({'status': 'started', 'running': timer_sw.stopwatch_running})

@app.route('/api/stopwatch/stop', methods=['POST'])
def stopwatch_stop():
    if timer_sw.stopwatch_running:
        timer_sw.stopwatch_elapsed = time.time() - timer_sw.stopwatch_start_time
        timer_sw.stopwatch_running = False
    return jsonify({'status': 'stopped', 'running': timer_sw.stopwatch_running})

@app.route('/api/stopwatch/reset', methods=['POST'])
def stopwatch_reset():
    timer_sw.stopwatch_start_time = None
    timer_sw.stopwatch_elapsed = 0
    timer_sw.stopwatch_running = False
    timer_sw.stopwatch_lap_times = []
    return jsonify({'status': 'reset', 'time': 0})

@app.route('/api/stopwatch/lap', methods=['POST'])
def stopwatch_lap():
    if timer_sw.stopwatch_running:
        current_time = time.time() - timer_sw.stopwatch_start_time
        lap_time = {
            'lap': len(timer_sw.stopwatch_lap_times) + 1,
            'time': current_time,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        timer_sw.stopwatch_lap_times.append(lap_time)
        return jsonify({'status': 'lap_added', 'lap': lap_time, 'laps': timer_sw.stopwatch_lap_times})
    return jsonify({'status': 'not_running'})

@app.route('/api/stopwatch/status')
def stopwatch_status():
    current_time = 0
    if timer_sw.stopwatch_running and timer_sw.stopwatch_start_time:
        current_time = time.time() - timer_sw.stopwatch_start_time
    elif not timer_sw.stopwatch_running:
        current_time = timer_sw.stopwatch_elapsed
    
    return jsonify({
        'running': timer_sw.stopwatch_running,
        'time': current_time,
        'laps': timer_sw.stopwatch_lap_times
    })

@app.route('/api/timer/start', methods=['POST'])
def timer_start():
    data = request.get_json()
    duration = data.get('duration', 0)
    
    if duration > 0 and not timer_sw.timer_running:
        timer_sw.timer_duration = duration
        timer_sw.timer_start_time = time.time()
        timer_sw.timer_running = True
        timer_sw.timer_paused_time = 0
    
    return jsonify({'status': 'started', 'running': timer_sw.timer_running})

@app.route('/api/timer/pause', methods=['POST'])
def timer_pause():
    if timer_sw.timer_running:
        timer_sw.timer_paused_time += time.time() - timer_sw.timer_start_time
        timer_sw.timer_running = False
    return jsonify({'status': 'paused', 'running': timer_sw.timer_running})

@app.route('/api/timer/resume', methods=['POST'])
def timer_resume():
    if not timer_sw.timer_running and timer_sw.timer_duration > 0:
        timer_sw.timer_start_time = time.time()
        timer_sw.timer_running = True
    return jsonify({'status': 'resumed', 'running': timer_sw.timer_running})

@app.route('/api/timer/reset', methods=['POST'])
def timer_reset():
    timer_sw.timer_duration = 0
    timer_sw.timer_start_time = None
    timer_sw.timer_running = False
    timer_sw.timer_paused_time = 0
    return jsonify({'status': 'reset'})

@app.route('/api/timer/status')
def timer_status():
    remaining_time = 0
    if timer_sw.timer_running and timer_sw.timer_start_time:
        elapsed = time.time() - timer_sw.timer_start_time + timer_sw.timer_paused_time
        remaining_time = max(0, timer_sw.timer_duration - elapsed)
        if remaining_time <= 0:
            timer_sw.timer_running = False
    elif timer_sw.timer_duration > 0:
        remaining_time = max(0, timer_sw.timer_duration - timer_sw.timer_paused_time)
    
    return jsonify({
        'running': timer_sw.timer_running,
        'remaining': remaining_time,
        'total': timer_sw.timer_duration,
        'finished': remaining_time <= 0 and timer_sw.timer_duration > 0
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)