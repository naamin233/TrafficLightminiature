from flask import Flask, request, jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

# Pin mappings for each traffic light
traffic_lights = {
    "Region-1": {"RED": 17, "YELLOW": 27, "GREEN": 22},  # TL1
    "Region-2": {"RED": 5,  "YELLOW": 6,  "GREEN": 13},  # TL2
    "Region-3": {"RED": 24, "YELLOW": 23, "GREEN": 18},  # TL3
    "Region-4": {"RED": 21, "YELLOW": 20, "GREEN": 16}   # TL4
}
# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ALL_PINS = [pin for tl in traffic_lights.values() for pin in tl.values()]
for pin in ALL_PINS:
    GPIO.setup(pin, GPIO.OUT)

# Set all pins LOW initially
pin_states = {pin: 0 for pin in ALL_PINS}
for pin, state in pin_states.items():
    GPIO.output(pin, state)
# Track car counts per region
region_counts = {
    "Region-1": 0,
    "Region-2": 0,
    "Region-3": 0,
    "Region-4": 0
}
# Store current traffic light state by region
current_states = {
    name: {"RED": 0, "YELLOW": 0, "GREEN": 0}
    for name in traffic_lights
}


@app.route('/set_pin', methods=['POST'])
def set_pin():
    global pin_states, current_states
    data = request.get_json()
    pins = data.get('pins', {})
    for pin, value in pins.items():
        GPIO.output(pin, value)
        pin_states[pin] = value
    # Update logical state for dashboard
    for region, tl in traffic_lights.items():
        current_states[region] = {
            "RED": pin_states[tl["RED"]],
            "YELLOW": pin_states[tl["YELLOW"]],
            "GREEN": pin_states[tl["GREEN"]]
        }
    return jsonify({"status": "success", "updated_pins": pins})


@app.route('/get_states')
def get_states():
    return jsonify(current_states)
@app.route('/get_counts')
def get_counts():
    return jsonify(region_counts)
@app.route('/update_counts', methods=['POST'])
def update_counts():
    global region_counts
    region_counts = request.get_json()
    return jsonify({"status": "updated"})
# Dashboard HTML with lights and car counts
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Traffic Light Dashboard</title>
    <style>
        body { font-family: Arial; background: #111; color: #eee; text-align: center; }
        .light { width: 30px; height: 30px; border-radius: 50%; margin: 5px auto; }
        .on { box-shadow: 0 0 10px 4px; }
        .red { background: red; }
        .yellow { background: yellow; }
        .green { background: limegreen; }
        .off { background: #333; }
        .tl-box { display: inline-block; margin: 20px; padding: 10px; background: #222; border-radius: 10px; width: 120px; }
    </style>
</head>
<body>
    <h1>Traffic Light Dashboard</h1>
    <div id="lights"></div>

    <script>
        const regionMap = {
            "Region-1": "1",
            "Region-2": "2",
            "Region-3": "3",
            "Region-4": "4"
        };

        async function fetchStates() {
            const [statesRes, countRes] = await Promise.all([
                fetch('/get_states'),
                fetch('/get_counts')
            ]);
            const statesData = await statesRes.json();
            const countData = await countRes.json();
            const lightsDiv = document.getElementById('lights');
            lightsDiv.innerHTML = '';

            for (const [name, states] of Object.entries(statesData)) {
                const redClass = states.RED ? 'light red on' : 'light red off';
                const yellowClass = states.YELLOW ? 'light yellow on' : 'light yellow off';
                const greenClass = states.GREEN ? 'light green on' : 'light green off';
                const count = countData[name] || 0;

                lightsDiv.innerHTML += `
                    <div class="tl-box">
                        <h3>${regionMap[name]}</h3>
                        <div class="${redClass}"></div>
                        <div class="${yellowClass}"></div>
                        <div class="${greenClass}"></div>
                        <p>Cars: ${count}</p>
                    </div>`;
            }
        }

        setInterval(fetchStates, 1000);
        fetchStates();
    </script>
</body>
</html>
"""
@app.route('/')
def dashboard():
    return DASHBOARD_HTML
# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
