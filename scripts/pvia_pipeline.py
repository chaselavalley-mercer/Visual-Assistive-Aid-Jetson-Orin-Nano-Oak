#!/usr/bin/env python3
"""
pvia_pipeline.py

PVIA main detection pipeline.
Captures RGB + stereo depth from OAK-D Lite, runs YOLOv8n inference,
fuses depth at bounding box center, classifies alert level,
and speaks navigation alerts via pyttsx3.

Usage:
    python scripts/pvia_pipeline.py
"""

import time
import threading
import numpy as np
import cv2
import depthai as dai
from ultralytics import YOLO
import pyttsx3

# -----------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------

MODEL_PATH       = "yolov8n.pt"
CONFIDENCE       = 0.4
COOLDOWN_S       = 2.0
PRINT_INTERVAL_S = 1.0

HIGH_THRESH   = 0.5
MEDIUM_THRESH = 1.5
LOW_THRESH    = 3.0

ROI_X = (0.25, 0.75)
ROI_Y = (0.25, 0.75)

MIN_DEPTH_MM = 350
MAX_DEPTH_MM = 8000

# -----------------------------------------------------------------------
# TTS — background thread so it never blocks the main loop
# -----------------------------------------------------------------------

class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 1.0)
        self._lock = threading.Lock()
        self._busy = False

    def speak(self, text: str):
        if self._busy:
            return
        def _run():
            self._busy = True
            with self._lock:
                self.engine.say(text)
                self.engine.runAndWait()
            self._busy = False
        threading.Thread(target=_run, daemon=True).start()

# -----------------------------------------------------------------------
# Alert logic
# -----------------------------------------------------------------------

def classify_alert(distance_m: float) -> str:
    if distance_m < HIGH_THRESH:
        return "HIGH"
    elif distance_m < MEDIUM_THRESH:
        return "MEDIUM"
    elif distance_m < LOW_THRESH:
        return "LOW"
    return "CLEAR"

def build_announcement(label, distance_m: float, level: str):
    if level == "CLEAR":
        return None
    if label:
        return f"{label}, {distance_m:.1f} meters ahead"
    return f"Obstacle, {distance_m:.1f} meters ahead"

# -----------------------------------------------------------------------
# Depth utilities
# -----------------------------------------------------------------------

def depth_at_bbox_center(depth_frame, x1, y1, x2, y2):
    cx = int((x1 + x2) / 2)
    cy = int((y1 + y2) / 2)
    h, w = depth_frame.shape

    px0 = max(0, cx - 5)
    px1 = min(w, cx + 5)
    py0 = max(0, cy - 5)
    py1 = min(h, cy + 5)

    patch = depth_frame[py0:py1, px0:px1]
    valid = patch[(patch >= MIN_DEPTH_MM) & (patch <= MAX_DEPTH_MM)]

    if valid.size == 0:
        return None
    return float(np.median(valid))

def depth_at_center_roi(depth_frame):
    h, w = depth_frame.shape
    x0 = int(w * ROI_X[0])
    x1 = int(w * ROI_X[1])
    y0 = int(h * ROI_Y[0])
    y1 = int(h * ROI_Y[1])

    roi = depth_frame[y0:y1, x0:x1]
    valid = roi[(roi >= MIN_DEPTH_MM) & (roi <= MAX_DEPTH_MM)]

    if valid.size == 0:
        return None
    return float(np.percentile(valid, 5))

# -----------------------------------------------------------------------
# OAK-D Pipeline
# -----------------------------------------------------------------------

def build_oak_pipeline():
    pipeline = dai.Pipeline()

    cam_rgb = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)
    rgb_queue = cam_rgb.requestOutput(
        (640, 480), dai.ImgFrame.Type.BGR888p
    ).createOutputQueue()

    mono_left  = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B)
    mono_right = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C)
    stereo     = pipeline.create(dai.node.StereoDepth)

    mono_left.requestFullResolutionOutput().link(stereo.left)
    mono_right.requestFullResolutionOutput().link(stereo.right)

    stereo.setRectification(True)
    stereo.setLeftRightCheck(True)
    stereo.setExtendedDisparity(True)
    stereo.setMedianFilter(dai.MedianFilter.KERNEL_7x7)

    depth_queue = stereo.depth.createOutputQueue()

    return pipeline, rgb_queue, depth_queue

# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

def main():
    print("Initializing PVIA pipeline...\n")
    print("  Loading YOLOv8n model...")
    model = YOLO(MODEL_PATH)

    print("  Initializing TTS engine...")
    tts = TTSEngine()

    print("  Building OAK-D pipeline...")
    pipeline, rgb_queue, depth_queue = build_oak_pipeline()

    print("\nAll systems initialized. Starting detection loop. Ctrl+C to stop.\n")

    last_alert_time = 0.0
    last_print_time = 0.0
    frame_count     = 0
    start_time      = time.monotonic()

    with pipeline:
        pipeline.start()

        while pipeline.isRunning():
            now = time.monotonic()

            rgb_msg   = rgb_queue.get()
            depth_msg = depth_queue.get()

            if not isinstance(rgb_msg, dai.ImgFrame):
                continue
            if not isinstance(depth_msg, dai.ImgFrame):
                continue

            rgb_np   = rgb_msg.getCvFrame()
            depth_np = depth_msg.getFrame()

            frame_count += 1

            # YOLO inference
            results = model(rgb_np, verbose=False)

            detections = []
            for result in results:
                for box in result.boxes:
                    conf = float(box.conf[0])
                    if conf >= CONFIDENCE:
                        cls_id = int(box.cls[0])
                        label  = model.names[cls_id]
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        detections.append((label, conf, x1, y1, x2, y2))

            # Depth fusion
            chosen_label    = None
            chosen_distance = None

            if detections:
                detections.sort(key=lambda d: d[1], reverse=True)
                label, conf, x1, y1, x2, y2 = detections[0]

                # Scale bbox coords from RGB res to depth res
                rgb_h, rgb_w = rgb_np.shape[:2]
                dep_h, dep_w = depth_np.shape
                sx = dep_w / rgb_w
                sy = dep_h / rgb_h

                depth_mm = depth_at_bbox_center(
                    depth_np,
                    int(x1*sx), int(y1*sy),
                    int(x2*sx), int(y2*sy)
                )
                if depth_mm is not None:
                    chosen_label    = label
                    chosen_distance = depth_mm / 1000.0
            else:
                depth_mm = depth_at_center_roi(depth_np)
                if depth_mm is not None:
                    chosen_distance = depth_mm / 1000.0

            # Alert output
            if chosen_distance is not None:
                level        = classify_alert(chosen_distance)
                announcement = build_announcement(chosen_label, chosen_distance, level)
                cooldown_ok  = (now - last_alert_time) >= COOLDOWN_S

                if announcement and cooldown_ok:
                    tts.speak(announcement)
                    last_alert_time = now
            else:
                level = "CLEAR"

            # Terminal print
            if now - last_print_time >= PRINT_INTERVAL_S:
                last_print_time = now
                elapsed = now - start_time
                fps     = frame_count / elapsed if elapsed > 0 else 0

                print(f"[t={elapsed:.1f}s | FPS={fps:.1f} | Alert={level}]")
                if chosen_label and chosen_distance:
                    print(f"  Object:   {chosen_label}")
                    print(f"  Distance: {chosen_distance:.2f}m")
                elif chosen_distance:
                    print(f"  No object — closest: {chosen_distance:.2f}m")
                else:
                    print("  No valid depth reading")
                if detections:
                    for d in detections:
                        print(f"    {d[0]} ({d[1]:.0%})")
                print()

if __name__ == "__main__":
    main()