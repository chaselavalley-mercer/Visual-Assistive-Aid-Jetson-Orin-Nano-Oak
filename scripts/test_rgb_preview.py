#!/usr/bin/env python3
import cv2
import depthai as dai

def main():
    with dai.Pipeline() as pipeline:
        cam = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)
        videoQueue = cam.requestOutput((1280, 720), dai.ImgFrame.Type.BGR888p).createOutputQueue()
        pipeline.start()
        while pipeline.isRunning():
            videoIn = videoQueue.get()
            assert isinstance(videoIn, dai.ImgFrame)
            cv2.imshow("OAK RGB Preview", videoIn.getCvFrame())
            if cv2.waitKey(1) == ord("q"):
                break

if __name__ == "__main__":
    main()