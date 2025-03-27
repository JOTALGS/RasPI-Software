import time
import subprocess

def open_image_fullscreen_non_blocking(file_path, image=True):
    # Run feh in fullscreen mode without blocking the rest of the code
    if image:
        # Hide the cursor
        subprocess.Popen(["unclutter", "-idle", "0"])
        subprocess.run(["sudo", "pkill", "feh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.5)
        subprocess.Popen(["feh", "-F", "--force-aliasing", file_path])
    else:
        subprocess.Popen(
            ["mpv", "--fullscreen", "--loop", file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
