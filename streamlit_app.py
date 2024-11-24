import streamlit as st
from datetime import datetime
import feedparser

from editing_winners import main_create
from article_thumnail_creator import thumbnail_create

# Function to fetch the latest podcast episodes
def fetch_latest_episodes(rss_url, count=5):
    feed = feedparser.parse(rss_url)
    episodes = [
        {
            "title": entry.title,
            "link": entry.link,
            "date": entry.published if "published" in entry else "Unknown Date",
            "description": entry.get("summary", "No description available"),
        }
        for entry in feed.entries[:count]
    ]
    return episodes

# Function to replace placeholders in a template
def generate_updated_text(template_path, url, first_place, second_place, third_place, month, date):
    try:
        # Print the raw date for debugging
        print(f"Original date: {date}")
        
        # Attempt to parse and format the date without timezone info
        episode_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S GMT")  # Adjusted format
        # Format the date as "4th November"
        formatted_date = episode_date.strftime("%d %B")
        
        # Add suffix to day (1st, 2nd, 3rd, 4th, etc.)
        day = int(episode_date.strftime("%d"))
        if 10 <= day <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        
        formatted_date = f"{day}{suffix} {episode_date.strftime('%B')}"
    
    except ValueError as e:
        # Log the error and the raw date string to understand the issue
        print(f"Error parsing date: {e}")
        formatted_date = "Unknown Date"
    
    # Open the template and replace placeholders
    with open(template_path, "r") as file:
        content = file.read()
    
    # Replace placeholders in the content
    content = content.replace("REPLACE_URL", url or "No URL provided")
    content = content.replace("REPLACE_FIRST", first_place or "N/A")
    content = content.replace("REPLACE_SECOND", second_place or "N/A")
    content = content.replace("REPLACE_THIRD", third_place or "N/A")
    content = content.replace("REPLACE_MONTH", month or "N/A")
    content = content.replace("REPLACE_DATE", formatted_date or "Unknown Date")
    
    return content

# Title for the app
st.title("Redz Rollover")

# Dropdown for selecting a month with the current month as default
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
current_month = datetime.now().strftime("%B")
selected_month = st.selectbox("Select Month", months, index=months.index(current_month))

# Dropdown for selecting a year with the current year as default
years = [str(year) for year in range(2020, datetime.now().year + 5)]
current_year = str(datetime.now().year)
selected_year = st.selectbox("Select Year", years, index=years.index(current_year))

# Define the RSS feed URL for your Acast podcast
rss_url = "https://feeds.acast.com/public/shows/6686586e4cb273e461b608c8"

# Fetch the last 5 episodes
try:
    episodes = fetch_latest_episodes(rss_url)
except Exception as e:
    st.error(f"Failed to fetch podcast episodes: {e}")
    episodes = []

# Dropdown for podcast episodes
selected_episode_url = None
selected_episode_date = None
if episodes:
    episode_titles = [ep["title"] for ep in episodes]
    selected_episode = st.selectbox("Select an Episode", episode_titles)

    # Find the URL and date of the selected episode
    for ep in episodes:
        if ep["title"] == selected_episode:
            selected_episode_url = ep["link"]
            selected_episode_date = ep["date"]
            break
else:
    st.error("No episodes found. Please check the RSS feed URL.")

# Create three columns
col1, col2, col3 = st.columns(3)

with col1:
    first_place = st.text_input("First Place")

with col2:
    second_place = st.text_input("Second Place")

with col3:
    third_place = st.text_input("Third Place")

# Button to display the results
if st.button("Show Results"):
    st.write("### Results:")
    st.write(f"1st Place: {first_place}")
    st.write(f"2nd Place: {second_place}")
    st.write(f"3rd Place: {third_place}")

    selected_year = selected_year[-2:]

    try:
        main_create(first_place, second_place, third_place, selected_month, selected_year)
        thumbnail_create(selected_month, selected_year)
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Generate the updated text
    template_path = "Graphics/Template_text.txt"
    
    try:
        updated_text = generate_updated_text(
            template_path, 
            selected_episode_url, 
            first_place, 
            second_place, 
            third_place, 
            selected_month, 
            selected_episode_date,
        )
        st.text_area("Updated Text", value=updated_text, height=300)
    except FileNotFoundError:
        st.error("Template file not found. Please ensure 'template_Text.txt' exists.")

    col6, col7 = st.columns(2)

    with col6:
        image_path = f"thumbnails/{selected_month}-{selected_year}-results.jpg"
        st.image(image_path, caption="Month's winners")

    with col7:
        try:
            with open(image_path, "rb") as file:
                st.download_button(
                    label="Download Image",
                    data=file,
                    file_name="winner_image.jpg",
                    mime="image/jpeg"
                )
        except FileNotFoundError:
            st.error("Results image not found.")

    col8, col9 = st.columns(2)

    with col8:
        thumbnail_path = f"thumbnails/{selected_month}-{selected_year}-thumbnail.jpg"
        st.image(thumbnail_path, caption="Website Thumbnail")

    with col9:
        try:
            with open(thumbnail_path, "rb") as file:
                st.download_button(
                    label="Download Thumbnail",
                    data=file,
                    file_name="thumbnail_image.jpg",
                    mime="image/jpeg"
                )
        except FileNotFoundError:
            st.error("Thumbnail image not found.")
