# CinemaHub - Movie Streaming Platform

## Overview
A premium movie streaming platform built with Flask. The platform allows users to browse and watch movies hosted externally (Google Drive, Vimeo, YouTube).

**Purpose**: Complete movie streaming solution for enjoying premium films.

**Current State**: Fully functional demo with sample video entries, complete responsive UI, search/filter, admin panel, and watch history.

## Project Structure
```
├── app.py              # Main Flask application with routes and video metadata
├── main.py             # Entry point for the server
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Base template with navbar and footer
│   ├── index.html      # Home page
│   ├── videos.html     # Video listing page with search/filter
│   ├── watch.html      # Video player page with sharing
│   ├── admin.html      # Admin panel for managing videos
│   ├── admin_form.html # Add/Edit video form
│   └── 404.html        # Error page
├── static/
│   ├── css/
│   │   └── style.css   # All CSS styles (mobile-first)
│   └── js/
│       └── main.js     # JavaScript for interactivity & watch history
├── design_guidelines.md # Design system documentation
└── replit.md           # This file
```

## Routes
- `/` or `/home` - Landing page with hero section
- `/videos` - Grid display of all available videos (with search & filter)
- `/watch/<video_id>` - Individual video player page with social sharing
- `/admin` - Admin panel to manage videos
- `/admin/add` - Add new video form
- `/admin/edit/<video_id>` - Edit video form
- `/admin/delete/<video_id>` - Delete video (POST only)
- `404` - Custom error page for invalid video IDs

## Tech Stack
- **Backend**: Python 3.11, Flask
- **Frontend**: HTML5, CSS3 (vanilla), JavaScript (vanilla)
- **Icons**: Feather Icons (CDN)
- **Storage**: In-memory Python dictionary (no database - demo project)
- **Watch History**: Browser localStorage

## Key Features
- Mobile-first responsive design
- External video embedding via iframe
- Hamburger menu for mobile navigation
- **Video Categories**: Adventure, Fantasy, Sci-Fi, Nature, Drama
- **Search & Filter**: Search by title/description, filter by category
- **Social Sharing**: Twitter, Facebook, LinkedIn, Copy Link buttons
- **Watch History**: Tracks watched videos in localStorage, shows "Watched" badge
- **Admin Panel**: Add, edit, delete videos via web interface
- Smooth hover effects and transitions
- Dark theme with professional styling
- Comprehensive code comments for learning

## Categories
- Adventure
- Fantasy
- Sci-Fi
- Nature
- Drama

## Adding New Videos
### Option 1: Admin Panel (Recommended)
1. Go to `/admin`
2. Click "Add Video"
3. Fill in the form and submit

### Option 2: Edit Code
Edit the `VIDEOS` dictionary in `app.py`:
```python
VIDEOS = {
    "7": {
        "id": "7",
        "title": "Your Video Title",
        "description": "Video description",
        "thumbnail": "URL to thumbnail image",
        "video_url": "Embed URL (YouTube/Vimeo/Google Drive)",
        "duration": "5:00",
        "category": "adventure"  # One of: adventure, fantasy, scifi, nature, drama
    }
}
```

## Running the App
The app runs on port 5000 via gunicorn:
```
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

## Important Notes
- **Demo Project**: Data is stored in memory and resets on server restart
- **No Database**: By design - keeps the project simple and lightweight
- **External Videos**: Videos are streamed from external sources (YouTube, Vimeo, Google Drive)

## Recent Changes
- **Dec 16, 2025**: Added Phase 2 features:
  - Video categories with filtering
  - Search functionality
  - Social sharing buttons
  - Watch history using localStorage
  - Admin panel for video management
- **Dec 16, 2025**: Initial build - complete video platform with home, videos listing, video player, and 404 pages
