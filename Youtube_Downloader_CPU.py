import os
import sys
import yt_dlp
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import subprocess

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    ffmpeg_exe_path = os.path.join(base_path, 'ffmpeg', 'bin', 'ffmpeg.exe')
    return ffmpeg_exe_path if os.path.exists(ffmpeg_exe_path) else None

def download_video(yt_url, ffmpeg_path):
    try:
        if not ffmpeg_path:
            print("'ffmpeg.exe' not found.")
            return

        base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_path, "Videos")
        os.makedirs(output_path, exist_ok=True)

        audio_or_video = input("Do you want audio only or video with audio? (a/v): ")

        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(yt_url, download=False)
            video_title = info_dict.get('title', 'Unknown_Title').replace(' ', '_').replace('/', '_')

            if audio_or_video == 'a':
                final_file_path = os.path.join(output_path, f'{video_title}.mp3')
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': final_file_path,
                    'noplaylist': True,
                    'ffmpeg_location': ffmpeg_path,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                    }],
                }
            else:
                temp_file_path = os.path.join(output_path, f'{video_title}_temp.mp4')
                final_file_path = os.path.join(output_path, f'{video_title}.mp4')
                ydl_opts = {
                    'outtmpl': temp_file_path,
                    'noplaylist': True,
                    'merge_output_format': 'mp4',
                    'ffmpeg_location': ffmpeg_path,
                }

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
                ydl.download([yt_url])

            if audio_or_video == 'v':
                ffmpeg_cmd = [
                    ffmpeg_path,
                    '-i', temp_file_path,
                    '-c:v', 'libx264',
                    '-preset', 'slow',
                    '-profile:v', 'main',
                    '-c:a', 'aac',
                    '-b:a', '160k',
                    final_file_path
                ]
                subprocess.run(ffmpeg_cmd)
                os.remove(temp_file_path)

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
