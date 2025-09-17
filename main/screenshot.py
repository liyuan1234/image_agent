import numpy as np
from mss import mss
from PIL import Image,ImageGrab
from skimage.metrics import structural_similarity as ssim
import time
import base64
import io
import pygetwindow as gw
import pyautogui
import pywinctl as pwc

from utils import get_save_filename, save_image

def bbox_to_ltwh(X: list[int, int, int, int]) -> list[int, int, int, int]:
    return [X[0],X[1],X[2] - X[0], X[3] - X[1]] # return left top width height


def screenshot(appname = None):
    backend = 'mss'  # 'PIL' or 'mss' or 'pyautogui'
    bbox = get_bbox(appname)


    if backend == 'PIL':
        img = ImageGrab.grab(bbox) # if bbox is None take full screen
    elif backend == 'mss':
        with mss() as sct:

            if bbox:
                X = bbox_to_ltwh(bbox)
                monitor = {
                    "left": bbox[0],
                    "top": bbox[1],
                    "width": bbox[2] - bbox[0],
                    "height": bbox[3] - bbox[1]
                }
            else:
                monitor = sct.monitors[1]
            img = sct.grab(monitor)
        img = Image.frombytes('RGB', img.size, img.rgb)
    elif backend == 'pyautogui':
        X = bbox_to_ltwh(bbox)
        img = pyautogui.screenshot(region=X)
    return img

def compare_images(img1, img2):
    # Convert images to grayscale
    img1_gray = img1.convert('L')
    img2_gray = img2.convert('L')
    
    # Convert images to numpy arrays
    arr1 = np.array(img1_gray)
    arr2 = np.array(img2_gray)
    
    if arr1.shape != arr2.shape:
        return None
    # Compute Structural Similarity Index (SSI)
    similarity, _ = ssim(arr1, arr2, full=True)
    return similarity

def detect_screen_change(appname = None):
    prev_screenshot = screenshot(appname)
    filename = get_save_filename().replace('.png','prev.png')
    save_image(prev_screenshot,filename)
    current_screenshot = None
    SIMILARITY_THRESHOLD = 0.98
    n = 0     
    while True:
        current_screenshot = screenshot(appname)

        if prev_screenshot is not None:
            similarity = compare_images(prev_screenshot, current_screenshot)
            if not similarity:
                print('similarity is None。 Shapes of img1 and img2 different. Skipping.')
                time.sleep(0.5)
                continue
            if similarity > SIMILARITY_THRESHOLD:
                print(f'\rscreenshots similarity {similarity:.5f}, wait for image change' + n//3*'.', end='')
                time.sleep(0.01)
            else:
                print(f'\rscreenshots similarity {similarity:.5f}, image changed. proceed. ', end='')

                break
    save_image(current_screenshot)
    return current_screenshot

def encode_image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")   # encode to PNG bytes
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def get_bbox(appname):
    window = pwc.getWindowsWithTitle(appname)
    if window:
        return window[0].bbox
    
    else:
        return None
