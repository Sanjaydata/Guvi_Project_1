**Youtube Data Harvesting & Warehousing using SQL and Streamlit**

*Overview*

This project fetches, stores and analyzes Youtube channel data using SQL and streamlit. Users can enter a Youtube channel ID, and the system will automatically collect details about:
  1. Channel Statistics
  2. Playlist and their videos
  3. Video Statistics (views,like,duration etc.)
  4. Data insights using SQL queries

*Technology used*

 1. Python - Core programming language
 2. Youtube data API - Fetching data from Youtube
 3. MySQL - Storing structured data
 4. Streamlit - Interactive UI for querying and displaying data

*Features* 

 1. Automatic Data Fetching - Enter a Channel ID, and all related data (Playlist, Videos etc.) is fetched.
 2. SQL-Based Analysis - Predefined queries help extract insights like top videos, most liked videos etc.
 3. Interactive UI - Built using streamlit for an easy-to-use experience

*Installation & Setup*

 1. Need to install the below mentioned python libraries.
    import mysql.connector
    import googleapiclient.discovery
    import pandas
    import datetime
    import isodate
    import streamlit

2. How to run the files
   In the VS code terminal, type the following commands
   Step 1: python youtube_database_setup.py
   streamlit run UI.py

*Project Structure*

📂Youtube Data Harvesting

|- youtube_database_setup.py  # Sets up the database

|- youtube_data_harvesting.py # Fetches and processes data, UI with streamlit

|- UI.py                      # Handles the Steamlit interface


*How it works*

 1. User enters a YouTube Channel ID
 2. System fetches channel details, playlists, and videos using the Youtube API
 3. Data is stored in MySQL for easy querying
 4. Predefined SQL queries extract insights from the stored data
 5. Streamlit UI displays the results in an interactive format

Created by
Sanjay

   
