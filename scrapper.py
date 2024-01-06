import youtube_transcript_api
import googleapiclient.discovery

"""
Search for videos in a YouTube channel and check if they contain a specific phrase in their transcript.
"""

# Set up YouTube Data API client
api_service_name = "youtube"
api_version = "v3"
api_key = "YOUR_API_KEY"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
channel_name = "CHANNEL_NAME"  # Replace with the name of the YouTube channel
phrase_to_search = "PHRASE_TO_SEARCH"  # Replace with the phrase you want to search for in the transcripts

# Get the channel ID - Yeah, it is not perfect, but it works
request = youtube.search().list(q=channel_name, type='channel', part='id', maxResults=1)
response = request.execute()
channel_id = response['items'][0]['id']['channelId']


videos = []
next_page_token = None

while True:
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=50,
        order="date",
        pageToken=next_page_token,
        type="video"
    )
    response = request.execute()
    videos.extend(response["items"])
    next_page_token = response.get("nextPageToken")
    if not next_page_token:
        break

# Search for the phrase in the transcripts of the videos
for video in videos:
    video_id = video["id"]["videoId"]
    try:
        transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id, languages=["en","es"])
        for line in transcript:
            if phrase_to_search.lower() in line['text'].lower():
                print(f"Video URL: https://www.youtube.com/watch?v={video_id}")
                break
    except youtube_transcript_api.TranscriptsDisabled:
        print(f"Transcripts are disabled for video: {video_id}")
    except youtube_transcript_api.NoTranscriptFound:
        print(f"No transcript found for video: {video_id}")
    except Exception as e:
        print(f"An error occurred while fetching the transcription for video: {video_id}")
        print(str(e))
        


