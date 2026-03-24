"""Basic RGB preview test for OAK camera.

Run:
    python scripts/test_rgb_preview.py
Press q to quit.
"""

from __future__ import annotations

import cv2
import depthai as dai


def main() -> None:
    pipeline = dai.Pipeline()

    cam = pipeline.create(dai.node.Camera)
    cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    cam.setSize(1280, 720)
    cam.setFps(30)

    out = pipeline.create(dai.node.XLinkOut)
    out.setStreamName("rgb")
    cam.video.link(out.input)

    with dai.Device(pipeline) as device:
        q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

        while True:
            packet = q_rgb.get()
            frame = packet.getCvFrame()
            cv2.imshow("OAK RGB Preview", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
