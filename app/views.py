import os
import requests
import re

from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def home(request):
    if request.method == 'POST':
        video_link = request.POST.get('video_link')
        save_path = "/Users/khalid/Desktop/video.mp4"

        final_url, html_code = retrieve_html_code(video_link)

        video_src = extract_video_src(html_code)
        if video_src:
            download_video(video_src, save_path)
        else:
            print("Failed to extract video source URL.")

    return render(request, 'app/home.html')

def retrieve_html_code(url):
    """Retrieves the HTML code from the given URL and follows redirects."""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    # Wait for the page to load completely
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    final_url = driver.current_url
    html_code = driver.page_source
    driver.quit()
    
    return final_url, html_code

def extract_video_src(html_code):
    """Extracts the video source URL from the given HTML code."""
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
