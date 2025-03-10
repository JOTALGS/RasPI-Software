import subprocess

def open_image_fullscreen_non_blocking(file_path, image=True):
    # Run feh in fullscreen mode without blocking the rest of the code
    if image:
        subprocess.Popen(["feh", "-F", file_path])
    else:
        subprocess.Popen(
            ["mpv", "--fullscreen", "--loop", file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
