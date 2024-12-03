// ===== DOM Element Selection =====
// Get references to all the HTML elements we'll need to manipulate
// I still use snake_case as it's easier / more narural for me
// Mixing the styles like this is untidy, But I read it well during 
// this learning phase. The L.L.M's are very adept at tidying code

const add_song_form = document.getElementById('addSongForm'); 
// Form for adding new songs via html ID 'addSongForm'.
// `getElementById` is used to retrieve the HTML element with the ID 'addSongForm'.
const song_title_input = document.getElementById('songTitle');
// Input field for song title
const song_artist_input = document.getElementById('songArtist');        // Input field for artist name
const song_list = document.getElementById('songList');                  // Container for displaying the playlist
const prev_track_button = document.getElementById('prevTrack');         // Button to go to previous track
const play_pause_button = document.getElementById('playPause');         // Button to toggle play/pause
const next_track_button = document.getElementById('nextTrack');         // Button to go to next track
const next_playlist_button = document.getElementById('nextPlaylist');   // Button to switch to next playlist
const stop_button = document.getElementById('stop');                    // Button to stop playback
const delete_track_button = document.getElementById('deleteTrack');     // Button to delete selected track
const add_track_button = document.getElementById('addTrack');           // Button to trigger add track form
const color_scheme_select = document.getElementById('colorScheme');     // Dropdown for theme selection

// ===== Application State Management =====
// These variables keep track of the current state of the music player
let playlists = [[]];              // Array of playlists, starting with one empty playlist
let current_playlist_index = 0;     // Index of the currently active playlist
let current_song_index = -1;        // Index of the currently playing song (-1 means no song playing)
let is_playing = false;             // Boolean to track if music is currently playing
let selected_song_index = -1;       // Index of the currently selected song in the UI (-1 means no selection)

/**
 * Updates the visual representation of the playlist in the UI
 * This function is called whenever the playlist state changes
 */
function update_playlist() {
    song_list.innerHTML = '';   // Clear the current playlist display
    const current_playlist = playlists[current_playlist_index];
    
    // Create and append DOM elements for each song in the playlist
    current_playlist.forEach((song, index) => {
        const song_item = document.createElement('div');
        song_item.classList.add('song');
        
        // Highlight currently playing song with green border
        if (index === current_song_index && is_playing) {
            song_item.style.borderColor = '#00ff00';
        }
        
        // Highlight selected song with light green background
        if (index === selected_song_index) {
            song_item.style.backgroundColor = 'rgba(0, 255, 0, 0.2)';
        }
        
        // Create the song item HTML with title, artist, and delete button
        song_item.innerHTML = `
            <p>${song.title} - ${song.artist}</p>
            <button class="deleteSong" data-index="${index}">Delete</button>
        `;
        
        // Add click handler for song selection (ignoring clicks on delete button)
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
 * Toggles between play and pause states
 * Handles edge cases like empty playlist and initial playback
 */
function toggle_play_pause() {
    const current_playlist = playlists[current_playlist_index];
    
    // Prevent playback if playlist is empty
    if (!current_playlist.length) {
        alert('Please add songs to the playlist first');
        return;
    }

    // Start playback from first song if no song is currently selected
    if (current_song_index === -1) {
        current_song_index = 0;
    }

    // Toggle play state and update button text
    is_playing = !is_playing;
    play_pause_button.textContent = is_playing ? 'Pause' : 'Play';
    update_playlist();
}

/**
 * Stops playback and resets the player state
 */
function stop_playback() {
    is_playing = false;
    current_song_index = -1;
    play_pause_button.textContent = 'Play';
    update_playlist();
}

/**
 * Advances to the next track in the playlist
 * Loops back to start if at the end of playlist
 */
function next_track() {
    const current_playlist = playlists[current_playlist_index];
    
    if (!current_playlist.length) return;
    
    // Move to next song or loop back to start
    if (current_song_index < current_playlist.length - 1) {
        current_song_index++;
    } else {
        current_song_index = 0;
    }
    
    // Only update UI if currently playing
    if (is_playing) {
        update_playlist();
    }
}

/**
 * Goes to the previous track in the playlist
 * Loops to end if at the start of playlist
 */
function prev_track() {
    const current_playlist = playlists[current_playlist_index];
    
    if (!current_playlist.length) return;
    
    // Move to previous song or loop to end
    if (current_song_index > 0) {
        current_song_index--;
    } else {
        current_song_index = current_playlist.length - 1;
    }
    
    // Only update UI if currently playing
    if (is_playing) {
        update_playlist();
    }
}

/**
 * Switches to the next playlist or creates a new one
 * Resets playback state for the new playlist
 */
function next_playlist() {
    // Move to next playlist or create new one if at the end
    if (current_playlist_index < playlists.length - 1) {
        current_playlist_index++;
    } else {
        playlists.push([]);
        current_playlist_index = playlists.length - 1;
    }
    
    // Reset all playback and selection states
    current_song_index = -1;
    selected_song_index = -1;
    is_playing = false;
    play_pause_button.textContent = 'Play';
    update_playlist();
}

/**
 * Deletes the currently selected track from the playlist
 * Handles updating playback state if the current song is deleted
 */
function delete_selected_track() {
    const current_playlist = playlists[current_playlist_index];
    
    // Prevent deletion if no song is selected
    if (selected_song_index === -1) {
        alert('Please select a song to delete');
        return;
    }
    
    // Remove the selected song
    current_playlist.splice(selected_song_index, 1);
    
    // Update playback state if necessary
    if (current_song_index === selected_song_index) {
        stop_playback();
    } else if (current_song_index > selected_song_index) {
        current_song_index--;
    }
    
    selected_song_index = -1;
    update_playlist();
}

/**
 * Focuses the song title input to prepare for adding a new track
 */
function add_new_track() {
    song_title_input.focus();
}

/**
 * Changes the application's color theme
 * @param {string} theme - The theme name to apply
 */
function change_theme(theme) {
    // Remove all possible theme classes
    document.body.classList.remove('theme-normal', 'theme-dark', 'theme-blue', 
        'theme-gold', 'theme-red', 'theme-cream', 'theme-light-grey');
    // Add the selected theme class
    document.body.classList.add(`theme-${theme}`);
}

// ===== Event Listeners =====
// Handle form submission for adding new songs
add_song_form.addEventListener('submit', (event) => {
    event.preventDefault();
    const song_title = song_title_input.value.trim();
    const song_artist = song_artist_input.value.trim();
    
    // Only add song if both title and artist are provided
    if (song_title && song_artist) {
        playlists[current_playlist_index].push({ 
            title: song_title, 
            artist: song_artist 
        });
        update_playlist();
        // Clear input fields after adding song
        song_title_input.value = '';
        song_artist_input.value = '';
    }
});

// Handle delete button clicks within the song list
song_list.addEventListener('click', (event) => {
    if (event.target.classList.contains('deleteSong')) {
        const index = parseInt(event.target.getAttribute('data-index'));
        playlists[current_playlist_index].splice(index, 1);
        
        // Update playback state if necessary
        if (current_song_index === index) {
            stop_playback();
        } else if (current_song_index > index) {
            current_song_index--;
        }
        
        selected_song_index = -1;
        update_playlist();
    }
});

// Connect control buttons to their respective functions
play_pause_button.addEventListener('click', toggle_play_pause);
stop_button.addEventListener('click', stop_playback);
next_track_button.addEventListener('click', next_track);
prev_track_button.addEventListener('click', prev_track);
next_playlist_button.addEventListener('click', next_playlist);
delete_track_button.addEventListener('click', delete_selected_track);
add_track_button.addEventListener('click', add_new_track);
color_scheme_select.addEventListener('change', (e) => {
    change_theme(e.target.value);
});

// ===== Initialization =====
// Set up initial state
update_playlist();
change_theme('normal');