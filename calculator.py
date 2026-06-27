<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="T-Calc Pro">
    <title>SEN 214 Calculator - Testimony</title>
    
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0; padding: 0; background-color: #121212;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: white; display: flex; flex-direction: column; height: 100vh;
            overflow: hidden; -webkit-user-select: none; user-select: none;
        }
        #display-area {
            flex: 1; display: flex; flex-direction: column; justify-content: flex-end;
            padding: 24px; align-items: flex-end; background-color: #0a0a0a;
            border-bottom: 1px solid #333;
        }
        #equation { font-size: 22px; color: #a1a1aa; min-height: 28px; margin-bottom: 8px; }
        #result { font-size: 60px; font-weight: 400; margin: 0; text-align: right; word-wrap: break-word; max-width: 100%; }
        
        #toggle-container {
            width: 100%; display: flex; justify-content: center; padding: 15px 0 5px;
        }
        #mode-toggle {
            background-color: #27272a; color: #0A84FF; border: 1px solid #0A84FF; border-radius: 8px;
            padding: 8px 24px; font-size: 15px; font-weight: 600; cursor: pointer; text-transform: uppercase; letter-spacing: 1px;
        }
        #mode-toggle:active { background-color: #0A84FF; color: white; }

        #keypad {
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
            padding: 20px; padding-bottom: env(safe-area-inset-bottom, 30px);
        }
        
        button {
            background-color: #27272a; border: none; border-radius: 16px; font-size: 24px;
            color: #f4f4f5; height: 65px; display: flex; justify-content: center; align-items: center;
            cursor: pointer; -webkit-tap-highlight-color: transparent; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        button:active { background-color: #3f3f46; transform: translateY(2px); box-shadow: none; }
        
        .operator { background-color: #0A84FF; font-size: 30px; font-weight: 500; }
        .operator:active { background-color: #0066CC; }
        .function { background-color: #e4e4e7; color: #18181b; font-size: 18px; font-weight: 600; }
        .function:active { background-color: #a1a1aa; }
        .danger { background-color: #ef4444; color: white; }
        .danger:active { background-color: #b91c1c; }
        .zero-btn { grid-column: span 2; }

        .sci-only { display: none; height: 50px; font-size: 16px; }
        .show-scientific .sci-only { display: flex; }
        .show-scientific button { height: 52px; font-size: 20px; border-radius: 12px; } 
        .show-scientific .operator { font-size: 24px; }
    </style>
</head>
<body>

    <div id="display-area">
        <div id="equation"></div>
        <div id="result">0</div>
    </div>

    <div id="toggle-container">
        <button id="mode-toggle" onclick="toggleMode()">Scientific Mode</button>
    </div>

    <div id="keypad">
        <button class="function sci-only" onclick="appendInput('π')">π</button>
        <button class="function sci-only" onclick="appendInput('e')">e</button>
        <button class="function sci-only" onclick="appendInput('^')">xʸ</button>
        <button class="function danger sci-only" onclick="backspace()">⌫</button>

        <button class="function sci-only" onclick="appendInput('sin(')">sin</button>
        <button class="function sci-only" onclick="appendInput('cos(')">cos</button>
        <button class="function sci-only" onclick="appendInput('tan(')">tan</button>
        <button class="function sci-only" onclick="appendInput('√(')">√</button>

        <button class="function sci-only" onclick="appendInput('ln(')">ln</button>
        <button class="function sci-only" onclick="appendInput('log(')">log</button>
        <button class="function sci-only" onclick="appendInput('(')">(</button>
        <button class="function sci-only" onclick="appendInput(')')">)</button>

        <button class="function" onclick="clearDisplay()">AC</button>
        <button class="function" onclick="appendInput('**2')">x²</button>
        <button class="function" onclick="appendInput('%')">%</button>
        <button class="operator" onclick="appendInput('÷')">÷</button>
        
        <button onclick="appendInput('7')">7</button>
        <button onclick="appendInput('8')">8</button>
        <button onclick="appendInput('9')">9</button>
        <button class="operator" onclick="appendInput('×')">×</button>
        
        <button onclick="appendInput('4')">4</button>
        <button onclick="appendInput('5')">5</button>
        <button onclick="appendInput('6')">6</button>
        <button class="operator" onclick="appendInput('-')">−</button>
        
        <button onclick="appendInput('1')">1</button>
        <button onclick="appendInput('2')">2</button>
        <button onclick="appendInput('3')">3</button>
        <button class="operator" onclick="appendInput('+')">+</button>
        
        <button class="zero-btn" onclick="appendInput('0')">0</button>
        <button onclick="appendInput('.')">.</button>
        <button class="operator" onclick="calculateResult()">=</button>
    </div>

    <script>
        let isScientific = false;
        let equationEl = document.getElementById('equation');
        let resultEl = document.getElementById('result');
        let currentInput = "";

        function toggleMode() {
            let keypad = document.getElementById('keypad');
            let toggleBtn = document.getElementById('mode-toggle');
            isScientific = !isScientific;
            
            if(isScientific) {
                keypad.classList.add('show-scientific');
                toggleBtn.innerText = "Standard Mode";
            } else {
                keypad.classList.remove('show-scientific');
                toggleBtn.innerText = "Scientific Mode";
            }
        }

        function updateDisplay() {
            let displayStr = currentInput.replace(/\*\*2/g, '²').replace(/\*\*/g, '^').replace(/\*/g, '×').replace(/\//g, '÷');
            equationEl.innerText = displayStr;
        }

        function appendInput(val) {
            if (resultEl.innerText !== "0" && currentInput === "" && resultEl.innerText !== "Error") {
                if (['+', '-', '×', '÷', '^', '**2', '%'].includes(val)) currentInput = resultEl.innerText + val;
                else { resultEl.innerText = "0"; currentInput = val; }
            } else currentInput += val;
            updateDisplay();
        }

        function backspace() {
            currentInput = currentInput.slice(0, -1);
            if(currentInput === "") resultEl.innerText = "0";
            updateDisplay();
        }

        function clearDisplay() {
            currentInput = ""; equationEl.innerText = ""; resultEl.innerText = "0";
        }

        function calculateResult() {
            try {
                let evalString = currentInput.replace(/π/g, 'Math.PI').replace(/e/g, 'Math.E').replace(/\^/g, '**').replace(/×/g, '*').replace(/÷/g, '/').replace(/%/g, '/100').replace(/√\(/g, 'Math.sqrt(').replace(/ln\(/g, 'Math.log(').replace(/log\(/g, 'Math.log10(').replace(/sin\(/g, 'Math.sin(Math.PI/180*').replace(/cos\(/g, 'Math.cos(Math.PI/180*').replace(/tan\(/g, 'Math.tan(Math.PI/180*');
                let answer = eval(evalString);
                if (answer === undefined || isNaN(answer) || !isFinite(answer)) throw "Error";
                answer = Math.round(answer * 10000000000) / 10000000000;
                resultEl.innerText = answer; currentInput = ""; 
            } catch (error) {
                resultEl.innerText = "Error"; currentInput = "";
            }
        }
    </script>
</body>
</html>
