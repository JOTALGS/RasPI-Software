import subprocess

def open_image_fullscreen_non_blocking(image_path):
    # Run feh in fullscreen mode without blocking the rest of the code
    subprocess.Popen(["feh", "-F", image_path])
