import yt_dlp


def get_platform_headers(url):
    """
    Returns platform-specific headers to avoid 403 Forbidden errors.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    if 'x.com' in url or 'twitter.com' in url:
        headers['Referer'] = 'https://x.com/'
    elif 'facebook.com' in url:
        headers['Referer'] = 'https://www.facebook.com/'
    
    return headers


# def fetch_video_data(url):
#     """
#     Extracts video metadata using yt-dlp with dynamic headers.
#     Returns video info including title, thumbnail, and available formats.
#     """
#     ydl_opts = {
#         'quiet': True,
#         'no_warnings': True,
#         'http_headers': get_platform_headers(url),
#         'nocheckcertificate': True,
#         'format': 'bestvideo+bestaudio/best',
#         'merge_output_format': 'mp4',
#         'noplaylist': True,
#     }
    
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)
            
#             # Get all available formats with both video and audio
#             all_formats = info.get('formats', [])
#             valid_formats = [
#                 f for f in all_formats 
#                 if f.get('vcodec') != 'none' and f.get('acodec') != 'none'
#             ]
            
#             if not valid_formats:
#                 return {
#                     'status': 'error', 
#                     'message': 'No downloadable formats found for this video.'
#                 }
            
#             formats = []
            
#             # Find best quality (HD)
#             best = valid_formats[-1]  # Last format is usually highest quality
#             formats.append({
#                 'res': 'HD (Best Quality)',
#                 'url': best.get('url'),
#                 'ext': best.get('ext', 'mp4')
#             })
            
#             # Find standard quality (360p-480p range)
#             standard = next(
#                 (f for f in valid_formats if 360 <= f.get('height', 0) <= 480),
#                 valid_formats[len(valid_formats)//2] if valid_formats else best
#             )
#             formats.append({
#                 'res': 'Standard (Lower Quality)',
#                 'url': standard.get('url'),
#                 'ext': standard.get('ext', 'mp4')
#             })
            
#             return {
#                 'status': 'success',
#                 'title': info.get('title', 'Unknown Title'),
#                 'thumbnail': info.get('thumbnail', ''),
#                 'formats': formats,
#                 'source': info.get('extractor_key', 'Unknown')
#             }

def fetch_video_data(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        # We don't force 'bestvideo+bestaudio' here so it finds 
        # the high-quality files that are already merged (sharpest MP4s)
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Using your exact filtering logic
            valid_formats = []
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    valid_formats.append({
                        'res': f.get('resolution') or f.get('format_note'),
                        'url': f.get('url'),
                        'ext': f.get('ext')
                    })
            
            if not valid_formats:
                return {'status': 'error', 'message': 'No playable formats found.'}

            # valid_formats is usually sorted low to high. 
            # HD = the last one (highest) | Standard = one from the middle
            hd_video = valid_formats[-1]
            standard_video = valid_formats[len(valid_formats)//2] if len(valid_formats) > 1 else hd_video

            final_formats = [
                {'res': 'HD (High Quality)', 'url': hd_video['url'], 'ext': hd_video['ext']},
                {'res': 'Standard (Low Quality)', 'url': standard_video['url'], 'ext': standard_video['ext']}
            ]
            
            return {
                'status': 'success',
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'formats': final_formats
            }
    except Exception as e:
        error_msg = str(e).lower()
        if 'private' in error_msg or 'login' in error_msg:
            return {'status': 'error', 'message': 'This video is private or restricted. We cannot access it, bro.'}
        return {'status': 'error', 'message': 'Video not found or link is broken.'}