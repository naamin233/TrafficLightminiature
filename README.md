# TrafficLightminiature
Implementation of miniatures traffic light using object detection yolov8

# 🚦 Smart Traffic Light System Using Object Detection

## 📘 Project Summary

This project aims to design and implement a smart traffic light control system that adapts to real-time traffic conditions using object detection. Traditional traffic lights operate on fixed timers, often causing unnecessary delays and congestion. By detecting the presence and type of vehicles (car, bus, lorry, van, and bicycle), the traffic light timing can be adjusted dynamically to improve flow and reduce idle time.

The system is tested in two environments: simulation using SUMO (Simulation of Urban Mobility) and a physical prototype using toy vehicles, Raspberry Pi, and LED-based traffic lights.

---

## 📂 Project Structure
'''pgsql
smart-traffic-light/
├── code/ # Python scripts for detection and control
│ ├── detect_and_control.py
│ └── flask_server.py (optional for GPIO control)
├── sumo/ # SUMO simulation files
│ ├── traffic_simulation.sumocfg
│ ├── network.net.xml
│ └── route.rou.xml
├── schematic/ # Circuit diagrams (PNG, PDF, Fritzing)
├── dataset/ # Images and annotations for training
├── models/ # YOLOv5, YOLOv8, YOLOv11 trained weights
├── results/ # Screenshots, performance metrics, test logs
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## 🧠 Features

- Real-time object detection using YOLOv8 and YOLOv11
- Trained on 5 vehicle classes: **car**, **bus**, **lorry**, **van**, **bicycle**
- Live traffic control using Raspberry Pi and LEDs
- Dynamic signal timing based on vehicle count
- Traffic simulation and comparison using SUMO
- Model comparison: YOLOv5 vs YOLOv8 vs YOLOv11
- Simple web interface for LED control (optional)

---

## 🔧 Tools & Technologies

| Tool               | Purpose                              |
|--------------------|--------------------------------------|
| Python             | Main programming language            |
| OpenCV             | Image processing & camera input      |
| Ultralytics YOLO   | Object detection model               |
| Roboflow           | Dataset labeling & model training    |
| Raspberry Pi       | Physical control unit                |
| SUMO               | Traffic simulation and analysis      |
| Flask              | Web communication (optional)         |
| Fritzing / KiCad   | Circuit schematic                    |

---

## 🚀 How to Run the Project

### ✅ 1. Clone the Repository
```bash
git clone https://github.com/yourusername/smart-traffic-light.git
cd smart-traffic-light

### ✅ 2. Install Python Requirements
```bash
pip install -r requirements.txt

### ✅ 3. Run the Detection & Control Code
```bash
cd code
python detect_and_control.py

### ✅ 4. Run SUMO Simulation
```bash
sumo-gui sumo/traffic_simulation.sumocfg

### ✅ 5. Run Flask Server on Raspberrypi
python flask_server.py

For questions or feedback, please contact:
📧 [naamin233@gmail.com]
🔗 GitHub: [github.com/naamin233]



