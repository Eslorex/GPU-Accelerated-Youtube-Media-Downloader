import subprocess

def install_yt_dlp():
    try:
        subprocess.run(["pip", "install", "yt-dlp"], check=True)
        print("yt-dlp installed successfully.")
        print("You can close the console now. Video Downloader should work.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing yt-dlp: {e}")

if __name__ == "__main__":
    install_yt_dlp()
    input("Press Enter to exit...")
