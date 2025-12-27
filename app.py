"""
=============================================================================
HOMOFLIXCINEMA - Flask Backend
=============================================================================
This is the main Flask application file for the premium movie streaming platform.
It handles all routes and stores video metadata in a Python dictionary.

NO DATABASE IS USED - All data is stored in memory using Python data structures.
Videos are NOT stored on the server - they are streamed from external sources.
=============================================================================
"""

import os
import logging
import requests
from flask import Flask, render_template, abort, request, jsonify, redirect, url_for, Response

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# =============================================================================
# FLASK APP CONFIGURATION
# =============================================================================

# Create the Flask application
app = Flask(__name__)

# Set the secret key from environment variable (required for sessions)
app.secret_key = os.environ.get("SESSION_SECRET")

# Enable debug mode for auto-reload on code changes
app.config['DEBUG'] = True

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
    {"id": "mythology", "name": "Mythology", "icon": "star"},
    {"id": "mystery", "name": "Mystery", "icon": "help-circle"},
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
        "video_url": "/stream/1",
        "original_url": "https://srv317.avitine.icu/s4/0/dff9b3d6e8d7d407fbd46dff176fdc51d02b436dda7175a71c598e3877d9aada/RReFI3v_dmgAmPMfO3A1EQ/1766662469/storage7/movies/1690097806-16428256-suzume-2022/1ab65acda5fe3a3fe9d5ba2f8f011039.mp4/index.m3u8",
        "duration": "2:01:28",
        "category": "adventure"
    },
    "2": {
        "id": "2",
        "title": "Bhool Bhulaiyaa 3",
        "description": "Bhool Bhulaiyaa 3 follows fake exorcist Ruhaan (Kartik Aaryan) as he's hired by a poor royal family in Bengal to fake an exorcism at their haunted palace to help them sell it, but he encounters real spirits, including the vengeful Manjulika, leading to confusion over which of two mysterious women (Vidya Balan, Madhuri Dixit) is the real ghost, culminating in a twist revealing the spirit's true identity is a male prince seeking revenge, with themes of LGBTQ+ acceptance in a horror-comedy package",
        "thumbnail": "/static/images/maxresdefault.jpg",
        "video_url": "/stream/2",
        "original_url": "https://srv317.avitine.icu/s4/0/8d2006d8999c1fb32f076df50a3eb033555caa111a3e98eb94e351cab476bad8/CRI4GtsZOQ2NZ_CI7R7RLg/1766663628/storage6/movies/1737202436-26932223-bhool-bhulaiyaa-3-2024/ba3bc8406df182a998416991b036f3d4.mp4/index.m3u8",
        "duration": "2:38:00",
        "category": "horror"
    },
    "3": {
        "id": "3",
        "title": "Mahavatar Narsimha",
        "description": "Mahavatar Narsimha is a landmark Indian animated epic, the first in a planned series, telling the story of Lord Vishnu's Narasimha avatar who defeats the demon king Hiranyakashipu, focusing on the faith of Prahlada, using high-quality 3D animation for divine battles, and aiming to revolutionize Indian animation with grand scale storytelling and a cinematic universe, produced by Kleem Productions and Hombale Filmss",
        "thumbnail": "/static/images/maha avtaar.jpg",
        "video_url": "/stream/3",
        "original_url": "https://srv317.bothoming.boats/s4/0/8f3fca44b42c26691b6bb569e877b6ece6a915fb5278128f32903b44fcef3465/k6irO19Lkxb-2b6xHuoqqQ/1766823758/storage1/movies/1758842342-34365591-mahavatar-narsimha-0/2d5ce30e0f67392be33d5304be7f545a.mp4/index.m3u8",
        "duration": "2:11:19",
        "category": "action",
        "tags": ["action", "mythology"]
    },
    "4": {
        "id": "4",
        "title": "Avengers: Endgame",
        "description": "Following the devastating events of Avengers: Infinity War, the universe is in ruins as half of all life has been erased. The remaining Avengers and their allies must assemble once more to undo Thanos's actions. To do so, they embark on a daring \"Time Heist\" to retrieve the Infinity Stones from the past, leading to a massive final showdown that determines the fate of the entire universe.",
        "thumbnail": "/static/images/avengers endgame.jpg",
        "video_url": "/stream/4",
        "original_url": "https://srv317.bothoming.boats/s4/0/7d0a7b2321483a51d765e81ed70ac40e49d72bc36110a46c908825d2246c4485/VdboE7RxrQ-4ae2f3QX8zw/1766824385/storage2/movies/1758227376-4154796-avengers-endgame-2019/2afe755e5fe894e675105023ed2f9a5b.mp4/index.m3u8",
        "duration": "3:01:00",
        "category": "action",
        "tags": ["action", "scifi"]
    }
    ,
    "5": {
        "id": "5",
        "title": "Inception",
        "description": "Dom Cobb is a professional thief with a rare ability: he can enter people's dreams to steal secrets from their subconscious. This has made him a master of corporate espionage but also a fugitive. He is offered a chance at redemption if he can perform the impossible—Inception. Instead of stealing an idea, he and his team must plant one in a target's mind. As they descend through layers of dreams within dreams, the lines between reality and the subconscious become dangerously blurred",
        "thumbnail": "/static/images/inception.jpg",
        "video_url": "/stream/5",
        "original_url": "https://srv317.bothoming.boats/s4/0/0653e37a943cc6b9ff9b667ed256e5e2419084c38b7e45d975910c5b970c8ee5/34Ecu-6xbiZ3SxrvYP7gOQ/1766825251/storage5/movies/1762728662-1375666-inception-2010/de3a4ad2556837d934caf7c91f78b49c.mp4/index.m3u8",
        "duration": "2:28:00",
        "category": "scifi",
        "tags": ["scifi", "action", "thriller", "mystery"]
    },
    "6": {
        "id": "6",
        "title": "The Garden of Words",
        "description": "Set in Tokyo during the rainy season, the story follows Takao Akizuki, a 15-year-old high school student who dreams of becoming a professional shoemaker. On rainy mornings, he skips his first class to sketch shoe designs in a quiet, lush Japanese garden (Shinjuku Gyoen). There, he repeatedly encounters Yukari Yukino, a mysterious 27-year-old woman who is also avoiding her responsibilities—spending her mornings in the park drinking beer and eating chocolate. Without knowing each other's names or backgrounds, they develop a bond through their shared solitude and a mutual appreciation for the rain. As the rainy season begins to end, they must confront the realities of their lives and the difficult paths they are \"walking\" on.",
        "thumbnail": "/static/images/the gardon of words.jpg",
        "video_url": "/stream/6",
        "original_url": "https://vod3.cf.dmcdn.net/sec2(Zr9DoYUWJeij6YQPEr0zEvM7ADz6POUZKYSCc4uDmPndzwgNRpCT_iAx7m9ZQGDvb4XlmJ_5pZn6macT1t0VB9T5YvmSgggyvoeM4OUt8WPgn8Ql_2N38sP4RwtlsFrAVt6vqaMM7T2JugRgLm3zzc-rTgD2-qsx0HjkQBrjML8wAHP-N90QVVz_3UNpg4cz)/video/005/803/534308500_mp4_h264_aac_hq_7.m3u8",
        "duration": "0:46:00",
        "category": "drama",
        "tags": ["drama", "romance", "adventure"]
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
    # Support search from Home to keep single-page UX
    search_query = request.args.get("search", "").strip()
    category = request.args.get("category", "all")
    videos = filter_videos(search_query, category)
    categories = get_all_categories()
    return render_template(
        "index.html",
        videos=videos,
        categories=categories,
        current_category=category,
        search_query=search_query,
        get_category_name=get_category_name
    )

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
    
    return render_template("watch.html", video=video, category_name=category_name, get_category_name=get_category_name)

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
# STREAM PROXY ROUTE
# =============================================================================

import re
from urllib.parse import urljoin, urlparse, quote

def get_base_url(url):
    """Extract the base URL (everything except the filename) from a URL."""
    parsed = urlparse(url)
    path = parsed.path.rsplit('/', 1)[0] + '/'
    return f"{parsed.scheme}://{parsed.netloc}{path}"

def rewrite_m3u8_urls(content, video_id, base_url):
    """
    Rewrite relative URLs in m3u8 playlist to use our proxy endpoint.
    This ensures all segment files are fetched through our server.
    """
    lines = content.split('\n')
    rewritten_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            rewritten_lines.append(line)
            continue
            
        # Skip comments/tags that aren't URLs
        if line.startswith('#'):
            # Check for URI in EXT-X-KEY or similar tags
            if 'URI="' in line:
                # Rewrite URI in tags like #EXT-X-KEY:METHOD=AES-128,URI="key.key"
                def replace_uri(match):
                    uri = match.group(1)
                    if not uri.startswith('http'):
                        full_url = urljoin(base_url, uri)
                        encoded_url = quote(full_url, safe='')
                        return f'URI="/segment/{video_id}?url={encoded_url}"'
                    else:
                        encoded_url = quote(uri, safe='')
                        return f'URI="/segment/{video_id}?url={encoded_url}"'
                line = re.sub(r'URI="([^"]+)"', replace_uri, line)
            rewritten_lines.append(line)
        else:
            # This is a URL line (segment or sub-playlist)
            if line.startswith('http'):
                # Absolute URL - proxy it directly
                encoded_url = quote(line, safe='')
                rewritten_lines.append(f'/segment/{video_id}?url={encoded_url}')
            else:
                # Relative URL - make it absolute first, then proxy
                full_url = urljoin(base_url, line)
                encoded_url = quote(full_url, safe='')
                rewritten_lines.append(f'/segment/{video_id}?url={encoded_url}')
    
    return '\n'.join(rewritten_lines)

@app.route("/stream/<video_id>")
def stream_video(video_id):
    """
    STREAM PROXY ROUTE
    ------------------
    Proxies video streams to bypass CORS, Referer protection, and token expiry.
    For HLS streams, rewrites the m3u8 playlist to proxy all segments.
    """
    video = get_video_by_id(video_id)
    if not video:
        abort(404)
    
    original_url = video.get("original_url")
    if not original_url:
        abort(404)
    
    try:
        # Set headers to mimic browser and bypass referer protection
        headers = {
            "User-Agent": request.headers.get("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "identity",
            "Referer": "https://quibblezoomfable.com/",
            "Origin": "https://quibblezoomfable.com",
            "Connection": "keep-alive",
        }
        
        # Add range header if client requests it (for seeking)
        if "Range" in request.headers:
            headers["Range"] = request.headers["Range"]
        
        # Stream the video
        logging.info(f"Proxying stream for video {video_id} from {original_url}")
        r = requests.get(original_url, headers=headers, stream=True, timeout=30)
        
        # Check if request was successful
        if r.status_code not in [200, 206]:
            logging.error(f"Stream request failed with status {r.status_code}")
            abort(502)
        
        content_type = r.headers.get('Content-Type', '')
        
        # Check if this is an m3u8 playlist that needs URL rewriting
        if 'm3u8' in original_url or 'mpegurl' in content_type.lower():
            # Read the entire playlist content
            content = r.text
            base_url = get_base_url(original_url)
            
            # Rewrite URLs to use our proxy
            rewritten_content = rewrite_m3u8_urls(content, video_id, base_url)
            
            response = Response(
                rewritten_content,
                status=200,
                content_type='application/vnd.apple.mpegurl'
            )
        else:
            # For non-m3u8 content, stream directly
            response = Response(
                r.iter_content(chunk_size=8192),
                status=r.status_code,
                content_type=content_type or 'application/octet-stream'
            )
            
            # Forward important headers
            if 'Content-Length' in r.headers:
                response.headers['Content-Length'] = r.headers['Content-Length']
            if 'Content-Range' in r.headers:
                response.headers['Content-Range'] = r.headers['Content-Range']
            if 'Accept-Ranges' in r.headers:
                response.headers['Accept-Ranges'] = r.headers['Accept-Ranges']
        
        # Allow CORS
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Range'
        
        return response
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Stream proxy error: {str(e)}")
        abort(502)


@app.route("/segment/<video_id>")
def proxy_segment(video_id):
    """
    SEGMENT PROXY ROUTE
    -------------------
    Proxies HLS segment files (.ts) and sub-playlists.
    The actual URL is passed as a query parameter.
    """
    from urllib.parse import unquote
    
    # Get the actual segment URL from query parameter
    segment_url = request.args.get('url')
    if not segment_url:
        abort(400)
    
    # Decode the URL
    segment_url = unquote(segment_url)
    
    # Verify the video exists (basic security check)
    video = get_video_by_id(video_id)
    if not video:
        abort(404)
    
    try:
        headers = {
            "User-Agent": request.headers.get("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "identity",
            "Referer": "https://quibblezoomfable.com/",
            "Origin": "https://quibblezoomfable.com",
            "Connection": "keep-alive",
        }
        
        # Add range header if client requests it
        if "Range" in request.headers:
            headers["Range"] = request.headers["Range"]
        
        logging.debug(f"Proxying segment: {segment_url}")
        r = requests.get(segment_url, headers=headers, stream=True, timeout=30)
        
        if r.status_code not in [200, 206]:
            logging.error(f"Segment request failed with status {r.status_code} for {segment_url}")
            abort(502)
        
        content_type = r.headers.get('Content-Type', 'video/mp2t')
        
        # Check if this is a sub-playlist (m3u8)
        if 'm3u8' in segment_url or 'mpegurl' in content_type.lower():
            content = r.text
            base_url = get_base_url(segment_url)
            rewritten_content = rewrite_m3u8_urls(content, video_id, base_url)
            
            response = Response(
                rewritten_content,
                status=200,
                content_type='application/vnd.apple.mpegurl'
            )
        else:
            # Stream segment content
            response = Response(
                r.iter_content(chunk_size=65536),  # Larger chunks for video segments
                status=r.status_code,
                content_type=content_type
            )
            
            if 'Content-Length' in r.headers:
                response.headers['Content-Length'] = r.headers['Content-Length']
            if 'Content-Range' in r.headers:
                response.headers['Content-Range'] = r.headers['Content-Range']
            if 'Accept-Ranges' in r.headers:
                response.headers['Accept-Ranges'] = r.headers['Accept-Ranges']
        
        # Allow CORS
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Range'
        
        return response
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Segment proxy error: {str(e)}")
        abort(502)

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
# MAIN ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    """
    Main entry point for the Flask application.
    
    In production (Azure), the app is run by Gunicorn, not this block.
    In development, this allows running with 'python app.py'.
    
    Azure automatically sets the PORT environment variable.
    """
    # Get port from environment variable or default to 8000
    port = int(os.environ.get('PORT', 8000))
    
    # Run the Flask development server
    app.run(
        host='0.0.0.0',  # Listen on all network interfaces
        port=port,
        debug=False  # Set to False for production
    )

# =============================================================================
# END OF FILE
# =============================================================================
