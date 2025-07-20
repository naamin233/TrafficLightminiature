# Smart Traffic Light System

This project implements a smart traffic light control system that detects and counts vehicles (toy cars in the simulation) in real time, adjusts the green light duration based on the number of cars, skips the green light if no cars are detected, and periodically checks for cars outside the camera’s view.

## Objectives

* Detect and count vehicles in real time using a trained YOLOv8 model.
* Dynamically adjust the green light duration based on the number of vehicles detected.
* Skip the green phase when no vehicles are detected.
* Continuously check for vehicles outside the camera range within a maximum green time.

---

## Setup Instructions

### 1️⃣ Define Detection Segments

1. Run `segmentcoordinator.py`.
2. On the displayed camera or image view:

   * **Left-click** to mark points of a segment.
   * **Right-click** to confirm the segment.
3. Copy the printed coordinates.
4. Open `finalcode.py` on your computer.
5. Paste the coordinates into the `region_point` section.
6. Repeat this process for all **4 lanes**.

---

### 2️⃣ Place the Trained Model

1. Copy the trained YOLOv8 `.pt` model file into the project folder.
2. In `finalcode.py`, ensure it is configured to load this `.pt` model.

---

### 3️⃣ Start the Raspberry Pi Server

1. Power on the Raspberry Pi.
2. Run `app.py` on the Raspberry Pi.
3. Note the displayed **IP address**.
4. In `finalcode.py` on your computer, set the URL as:

   ```
   http://<RaspberryPiIP>:5000
   ```

   Replace `<RaspberryPiIP>` with the actual IP address of your Raspberry Pi.

---

### 4️⃣ Check Network Connection

✅ Ensure the Raspberry Pi and the computer are connected to the **same network** (Wi-Fi or LAN).

---

### 5️⃣ Run the System

1. Run `finalcode.py` on your computer.
2. Run `app.py` (Flask server) on the Raspberry Pi.
3. The system will start detecting vehicles and controlling the traffic lights.

---

## ⚙️ Behavior of the System

* **Green Light Time**: 2 seconds per detected car, up to a maximum of 15 seconds.
* **Skip Green**: If no cars are detected, the green phase is skipped.
* **Checking Mode**: If cars move outside the camera’s view and more than 2 cars are detected, the system checks every second until cars return or maximum green time is reached.

---

## 📌 Notes & Limitations

* The detection model is trained on toy cars; it may misidentify hands or other objects during simulation.
* The current camera is a standard one; for better coverage and avoiding tall stands, a 360° camera is recommended.
* The system is designed for simulation and needs further tuning for real-world deployment.

---

## 🛠️ Files in This Project

| File                    | Purpose                                           |
| ----------------------- | ------------------------------------------------- |
| `regioncoordinator.py`  | Plot detection segments and get coordinates       |
| `Finalcode.py`          | Main detection and traffic light control logic    |
| `Raspberrycodevvv       | Flask server running on Raspberry Pi              |
| `best.pt`               | Trained YOLOv8 model file (you must provide this) |

---

## 📞 Contact

For any questions or improvements, feel free to reach out to the project developer.

---
