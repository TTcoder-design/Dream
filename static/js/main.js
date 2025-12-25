/**
 * =============================================================================
 * SHIV'S ANIMATION STUDIO - JavaScript
 * =============================================================================
 * This file contains all the JavaScript functionality for the video platform.
 * It handles:
 * - Mobile navigation toggle
 * - Smooth interactions
 * - Watch history using localStorage
 * - Video card interactions
 * 
 * All code is written in vanilla JavaScript - no frameworks or libraries.
 * =============================================================================
 */

/**
 * Wait for the DOM to be fully loaded before running any JavaScript.
 * This ensures all HTML elements are available to be manipulated.
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Shiv\'s Animation Studio loaded successfully!');
    
    // Initialize all functionality
    initMobileNavigation();
    initSmoothScrolling();
    initVideoCards();
    initWatchHistory();
});

/**
 * =============================================================================
 * MOBILE NAVIGATION
 * =============================================================================
 * Handles the hamburger menu toggle on mobile devices.
 * When clicked, shows/hides the navigation menu.
 */
function initMobileNavigation() {
    // Get the navigation elements
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    // Check if elements exist (they might not on some pages)
    if (!navToggle || !navMenu) {
        return;
    }
    
    // Toggle menu visibility when hamburger is clicked
    navToggle.addEventListener('click', function() {
        // Toggle the 'active' class on the menu
        navMenu.classList.toggle('active');
        
        // Update aria-expanded attribute for accessibility
        const isExpanded = navMenu.classList.contains('active');
        navToggle.setAttribute('aria-expanded', isExpanded);
        
        // Log for debugging (remove in production)
        console.log('Mobile menu toggled:', isExpanded ? 'open' : 'closed');
    });
    
    // Close menu when a link is clicked (for mobile UX)
    const navLinks = navMenu.querySelectorAll('.nav-link');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
        });
    });
    
    // Close menu when clicking outside of it
    document.addEventListener('click', function(event) {
        // Check if the click was outside the navbar
        const isClickInsideNav = navToggle.contains(event.target) || 
                                  navMenu.contains(event.target);
        
        if (!isClickInsideNav && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    });
}

/**
 * =============================================================================
 * SMOOTH SCROLLING
 * =============================================================================
 * Adds smooth scrolling behavior to anchor links.
 * This is a progressive enhancement - browsers without support will still work.
 */
function initSmoothScrolling() {
    // Get all links that point to an anchor on the page
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            // Get the target element
            const targetId = this.getAttribute('href');
            
            // Skip if it's just "#"
            if (targetId === '#') {
                return;
            }
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Prevent default jump behavior
                event.preventDefault();
                
                // Smooth scroll to the target
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * =============================================================================
 * VIDEO CARDS INTERACTION
 * =============================================================================
 * Adds interactive features to video cards like keyboard navigation.
 */
function initVideoCards() {
    // Get all video cards
    const videoCards = document.querySelectorAll('.video-card');
    
    videoCards.forEach(function(card) {
        // Make the entire card clickable via keyboard
        card.setAttribute('tabindex', '0');
        
        // Handle keyboard navigation
        card.addEventListener('keypress', function(event) {
            // Activate on Enter or Space key
            if (event.key === 'Enter' || event.key === ' ') {
                // Find and click the watch button inside the card
                const watchButton = card.querySelector('.btn-watch');
                if (watchButton) {
                    event.preventDefault();
                    watchButton.click();
                }
            }
        });
        
        // Add visual feedback on focus
        card.addEventListener('focus', function() {
            this.style.outline = '2px solid var(--color-primary)';
            this.style.outlineOffset = '4px';
        });
        
        card.addEventListener('blur', function() {
            this.style.outline = '';
            this.style.outlineOffset = '';
        });
    });
}

/**
 * =============================================================================
 * WATCH HISTORY
 * =============================================================================
 * Uses localStorage to track which videos the user has watched.
 * Marks watched videos on the videos listing page.
 * Records when the user visits a video watch page.
 */

const WATCH_HISTORY_KEY = 'cinema_hub_watch_history';
const WATCH_THRESHOLD = 60000; // 1 minute in milliseconds

/**
 * Initialize watch history functionality.
 * - On videos page: Mark watched videos with progress
 * - On watch page: Track watch time
 */
function initWatchHistory() {
    // Check if we're on the watch page (has video player)
    const videoPlayer = document.querySelector('.video-player');
    if (videoPlayer) {
        // Get video ID from the URL
        const pathParts = window.location.pathname.split('/');
        const videoId = pathParts[pathParts.length - 1];
        if (videoId) {
            startTrackingWatchTime(videoId);
        }
    }
    
    // Check if we're on the videos listing page
    const videoCards = document.querySelectorAll('.video-card[data-video-id]');
    if (videoCards.length > 0) {
        markWatchedVideos(videoCards);
    }
}

/**
 * Get the watch history from localStorage.
 * Returns an object with video IDs as keys and timestamps as values.
 * 
 * @returns {Object} - Watch history object
 */
function getWatchHistory() {
    try {
        const history = localStorage.getItem(WATCH_HISTORY_KEY);
        return history ? JSON.parse(history) : {};
    } catch (error) {
        console.error('Error reading watch history:', error);
        return {};
    }
}

/**
 * Save the watch history to localStorage.
 * 
 * @param {Object} history - Watch history object to save
 */
function saveWatchHistory(history) {
    try {
        localStorage.setItem(WATCH_HISTORY_KEY, JSON.stringify(history));
    } catch (error) {
        console.error('Error saving watch history:', error);
    }
}

/**
 * Add a video to the watch history.
 * 
 * @param {string} videoId - The ID of the video that was watched
 */
function startTrackingWatchTime(videoId) {
    const history = getWatchHistory();
    const now = new Date().toISOString();
    
    // Initialize or update watch tracking
    if (!history[videoId]) {
        history[videoId] = {
            startedAt: now,
            minutesWatched: 0,
            status: 'in-progress'
        };
        saveWatchHistory(history);
    }
    
    // Track time only while "trackingActive" is true. Toggle tracking by
    // clicking the video container (not clicks near control area or double-clicks).
    const videoPlayerEl = document.querySelector('.video-player');
    const iframeEl = document.getElementById('videoFrame');
    let trackingActive = true;
    let trackingInterval = null;

    function performTick() {
        const updatedHistory = getWatchHistory();
        if (updatedHistory[videoId] && trackingActive) {
            updatedHistory[videoId].minutesWatched += 0.0833; // ~5 seconds
            updatedHistory[videoId].lastWatchedAt = new Date().toISOString();
            saveWatchHistory(updatedHistory);
            console.log(`Video ${videoId} watch time: ${updatedHistory[videoId].minutesWatched.toFixed(2)} minutes`);
        }
    }

    function startInterval() {
        if (!trackingInterval) {
            trackingInterval = setInterval(performTick, 5000);
        }
    }

    function stopInterval() {
        if (trackingInterval) {
            clearInterval(trackingInterval);
            trackingInterval = null;
        }
    }

    // start tracking by default
    startInterval();

    // Toggle tracking when user clicks the video container itself.
    if (videoPlayerEl) {
        videoPlayerEl.addEventListener('click', function(event) {
                // Only toggle when the click target is the container itself or the iframe
                // (prevents toggling when clicking other UI elements)
                const isOnContainer = event.target === videoPlayerEl || event.target === iframeEl;
                if (!isOnContainer) return;

            // Ignore double-clicks (often used for fullscreen)
            if (event.detail === 2) return;

            // Ignore clicks close to the bottom area where controls/buttons may appear
            const rect = videoPlayerEl.getBoundingClientRect();
            const clickY = event.clientY - rect.top;
            const bottomIgnorePx = 80; // px from bottom to ignore (controls area)
            if (rect.height - clickY <= bottomIgnorePx) return;

            // Toggle tracking
            trackingActive = !trackingActive;
            console.log('Watch time tracking', trackingActive ? 'resumed' : 'paused');

            // Stop the interval entirely when paused to avoid extra reads
            if (!trackingActive) {
                stopInterval();
            } else {
                startInterval();
            }
        });
    }

    // Stop tracking and save when user leaves the page
    window.addEventListener('beforeunload', function() {
        stopInterval();
        // Final save of watch history
        const finalHistory = getWatchHistory();
        if (finalHistory[videoId]) {
            finalHistory[videoId].status = 'completed';
            finalHistory[videoId].lastWatchedAt = new Date().toISOString();
            saveWatchHistory(finalHistory);
            console.log(`Video ${videoId} final time: ${finalHistory[videoId].minutesWatched.toFixed(2)} minutes`);
        }
    });
}

/**
 * Check if a video has been watched for the threshold.
 * 
 * @param {string} videoId - The ID of the video to check
 * @returns {Object|null} - Watch info if watched enough, null otherwise
 */
function getVideoWatchInfo(videoId) {
    const history = getWatchHistory();
    if (history[videoId] && history[videoId].minutesWatched >= 1) {
        return history[videoId];
    }
    return null;
}

/**
 * Check if a video has been watched.
 * 
 * @param {string} videoId - The ID of the video to check
 * @returns {boolean} - True if the video has been watched
 */
function isVideoWatched(videoId) {
    const info = getVideoWatchInfo(videoId);
    return !!info;
}

/**
/**
 * Mark watched videos on the videos listing page.
 * Adds watch progress info to video cards.
 * 
 * @param {NodeList} videoCards - List of video card elements
 */
function markWatchedVideos(videoCards) {
    const history = getWatchHistory();
    console.log('Watch History:', history);
    
    videoCards.forEach(function(card) {
        const videoId = card.getAttribute('data-video-id');
        console.log(`Checking video ${videoId}:`, history[videoId]);
        
        if (videoId && history[videoId]) {
            const watchInfo = history[videoId];
            console.log(`Video ${videoId} minutes watched: ${watchInfo.minutesWatched}`);
            
            if (watchInfo.minutesWatched >= 1) {
                // Has watched for 1+ minute
                card.classList.add('watched');
                console.log(`Adding watched class to ${videoId}`);
                
                // Calculate remaining time (total duration - minutes watched)
                const durationText = card.querySelector('.video-duration')?.textContent || '0:00';
                const remainingMinutes = calculateRemainingMinutes(durationText, watchInfo.minutesWatched);
                console.log(`Video ${videoId} remaining: ${remainingMinutes} minutes`);
                
                // Add watch progress badge
                const progressBadge = document.createElement('div');
                progressBadge.className = 'watch-progress-badge';
                progressBadge.textContent = `${Math.ceil(remainingMinutes)}m left`;
                
                const thumbnail = card.querySelector('.video-thumbnail');
                if (thumbnail) {
                    thumbnail.appendChild(progressBadge);
                    console.log(`Added badge to ${videoId}`);
                }
            }
        }
    });
}

/**
 * Calculate remaining minutes from duration string and minutes watched.
 * 
 * @param {string} durationText - Duration text (e.g., "2:01:28")
 * @param {number} minutesWatched - Minutes already watched
 * @returns {number} - Remaining minutes
 */
function calculateRemainingMinutes(durationText, minutesWatched) {
    const parts = durationText.split(':');
    let totalMinutes = 0;
    
    if (parts.length === 3) {
        // H:MM:SS format
        totalMinutes = parseInt(parts[0]) * 60 + parseInt(parts[1]);
    } else if (parts.length === 2) {
        // MM:SS format
        totalMinutes = parseInt(parts[0]);
    }
    
    return Math.max(0, totalMinutes - minutesWatched);
}

/**
 * Clear all watch history.
 * (Can be called from browser console for testing)
 */
function clearWatchHistory() {
    try {
        localStorage.removeItem(WATCH_HISTORY_KEY);
        console.log('Watch history cleared');
        
        // Remove 'watched' class and badges from all cards if on videos page
        const videoCards = document.querySelectorAll('.video-card.watched');
        videoCards.forEach(function(card) {
            card.classList.remove('watched');
            const badge = card.querySelector('.watch-progress-badge');
            if (badge) {
                badge.remove();
            }
        });
    } catch (error) {
        console.error('Error clearing watch history:', error);
    }
}

/**
 * Get statistics about watch history.
 * (Can be called from browser console for testing)
 * 
 * @returns {Object} - Statistics object
 */
function getWatchHistoryStats() {
    const history = getWatchHistory();
    const videoIds = Object.keys(history);
    
    return {
        totalVideosWatched: videoIds.length,
        videos: history
    };
}

/**
 * =============================================================================
 * UTILITY FUNCTIONS
 * =============================================================================
 * Helper functions that can be used throughout the application.
 */

/**
 * Debounce function - limits how often a function can be called.
 * Useful for scroll and resize event handlers.
 * 
 * @param {Function} func - The function to debounce
 * @param {number} wait - Milliseconds to wait before calling
 * @returns {Function} - Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = function() {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Format duration from seconds to MM:SS format.
 * (For future use if needed)
 * 
 * @param {number} seconds - Duration in seconds
 * @returns {string} - Formatted duration string
 */
function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

/**
 * Copy text to clipboard.
 * Used for the share link button.
 * 
 * @param {string} text - Text to copy
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert('Link copied to clipboard!');
    }, function() {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            alert('Link copied to clipboard!');
        } catch (err) {
            alert('Failed to copy link.');
        }
        document.body.removeChild(textArea);
    });
}

/**
 * =============================================================================
 * END OF FILE
 * =============================================================================
 */
