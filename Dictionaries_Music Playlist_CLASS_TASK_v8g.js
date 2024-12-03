/**
 * Music Player Implementation
 * This code implements a multi-playlist music player with basic playback controls
 * and playlist management functionality.
 */

// DOM Elements Section
// These constants store references to HTML elements that the player interacts with
const add_song_form = document.getElementById('addSongForm');
const song_title_input = document.getElementById('songTitle');
const song_artist_input = document.getElementById('songArtist');
const song_list = document.getElementById('songList');
const prev_track_button = document.getElementById('prevTrack');
const play_pause_button = document.getElementById('playPause');
const next_track_button = document.getElementById('nextTrack');
const next_playlist_button = document.getElementById('nextPlaylist');
const stop_button = document.getElementById('stop');
const delete_track_button = document.getElementById('deleteTrack');
const add_track_button = document.getElementById('addTrack');

/**
 * State Management
 * The player maintains several pieces of state to track:
 * - playlists: An array of arrays, where each inner array represents a playlist
 * - current_playlist_index: Which playlist is currently active
 * - current_song_index: Which song is currently playing (-1 means no song)
 * - is_playing: Whether music is currently playing
 * - selected_song_index: Which song is selected in the UI (-1 means no selection)
 */
let playlists = [[]];  // Initialize with one empty playlist
let current_playlist_index = 0;
let current_song_index = -1;
let is_playing = false;
let selected_song_index = -1;

/**
 * Updates the visual display of the current playlist
 * This function:
 * 1. Clears the existing song list
 * 2. Creates new DOM elements for each song
 * 3. Applies visual styling for playing/selected states
 * 4. Sets up click handlers for selection
 */
function update_playlist() {
    song_list.innerHTML = '';
    const current_playlist = playlists[current_playlist_index];
    
    current_playlist.forEach((song, index) => {
        const song_item = document.createElement('div');
        song_item.classList.add('song');
        
        // Visual feedback: Green border for playing song
        if (index === current_song_index && is_playing) {
            song_item.style.borderColor = '#00ff00';
        }
        
        // Visual feedback: Light green background for selected song
        if (index === selected_song_index) {
            song_item.style.backgroundColor = 'rgba(0, 255, 0, 0.2)';
        }
        
        // Create song display with delete button
        song_item.innerHTML = `
            <p>${song.title} - ${song.artist}</p>
            <button class="deleteSong" data-index="${index}">Delete</button>
        `;
        
        // Enable song selection on click, but not when clicking delete button
        song_item.addEventListener('click', (e) => {
            if (!e.target.classList.contains('deleteSong')) {
                selected_song_index = index;
                update_playlist();
            }
        });
        
        song_list.appendChild(song_item);
    });
}

/**
 * Handles play/pause functionality
 * - Checks if playlist has songs
 * - Toggles play state
 * - Updates button text
 * - Starts from beginning if no song is selected
 */
function toggle_play_pause() {
    const current_playlist = playlists[current_playlist_index];
    
    if (!current_playlist.length) {
        alert('Please add songs to the playlist first');
        return;
    }

    // Start from first song if none is selected
    if (current_song_index === -1) {
        current_song_index = 0;
    }

    is_playing = !is_playing;
    play_pause_button.textContent = is_playing ? 'Pause' : 'Play';
    update_playlist();
}

/**
 * Stops playback completely
 * - Resets playing state
 * - Clears current song
 * - Updates UI
 */
function stop_playback() {
    is_playing = false;
    current_song_index = -1;
    play_pause_button.textContent = 'Play';
    update_playlist();
}

/**
 * Advances to next track
 * - Loops back to start if at end of playlist
 * - Only updates UI if currently playing
 */
function next_track() {
    const current_playlist = playlists[current_playlist_index];
    
    if (!current_playlist.length) return;
    
    if (current_song_index < current_playlist.length - 1) {
        current_song_index++;
    } else {
        current_song_index = 0;  // Loop back to start
    }
    
    if (is_playing) {
        update_playlist();
    }
}

/**
 * Moves to previous track
 * - Loops to end if at start of playlist
 * - Only updates UI if currently playing
 */
function prev_track() {
    const current_playlist = playlists[current_playlist_index];
    
    if (!current_playlist.length) return;
    
    if (current_song_index > 0) {
        current_song_index--;
    } else {
        current_song_index = current_playlist.length - 1;  // Loop to end
    }
    
    if (is_playing) {
        update_playlist();
    }
}

/**
 * Switches to next playlist
 * - Creates new playlist if at last playlist
 * - Resets playback state
 * - Updates UI
 */
function next_playlist() {
    if (current_playlist_index < playlists.length - 1) {
        current_playlist_index++;
    } else {
        playlists.push([]);  // Create new empty playlist
        current_playlist_index = playlists.length - 1;
    }
    // Reset all playback state for new playlist
    current_song_index = -1;
    selected_song_index = -1;
    is_playing = false;
    play_pause_button.textContent = 'Play';
    update_playlist();
}

/**
 * Deletes the currently selected track
 * - Handles updating current_song_index if needed
 * - Clears selection after delete
 */
function delete_selected_track() {
    const current_playlist = playlists[current_playlist_index];
    
    if (selected_song_index === -1) {
        alert('Please select a song to delete');
        return;
    }
    
    current_playlist.splice(selected_song_index, 1);
    
    // Handle current_song_index updates
    if (current_song_index === selected_song_index) {
        stop_playback();  // Stop if current song was deleted
    } else if (current_song_index > selected_song_index) {
        current_song_index--;  // Adjust index if deleted song was before current
    }
    
    selected_song_index = -1;
    update_playlist();
}

/**
 * Initiates adding a new track by focusing the title input
 */
function add_new_track() {
    song_title_input.focus();
}

/**
 * Event Listeners Section
 * Sets up all interaction handlers
 */

// Form submission handler for adding new songs
add_song_form.addEventListener('submit', (event) => {
    event.preventDefault();
    const song_title = song_title_input.value.trim();
    const song_artist = song_artist_input.value.trim();
    
    if (song_title && song_artist) {
        playlists[current_playlist_index].push({ 
            title: song_title, 
            artist: song_artist 
        });
        update_playlist();
        song_title_input.value = '';
        song_artist_input.value = '';
    }
});

// Click handler for song list (handles delete button clicks)
song_list.addEventListener('click', (event) => {
    if (event.target.classList.contains('deleteSong')) {
        const index = parseInt(event.target.getAttribute('data-index'));
        playlists[current_playlist_index].splice(index, 1);
        
        // Handle current_song_index updates
        if (current_song_index === index) {
            stop_playback();
        } else if (current_song_index > index) {
            current_song_index--;
        }
        
        selected_song_index = -1;
        update_playlist();
    }
});

// Set up all button click handlers
play_pause_button.addEventListener('click', toggle_play_pause);
stop_button.addEventListener('click', stop_playback);
next_track_button.addEventListener('click', next_track);
prev_track_button.addEventListener('click', prev_track);
next_playlist_button.addEventListener('click', next_playlist);
delete_track_button.addEventListener('click', delete_selected_track);
add_track_button.addEventListener('click', add_new_track);

// Initialize the playlist display
update_playlist();