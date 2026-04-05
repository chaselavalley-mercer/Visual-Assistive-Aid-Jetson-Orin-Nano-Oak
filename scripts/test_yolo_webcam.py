#!/usr/bin/env python3
"""
test_yolo_webcam.py

Validates YOLOv8 inference pipeline using the laptop webcam.
Prints detected objects, confidence scores, and FPS to terminal.
No display window — safe over SSH and headless environments.

Usage:
    python scripts/test_yolo_webcam.py
"""

import time
import cv2
from ultralytics import YOLO

# -----------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------

MODEL_PATH = "yolov8n.pt"       # Nano model — fastest inference
CONFIDENCE_THRESHOLD = 0.4      # Only report detections above this
PRINT_INTERVAL_S = 1.0          # Print summary once per second
RUN_DURATION_S = 30             # How long to run before auto-stopping

# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

def main():
    print(f"Loading YOLOv8 model: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)
    print("Model loaded.\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open webcam. Check device index.")
        return

    print(f"Running inference for {RUN_DURATION_S} seconds. Press Ctrl+C to stop early.\n")

    start_time = time.monotonic()
    last_print = 0.0
    frame_count = 0

    try:
        while True:
            now = time.monotonic()
            elapsed = now - start_time

            if elapsed > RUN_DURATION_S:
                print("\nRun duration reached. Stopping.")
                break

            ret, frame = cap.read()
            if not ret:
                print("WARNING: Failed to grab frame.")
                continue

            frame_count += 1
            results = model(frame, verbose=False)

            if now - last_print >= PRINT_INTERVAL_S:
                last_print = now
                fps = frame_count / elapsed if elapsed > 0 else 0

                detections = []
                for result in results:
                    for box in result.boxes:
                        conf = float(box.conf[0])
                        if conf >= CONFIDENCE_THRESHOLD:
                            cls_id = int(box.cls[0])
                            label = model.names[cls_id]
                            detections.append((label, conf))

                print(f"[t={elapsed:.1f}s | FPS={fps:.1f}]")
                if detections:
                    for label, conf in detections:
                        print(f"  Detected: {label} ({conf:.0%} confidence)")
                else:
                    print("  No detections above threshold.")
                print()

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        cap.release()
        total_time = time.monotonic() - start_time
        avg_fps = frame_count / total_time if total_time > 0 else 0
        print(f"\nSummary: {frame_count} frames in {total_time:.1f}s | Avg FPS: {avg_fps:.1f}")

if __name__ == "__main__":
    main()