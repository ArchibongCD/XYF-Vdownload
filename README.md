# ⚡ XYF Vdownload
A fast, minimalist, and powerful video downloader built with Django and yt-dlp.

## 🚀 Features
- **Multi-Platform Support**: Download from YouTube, X (Twitter), Facebook, and more.
- **Dynamic Quality Selection**: Fetch available resolutions (720p, 480p, etc.).
- **Modern UI**: Custom theme with CSS variables and full Light/Dark mode.
- **Optimized Performance**: Uses WhiteNoise for static assets and Streaming Responses for downloads.
- **Production Ready**: Configured for immediate deployment on Render.

## 🛠️ Tech Stack
- **Backend**: Python / Django
- **Engine**: yt-dlp
- **Frontend**: HTML5, CSS3 (Custom Properties), Vanilla JS
- **Deployment**: Render + WhiteNoise + FFmpeg

## 💻 Local Setup
1. **Clone the repo**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/XYF-Vdownload.git](https://github.com/YOUR_USERNAME/XYF-Vdownload.git)
   cd XYF-Vdownload

## Create a virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

pip install -r requirements.txt
Environment Variables Create a .env file in the root:

## Code snippet

DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
Run the server

python manage.py migrate
python manage.py runserver

## Deployment (Render)
**This project is pre-configured for Render.**

Create a new Web Service.

Set the Build Command to: ./render-build.sh

Set the Start Command to: gunicorn core.wsgi:application

Important: Add the FFmpeg Buildpack in the Render settings: https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git