
import os
import requests
import re

from django.shortcuts import render

def home(request):
    if request.method == 'POST':
        video_link = request.POST.get('video_link')
        save_path = "/Users/khalid/Desktop/video.mp4"
        
        video_src = extract_video_src(video_link)
        if video_src:
            download_video(video_src, save_path)
        else:
            print("Failed to extract video source URL.")

    return render(request, 'app/home.html')

def extract_video_src(video_link):
    """Extracts the video source URL from the given URL."""
    html_code = retrieve_html_code(video_link)
    video_src = None
    pattern = r'url":"(https?://[^"]+\.mp4)"'
    match = re.search(pattern, html_code)
    if match:
        video_src = match.group(1)
    
    if video_src:
        print(f"Scraped video source link: {video_src}")
    else:
        print("No valid video source link found.")
        
    return video_src


def download_video(video_src, save_path):
    """Downloads the video from the given source URL to the specified path."""
    if video_src:
        response = requests.get(video_src, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"Successfully downloaded video to {save_path}")
        else:
            print(f"Failed to download video from {video_src}")
    else:
        print("No valid video source URL to download.")

def retrieve_html_code(url):
    """Retrieves the HTML code from the given URL."""
    response = requests.get(url)
    html_code = response.text
    return html_code
