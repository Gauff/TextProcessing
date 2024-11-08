import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
import os
import json
import isodate
import argparse
import environment
import sys

def get_video_id(url):
    # Extract video ID from URL
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_comments(youtube, video_id):
    comments = []

    try:
        # Fetch top-level comments
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100  # Adjust based on needs
        )

        while request:
            response = request.execute()
            for item in response['items']:
                # Top-level comment
                topLevelComment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(topLevelComment)
                
                # Check if there are replies in the thread
                if 'replies' in item:
                    for reply in item['replies']['comments']:
                        replyText = reply['snippet']['textDisplay']
                        # Add incremental spacing and a dash for replies
                        comments.append("    - " + replyText)
            
            # Prepare the next page of comments, if available
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list_next(
                    previous_request=request, previous_response=response)
            else:
                request = None

    except HttpError as e:
        print(f"Failed to fetch comments: {e}")

    return comments


def main_function(url, options):

    # Get YouTube API key from environment variable
    api_key = environment.YOUTUBE_API_KEY
    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in ~/.config/fabric/.env")
        return

    # Extract video ID from URL
    video_id = get_video_id(url)
    if not video_id:
        print("Invalid YouTube URL")
        return

    try:
        # Initialize the YouTube API client
        youtube = build("youtube", "v3", developerKey=api_key)

        # Get video details
        video_response = youtube.videos().list(
            id=video_id, part="contentDetails,snippet").execute()

        # Extract video duration and convert to minutes
        duration_iso = video_response["items"][0]["contentDetails"]["duration"]
        duration_seconds = isodate.parse_duration(duration_iso).total_seconds()
        duration_minutes = round(duration_seconds / 60)
        # Set up metadata
        metadata = {}
        metadata['id'] = video_response['items'][0]['id']
        metadata['title'] = video_response['items'][0]['snippet']['title']
        metadata['channel'] = video_response['items'][0]['snippet']['channelTitle']
        metadata['published_at'] = video_response['items'][0]['snippet']['publishedAt']

        # Get video transcript
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[options.lang])
            transcript_text = " ".join([item["text"] for item in transcript_list])
            transcript_text = transcript_text.replace("\n", " ")
        except Exception as e:
            transcript_text = f"Transcript not available in the selected language ({options.lang}). ({e})"

        # Get comments if the flag is set
        comments = []
        if options.comments:
            comments = get_comments(youtube, video_id)

        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8')

            # Output based on options
            if options.duration:
                print(duration_minutes)
            elif options.transcript:
                # Direct UTF-8 print without encode/decode
                print(transcript_text)
            elif options.comments:
                print(json.dumps(comments, indent=2, ensure_ascii=False))
            elif options.metadata:
                print(json.dumps(metadata, indent=2, ensure_ascii=False))
            else:
                # Create JSON object with all data
                output = {
                    "transcript": transcript_text,
                    "duration": duration_minutes,
                    "comments": comments,
                    "metadata": metadata
                }
                # Print JSON object with proper UTF-8 encoding
                print(json.dumps(output, indent=2, ensure_ascii=False))
    except HttpError as e:
        print(f"Error: Failed to access YouTube API. Please check your YOUTUBE_API_KEY and ensure it is valid: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='yt (video meta) extracts metadata about a video, such as the transcript, the video\'s duration, and now comments. By Daniel Miessler.')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--duration', action='store_true', help='Output only the duration')
    parser.add_argument('--transcript', action='store_true', help='Output only the transcript')
    parser.add_argument('--comments', action='store_true', help='Output the comments on the video')
    parser.add_argument('--metadata', action='store_true', help='Output the video metadata')
    parser.add_argument('--lang', default='en', help='Language for the transcript (default: English)')
    
    args = parser.parse_args()

    if args.url is None:
        print("Error: No URL provided.")
        return

    main_function(args.url, args)

if __name__ == "__main__":
    main()
