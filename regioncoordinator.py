import cv2

# Load video or use webcam
cap = cv2.VideoCapture(0)  # Change to "your_video.mp4" for video file

points = []
drawing = False

def draw_polygon(event, x, y, flags, param):
    global points, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        drawing = True

    elif event == cv2.EVENT_RBUTTONDOWN:
        # Finish region on right click
        print("Region points:", points)
        points = []

# Set up window
cv2.namedWindow("Select Region (Left-click to add points, Right-click to finish)")
cv2.setMouseCallback("Select Region (Left-click to add points, Right-click to finish)", draw_polygon)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Rotate frame 180 degrees
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # Draw the polygon lines
    for i in range(len(points)):
        cv2.circle(frame, points[i], 5, (0, 255, 0), -1)
        if i > 0:
            cv2.line(frame, points[i - 1], points[i], (0, 255, 255), 2)

    # Connect last point to first for closed polygon
    if len(points) > 2:
        cv2.line(frame, points[-1], points[0], (0, 255, 255), 2)

    cv2.imshow("Select Region (Left-click to add points, Right-click to finish)", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
