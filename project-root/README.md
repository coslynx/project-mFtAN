# Discord Music Bot

## Project Overview

This project aims to develop a Discord bot that provides a comprehensive music experience within Discord servers. The bot will allow users to request, play, and manage music, enhancing social interaction and creating a dynamic music atmosphere.

## Features

* **Music Playback:** Users can request songs by title, artist, or URL from supported streaming services (YouTube, Spotify, SoundCloud).
* **Queue Management:** Maintain a queue of requested songs for seamless playback, allowing users to view, add, remove, and shuffle songs.
* **Voice Channel Integration:** The bot seamlessly joins and leaves voice channels, enabling music playback within the user's current voice channel.
* **User Interface:** An intuitive command system using commands like `!play`, `!skip`, `!queue`, etc., allows users to interact with the bot.
* **Moderation:** Administrators can control bot permissions, manage the queue, and restrict certain actions for improved control.
* **Advanced Features:**  
    * **Seek functionality:**  Skip to specific parts of a song.
    * **Shuffle queue:** Randomize the order of songs in the queue for diverse playback.
    * **Looping:**  Loop a song or the entire queue.
    * **Custom playlists:**  Create and manage personal playlists.
    * **Local Music:** Upload and play local audio files.
    * **Discord Rich Presence:** Display information about the currently playing song on user profiles.
    * **Third-Party APIs:**  Integrate with APIs for lyrics, artist information, and album art fetching.

## Tech Stack

**Main Tech Stack:** Python with Discord.py

**APIs:**

* **Discord API:** For bot registration, interaction with Discord servers, voice channel management, and message handling.
* **YouTube Data API (v3):** For fetching song information, audio streams, and metadata from YouTube.
* **Spotify Web API:** For fetching song information, audio streams, and metadata from Spotify.
* **SoundCloud API:** For fetching song information, audio streams, and metadata from SoundCloud.

**Packages and Versions:**

* **discord.py (latest):** The main library for interacting with the Discord API.
* **youtube-dl (latest):** For downloading audio streams from YouTube.
* **spotipy (latest):** For interacting with the Spotify Web API.
* **soundcloud (latest):** For interacting with the SoundCloud API.
* **requests (latest):** For making HTTP requests to APIs.
* **asyncio (built-in):** For handling asynchronous operations.
* **PyMySQL (latest):** For interacting with MySQL databases.
* **psycopg2 (latest):** For interacting with PostgreSQL databases.
* **pymongo (latest):** For interacting with MongoDB databases.

**Other Technical Details:**

* **Database:** MySQL, PostgreSQL, or MongoDB (depending on scalability needs and project requirements).
* **Logging:** Use a logging library like `logging` or `structlog` to log bot activity, errors, and events for debugging and monitoring.
* **Error Handling:** Implement robust error handling mechanisms to catch and handle unexpected errors gracefully.
* **Security:** Implement proper security measures, including sanitizing user input to prevent SQL injection attacks and secure API key storage.
* **Deployment:** Deploy the bot using a hosting service like Heroku, AWS, or Google Cloud Platform.

## Setup Instructions

1. **Prerequisites:**
    * Python 3.6 or higher
    * A Discord account
    * A Discord server where you want to deploy the bot
    * A database (MySQL, PostgreSQL, or MongoDB)

2. **Installation:**
    * Clone the repository.
    * Navigate to the project directory.
    * Install the required packages using `pip install -r requirements.txt`.

3. **Configuration:**
    * Create a `.env` file in the project root.
    * Add the following environment variables:
        * `DISCORD_TOKEN`: Your Discord bot token.
        * `YOUTUBE_API_KEY`: Your YouTube Data API (v3) key.
        * `SPOTIFY_CLIENT_ID`: Your Spotify Web API client ID.
        * `SPOTIFY_CLIENT_SECRET`: Your Spotify Web API client secret.
        * `SOUNDCLOUD_CLIENT_ID`: Your SoundCloud API client ID.
        * `SOUNDCLOUD_CLIENT_SECRET`: Your SoundCloud API client secret.
        * `DATABASE_HOST`: Your database host address.
        * `DATABASE_USER`: Your database username.
        * `DATABASE_PASSWORD`: Your database password.
        * `DATABASE_NAME`: Your database name.

4. **Running the Bot:**
    * Execute the `main.py` file using `python main.py`.

## Usage Instructions

1. **Add the bot to your Discord server:**
    * Go to the bot's application page on Discord Developer Portal.
    * Click on "OAuth2" and select "bot".
    * Enable the required permissions (e.g., "Manage Channels", "Connect", "Speak").
    * Copy the generated link and use it to add the bot to your server.

2. **Use the following commands:**
    * `!play <song name>`: Requests a song.
    * `!skip`: Skips the current song.
    * `!stop`: Stops playback and clears the queue.
    * `!pause`: Pauses playback.
    * `!resume`: Resumes playback after a pause.
    * `!queue`: Displays the current song queue.
    * `!join`: Makes the bot join your voice channel.
    * `!leave`: Makes the bot leave the voice channel.
    * `!volume <number>`: Adjusts the volume (0-100).

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.

## Acknowledgements

This project is built upon the excellent work of the Discord.py community and the creators of the various APIs used.