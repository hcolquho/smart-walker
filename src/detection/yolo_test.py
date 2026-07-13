from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model(
    "data/samples/walking_test.mov",
    save=True
)