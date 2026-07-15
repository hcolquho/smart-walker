# Smart Walker Gait Analysis -- Software Architecture

## Philosophy

Build the system as a modular data-processing pipeline. Each module
performs one task, has a well-defined input/output, and can be replaced
independently.

``` text
Frame Source
    ↓
Person Detector
    ↓
Pose Estimator
    ↓
3D Reconstruction
    ↓
Gait Metrics
    ↓
Clinical UI
```

## Project Structure

``` text
smart-walker/
├── configs/
├── data/
├── docs/
│   └── architecture.md
├── models/
├── src/
│   ├── detection/
│   ├── pose/
│   ├── depth/
│   ├── gait/
│   ├── sensors/
│   ├── logger/
│   ├── pipeline/
│   └── utils/
└── tests/
```

## Core Data Contracts

### Frame

-   frame_index: int
-   timestamp: float
-   rgb_image: ndarray

### Detection

-   track_id: int
-   class_id: int
-   confidence: float
-   bbox: \[x1, y1, x2, y2\]

### Pose

-   model_name: str
-   keypoints_2d: Nx2
-   confidence: N

### Skeleton3D

-   joints_xyz: Nx3
-   timestamp: float

### SensorPacket

-   timestamp: float
-   fsr_values
-   imu_values

## Module Interfaces

### FrameSource

Input: video file or live camera. Output: Frame.

### Detector

Input: Frame. Output: list[Detection](#detection).

Implementations: - YOLOv8 (initial) - RT-DETR (future)

### PoseEstimator

Input: - Frame - Detection

Output: - Pose

Implementations: - RTMPose - ViTPose - Future models without changing
downstream code.

### Depth Module

Input: - Pose - Depth image Output: - Skeleton3D

### Gait Metrics

Input: - Skeleton3D Output: - cadence - stride length - gait speed -
stance/swing times - symmetry metrics - joint angles

### Sensor Receiver

Receives: - FSR (UDP) - IMU

Produces SensorPacket objects.

### Logger

Owns all disk writes.

Stores: - RGB - depth - detections - poses - 3D skeletons - IMU - FSR

Format: - HDF5

### Clinical UI

Consumes processed data only. Never communicates directly with detectors
or sensors.

## Design Rules

1.  Never hardcode model-specific outputs outside their module.
2.  Use timestamps everywhere.
3.  Store bounding boxes as \[x1, y1, x2, y2\].
4.  Do not commit model weights (.pt/.pth).
5.  Every module has its own unit test.
6.  Visualization is separate from processing.
7.  Configuration values belong in YAML files under configs/.
8.  The pipeline should work with either phone video or the Orbbec Femto
    Bolt by swapping only the FrameSource.

## Development Roadmap

1.  Environment
2.  YOLO detector
3.  Pose interface
4.  RTMPose implementation
5.  ViTPose implementation
6.  Depth back-projection
7.  Human3.6M validation
8.  ESP32 FSR integration
9.  HDF5 session logging
10. Full Femto Bolt pipeline
11. Clinical dashboard
