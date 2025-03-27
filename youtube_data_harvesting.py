import mysql.connector
from googleapiclient.discovery import build
from datetime import datetime
import isodate

# Initialization Block
# Initialize YouTube API
API_KEY = "AIzaSyDtTV-Zwa6UJRX2Smyd7nqy-rsLXJCLZeQ"
youtube = build("youtube", "v3", developerKey=API_KEY)

# Initialize MySQL Connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="Sanjay_DS",
            password="Xy9@dF!73pQz",
            database="youtube_data"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        return None
#------------------End of Initialization block------------------# 
# Fetch block:

# Fetch channel details:
def fetch_channel_details(channel_id):
    try:
        request = youtube.channels().list(
            part="snippet,statistics,contentDetails",
            id=channel_id
        )
        response = request.execute()

        if "items" not in response or len(response["items"]) == 0:
            print(f"No data found for channel ID: {channel_id}")
            return None

        channel_data = response["items"][0]
        channel_status = channel_data.get("status",{}).get("privacyStatus","Unknown")
        video_count = int(channel_data['statistics'].get('videoCount',0))
        channel_info = {
            "channel_id": channel_data["id"],
            "channel_name": channel_data["snippet"]["title"],
            "channel_views": int(channel_data["statistics"].get("viewCount",0)),
            "channel_description": channel_data["snippet"].get("description","No description"),
            "channel_status": channel_status,
            "total_videos": video_count
        }
        return channel_info
    
    except Exception as e:
        print(f"Error fetching channel details: {e}")
        return None

#Fetch playlist details:
def fetch_playlist_details(channel_id):
    try:
        playlists = []
        next_page_token = None

        while True:
            request = youtube.playlists().list(part="id,snippet", channelId=channel_id, maxResults=50, pageToken=next_page_token)
            response = request.execute()

            for item in response.get("items",[]):
                playlist_data = {
                    "playlist_id": item["id"],
                    "channel_id": channel_id,
                    "playlist_name": item["snippet"]["title"]
                }
                playlists.append(playlist_data)

            next_page_token=response.get("nextPageToken")
            if not next_page_token:
                break
        return playlists
    
    except Exception as e:
        print(f'Error fetching playlist details: {e}')
        return []
    
#Fetch video details:
def fetch_video_details(channel_id):
    try:
        videos = []
        next_page_token = None
        ch_req = youtube.channels().list(
            part='snippet,statistics,contentDetails',
            id=channel_id)
        ch_resp = ch_req.execute()
        Main_playlist_id = ch_resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        while True:
            # Fetch basic video details
            request = youtube.playlistItems().list(
                part="snippet", 
                playlistId=Main_playlist_id, 
                maxResults=50, 
                pageToken=next_page_token
            )
            response = request.execute()

            video_ids = []
            for item in response.get("items", []):
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_data = {
                    "video_id": video_id,
                    "channel_id": channel_id,
                    "video_name": item["snippet"]["title"],
                    "video_description": item["snippet"]["description"],
                    "published_date": item["snippet"]["publishedAt"]
                }
                videos.append(video_data)
                video_ids.append(video_id)

            # Fetch video statistics for the collected video IDs
            if video_ids:
                stats_request = youtube.videos().list(
                    part="statistics,contentDetails,snippet", 
                    id=",".join(video_ids)
                )
                stats_response = stats_request.execute()

                for item in stats_response.get("items", []):
                    video_id = item["id"]
                    for video in videos:
                        if video["video_id"] == video_id:
                            video["view_count"] = int(item["statistics"].get("viewCount", 0))
                            video["like_count"] = int(item["statistics"].get("likeCount", 0))
                            video["favorite_count"] = int(item["statistics"].get("favoriteCount", 0))
                            video["comment_count"] = int(item["statistics"].get("commentCount", 0))
                            video["duration"] = int(isodate.parse_duration(item["contentDetails"]["duration"]).total_seconds())
                            video["caption_status"] = item["contentDetails"]["caption"]
                            video["thumbnail"] = item["snippet"]["thumbnails"].get("default", {}).get("url", "No Thumbnail")

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return videos

    except Exception as e:
        print(f"Error fetching video details: {e}")
        return []

#Fetch comment details
def fetch_comments(video_ids):
    all_comments = {}

    for video_id in video_ids:
        try:
            comments = []
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100
            )
            response = request.execute()

            while response:
                for item in response.get("items", []):
                    snippet = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})

                    comment_data = {
                        "comment_id": item.get("id", "N/A"),
                        "video_id": video_id,
                        "comment_text": snippet.get("textDisplay", "N/A"),
                        "comment_author": snippet.get("authorDisplayName", "N/A"),
                        "comment_published_date": snippet.get("publishedAt", "N/A")
                    }
                    comments.append(comment_data)

                if "nextPageToken" in response:
                    request = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        maxResults=100,
                        pageToken=response["nextPageToken"]
                    )
                    response = request.execute()
                else:
                    break

            all_comments[video_id] = comments

        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {e}")

    return all_comments
#------------------End of Fetch block------------------# 

#Store block

def store_channel_details(channel_info):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO Channel (channel_id, channel_name, channel_views, channel_description, channel_status, total_videos)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                channel_name = VALUES(channel_name),
                channel_views = VALUES(channel_views),
                channel_description = VALUES(channel_description),
                channel_status = VALUES(channel_status),
                total_videos = VALUES(total_videos);
        """
        data = (
            channel_info["channel_id"],
            channel_info["channel_name"],
            channel_info["channel_views"],
            channel_info["channel_description"],
            channel_info["channel_status"],
            channel_info["total_videos"]
        )

        cursor.execute(insert_query, data)
        conn.commit()
        print(f"Channel details stored for: {channel_info['channel_name']}")

    except Exception as e:
        print(f"Error storing channel details: {e}")

    finally:
        cursor.close()
        conn.close()

def store_playlist_details(playlist_info):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO Playlist (playlist_id, channel_id, playlist_name)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                playlist_name = VALUES(playlist_name)
        """
        data = (
            playlist_info["playlist_id"],
            playlist_info["channel_id"],
            playlist_info["playlist_name"]
        )

        cursor.execute(insert_query, data)
        conn.commit()
        print(f"Playlist details stored for: {playlist_info['playlist_name']}")

    except Exception as e:
        print(f"Error storing playlist details: {e}")

    finally:
        cursor.close()
        conn.close()

def store_video_details(video_details):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO Video (video_id, channel_id, video_name, video_description, published_date, view_count, like_count, favorite_count, comment_count, duration, thumbnail, caption_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                video_name = VALUES(video_name),
                video_description = VALUES(video_description),
                published_date = VALUES(published_date),
                view_count = VALUES(view_count),
                like_count = VALUES(like_count),
                favorite_count = VALUES(favorite_count),
                comment_count = VALUES(comment_count),
                duration = VALUES(duration),
                thumbnail = VALUES(thumbnail),
                caption_status = VALUES(caption_status)
        """
        video_details["published_date"] = datetime.strptime(video_details["published_date"], "%Y-%m-%dT%H:%M:%SZ")

        data = (
            video_details["video_id"],
            video_details["channel_id"],
            video_details["video_name"],
            video_details["video_description"],
            video_details["published_date"],
            video_details["view_count"],
            video_details["like_count"],
            video_details["favorite_count"],
            video_details["comment_count"],
            video_details["duration"],
            video_details["thumbnail"],
            video_details["caption_status"]
        )

        cursor.execute(insert_query, data)
        conn.commit()
        print(f"Video details stored for: {video_details['video_id']}")

    except Exception as e:
        print(f"Error storing video details: {e}")

    finally:
        cursor.close()
        conn.close()


def store_video_comments(comments_dict):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO Comment (comment_id, video_id, comment_text, comment_author, comment_published_date)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                comment_text = VALUES(comment_text),
                comment_author = VALUES(comment_author),
                comment_published_date = VALUES(comment_published_date)
        """
        for video_id, comments in comments_dict.items():
            for comment in comments:
                published_date=comment["comment_published_date"]
                if isinstance(published_date, str):
                    formatted_date = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
                else:
                    formatted_date = published_date
                comment_data =(
                    comment["comment_id"],
                    video_id,
                    comment["comment_text"],
                    comment["comment_author"],
                    formatted_date
                )
                cursor.execute(query, comment_data)

        conn.commit()
        cursor.close()
        conn.close()
        print("Comments stored successfully!")
    
    except Exception as e:
        print(f"Error storing comments: {e}")
#------------------End of Store block------------------# 