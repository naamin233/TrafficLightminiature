import cv2
import requests
import time
import numpy as np
from ultralytics import solutions

# --- Config ---
RASPBERRY_PI_URL = 'http://10.206.110.252:5000/set_pin' # change this based on the http://<RaspberryIpAddress>:5000/set_pin ----1
GREEN_TIME_PER_CAR = 2  # seconds
MAX_GREEN_TIME = 4     # max green light duration

traffic_lights = {
    "Region-1": {"RED": 24, "YELLOW": 23, "GREEN": 18},
    "Region-2": {"RED": 21, "YELLOW": 20, "GREEN": 16},
    "Region-3": {"RED": 17, "YELLOW": 27, "GREEN": 22},
    "Region-4": {"RED": 5,  "YELLOW": 6,  "GREEN": 13}
}

region_points = {
    "Region-1": [(215, 372), (327, 372), (327, 478), (212, 479)],
    "Region-2": [(459, 260), (639, 255), (638, 371), (458, 369)],
    "Region-3": [(346, 2), (449, 2), (452, 138), (342, 135)],
    "Region-4": [(5, 135), (224, 133), (216, 240), (3, 241)],
} # ------Input region from region coordinator -----2

# --- Helper Functions ---
def all_red():
    return {pin: 1 if name == "RED" else 0 for tl in traffic_lights.values() for name, pin in tl.items()}

def set_state(pin_states):
    try:
        response = requests.post(RASPBERRY_PI_URL, json={"pins": pin_states}, timeout=2)
        print("SET STATE:", response.json())
    except Exception as e:
        print("ERROR sending to Raspberry Pi:", e)

def detect_current_counts(frame, regioncounter):
    frame_resized = cv2.resize(frame, (640, 480))
    frame_resized = cv2.rotate(frame_resized, cv2.ROTATE_180)

    # Run detection
    regioncounter(frame_resized)

    # Extract and print real-time counts
    current_counts = regioncounter.region_counts
    print("📊 Real-Time Counts:", current_counts)

    # Manually reset counts so empty lanes go back to zero
    regioncounter.region_counts = {key: 0 for key in regioncounter.region_counts}

    return current_counts, frame_resized

# --- Main Control Loop ---
def run_loop_realtime_counts():
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), "❌ Could not open camera."

    region_order = list(traffic_lights.keys())

    regioncounter = solutions.RegionCounter(
        show=False,
        region=region_points,
        model="best.pt",
        verbose=False
    )

    while True:
        # Capture new frame
        success, frame = cap.read()
        if not success:
            print("❌ Could not read frame.")
            continue

        current_counts, frame_resized = detect_current_counts(frame, regioncounter)

        for region in region_order:
            car_count = current_counts.get(region, 0)

            if car_count == 0:
                print(f"⏩ Skipping {region} (no cars)")
                continue

            print(f"🚦 {region} GREEN phase (cars: {car_count})")

            set_state(all_red())
            time.sleep(1)

            pins = traffic_lights[region]
            pin_states = all_red()
            pin_states[pins["RED"]] = 0
            pin_states[pins["GREEN"]] = 1
            set_state(pin_states)

            # Dynamically adjust green time
            green_time = car_count * GREEN_TIME_PER_CAR
            green_time = min(green_time, MAX_GREEN_TIME)
            print(f"🟢 {region} GREEN for {green_time} seconds (cars: {car_count})")
            time.sleep(green_time)

            # Extra detection loop if green light hits maximum
            if green_time == MAX_GREEN_TIME:
                print(f"🔁 Max GREEN reached. Checking for remaining cars up to 5 times...")
                for i in range(5):
                    time.sleep(2)
                    # Capture new frame
                    success, extra_frame = cap.read()
                    if not success:
                        print("⚠️ Could not read frame during extra check.")
                        break

                    extra_counts, _ = detect_current_counts(extra_frame, regioncounter)
                    extra_car_count = extra_counts.get(region, 0)
                    print(f"  🔍 Extra check {i + 1}: {extra_car_count} cars")

                    if extra_car_count == 0:
                        print("✅ No more cars. Ending green early.")
                        break
                    else:
                        print("🚗 Car(s) still present. Holding green.")

            # Yellow
            pin_states[pins["GREEN"]] = 0
            pin_states[pins["YELLOW"]] = 1
            set_state(pin_states)
            time.sleep(2)

            # Back to Red
            pin_states[pins["YELLOW"]] = 0
            pin_states[pins["RED"]] = 1
            set_state(pin_states)
            time.sleep(1)

            # Let cars move before next detection
            time.sleep(2)

            # Capture new frame after light cycle
            success, frame = cap.read()
            if not success:
                print("⚠️ Could not read frame after region cycle.")
                continue

            current_counts, frame_resized = detect_current_counts(frame, regioncounter)

        # Draw regions
        for region_name, points in region_points.items():
            pts = np.array(points, np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame_resized, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            label_x, label_y = points[0][0], points[0][1] - 10
            cv2.putText(
                frame_resized,
                region_name,
                (label_x, label_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
                cv2.LINE_AA
            )

        # Show updated frame
        cv2.imshow("Region View", frame_resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# --- MAIN ---
if __name__ == '__main__':
    run_loop_realtime_counts()
