#!/usr/bin/env bash
set -o errexit

# 1. Download a portable version of FFmpeg
mkdir -p ffmpeg
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ -C ffmpeg --strip-components 1

# 2. Add FFmpeg to the path so yt-dlp can find it
export PATH=$PATH:$(pwd)/ffmpeg

# 3. Standard build commands
pip install -r requirements.txt
python manage.py collectstatic --no-input

python manage.py migrate