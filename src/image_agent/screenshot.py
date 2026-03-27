from __future__ import annotations

import base64
import io
import time

import numpy as np
import pywinctl as pwc
from mss import mss
from PIL import Image, ImageGrab
from skimage.metrics import structural_similarity as ssim

from .config import AppPaths, load_config
from .utils import get_save_filename, save_image


SCREENSHOT_BACKEND = "mss"


def bbox_to_ltwh(bounds: tuple[int, int, int, int] | list[int]) -> list[int]:
    return [bounds[0], bounds[1], bounds[2] - bounds[0], bounds[3] - bounds[1]]



def get_bbox(appname: str | None):
    if not appname:
        return None
    windows = pwc.getWindowsWithTitle(appname)
    if windows:
        return windows[0].bbox
    return None



def screenshot(appname: str | None = None):
    bbox = get_bbox(appname)

    if SCREENSHOT_BACKEND == "PIL":
        return ImageGrab.grab(bbox)
    if SCREENSHOT_BACKEND == "mss":
        with mss() as sct:
            monitor = (
                {
                    "left": bbox[0],
                    "top": bbox[1],
                    "width": bbox[2] - bbox[0],
                    "height": bbox[3] - bbox[1],
                }
                if bbox
                else sct.monitors[1]
            )
            captured = sct.grab(monitor)
        return Image.frombytes("RGB", captured.size, captured.rgb)

    import pyautogui

    if bbox is None:
        return pyautogui.screenshot()
    return pyautogui.screenshot(region=bbox_to_ltwh(bbox))



def compare_images(img1, img2):
    arr1 = np.array(img1.convert("L"))
    arr2 = np.array(img2.convert("L"))
    if arr1.shape != arr2.shape:
        return None
    similarity, _ = ssim(arr1, arr2, full=True)
    return similarity



def detect_screen_change(paths: AppPaths, appname: str | None = None):
    config = load_config(paths)
    similarity_threshold = float(config.get("SIMILARITY_THRESHOLD", 0.98))
    poll_interval = float(config.get("POLL_INTERVAL_SECONDS", 0.01))

    prev_screenshot = screenshot(appname)
    previous_path = get_save_filename(paths)
    previous_path = previous_path.with_name(previous_path.stem + "_prev.png")
    save_image(prev_screenshot, paths, previous_path)

    while True:
        current_screenshot = screenshot(appname)
        similarity = compare_images(prev_screenshot, current_screenshot)
        if similarity is None:
            print("similarity is None. Shapes of img1 and img2 differ. Skipping.")
            time.sleep(max(poll_interval, 0.5))
            continue
        if similarity > similarity_threshold:
            print(f"\rscreenshots similarity {similarity:.5f}, wait for image change", end="")
            time.sleep(poll_interval)
            continue

        print(f"\rscreenshots similarity {similarity:.5f}, image changed. proceed. ", end="")
        break

    save_image(current_screenshot, paths)
    return current_screenshot



def encode_image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")



def list_window_titles() -> list[str]:
    return ["Fullscreen", *pwc.getAllTitles()]
