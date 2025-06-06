from flask import Flask, render_template_string
import time
import datetime

app = Flask(__name__)
counter = 0
history = []
last_action = None
start_time = time.time()
step_value = 1

@app.route('/')
def index():
    elapsed = int(time.time() - start_time)
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🎯 Advanced Counter</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .counter-display {
            text-align: center;
            margin: 30px 0;
        }
        .counter {
            font-size: 5em;
            font-weight: bold;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            margin-bottom: 10px;
            color: {{ color }};
            transition: all 0.3s ease;
        }
        .status { font-size: 1.2em; opacity: 0.8; margin-bottom: 20px; }
        .controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        button {
            font-size: 1.2em;
            padding: 15px 25px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.4);
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px 0 rgba(31, 38, 135, 0.6); }
        button:active { transform: translateY(0); }
        .btn-inc { background: linear-gradient(45deg, #4CAF50, #45a049); color: white; }
        .btn-dec { background: linear-gradient(45deg, #f44336, #da190b); color: white; }
        .btn-reset { background: linear-gradient(45deg, #008CBA, #005f73); color: white; }
        .btn-step { background: linear-gradient(45deg, #ff9800, #e68900); color: white; }
        .btn-quick { background: linear-gradient(45deg, #9c27b0, #7b1fa2); color: white; font-size: 1em; padding: 10px 20px; }
        .quick-controls {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 15px 0;
            flex-wrap: wrap;
        }
        .step-controls {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
            align-items: center;
        }
        .step-input {
            padding: 10px;
            border: none;
            border-radius: 10px;
            text-align: center;
            font-size: 1.1em;
            width: 80px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            backdrop-filter: blur(5px);
        }
        .step-input::placeholder { color: rgba(255, 255, 255, 0.7); }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }
        .stat-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 15px;
            text-align: center;
            backdrop-filter: blur(5px);
        }
        .stat-number { font-size: 1.5em; font-weight: bold; }
        .stat-label { font-size: 0.9em; opacity: 0.8; margin-top: 5px; }
        .history {
            max-height: 200px;
            overflow-y: auto;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            margin-top: 20px;
        }
        .history-item {
            padding: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 0.9em;
        }
        .history-item:last-child { border-bottom: none; }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            overflow: hidden;
            margin: 20px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            width: {{ progress }}%;
            transition: width 0.3s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Advanced Counter</h1>
        
        <div class="counter-display">
            <div class="counter">{{ counter }}</div>
            <div class="status">{{ status }}</div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
        
        <div class="controls">
            <button class="btn-inc" onclick="increment()">➕ Add</button>
            <button class="btn-dec" onclick="decrement()">➖ Subtract</button>
            <button class="btn-reset" onclick="reset()">🔄 Reset</button>
        </div>
        
        <div class="step-controls">
            <span>Step:</span>
            <input type="number" id="step" class="step-input" value="{{ step_value }}" min="1" max="1000" placeholder="1" onchange="updateStep()">
            <button class="btn-step" onclick="addStep()">+ Step</button>
            <button class="btn-step" onclick="subStep()">- Step</button>
        </div>
        
        <div class="quick-controls">
            <button class="btn-quick" onclick="quickAdd(10)">+10</button>
            <button class="btn-quick" onclick="quickSub(10)">-10</button>
            <button class="btn-quick" onclick="quickAdd(100)">+100</button>
            <button class="btn-quick" onclick="quickSub(100)">-100</button>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{{ total_clicks }}</div>
                <div class="stat-label">Total Clicks</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{{ max_value }}</div>
                <div class="stat-label">Max Value</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{{ min_value }}</div>
                <div class="stat-label">Min Value</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{{ elapsed_time }}</div>
                <div class="stat-label">Session Time</div>
            </div>
        </div>
        
        {% if history %}
        <div class="history">
            <h3>📊 Recent Actions</h3>
            {% for item in history[-10:] %}
            <div class="history-item">{{ item }}</div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
    
    <script>
        function increment() { 
            fetch('/increment', {method: 'POST'}).then(() => location.reload()); 
        }
        function decrement() { 
            fetch('/decrement', {method: 'POST'}).then(() => location.reload()); 
        }
        function reset() { 
            fetch('/reset', {method: 'POST'}).then(() => location.reload()); 
        }
        function addStep() {
            const step = document.getElementById('step').value;
            fetch('/add_step/' + step, {method: 'POST'}).then(() => location.reload());
        }
        function subStep() {
            const step = document.getElementById('step').value;
            fetch('/sub_step/' + step, {method: 'POST'}).then(() => location.reload());
        }
        
        // Update session time every second
        function updateSessionTime() {
            const startTime = {{ start_time }};
            const now = Date.now() / 1000;
            const elapsed = Math.floor(now - startTime);
            const hours = Math.floor(elapsed / 3600);
            const minutes = Math.floor((elapsed % 3600) / 60);
            const seconds = elapsed % 60;
            const timeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            const timeElement = document.querySelector('.stat-box:last-child .stat-number');
            if (timeElement) {
                timeElement.textContent = timeString;
            }
        }
        
        // Update time every second
        setInterval(updateSessionTime, 1000);
        
        function updateStep() {
            const step = document.getElementById('step').value;
            fetch('/update_step/' + step, {method: 'POST'});
        }
        
        function quickAdd(amount) {
            fetch('/add_step/' + amount, {method: 'POST'}).then(() => location.reload());
        }
        
        function quickSub(amount) {
            fetch('/sub_step/' + amount, {method: 'POST'}).then(() => location.reload());
        }
    </script>
</body>
</html>
    ''', 
    counter=counter,
    color='#ffeb3b' if counter == 0 else '#4CAF50' if counter > 0 else '#f44336',
    status=get_status(),
    progress=min(abs(counter), 100),
    total_clicks=len(history),
    max_value=max([0] + [h['value'] for h in history if isinstance(h, dict)]),
    min_value=min([0] + [h['value'] for h in history if isinstance(h, dict)]),
    elapsed_time=f"{hours:02d}:{minutes:02d}:{seconds:02d}",
    history=[format_history_item(h) for h in history],
    step_value=step_value,
    start_time=start_time
    )

def get_status():
    if counter == 0:
        return "Starting Point"
    elif counter > 0:
        return f"Positive Territory (+{counter})"
    else:
        return f"Negative Territory ({counter})"

def format_history_item(item):
    if isinstance(item, dict):
        return f"{item['time']} - {item['action']} (Value: {item['value']})"
    return str(item)

def add_to_history(action, value):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    history.append({
        'time': timestamp,
        'action': action,
        'value': value
    })
    if len(history) > 50:  # Keep only last 50 actions
        history.pop(0)

@app.route('/increment', methods=['POST'])
def increment():
    global counter
    counter += 1
    add_to_history('Increment +1', counter)
    return '', 204

@app.route('/decrement', methods=['POST'])
def decrement():
    global counter
    counter -= 1
    add_to_history('Decrement -1', counter)
    return '', 204

@app.route('/add_step/<int:step>', methods=['POST'])
def add_step(step):
    global counter
    counter += step
    add_to_history(f'Add +{step}', counter)
    return '', 204

@app.route('/sub_step/<int:step>', methods=['POST'])
def sub_step(step):
    global counter
    counter -= step
    add_to_history(f'Subtract -{step}', counter)
    return '', 204

@app.route('/update_step/<int:step>', methods=['POST'])
def update_step(step):
    global step_value
    step_value = step
    return '', 204

@app.route('/reset', methods=['POST'])
def reset():
    global counter
    old_value = counter
    counter = 0
    add_to_history(f'Reset from {old_value}', counter)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    