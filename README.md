# Color Inspector Pipeline

A modular computer vision pipeline that detects people in video and classifies them based on clothing color.

---

## Overview

This pipeline processes video frames to:

- Detect people using YOLOv8  
- Extract the upper body region  
- Identify if the person is wearing a target color using HSV filtering  
- Log events with timestamps and alerts  

It is designed to run alongside other models and can be easily extended or integrated.

---

## Pipeline

```
Video → Frame Sampling → Person Detection → Region Cropping
      → Color Classification → Event Logging
```

---

## Project Structure

```
Color_Inspector/
│── detector.py
│── color_classifier.py
│── video_loader.py
│── logger.py
│── config.py
│── output/
│── videos/
```

---

## Setup

```bash
git clone https://github.com/AryahCodes/Color_Inspector.git
cd Color_Inspector
pip install -r requirements.txt
```

Make sure a YOLOv8 model file (e.g., `yolov8n.pt`) is in the project folder.

---

## Usage

```bash
python main.py
```

You can change settings in `config.py`, including:

- Target color  
- Detection thresholds  
- Input video  
- Frame sampling rate  

---

## Output

- Console logs during execution  
- `output/logs.txt` with:
  - Events  
  - Timestamps  
  - Alerts  
