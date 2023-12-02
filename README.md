# GPU-Accelerated-Youtube-Media-Downloader

# Purpose
- Quickly sample content from youtube for music producers or video editors to use. As high quality and fast as possible. Don't get surprised if you see 5-10 minutes of video to have 200 megabytes of size when downloading or encoding "video". Its literally the raw video itself. Audio is pretty quick though.
- Avoid websites filled with ads, that doesn't provide video for you higher than 30fps or 1080p. This tool can download whatever is possible for that video. Without losing nearly any detail. For free and faster. Finally its worth to have god-like pc.

# Requirements
- Python & Libraries https://www.python.org/downloads/ & Execute "install_libraries.py"
- ffmpeg is included in .exe file, so you don't have to download it by yourself. But for people who doesn't trust my .exe file :). I provided a zip file on release with source files & ffmpeg with correct file structure.

# Features
- Can download mp3 or mp4 files from Youtube & Youtube Short links highest quality & bitrate possible. CPU & GPU ones are for video editors that use softwares like After Effects. It encodes the video to make it compatible with AE.
- Youtube_Downloader_daily is for daily usage and fastest since it doesn't do extra encoding for AE. It might work for AE sometimes. But not as certain as Youtube_Downloader_GPU.
- Youtube_Downloader_GPU is most of the time faster than CPU if you don't have crappy GPU. But for people who have really crappy GPU, i also released one that works with CPU too.
- Downloaded video will be in file "Videos" which is in the same path with executable

# Usage
- Enter Single URL and press enter 2 times.
- Pick audio or video. (a/v)
- If video, pick available quality.
- Done.

# Known Issues
- Using .exe instead of .py files is slower. Use source files if you're having trouble.
- Most videos are compatible with Windows Media Player but since the Youtube keeps their videos in different formats for different scenerios, this situation might change depending on the video and its quality. Since we don't encode everything into single codec standard to avoid long, encoding progress, it MIGHT cause incompatibilities in Windows Media Player. GPU one solves this issue by encoding everything into a compatible standart with Media Player and After Effects but it takes a little while but not longer than online websites for sure. Since most websites doesn't even provide 4k video download option without any compression. So, if you have any issues with Windows Media Player, just use something like VLC Player and problem will be solved. Its kinda funny that Windows have less range of support on codecs than 3rd party media players. 

