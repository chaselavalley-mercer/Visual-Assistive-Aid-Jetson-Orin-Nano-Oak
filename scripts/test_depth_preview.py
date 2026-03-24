"""Basic stereo depth preview test for OAK-D Lite.

Run:
    python scripts/test_depth_preview.py
Press q to quit.
"""

from __future__ import annotations

import cv2
import depthai as dai


def main() -> None:
    pipeline = dai.Pipeline()

    left = pipeline.create(dai.node.Camera)
    left.setBoardSocket(dai.CameraBoardSocket.CAM_B)
    left.setSize(640, 400)
    left.setFps(30)

    right = pipeline.create(dai.node.Camera)
    right.setBoardSocket(dai.CameraBoardSocket.CAM_C)
    right.setSize(640, 400)
    right.setFps(30)

    stereo = pipeline.create(dai.node.StereoDepth)
    stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.DEFAULT)
    stereo.setLeftRightCheck(True)
    stereo.setSubpixel(True)

    left.requestOutput((640, 400), dai.ImgFrame.Type.GRAY8).link(stereo.left)
    right.requestOutput((640, 400), dai.ImgFrame.Type.GRAY8).link(stereo.right)

    out = pipeline.create(dai.node.XLinkOut)
    out.setStreamName("depth")
    stereo.depth.link(out.input)

    with dai.Device(pipeline) as device:
        q_depth = device.getOutputQueue(name="depth", maxSize=4, blocking=False)

        while True:
            packet = q_depth.get()
            frame = packet.getFrame()
            depth_vis = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
            depth_vis = depth_vis.astype("uint8")
            depth_vis = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
            cv2.imshow("OAK Depth Preview", depth_vis)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
