import cv2

import config
from video_loader import VideoLoader
from detector import detect_people
from color_classifier import is_inspector
from logger import Logger


def flush_event(log, event_start, event_end, event_max_people, event_inspector):
    if event_start is None:
        return
    start = int(event_start)
    end = int(event_end)
    time_str = f"{start}s-{end}s" if end > start else f"{start}s"
    inspector_str = "YES" if event_inspector else "NO"
    log.log(f"[EVENT]  {time_str:14s} | max_people={event_max_people} | inspector={inspector_str}")


def process_video():
    if config.TARGET_COLOR not in config.HSV_COLORS:
        raise ValueError(
            f"TARGET_COLOR '{config.TARGET_COLOR}' not found in HSV_COLORS. "
            f"Available: {list(config.HSV_COLORS.keys())}"
        )
    hsv_ranges = config.HSV_COLORS[config.TARGET_COLOR]

    log = Logger(config.LOG_FILE)
    try:
        log.log("=== Color Inspector ===")
        log.log(f"Video: {config.VIDEO_PATH}")
        log.log(f"Color: {config.TARGET_COLOR} | Threshold: {config.COLOR_THRESHOLD}")

        with VideoLoader(config.VIDEO_PATH) as loader:
            log.log(f"FPS: {loader.fps} | Total frames: {loader.total_frames}")
            log.log("-" * 50)

            event_start = None
            event_end = None
            event_max_people = 0
            event_inspector = False
            inspector_timestamps = []
            total_events = 0

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

                if people_count > 0:
                    if event_start is None:
                        event_start = timestamp
                        event_end = timestamp
                        event_max_people = people_count
                        event_inspector = inspector_found
                    else:
                        event_end = timestamp
                        event_max_people = max(event_max_people, people_count)
                        event_inspector = event_inspector or inspector_found

                    if inspector_found:
                        log.log(f"[ALERT]  {int(timestamp)}s{'':9s} | people={people_count} | INSPECTOR DETECTED")
                        inspector_timestamps.append(int(timestamp))
                else:
                    if event_start is not None:
                        flush_event(log, event_start, event_end, event_max_people, event_inspector)
                        total_events += 1
                        event_start = None
                        event_end = None
                        event_max_people = 0
                        event_inspector = False

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

            if event_start is not None:
                flush_event(log, event_start, event_end, event_max_people, event_inspector)
                total_events += 1

            duration = int(loader.total_frames / loader.fps) if loader.fps > 0 else 0

        log.log("-" * 50)
        log.log("SUMMARY")
        log.log(f"  Total events: {total_events}")
        log.log(f"  Inspector detected: {len(inspector_timestamps)} times")
        if inspector_timestamps:
            ts_str = ", ".join(f"{t}s" for t in inspector_timestamps)
            log.log(f"  Inspector timestamps: {ts_str}")
        log.log(f"  Video duration: {duration}s")
    finally:
        if config.SHOW_DEBUG:
            cv2.destroyAllWindows()
        log.close()


if __name__ == "__main__":
    process_video()
