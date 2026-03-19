import cv2

import config
from video_loader import VideoLoader
from detector import detect_people
from color_classifier import is_inspector
from logger import Logger


def process_video():
    if config.TARGET_COLOR not in config.HSV_COLORS:
        raise ValueError(
            f"TARGET_COLOR '{config.TARGET_COLOR}' not found in HSV_COLORS. "
            f"Available: {list(config.HSV_COLORS.keys())}"
        )
    hsv_ranges = config.HSV_COLORS[config.TARGET_COLOR]

    log = Logger(config.LOG_FILE)
    try:
        log.log(f"Starting processing: {config.VIDEO_PATH}")
        log.log(f"Target color: {config.TARGET_COLOR} | Threshold: {config.COLOR_THRESHOLD}")
        log.log("-" * 50)

        with VideoLoader(config.VIDEO_PATH) as loader:
            log.log(f"Video FPS: {loader.fps} | Total frames: {loader.total_frames}")

            for timestamp, frame in loader.sample_frames(config.FRAME_INTERVAL):
                boxes = detect_people(frame)
                people_count = len(boxes)

                inspector_found = False
                inspector_boxes = []

                for (x1, y1, x2, y2) in boxes:
                    crop = frame[y1:y2, x1:x2]
                    match = is_inspector(crop, hsv_ranges, config.COLOR_THRESHOLD)
                    inspector_boxes.append(((x1, y1, x2, y2), match))
                    if match:
                        inspector_found = True

                inspector_flag = 1 if inspector_found else 0

                should_log = people_count > 0 or int(timestamp) % config.LOG_INTERVAL == 0
                if should_log:
                    log.log(f"time={int(timestamp)}s | people={people_count} | inspector={inspector_flag}")

                if config.SHOW_DEBUG:
                    debug_frame = frame.copy()
                    for (x1, y1, x2, y2), match in inspector_boxes:
                        color = (0, 255, 0) if match else (0, 0, 255)
                        label = "INSPECTOR" if match else "person"
                        cv2.rectangle(debug_frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(
                            debug_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2,
                        )
                    cv2.imshow("Debug", debug_frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

        log.log("-" * 50)
        log.log("Processing complete.")
    finally:
        if config.SHOW_DEBUG:
            cv2.destroyAllWindows()
        log.close()


if __name__ == "__main__":
    process_video()
