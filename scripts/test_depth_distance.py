#!/usr/bin/env python3
"""
closest_distance.py

Prints the distance to the closest object twice per second.
Terminal only — no display required. Safe over SSH.

Usage:
    python scripts/closest_distance.py
"""

import time
import depthai as dai
import numpy as np

# -----------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------

PRINT_INTERVAL_S = 0.5   # 2 prints per second

# OAK-D Lite with extendedDisparity: reliable floor is ~350mm.
# Readings below this are almost certainly stereo noise.
MIN_VALID_MM = 350
MAX_VALID_MM = 8000

# Only examine the center 50% of the frame horizontally and vertically.
# This avoids the floor (bottom of frame) and ceiling (top), which would
# otherwise always report as the closest surface when the camera is tilted.
ROI_X = (0.25, 0.75)
ROI_Y = (0.25, 0.75)

# 5th percentile of valid pixels = closest cluster, not a single noise spike.
PERCENTILE = 5


# -----------------------------------------------------------------------
# Computation
# -----------------------------------------------------------------------

def closest_in_roi(depth_frame: np.ndarray) -> float | None:
    """
    Returns the closest valid distance in mm within the center ROI,
    or None if no valid pixels exist.
    """
    h, w = depth_frame.shape

    x0, x1 = int(w * ROI_X[0]), int(w * ROI_X[1])
    y0, y1 = int(h * ROI_Y[0]), int(h * ROI_Y[1])

    roi = depth_frame[y0:y1, x0:x1]

    valid = roi[(roi >= MIN_VALID_MM) & (roi <= MAX_VALID_MM)]

    if valid.size == 0:
        return None

    return float(np.percentile(valid, PERCENTILE))


# -----------------------------------------------------------------------
# Pipeline
# -----------------------------------------------------------------------

def build_pipeline():
    pipeline  = dai.Pipeline()
    mono_left  = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B)
    mono_right = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C)
    stereo     = pipeline.create(dai.node.StereoDepth)

    mono_left.requestFullResolutionOutput().link(stereo.left)
    mono_right.requestFullResolutionOutput().link(stereo.right)

    stereo.setRectification(True)
    stereo.setLeftRightCheck(True)
    stereo.setExtendedDisparity(True)
    stereo.setMedianFilter(dai.MedianFilter.KERNEL_7x7)  # v3 direct call

    depth_queue = stereo.depth.createOutputQueue()

    return pipeline, depth_queue


# -----------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------

def main():
    pipeline, depth_queue = build_pipeline()

    print("Starting closest distance monitor (2x/sec). Ctrl+C to stop.\n")

    last_print = 0.0

    with pipeline:
        pipeline.start()

        while pipeline.isRunning():
            frame = depth_queue.get()
            assert isinstance(frame, dai.ImgFrame)

            now = time.monotonic()
            if now - last_print < PRINT_INTERVAL_S:
                continue  # drain the queue but don't process yet

            last_print = now
            depth_np = frame.getFrame()
            closest  = closest_in_roi(depth_np)

            if closest is None:
                print("[--]  No valid reading in ROI")
            else:
                meters = closest / 1000.0
                print(f"[>>]  Closest object: {meters:.2f} m  ({closest:.0f} mm)")


if __name__ == "__main__":
    main()