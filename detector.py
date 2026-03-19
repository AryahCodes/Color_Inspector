from ultralytics import YOLO

model = YOLO("yolov8n.pt")


def detect_people(frame):
    results = model(frame, verbose=False)
    boxes = []
    for result in results:
        for box in result.boxes:
            if int(box.cls[0]) == 0:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                boxes.append((int(x1), int(y1), int(x2), int(y2)))
    return boxes
