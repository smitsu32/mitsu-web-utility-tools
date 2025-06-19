from flask import Flask, render_template_string
import time
import datetime

app = Flask(__name__)
counter = 0
history = []
last_action = None
start_time = time.time()
step_value = 1
memory_slots = {1: 0, 2: 0, 3: 0}  # 3つのメモリスロット

# ポモドーロタイマーの状態管理
pomodoro_state = {
    'is_running': False,
    'start_time': None,
    'duration': 25 * 60,  # 25分（秒）
    'type': 'work',  # 'work', 'short_break', 'long_break'
    'pomodoro_count': 0,
    'session_pomodoros': 0
}

@app.route('/')
def index():
    elapsed = int(time.time() - start_time)
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    pomodoro_data = get_pomodoro_display()
    
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
        .btn-quick { background: linear-gradient(45deg, #9c27b0, #7b1fa2); color: white; font-size: 1.3em; padding: 15px 30px; min-width: 100px; }
        .quick-controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 15px 0;
            flex-wrap: wrap;
        }
        .memory-section {
            margin: 30px 0;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            backdrop-filter: blur(5px);
        }
        .memory-section h3 {
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        .memory-controls {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-bottom: 20px;
        }
        .memory-slot {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .memory-label {
            font-weight: bold;
            min-width: 80px;
            font-size: 1.1em;
        }
        .btn-memory {
            background: linear-gradient(45deg, #607d8b, #455a64);
            color: white;
            font-size: 0.9em;
            padding: 8px 15px;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-memory:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .btn-memory-clear {
            background: linear-gradient(45deg, #e91e63, #c2185b);
            color: white;
            font-size: 1em;
            padding: 10px 20px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: block;
            margin: 0 auto;
        }
        .btn-memory-clear:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.4);
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
        
        /* ポモドーロタイマー関連のスタイル */
        .pomodoro-section {
            margin: 30px 0;
            padding: 30px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .pomodoro-section h3 {
            text-align: center;
            margin-bottom: 25px;
            font-size: 1.8em;
            color: #ff6b6b;
        }
        .pomodoro-display {
            text-align: center;
            margin: 25px 0;
        }
        .pomodoro-type {
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #ff8a80;
        }
        .pomodoro-timer {
            font-size: 4em;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            margin: 20px 0;
            color: #ffeb3b;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            background: rgba(0,0,0,0.2);
            padding: 20px;
            border-radius: 15px;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        .pomodoro-progress-container {
            margin: 20px 0;
        }
        .pomodoro-progress-bar {
            width: 100%;
            height: 25px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        .pomodoro-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff6b6b, #ff8a80);
            transition: width 0.5s ease;
            border-radius: 15px;
        }
        .pomodoro-controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 25px 0;
            flex-wrap: wrap;
        }
        .btn-pomodoro {
            font-size: 1.1em;
            padding: 12px 25px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.4);
            min-width: 120px;
        }
        .btn-pomodoro:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px 0 rgba(31, 38, 135, 0.6);
        }
        .btn-pomodoro-start {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
        }
        .btn-pomodoro-start.paused {
            background: linear-gradient(45deg, #ff9800, #e68900);
        }
        .btn-pomodoro-reset {
            background: linear-gradient(45deg, #f44336, #da190b);
            color: white;
        }
        .btn-pomodoro-complete {
            background: linear-gradient(45deg, #2196F3, #1976D2);
            color: white;
        }
        .pomodoro-stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 25px 0;
            flex-wrap: wrap;
        }
        .pomodoro-stat {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            min-width: 120px;
        }
        .pomodoro-stat-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #ff6b6b;
        }
        .pomodoro-stat-label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-top: 5px;
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
        
        <div class="quick-controls">
            <button class="btn-quick" onclick="quickAdd(100)">+100</button>
            <button class="btn-quick" onclick="quickAdd(10)">+10</button>
            <button class="btn-quick" onclick="quickSub(10)">-10</button>
            <button class="btn-quick" onclick="quickSub(100)">-100</button>
        </div>
        
        <div class="step-controls">
            <button class="btn-step" onclick="addStep()">+ Step</button>
            <button class="btn-step" onclick="subStep()">- Step</button>
            <input type="number" id="step" class="step-input" value="{{ step_value }}" min="1" max="1000" placeholder="1" onchange="updateStep()">
            <span>Step</span>
        </div>
        
        <div class="memory-section">
            <h3>🧠 Memory</h3>
            <div class="memory-controls">
                <div class="memory-slot">
                    <span class="memory-label">M1: {{ memory_slots[1] }}</span>
                    <button class="btn-memory" onclick="memoryStore(1)">Store</button>
                    <button class="btn-memory" onclick="memoryRecall(1)">Recall</button>
                    <button class="btn-memory" onclick="memoryAdd(1)">M+</button>
                </div>
                <div class="memory-slot">
                    <span class="memory-label">M2: {{ memory_slots[2] }}</span>
                    <button class="btn-memory" onclick="memoryStore(2)">Store</button>
                    <button class="btn-memory" onclick="memoryRecall(2)">Recall</button>
                    <button class="btn-memory" onclick="memoryAdd(2)">M+</button>
                </div>
                <div class="memory-slot">
                    <span class="memory-label">M3: {{ memory_slots[3] }}</span>
                    <button class="btn-memory" onclick="memoryStore(3)">Store</button>
                    <button class="btn-memory" onclick="memoryRecall(3)">Recall</button>
                    <button class="btn-memory" onclick="memoryAdd(3)">M+</button>
                </div>
            </div>
            <button class="btn-memory-clear" onclick="memoryClear()">Clear All Memory</button>
        </div>
        
        <div class="pomodoro-section">
            <h3>🍅 ポモドーロタイマー</h3>
            
            <div class="pomodoro-display">
                <div class="pomodoro-type">{{ pomodoro.type_display }}</div>
                <div class="pomodoro-timer" id="pomodoro-timer">{{ pomodoro.time_display }}</div>
                <div class="pomodoro-progress-container">
                    <div class="pomodoro-progress-bar">
                        <div class="pomodoro-progress-fill" style="width: {{ pomodoro.progress }}%"></div>
                    </div>
                </div>
            </div>
            
            <div class="pomodoro-controls">
                <button class="btn-pomodoro btn-pomodoro-start" id="pomodoro-start" onclick="startPomodoro()">
                    {% if pomodoro.is_running %}⏸️ 一時停止{% else %}▶️ 開始{% endif %}
                </button>
                <button class="btn-pomodoro btn-pomodoro-reset" onclick="resetPomodoro()">🔄 リセット</button>
                <button class="btn-pomodoro btn-pomodoro-complete" onclick="completePomodoro()">✅ 完了</button>
            </div>
            
            <div class="pomodoro-stats">
                <div class="pomodoro-stat">
                    <div class="pomodoro-stat-number">{{ pomodoro.pomodoro_count }}</div>
                    <div class="pomodoro-stat-label">完了したポモドーロ</div>
                </div>
                <div class="pomodoro-stat">
                    <div class="pomodoro-stat-number">{{ pomodoro.session_pomodoros }}</div>
                    <div class="pomodoro-stat-label">今日のポモドーロ</div>
                </div>
            </div>
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
        
        function memoryStore(slot) {
            fetch('/memory_store/' + slot, {method: 'POST'}).then(() => location.reload());
        }
        
        function memoryRecall(slot) {
            fetch('/memory_recall/' + slot, {method: 'POST'}).then(() => location.reload());
        }
        
        function memoryAdd(slot) {
            fetch('/memory_add/' + slot, {method: 'POST'}).then(() => location.reload());
        }
        
        function memoryClear() {
            fetch('/memory_clear', {method: 'POST'}).then(() => location.reload());
        }
        
        // ポモドーロタイマー関連の機能
        let pomodoroInterval;
        let isTimerCompleted = false;
        
        function startPomodoro() {
            const startBtn = document.getElementById('pomodoro-start');
            const isRunning = startBtn.textContent.includes('一時停止');
            
            if (isRunning) {
                // 一時停止
                fetch('/pomodoro/pause', {method: 'POST'}).then(() => {
                    startBtn.textContent = '▶️ 開始';
                    startBtn.classList.remove('paused');
                    clearInterval(pomodoroInterval);
                });
            } else {
                // 開始
                fetch('/pomodoro/start', {method: 'POST'}).then(() => {
                    startBtn.textContent = '⏸️ 一時停止';
                    startBtn.classList.add('paused');
                    startPomodoroTimer();
                });
            }
        }
        
        function resetPomodoro() {
            fetch('/pomodoro/reset', {method: 'POST'}).then(() => {
                location.reload();
            });
        }
        
        function completePomodoro() {
            fetch('/pomodoro/complete', {method: 'POST'}).then(() => {
                location.reload();
            });
        }
        
        function startPomodoroTimer() {
            clearInterval(pomodoroInterval);
            pomodoroInterval = setInterval(updatePomodoroDisplay, 1000);
        }
        
        function updatePomodoroDisplay() {
            fetch('/pomodoro/status')
                .then(response => response.json())
                .then(data => {
                    const timerElement = document.getElementById('pomodoro-timer');
                    const progressBar = document.querySelector('.pomodoro-progress-fill');
                    const startBtn = document.getElementById('pomodoro-start');
                    
                    if (data.remaining <= 0 && data.is_running && !isTimerCompleted) {
                        // タイマー完了
                        isTimerCompleted = true;
                        clearInterval(pomodoroInterval);
                        
                        // アラート表示
                        const typeNames = {
                            'work': '作業時間',
                            'short_break': '短い休憩',
                            'long_break': '長い休憩'
                        };
                        alert(`🍅 ${typeNames[data.type] || '作業時間'}が終了しました！`);
                        
                        // 自動的に次のフェーズに移行
                        setTimeout(() => {
                            completePomodoro();
                        }, 1000);
                        return;
                    }
                    
                    if (data.is_running) {
                        const minutes = Math.floor(data.remaining / 60);
                        const seconds = data.remaining % 60;
                        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                        
                        const progress = ((data.total_duration - data.remaining) / data.total_duration) * 100;
                        progressBar.style.width = `${progress}%`;
                        
                        startBtn.textContent = '⏸️ 一時停止';
                        startBtn.classList.add('paused');
                    } else {
                        startBtn.textContent = '▶️ 開始';
                        startBtn.classList.remove('paused');
                        clearInterval(pomodoroInterval);
                    }
                })
                .catch(error => {
                    console.error('ポモドーロ状態の取得に失敗:', error);
                });
        }
        
        // ページロード時にタイマーが実行中かチェック
        document.addEventListener('DOMContentLoaded', function() {
            fetch('/pomodoro/status')
                .then(response => response.json())
                .then(data => {
                    if (data.is_running) {
                        startPomodoroTimer();
                        isTimerCompleted = false;
                    }
                })
                .catch(error => {
                    console.error('初期ポモドーロ状態の取得に失敗:', error);
                });
        });
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
    start_time=start_time,
    memory_slots=memory_slots,
    pomodoro=pomodoro_data
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

@app.route('/memory_store/<int:slot>', methods=['POST'])
def memory_store(slot):
    global memory_slots, counter
    if slot in memory_slots:
        memory_slots[slot] = counter
        add_to_history(f'Store M{slot} = {counter}', counter)
    return '', 204

@app.route('/memory_recall/<int:slot>', methods=['POST'])
def memory_recall(slot):
    global memory_slots, counter
    if slot in memory_slots:
        old_value = counter
        counter = memory_slots[slot]
        add_to_history(f'Recall M{slot} = {counter} (was {old_value})', counter)
    return '', 204

@app.route('/memory_add/<int:slot>', methods=['POST'])
def memory_add(slot):
    global memory_slots, counter
    if slot in memory_slots:
        memory_slots[slot] += counter
        add_to_history(f'M{slot}+ = {memory_slots[slot]} (+{counter})', counter)
    return '', 204

@app.route('/memory_clear', methods=['POST'])
def memory_clear():
    global memory_slots
    memory_slots = {1: 0, 2: 0, 3: 0}
    add_to_history('Clear all memory slots', counter)
    return '', 204

@app.route('/reset', methods=['POST'])
def reset():
    global counter
    old_value = counter
    counter = 0
    add_to_history(f'Reset from {old_value}', counter)
    return '', 204

# ポモドーロタイマー関連のルート
@app.route('/pomodoro/start', methods=['POST'])
def start_pomodoro():
    global pomodoro_state
    if not pomodoro_state['is_running']:
        pomodoro_state['is_running'] = True
        pomodoro_state['start_time'] = time.time()
        add_to_history(f'Started {pomodoro_state["type"]} timer', counter)
    return '', 204

@app.route('/pomodoro/pause', methods=['POST'])
def pause_pomodoro():
    global pomodoro_state
    if pomodoro_state['is_running']:
        pomodoro_state['is_running'] = False
        add_to_history('Paused pomodoro timer', counter)
    return '', 204

@app.route('/pomodoro/reset', methods=['POST'])
def reset_pomodoro():
    global pomodoro_state
    pomodoro_state['is_running'] = False
    pomodoro_state['start_time'] = None
    pomodoro_state['type'] = 'work'
    pomodoro_state['duration'] = 25 * 60
    add_to_history('Reset pomodoro timer', counter)
    return '', 204

@app.route('/pomodoro/complete', methods=['POST'])
def complete_pomodoro():
    global pomodoro_state
    if pomodoro_state['type'] == 'work':
        pomodoro_state['pomodoro_count'] += 1
        pomodoro_state['session_pomodoros'] += 1
        
        # 4ポモドーロ後は長い休憩
        if pomodoro_state['pomodoro_count'] % 4 == 0:
            pomodoro_state['type'] = 'long_break'
            pomodoro_state['duration'] = 15 * 60  # 15分
        else:
            pomodoro_state['type'] = 'short_break'
            pomodoro_state['duration'] = 5 * 60  # 5分
            
        add_to_history(f'Completed pomodoro #{pomodoro_state["pomodoro_count"]}', counter)
    else:
        # 休憩終了後は作業に戻る
        pomodoro_state['type'] = 'work'
        pomodoro_state['duration'] = 25 * 60  # 25分
        add_to_history('Break completed, back to work', counter)
    
    pomodoro_state['is_running'] = False
    pomodoro_state['start_time'] = None
    return '', 204

@app.route('/pomodoro/status')
def pomodoro_status():
    global pomodoro_state
    current_time = time.time()
    
    if pomodoro_state['is_running'] and pomodoro_state['start_time']:
        elapsed = current_time - pomodoro_state['start_time']
        remaining = max(0, pomodoro_state['duration'] - elapsed)
    else:
        remaining = pomodoro_state['duration']
    
    return {
        'is_running': pomodoro_state['is_running'],
        'type': pomodoro_state['type'],
        'remaining': int(remaining),
        'total_duration': pomodoro_state['duration'],
        'pomodoro_count': pomodoro_state['pomodoro_count'],
        'session_pomodoros': pomodoro_state['session_pomodoros']
    }

def get_pomodoro_display():
    """ポモドーロタイマーの表示用データを取得"""
    current_time = time.time()
    
    if pomodoro_state['is_running'] and pomodoro_state['start_time']:
        elapsed = current_time - pomodoro_state['start_time']
        remaining = max(0, pomodoro_state['duration'] - elapsed)
    else:
        remaining = pomodoro_state['duration']
    
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    
    return {
        'time_display': f"{minutes:02d}:{seconds:02d}",
        'is_running': pomodoro_state['is_running'],
        'type': pomodoro_state['type'],
        'type_display': {
            'work': '🍅 作業時間',
            'short_break': '☕ 短い休憩',
            'long_break': '🛋️ 長い休憩'
        }.get(pomodoro_state['type'], '🍅 作業時間'),
        'pomodoro_count': pomodoro_state['pomodoro_count'],
        'session_pomodoros': pomodoro_state['session_pomodoros'],
        'progress': ((pomodoro_state['duration'] - remaining) / pomodoro_state['duration']) * 100 if pomodoro_state['duration'] > 0 else 0
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    