import numpy as np
from mss import mss
from PIL import Image,ImageGrab
from skimage.metrics import structural_similarity as ssim
import time
import base64
import io

def screenshot():
    backend = 'PIL'  # 'PIL' or 'mss'
    if backend == 'PIL':
        img = ImageGrab.grab()
    elif backend == 'mss':
        from mss import mss
        sct = mss()
        img = sct.grab(sct.monitors[0])
        img = Image.frombytes('RGB', img.size, img.rgb)
    return img

def compare_images(img1, img2):
    # Convert images to grayscale
    img1_gray = img1.convert('L')
    img2_gray = img2.convert('L')
    
    # Convert images to numpy arrays
    arr1 = np.array(img1_gray)
    arr2 = np.array(img2_gray)
    
    # Compute Structural Similarity Index (SSI)
    similarity, _ = ssim(arr1, arr2, full=True)
    return similarity

def detect_screen_change():
    prev_screenshot = None
    current_screenshot = None
    SIMILARITY_THRESHOLD = 0.99     
    while True:
        prev_screenshot = current_screenshot 
        current_screenshot = screenshot()

        if prev_screenshot is not None:
            similarity = compare_images(prev_screenshot, current_screenshot)
            if similarity > SIMILARITY_THRESHOLD:
                print(f'\rscreenshots similarity {similarity:.5f}, wait for image change...', end='')
                time.sleep(0.01)
            else:
                break
    return current_screenshot

def encode_image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")   # encode to PNG bytes
    return base64.b64encode(buffer.getvalue()).decode("utf-8")