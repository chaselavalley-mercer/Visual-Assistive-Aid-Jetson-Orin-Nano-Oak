#!/usr/bin/env python3
"""
closest_distance_alert.py

Prints the closest object distance and its alert level twice per second.
Alert levels: HIGH / MEDIUM / LOW / CLEAR

This is the pre-audio version — classifications are printed only.
Tune THRESHOLDS before connecting to audio output.
"""

import time
import depthai as dai
import numpy as np

# -----------------------------------------------------------------------
# Tunable constants — adjust these before finalizing audio triggers
# -----------------------------------------------------------------------

PRINT_INTERVAL_S = 0.5   # 2x per second

MIN_VALID_MM = 350
MAX_VALID_MM = 8000

ROI_X = (0.25, 0.75)
ROI_Y = (0.25, 0.75)

PERCENTILE = 5

# Distance thresholds in meters — change these to tune sensitivity
THRESHOLD_HIGH_M   = 0.5   # closer than this → HIGH
THRESHOLD_MEDIUM_M = 1.5   # closer than this → MEDIUM
THRESHOLD_LOW_M    = 3.0   # closer than this → LOW
                            # beyond LOW threshold → CLEAR


# -----------------------------------------------------------------------
# Classification
# -----------------------------------------------------------------------

def classify(distance_mm: float | None) -> str:
    """
    Maps a distance in mm to an alert level string.
    Returns 'NO_SIGNAL' if distance is None.
    """
    if distance_mm is None:
        return "NO_SIGNAL"

    meters = distance_mm / 1000.0

    if meters < THRESHOLD_HIGH_M:
        return "HIGH"
    elif meters < THRESHOLD_MEDIUM_M:
        return "MEDIUM"
    elif meters < THRESHOLD_LOW_M:
        return "LOW"
    else:
        return "CLEAR"


# -----------------------------------------------------------------------
# Depth processing
# -----------------------------------------------------------------------

def closest_in_roi(depth_frame: np.ndarray) -> float | None:
    h, w = depth_frame.shape

    x0, x1 = int(w * ROI_X[0]), int(w * ROI_X[1])
    y0, y1 = int(h * ROI_Y[0]), int(h * ROI_Y[1])

    roi = depth_frame[y0:y1, x0:x1]
    valid = roi[(roi >= MIN_VALID_MM) & (roi <= MAX_VALID_MM)]

    if valid.size == 0:
        return None

    return float(np.percentile(valid, PERCENTILE))


# -----------------------------------------------------------------------
# Display
# -----------------------------------------------------------------------

# Visual indicators for each level — makes scanning the terminal easier
LEVEL_DISPLAY = {
    "HIGH":      "🔴 HIGH",
    "MEDIUM":    "🟡 MEDIUM",
    "LOW":       "🟢 LOW",
    "CLEAR":     "   CLEAR",
    "NO_SIGNAL": "   --",
}

def format_output(distance_mm: float | None, level: str) -> str:
    indicator = LEVEL_DISPLAY[level]
    if distance_mm is not None:
        return f"{indicator:<18}  {distance_mm / 1000:.2f} m  ({distance_mm:.0f} mm)"
    else:
        return f"{indicator:<18}  no valid reading"


# -----------------------------------------------------------------------
# Pipeline
# -----------------------------------------------------------------------

def build_pipeline():
    pipeline   = dai.Pipeline()
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
    return pipeline, depth_queue


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

def main():
    pipeline, depth_queue = build_pipeline()

    print("Closest object alert monitor  (Ctrl+C to stop)")
    print(f"Thresholds:  HIGH < {THRESHOLD_HIGH_M}m  |  "
          f"MEDIUM < {THRESHOLD_MEDIUM_M}m  |  "
          f"LOW < {THRESHOLD_LOW_M}m\n")

    last_print  = 0.0
    last_level  = None   # track level changes for future audio trigger logic

    with pipeline:
        pipeline.start()

        while pipeline.isRunning():
            frame = depth_queue.get()
            assert isinstance(frame, dai.ImgFrame)

            now = time.monotonic()
            if now - last_print < PRINT_INTERVAL_S:
                continue

            last_print  = now
            depth_np    = frame.getFrame()
            closest     = closest_in_roi(depth_np)
            level       = classify(closest)

            # Note when the level changes — this is where audio trigger logic
            # will eventually live
            level_changed = (level != last_level)
            last_level    = level

            line = format_output(closest, level)
            if level_changed:
                print(f"{line}  ← level changed")
            else:
                print(line)


if __name__ == "__main__":
    main()