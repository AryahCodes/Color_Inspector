import cv2
import numpy as np


def is_inspector(crop, hsv_ranges, threshold):
    if crop.shape[0] == 0 or crop.shape[1] == 0:
        return False

    upper_body_h = int(crop.shape[0] * 0.6)
    upper_body = crop[:upper_body_h, :]

    if upper_body.shape[0] == 0 or upper_body.shape[1] == 0:
        return False

    hsv = cv2.cvtColor(upper_body, cv2.COLOR_BGR2HSV)

    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for (low, high) in hsv_ranges:
        mask |= cv2.inRange(hsv, np.array(low), np.array(high))

    total_pixels = mask.shape[0] * mask.shape[1]
    matching_pixels = cv2.countNonZero(mask)
    ratio = matching_pixels / total_pixels

    return ratio >= threshold
