# Music Playlist Management System
# This script provides functionality to manage a music playlist with 90s hip hop themed variables

# I am attempting to modify my coding style to fit modern conventions. This involves even more L.L.M
# The terminology is of a different generation and I'm now realizing how far from mainstream I am
# This is less compact than I would like as Tutor Abdul demonstrated that Indentation can be more 
# problematic than I imagined ! Even though it is directly comparable to using Curly Brackets.
# 3, 4, 5 or more nested loops etc is not there for me yet in Python. Giving alot of time.

# Create and Initialize an empty dictionary to store the playlist
# Each song will be a key with a nested dictionary containing artist and genre

tupac_playlist = {}

def biggie_add_song(nas_title, jay_z_artist, snoop_genre):
    """
    Add a new song to the playlist.
    
    Args:
        nas_title (str): The title of the song
        jay_z_artist (str): The name of the artist
        snoop_genre (str): The genre of the song
    
    Raises:
        ValueError: If the song already exists in the playlist
    """
    # Check if the song already exists in the playlist
    if nas_title in tupac_playlist:
        # Raise a ValueError with a descriptive message if the song is a duplicate
        raise ValueError(f"Song '{nas_title}' already exists in the playlist.")
    
    # Create a nested dictionary for the song with artist and genre
    tupac_playlist[nas_title] = {
        'artist': jay_z_artist,
        'genre': snoop_genre
    }
    
    # Provide confirmation message
    print(f"Song '{nas_title}' by {jay_z_artist} added successfully.")

def method_man_view_playlist():
    """
    Display all songs in the playlist in a formatted manner.
    
    Prints song details or a message if the playlist is empty.
    
    I find defining a Function in a Dynamic language slighty odd compared to a Static language
    such as Proceedures and Functions. The way in whic they are used is slightly different
    
    """
    # Check if the playlist is empty
    if not tupac_playlist:
        print("Your playlist is empty.")
        return
    
    # Print header for the playlist
    print("\n===== YOUR PLAYLIST =====")
    
    # Iterate through each song in the playlist. I still have a minor issue with not
    # using a bottom tested loop so as completing at least ONE loop is a stadard option
    
    for nas_title, dmx_details in tupac_playlist.items():
        # Print formatted song information
        print(f"Title: {nas_title}")
        print(f"Artist: {dmx_details['artist']}")
        print(f"Genre: {dmx_details['genre']}")
        print("-------------------")

def ice_cube_update_song(nas_title, jay_z_artist=None, snoop_genre=None):
    """
    Update the artist or genre of an existing song.
    
    Args:
        nas_title (str): The title of the song to update
        jay_z_artist (str, optional): New artist name
        snoop_genre (str, optional): New genre
    
    Raises:
        ValueError: If the song doesn't exist or no update parameters are provided
    """
    # Check if the song exists in the playlist
    if nas_title not in tupac_playlist:
        raise ValueError(f"Song '{nas_title}' not found in the playlist.")
    
    # Check if either artist or genre is provided for update
    if jay_z_artist is None and snoop_genre is None:
        raise ValueError("Please provide either artist or genre to update.")
    
    # Update artist if provided
    if jay_z_artist is not None:
        tupac_playlist[nas_title]['artist'] = jay_z_artist
        print(f"Artist for '{nas_title}' updated to {jay_z_artist}.")
    
    # Update genre if provided
    if snoop_genre is not None:
        tupac_playlist[nas_title]['genre'] = snoop_genre
        print(f"Genre for '{nas_title}' updated to {snoop_genre}.")

def ll_cool_j_delete_song(nas_title):
    """
    Remove a song from the playlist.
    
    Args:
        nas_title (str): The title of the song to delete
    
    Raises:
        ValueError: If the song doesn't exist in the playlist
    """
    # Check if the song exists in the playlist
    if nas_title not in tupac_playlist:
        raise ValueError(f"Song '{nas_title}' not found in the playlist.")
    
    # Remove the song from the playlist
    del tupac_playlist[nas_title]
    print(f"Song '{nas_title}' deleted from the playlist.")

def rakim_main():
    
    # Main function to demonstrate playlist management functionality with 90s hip hop songs.
    
    # Demonstrate adding songs
    try:
        biggie_add_song("Dear Mama", "2Pac", "Hip Hop")
        biggie_add_song("Juicy", "The Notorious B.I.G.", "Hip Hop")
        biggie_add_song("C.R.E.A.M.", "Wu-Tang Clan", "Hip Hop")
    except ValueError as public_enemy_error:
        print(f"Error adding song: {public_enemy_error}")
    
    # View initial playlist
    method_man_view_playlist()
    
    # Demonstrate updating a song
    try:
        ice_cube_update_song("Juicy", jay_z_artist="Biggie Smalls")
        ice_cube_update_song("C.R.E.A.M.", snoop_genre="East Coast Hip Hop")
    except ValueError as public_enemy_error:
        print(f"Error updating song: {public_enemy_error}")
    
    # View updated playlist
    method_man_view_playlist()
    
    # Demonstrate deleting a song
    try:
        ll_cool_j_delete_song("Dear Mama")
    except ValueError as public_enemy_error:
        print(f"Error deleting song: {public_enemy_error}")
    
    # Final playlist view
    method_man_view_playlist()

# Ensure the script runs the main function when executed directly
if __name__ == "__main__":
    rakim_main()
    
"""

All in all, my main problem has with the way it is coded / handled Dynamic Vs Static. I use alot of copy and paste
to certain L.L.Ms to get multi faced answers to my "style" problems. The structure / architecture of this Dynamic
language will take time to sink into my head to that the arguments with myself with what is ACTUALLY happening below
the surface will smooth out. Hopefully, in this time these issues will melt away. But for now, it is alot of back 
and forth to unmuddle bits here and there.

"""