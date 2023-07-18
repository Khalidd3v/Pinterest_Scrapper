# import os
# import requests
# import re

# from django.shortcuts import render

# def home(request):
#     if request.method == 'POST':
#         video_link = request.POST.get('video_link')
#         save_path = "/Users/khalid/Desktop/video.mp4"

#         video_src = process_link(video_link, save_path)
#         if video_src:
#             download_video(video_src, save_path)
#         else:
#             print("Failed to extract video source URL.")

#     return render(request, 'app/home.html')

# def process_link(video_link, save_path):
#     """Processes the video link, handles redirection if necessary, and extracts the video source URL."""
#     redirected_link = follow_redirection(video_link)
#     if redirected_link:
#         redirected_link2 = follow_redirection(redirected_link)
#         if redirected_link2:
#             video_src = extract_video_src(redirected_link2)
#         else:
#             video_src = extract_video_src(redirected_link)
#     else:
#         video_src = extract_video_src(video_link)

#     return video_src

# def follow_redirection(url):
#     """Follows the redirection for the given URL and returns the final URL."""
#     session = requests.Session()
#     response = session.head(url, allow_redirects=True)
#     final_url = response.url
#     if final_url != url:
#         print(f"Redirected to: {final_url}")
#         return final_url

#     return None

# def extract_video_src(video_link):
#     """Extracts the video source URL from the given URL."""
#     html_code = retrieve_html_code(video_link)
#     video_src = None
#     pattern = r'url":"(https?://[^"]+\.mp4)"'
#     match = re.search(pattern, html_code)
#     if match:
#         video_src = match.group(1)

#     if video_src:
#         print(f"Scraped video source link: {video_src}")
#     else:
#         print("No valid video source link found.")

#     return video_src

# def retrieve_html_code(url):
#     """Retrieves the HTML code from the given URL."""
#     response = requests.get(url)
#     html_code = response.text
#     return html_code

# def download_video(video_src, save_path):
#     """Downloads the video from the given source URL to the specified path."""
#     if video_src:
#         response = requests.get(video_src, stream=True)
#         if response.status_code == 200:
#             with open(save_path, "wb") as f:
#                 for chunk in response.iter_content(chunk_size=1024):
#                     if chunk:
#                         f.write(chunk)
#             print(f"Successfully downloaded video to {save_path}")
#         else:
#             print(f"Failed to download video from {video_src}")
#     else:
#         print("No valid video source URL to download.")

import os
import requests
import re
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import StreamingHttpResponse

def home(request):
    if request.method == 'POST':
        # Get the video link from the form
        video_link = request.POST.get('video_link')

        # Get the response from the URL, following redirections
        response = requests.get(video_link, allow_redirects=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the HTML content of the page
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the canonical link in the webpage code
            canonical_link = soup.find('link', {'rel': 'canonical'})

            if canonical_link:
                href = canonical_link.get('href')
                print(f"Canonical link found: {href}")

                # Call the rest of the functions with the canonical link
                video_src = process_link(href)
                if video_src:
                    return download_video(video_src)
                else:
                    print("Failed to extract video source URL from the canonical link.")
            else:
                print("No canonical link found in the webpage.")
        else:
            print(f"Failed to download the webpage. Status code: {response.status_code}")

    return render(request, 'app/home.html')


def process_link(video_link):
    """Processes the video link, handles redirection if necessary, and extracts the video source URL."""
    redirected_link = follow_redirection(video_link)
    if redirected_link:
        redirected_link2 = follow_redirection(redirected_link)
        if redirected_link2:
            video_src = extract_video_src(redirected_link2)
        else:
            video_src = extract_video_src(redirected_link)
    else:
        video_src = extract_video_src(video_link)

    return video_src


def follow_redirection(url):
    """Follows the redirection for the given URL and returns the final URL."""
    session = requests.Session()
    response = session.head(url, allow_redirects=True)
    final_url = response.url
    if final_url != url:
        print(f"Redirected to: {final_url}")
        return final_url

    return None


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


def retrieve_html_code(url):
    """Retrieves the HTML code from the given URL."""
    response = requests.get(url)
    html_code = response.text
    return html_code


def download_video(video_src):
    """Streams the video from the given source URL and sends it as a response to the user's browser."""
    if video_src:
        response = requests.get(video_src, stream=True)

        if response.status_code == 200:
            # Set appropriate headers for the response to prompt download
            file_size = int(response.headers['Content-Length'])
            response = StreamingHttpResponse(
                response.iter_content(chunk_size=8192),
                content_type='video/mp4'
            )
            response['Content-Disposition'] = f'attachment; filename="video.mp4"'
            response['Content-Length'] = file_size
            return response
        else:
            print(f"Failed to download video from {video_src}")
    else:
        print("No valid video source URL to download.")
        return render(request, 'app/home.html')


