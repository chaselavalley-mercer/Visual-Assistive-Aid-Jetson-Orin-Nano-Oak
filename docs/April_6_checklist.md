# PVIA Testing Checklist — CDR April 7, 2026

## Software Tests (Laptop + Camera)
- [ ] Run `scripts/check_oak.py` — copy terminal output into doc
- [ ] Run `scripts/test_rgb_preview.py` — note FPS and quality
- [ ] Run `scripts/test_depth_preview.py` — note visual quality
- [ ] Run `scripts/test_depth_distance.py` — place objects at known distances, copy readings
- [ ] Run `scripts/test_tts.py` through laptop speakers
- [ ] Pair Bluetooth headphones and run `scripts/test_tts.py` again — confirm wireless audio
- [ ] Run `scripts/test_yolo_webcam.py` — screenshot terminal output with FPS and detections

## Jetson
- [ ] Attempt Jetson boot — document result either way
- [ ] If boots: run `scripts/check_oak.py` on Jetson
- [ ] If boots + camera connects: run full pipeline end to end

## After Testing
- [ ] Fill in all 4.1 bracketed placeholders with real outputs
- [ ] Final consistency pass on Jetson status language across entire document