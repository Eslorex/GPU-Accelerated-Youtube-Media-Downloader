import os
import sys
import yt_dlp
import random
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import subprocess

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        # When running as an executable
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        # When running as a script
        base_path = os.path.dirname(os.path.abspath(__file__))

    ffmpeg_exe_path = os.path.join(base_path, 'ffmpeg', 'bin', 'ffmpeg.exe')

    if os.path.exists(ffmpeg_exe_path):
        return ffmpeg_exe_path
    else:
        print(f"'ffmpeg.exe' not found at: {ffmpeg_exe_path}")
        return None



def download_video(yt_url, ffmpeg_path):
    try:
        if not os.path.exists(ffmpeg_path):
            print(f"'ffmpeg.exe' not found at: {ffmpeg_path}")
            return

        if getattr(sys, 'frozen', False):
            # When running as an executable
            base_path = os.path.dirname(sys.executable)
        else:
            # When running as a script
            base_path = os.path.dirname(os.path.abspath(__file__))

        output_path = os.path.join(base_path, "Videos")
        os.makedirs(output_path, exist_ok=True)

        audio_or_video = input("Do you want audio only or video with audio? (a/v): ")

        final_file_path = os.path.join(output_path, '%(title)s.%(ext)s')
        ydl_opts = {
            'outtmpl': final_file_path,
            'noplaylist': True,
            'ffmpeg_location': ffmpeg_path,
        }

        if audio_or_video == 'a':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        else:
            ydl_opts['format'] = 'bestvideo+bestaudio'
            ydl_opts['merge_output_format'] = 'mp4'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(yt_url, download=False)
                available_formats = [f for f in info_dict['formats'] if f.get('vcodec') != 'none']
                
                format_by_resolution = defaultdict(list)
                for fmt in available_formats:
                    format_by_resolution[fmt.get('format_note', 'Unknown')].append(fmt)
                
                best_formats = [max(formats, key=lambda x: x.get('tbr', 0)) for formats in format_by_resolution.values()]

                print("Available video qualities:")
                for i, fmt in enumerate(best_formats):
                    print(f"{i}. {fmt.get('format_note', 'Unknown')} - {fmt.get('format_id')}")

                choice = int(input("Pick a video quality by number: "))
                selected_video_format = best_formats[choice]['format_id']
                ydl_opts['format'] = f'{selected_video_format}+bestaudio'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {yt_url}")
            ydl.download([yt_url])

        print(f"Downloaded: {yt_url}\n")

    except Exception as e:
        print(f"Error: {e}")



def main():
    ffmpeg_path = get_ffmpeg_path()
    print(f"Derived ffmpeg path: {ffmpeg_path}")

    while True:
        print("Enter YouTube video URLs, one per line. Press Enter twice to start downloading.")
        yt_urls = []
        while True:
            yt_url = input().strip()
            if yt_url.startswith("http"):
                yt_urls.append(yt_url)
            elif yt_url == "":
                break
            else:
                print("Invalid URL entered. Please enter a valid YouTube URL.")

        with ThreadPoolExecutor() as executor:
            executor.map(lambda url: download_video(url, ffmpeg_path), yt_urls)

if __name__ == "__main__":
    main()
