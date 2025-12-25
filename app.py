"""
=============================================================================
CINEMAHUB - Flask Backend
=============================================================================
This is the main Flask application file for the premium movie streaming platform.
It handles all routes and stores video metadata in a Python dictionary.

NO DATABASE IS USED - All data is stored in memory using Python data structures.
Videos are NOT stored on the server - they are streamed from external sources.
=============================================================================
"""

import os
import logging
from flask import Flask, render_template, abort, request, jsonify, redirect, url_for

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# =============================================================================
# FLASK APP CONFIGURATION
# =============================================================================

# Create the Flask application
app = Flask(__name__)

# Set the secret key from environment variable (required for sessions)
app.secret_key = os.environ.get("SESSION_SECRET")

# =============================================================================
# CATEGORIES
# =============================================================================
# List of available movie genres for organization and filtering.
# =============================================================================

CATEGORIES = [
    {"id": "action", "name": "Action", "icon": "zap"},
    {"id": "adventure", "name": "Adventure", "icon": "compass"},
    {"id": "drama", "name": "Drama", "icon": "heart"},
    {"id": "thriller", "name": "Thriller", "icon": "alert-circle"},
    {"id": "comedy", "name": "Comedy", "icon": "smile"},
    {"id": "scifi", "name": "Sci-Fi", "icon": "rocket"},
    {"id": "horror", "name": "Horror", "icon": "moon"},
    {"id": "romance", "name": "Romance", "icon": "heart"},
    {"id": "documentary", "name": "Documentary", "icon": "film"},
]

# =============================================================================
# MOVIE METADATA STORAGE
# =============================================================================
# This dictionary stores all movie information.
# Movies are uploaded to Google Drive and shared via embed links.
# To add movies, edit this dictionary directly in the code.
#
# HOW TO ADD MOVIES FROM GOOGLE DRIVE:
# 1. Upload your movie file to Google Drive
# 2. Right-click → Share → Change to "Viewer" access
# 3. Copy the shareable link (e.g., https://drive.google.com/file/d/FILE_ID/view?usp=sharing)
# 4. Extract the FILE_ID from the URL
# 5. Create embed URL: https://drive.google.com/file/d/FILE_ID/preview
# 6. Add entry below with all required fields
#
# MOVIE LINK FORMAT:
# - Google Drive: https://drive.google.com/file/d/FILE_ID/preview
# =============================================================================

VIDEOS = {
    "1": {
        "id": "1",
        "title": "Suzume",
        "description": "Suzume is a Japanese animated fantasy film by Makoto Shinkai about a high school girl, Suzume, who teams up with a mysterious young man, Souta, to close supernatural doors across Japan that unleash disasters like earthquakes, leading to a magical road-trip adventure to seal these portals and prevent calamity, all while exploring themes of loss, memory, and healing from past trauma",
        "thumbnail": "/static/images/suzume-poster.jpg",
        "video_url": "https://srv317.avitine.icu/s4/0/dff9b3d6e8d7d407fbd46dff176fdc51d02b436dda7175a71c598e3877d9aada/RReFI3v_dmgAmPMfO3A1EQ/1766662469/storage7/movies/1690097806-16428256-suzume-2022/1ab65acda5fe3a3fe9d5ba2f8f011039.mp4/index.m3u8",
        "duration": "2:01:28",
        "category": "adventure"
    },
    "2": {
        "id": "2",
        "title": "Bhool Bhulaiyaa 3",
        "description": "Bhool Bhulaiyaa 3 follows fake exorcist Ruhaan (Kartik Aaryan) as he's hired by a poor royal family in Bengal to fake an exorcism at their haunted palace to help them sell it, but he encounters real spirits, including the vengeful Manjulika, leading to confusion over which of two mysterious women (Vidya Balan, Madhuri Dixit) is the real ghost, culminating in a twist revealing the spirit's true identity is a male prince seeking revenge, with themes of LGBTQ+ acceptance in a horror-comedy package",
        "thumbnail": "/static/images/maxresdefault.jpg",
        "video_url": "https://srv317.avitine.icu/s4/0/8d2006d8999c1fb32f076df50a3eb033555caa111a3e98eb94e351cab476bad8/CRI4GtsZOQ2NZ_CI7R7RLg/1766663628/storage6/movies/1737202436-26932223-bhool-bhulaiyaa-3-2024/ba3bc8406df182a998416991b036f3d4.mp4/index.m3u8",
        "duration": "2:38:00",
        "category": "horror"
    }
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_videos():
    """
    Returns a list of all videos.
    This converts the dictionary to a list for easy iteration in templates.
    """
    return list(VIDEOS.values())

def get_video_by_id(video_id):
    """
    Returns a single video by its ID.
    Returns None if the video is not found.
    """
    return VIDEOS.get(video_id)

def get_all_categories():
    """
    Returns the list of all categories.
    """
    return CATEGORIES

def get_category_by_id(category_id):
    """
    Returns a category by its ID.
    Returns None if not found.
    """
    for cat in CATEGORIES:
        if cat["id"] == category_id:
            return cat
    return None

def get_category_name(category_id):
    """
    Returns the display name of a category.
    Returns the ID if category not found.
    """
    cat = get_category_by_id(category_id)
    return cat["name"] if cat else category_id.capitalize()

def filter_videos(search_query=None, category=None):
    """
    Filters videos by search query and/or category.
    Returns a list of matching videos.
    """
    videos = get_all_videos()
    
    # Filter by category if specified
    if category and category != "all":
        videos = [v for v in videos if v.get("category") == category]
    
    # Filter by search query if specified
    if search_query:
        search_lower = search_query.lower()
        videos = [v for v in videos if 
                  search_lower in v["title"].lower() or 
                  search_lower in v["description"].lower()]
    
    return videos

def get_next_video_id():
    """
    Returns the next available video ID for adding new videos.
    """
    if not VIDEOS:
        return "1"
    max_id = max(int(vid) for vid in VIDEOS.keys())
    return str(max_id + 1)

# =============================================================================
# ROUTES
# =============================================================================

@app.route("/")
@app.route("/home")
def home():
    """
    HOME PAGE ROUTE
    ---------------
    This is the landing page of the website.
    It displays a welcome message and a button to browse videos.
    Both "/" and "/home" routes point to this function.
    """
    return render_template("index.html")

@app.route("/videos")
def videos():
    """
    VIDEOS LISTING PAGE ROUTE
    -------------------------
    This page displays all available videos in a card format.
    Supports filtering by category and search query.
    """
    # Get filter parameters from URL
    search_query = request.args.get("search", "").strip()
    category = request.args.get("category", "all")
    
    # Filter videos
    filtered_videos = filter_videos(search_query, category)
    
    # Get all categories for the filter dropdown
    categories = get_all_categories()
    
    return render_template(
        "videos.html", 
        videos=filtered_videos, 
        categories=categories,
        current_category=category,
        search_query=search_query,
        get_category_name=get_category_name
    )

@app.route("/watch/<video_id>")
def watch(video_id):
    """
    VIDEO PLAYER PAGE ROUTE
    -----------------------
    This page displays a single video with its embedded player.
    If the video ID is invalid, it shows a 404 error page.
    
    Parameters:
    - video_id: The unique identifier of the video to watch
    """
    # Try to find the video
    video = get_video_by_id(video_id)
    
    # If video not found, show 404 error
    if video is None:
        abort(404)
    
    # Get category name for display
    category_name = get_category_name(video.get("category", ""))
    
    return render_template("watch.html", video=video, category_name=category_name)

# =============================================================================
# ADMIN ROUTES
# =============================================================================

@app.route("/admin")
def admin():
    """
    ADMIN PANEL ROUTE
    -----------------
    Displays all videos in a management interface.
    Allows adding, editing, and deleting videos.
    """
    all_videos = get_all_videos()
    categories = get_all_categories()
    return render_template(
        "admin.html", 
        videos=all_videos, 
        categories=categories,
        get_category_name=get_category_name
    )

@app.route("/admin/add", methods=["GET", "POST"])
def admin_add():
    """
    ADD VIDEO ROUTE
    ---------------
    GET: Shows the form to add a new video.
    POST: Processes the form and adds the video.
    
    Note: This is a demo project - data is stored in memory and will reset on server restart.
    """
    categories = get_all_categories()
    error = None
    
    if request.method == "POST":
        # Get and validate form data
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        thumbnail = request.form.get("thumbnail", "").strip()
        video_url = request.form.get("video_url", "").strip()
        duration = request.form.get("duration", "").strip()
        category = request.form.get("category", "adventure")
        
        # Validate required fields
        if not title or not description or not thumbnail or not video_url or not duration:
            error = "All fields are required. Please fill in all fields."
            return render_template("admin_form.html", video={
                "title": title, "description": description, "thumbnail": thumbnail,
                "video_url": video_url, "duration": duration, "category": category
            }, categories=categories, action="Add", error=error)
        
        new_id = get_next_video_id()
        new_video = {
            "id": new_id,
            "title": title,
            "description": description,
            "thumbnail": thumbnail,
            "video_url": video_url,
            "duration": duration,
            "category": category
        }
        
        # Add to videos dictionary
        VIDEOS[new_id] = new_video
        
        return redirect(url_for("admin"))
    
    return render_template("admin_form.html", video=None, categories=categories, action="Add", error=None)

@app.route("/admin/edit/<video_id>", methods=["GET", "POST"])
def admin_edit(video_id):
    """
    EDIT VIDEO ROUTE
    ----------------
    GET: Shows the form to edit an existing video.
    POST: Processes the form and updates the video.
    
    Note: This is a demo project - data is stored in memory and will reset on server restart.
    """
    video = get_video_by_id(video_id)
    if video is None:
        abort(404)
    
    categories = get_all_categories()
    error = None
    
    if request.method == "POST":
        # Get and validate form data
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        thumbnail = request.form.get("thumbnail", "").strip()
        video_url = request.form.get("video_url", "").strip()
        duration = request.form.get("duration", "").strip()
        category = request.form.get("category", "adventure")
        
        # Validate required fields
        if not title or not description or not thumbnail or not video_url or not duration:
            error = "All fields are required. Please fill in all fields."
            return render_template("admin_form.html", video={
                "id": video_id, "title": title, "description": description, 
                "thumbnail": thumbnail, "video_url": video_url, "duration": duration, 
                "category": category
            }, categories=categories, action="Edit", error=error)
        
        # Update video data
        VIDEOS[video_id]["title"] = title
        VIDEOS[video_id]["description"] = description
        VIDEOS[video_id]["thumbnail"] = thumbnail
        VIDEOS[video_id]["video_url"] = video_url
        VIDEOS[video_id]["duration"] = duration
        VIDEOS[video_id]["category"] = category
        
        return redirect(url_for("admin"))
    
    return render_template("admin_form.html", video=video, categories=categories, action="Edit", error=None)

@app.route("/admin/delete/<video_id>", methods=["POST"])
def admin_delete(video_id):
    """
    DELETE VIDEO ROUTE
    ------------------
    Deletes a video from the collection.
    Only accepts POST requests for safety.
    """
    if video_id in VIDEOS:
        del VIDEOS[video_id]
    
    return redirect(url_for("admin"))

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """
    404 ERROR HANDLER
    -----------------
    This handler is called when a page or video is not found.
    It displays a friendly error message with a link back to videos.
    """
    return render_template("404.html"), 404

# =============================================================================
# END OF FILE
# =============================================================================
