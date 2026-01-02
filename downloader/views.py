from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseBadRequest
from .services import fetch_video_data
import requests
import re


def home(request):
    """Render home page with video downloader."""
    return render(request, 'home.html')


def fetch_info(request):
    """
    Fetch video information from provided URL.
    Returns JSON with video metadata and available formats.
    """
    url = request.GET.get('url', '').strip()
    
    if not url:
        return JsonResponse({
            'status': 'error',
            'message': 'No URL provided'
        }, status=400)
    
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid URL format. URL must start with http:// or https://'
        }, status=400)
    
    # Fetch video data using service
    data = fetch_video_data(url)
    return JsonResponse(data)


def download_video(request):
    """
    Stream video file directly to user's device.
    Uses chunked transfer for efficient memory usage.
    """
    video_url = request.GET.get('url')
    title = request.GET.get('title', 'XYF_Video')
    
    if not video_url:
        return HttpResponseBadRequest('Video URL is required')
    
    # Sanitize filename - remove special characters
    safe_title = re.sub(r'[^\w\s-]', '', title).strip()
    safe_title = re.sub(r'[-\s]+', '-', safe_title) or 'XYF_Video'
    
    # Headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'identity',
        'Connection': 'keep-alive'
    }
    
    try:
        # Stream video from source
        response = requests.get(video_url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        # Create streaming response
        streaming_response = StreamingHttpResponse(
            response.iter_content(chunk_size=1048576),  # 1MB chunks
            content_type=response.headers.get('Content-Type', 'video/mp4')
        )
        
        # Set content length for progress tracking
        content_length = response.headers.get('Content-Length')
        if content_length:
            streaming_response['Content-Length'] = content_length
        
        # Force download with proper filename
        streaming_response['Content-Disposition'] = f'attachment; filename="{safe_title}.mp4"'
        streaming_response['Accept-Ranges'] = 'bytes'
        
        return streaming_response
        
    except requests.exceptions.RequestException as e:
        return HttpResponseBadRequest(f'Failed to download video: {str(e)}')


def about(request):
    """Render about page."""
    return render(request, 'about.html')


def contact(request):
    """Render contact page."""
    return render(request, 'contact.html')


def privacy(request):
    """Render privacy policy page."""
    return render(request, 'privacy.html')


def terms(request):
    """Render terms of service page."""
    return render(request, 'terms.html')


def help_center(request):
    """Render help center page."""
    return render(request, 'help.html')