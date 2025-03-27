import streamlit as st
import mysql.connector
import pandas as pd
from youtube_data_harvesting import (
    fetch_channel_details, fetch_playlist_details, fetch_video_details,
    store_channel_details, store_playlist_details, store_video_details
)

# Set up Streamlit UI
st.set_page_config(page_title="YouTube Data Harvesting", layout="wide")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg", width=200)
st.sidebar.title("YouTube Data Harvesting and Warehousing using SQL and Streamlit")

menu = st.sidebar.radio("Navigation", ["🏠 Home", "📡 Data Hunt", "📊 Data Clarity"])

# Home Page
if menu == "🏠 Home":
    st.title("Welcome to YouTube Data Harvesting and Warehousing! 🚀")
    st.write("Fetch, store, and analyze YouTube channel data with ease!")

# Data Hunt Page (Fetching & Storing Data)
elif menu == "📡 Data Hunt":
    st.title("Data Hunt 🎯")
    channel_id = st.text_input("Enter YouTube Channel ID", "")

    if st.button("Fetch & Store Data"):
        if channel_id:
            st.write("🔍 Fetching Data...")

            # Fetch data
            channel_data = fetch_channel_details(channel_id)
            playlist_data = fetch_playlist_details(channel_id)
            video_data = fetch_video_details(channel_id)

            st.write("✅ Data Fetched Successfully! Now storing in SQL...")

            # Store data in SQL (comments removed)
            store_channel_details(channel_data)
            for pl_data in playlist_data:
                store_playlist_details(pl_data)
            for v_data in video_data:
                store_video_details(v_data)

            st.success("✅ Data Stored Successfully in SQL!")

        else:
            st.error("❌ Please enter a valid Channel ID.")

# 📊 Data Clarity Page (Executing SQL Queries)
elif menu == "📊 Data Clarity":
    st.title("Data Clarity 📊")

    #db connection
    def get_db_connection():
        return mysql.connector.connect(
            host="localhost",
            user="Sanjay_DS",
            password="Xy9@dF!73pQz",
            database="youtube_data"
        )

    #SQL query in dict:
    queries = {
        "1. Names of all videos and their corresponding channels":
            "SELECT video.video_name, channel.channel_name from video JOIN channel ON video.channel_id = channel.channel_id;",

        "2. Channel with the most videos" :
            "SELECT channel_name, total_videos FROM channel ORDER BY total_videos DESC LIMIT 10;",

        "3. Top 10 most viewed videos":
            "SELECT channel.channel_name, video.video_name, video.view_count FROM video JOIN channel ON video.channel_id = channel.channel_id ORDER BY video.view_count DESC LIMIT 10;",

        "4. Comment count for each video" :
            "SELECT video_name, comment_count FROM video ORDER BY comment_count DESC;",

        "5. Video with the highest likes" :
            "SELECT channel.channel_name, video.video_name, video.like_count FROM video JOIN channel ON video.channel_id = channel.channel_id ORDER BY video.like_count DESC LIMIT 1;",

        "6. Total likes per video" :
            "SELECT video_name, like_count FROM video ORDER BY like_count DESC;",

        "7. Total views for each channel" :
            "SELECT channel_name, channel_views FROM channel;",
        
        "8. Channels that published videos in 2022":
            "SELECT channel.channel_name, COUNT(video.video_id) AS video_count FROM channel JOIN video ON channel.channel_id = video.channel_id WHERE YEAR(video.published_date)=2022 GROUP BY channel.channel_name;",

        "9. Average video duration per channel" :
            "SELECT channel.channel_name, CONCAT(FLOOR(AVG(video.duration) / 60), 'min', ROUND(AVG(video.duration) % 60), 'sec') AS avg_video_duration FROM channel JOIN video ON channel.channel_id = video.channel_id GROUP BY channel.channel_name;",

        "10. Video with the highest number of comments":
            "SELECT video.video_name, channel.channel_name, video.comment_count FROM channel JOIN video ON channel.channel_id = video.channel_id ORDER BY video.comment_count DESC LIMIT 1;"
    }
    
    selected_query = st.selectbox("Select a Query to Execute", list(queries.keys()))

    if st.button("Run Query"):
        st.write("🔎 Fetching results...")

        #connect to database and execute query
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(queries[selected_query])
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(result, columns=columns)
            df.index = range(1, len(df)+1)
            df.index.name = "S. No"
            st.dataframe(df)

        except Exception as e:
            st.error(f"Error executing query: {e}")
        
        finally:
            cursor.close()
            conn.close()
