import cv2
from ultralytics import solutions

# Open webcam
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Error: Could not open camera 0."

# Define 4 regions for car counting
region_points = {
    "Region-1": [(360, 0), (462, 3), (469, 170), (358, 169)],
    "Region-2": [(479, 293), (639, 287), (639, 399), (476, 397)],
    "Region-3": [(239, 403), (350, 402), (350, 476), (242, 475)],
    "Region-4": [(3, 169), (240, 166), (231, 277), (2, 279)],
}

# Initialize RegionCounter with default 'line' mode
regioncounter = solutions.RegionCounter(
    show=True,
    region=region_points,
    model="best.pt",
    verbose=False
)

# Main loop
while True:
    success, frame = cap.read()
    if not success:
        print("Error: Couldn't read frame.")
        break

    # Resize frame for consistent detection
    frame_resized = cv2.resize(frame, (640, 480))
    frame_resized = cv2.rotate(frame_resized, cv2.ROTATE_180)

    # Run region counter
    results = regioncounter(frame_resized)

    # Print live counts
    print("📊 Region Counts (Frame-based):")
    for region, count in regioncounter.region_counts.items():
        print(f"  {region}: {count} cars")

    # Reset after each frame to ensure fresh counts
    regioncounter.region_counts = {key: 0 for key in regioncounter.region_counts}


    # Show output
    cv2.imshow("Car Detection + 4 Region Counting", results.plot_im)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
