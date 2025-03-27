import mysql.connector
#connect to Mysql
conn = mysql.connector.connect(
    host = "localhost",
    user ="Sanjay_DS",
    password="Xy9@dF!73pQz"
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS youtube_data")
print("Database 'youtube_data' created or already exists.")

cursor.execute("USE youtube_data")

#create 'Channel' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Channel (
        channel_id VARCHAR(255) PRIMARY KEY,
        channel_name VARCHAR(255),
        channel_views BIGINT,
        channel_description TEXT,
        channel_status VARCHAR(255),
        total_videos INT
    )
""")
print("Table 'channels' created or already exists")

#create 'playlist' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Playlist (
        playlist_id VARCHAR(255) PRIMARY KEY,
        channel_id VARCHAR(255),
        playlist_name VARCHAR(255),
        FOREIGN KEY (channel_id) REFERENCES channel(channel_id)
    )
""")
print("Table 'Playlist' created or already exists")

#create 'Video' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Video(
        video_id VARCHAR(255) PRIMARY KEY,
        channel_id VARCHAR(255),
        video_name VARCHAR(255),
        video_description TEXT,
        published_date DATETIME,
        view_count INT,
        like_count INT,
        favorite_count INT,
        comment_count INT,
        duration INT,
        thumbnail VARCHAR(255),
        caption_status VARCHAR(255),
        FOREIGN KEY (channel_id) REFERENCES channel(channel_id)
    )
""")
print("Table 'videos' created or already exists")

#create 'Comment' table

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Comment (
        comment_id VARCHAR(255) PRIMARY KEY,
        video_id VARCHAR(255),
        comment_text TEXT,
        comment_author VARCHAR(255),
        comment_published_date DATETIME,
        FOREIGN KEY (video_id) REFERENCES Video(video_id)
    )
""")
print("Table 'comments' created or already exists")

#closing the connection
cursor.close()
conn.close()
print("MySQL connection closed")