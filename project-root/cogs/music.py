import discord
from discord.ext import commands
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import soundcloud
import requests
import asyncio
from utils.music_player import MusicPlayer
from utils.config import Config

# Suppress noisy youtube_dl logging
youtube_dl.utils.bug_reports_message = lambda: ''

class MusicCog(commands.Cog):
    """Cog for music-related commands."""

    def __init__(self, bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.voice_client = None
        self.current_song = None
        self.music_player = MusicPlayer()
        self.config = Config()

        # Spotify API credentials
        self.spotify_client_id = self.config.get_value("SPOTIFY_CLIENT_ID")
        self.spotify_client_secret = self.config.get_value("SPOTIFY_CLIENT_SECRET")
        self.spotify_client_credentials_manager = SpotifyClientCredentials(
            client_id=self.spotify_client_id,
            client_secret=self.spotify_client_secret
        )
        self.spotify = spotipy.Spotify(client_credentials_manager=self.spotify_client_credentials_manager)

        # SoundCloud API credentials
        self.soundcloud_client_id = self.config.get_value("SOUNDCLOUD_CLIENT_ID")
        self.soundcloud_client_secret = self.config.get_value("SOUNDCLOUD_CLIENT_SECRET")
        self.soundcloud = soundcloud.Client(client_id=self.soundcloud_client_id, client_secret=self.soundcloud_client_secret)

    @commands.command(name="play", description="Plays a song from YouTube, Spotify, or SoundCloud.")
    async def play(self, ctx, *, song_name: str):
        """Plays a song from YouTube, Spotify, or SoundCloud.

        Args:
            ctx: The context of the command.
            song_name: The name or URL of the song to play.
        """
        try:
            # Check if the bot is already connected to a voice channel
            if not ctx.author.voice:
                await ctx.send("You need to be in a voice channel to use this command.")
                return

            if not self.voice_client:
                self.voice_client = await ctx.author.voice.channel.connect()

            # Check if the user provided a URL
            if "youtube.com" in song_name or "youtu.be" in song_name:
                await self.play_youtube(ctx, song_name)
            elif "spotify.com" in song_name:
                await self.play_spotify(ctx, song_name)
            elif "soundcloud.com" in song_name:
                await self.play_soundcloud(ctx, song_name)
            else:
                await self.play_youtube(ctx, song_name)  # Default to YouTube search

        except Exception as e:
            print(f"Error in play command: {e}")
            await ctx.send(f"An error occurred while playing the song: {e}")

    async def play_youtube(self, ctx, song_name: str):
        """Plays a song from YouTube."""
        try:
            # Search YouTube for the song
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                'noplaylist': True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song_name, download=False)
                url = info['formats'][0]['url']
                title = info['title']
                artist = info.get('artist', 'Unknown Artist')

            # Add the song to the queue
            await self.queue.put({'url': url, 'title': title, 'artist': artist})

            # Start playing the next song
            await self.play_next(ctx)

        except Exception as e:
            print(f"Error in play_youtube: {e}")
            await ctx.send(f"An error occurred while playing the song from YouTube: {e}")

    async def play_spotify(self, ctx, song_name: str):
        """Plays a song from Spotify."""
        try:
            # Search Spotify for the song
            results = self.spotify.search(q=song_name, type="track", limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                track_url = track['external_urls']['spotify']
                title = track['name']
                artist = track['artists'][0]['name']

                # Add the song to the queue
                await self.queue.put({'url': track_url, 'title': title, 'artist': artist})

                # Start playing the next song
                await self.play_next(ctx)
            else:
                await ctx.send("Song not found on Spotify.")

        except Exception as e:
            print(f"Error in play_spotify: {e}")
            await ctx.send(f"An error occurred while playing the song from Spotify: {e}")

    async def play_soundcloud(self, ctx, song_name: str):
        """Plays a song from SoundCloud."""
        try:
            # Search SoundCloud for the song
            results = self.soundcloud.get('/tracks', q=song_name)
            if results:
                track = results[0]
                track_url = track.permalink_url
                title = track.title
                artist = track.user['username']

                # Add the song to the queue
                await self.queue.put({'url': track_url, 'title': title, 'artist': artist})

                # Start playing the next song
                await self.play_next(ctx)
            else:
                await ctx.send("Song not found on SoundCloud.")

        except Exception as e:
            print(f"Error in play_soundcloud: {e}")
            await ctx.send(f"An error occurred while playing the song from SoundCloud: {e}")

    async def play_next(self, ctx):
        """Plays the next song in the queue."""
        try:
            if self.voice_client and self.voice_client.is_connected():
                if not self.music_player.is_playing():
                    next_song = await self.queue.get()
                    self.current_song = next_song
                    self.music_player.play(next_song['url'], self.voice_client)

                    await ctx.send(f"Now playing: **{self.current_song['title']}** by **{self.current_song['artist']}**")

        except Exception as e:
            print(f"Error in play_next: {e}")
            await ctx.send(f"An error occurred while playing the next song: {e}")

    @commands.command(name="skip", description="Skips the current song.")
    async def skip(self, ctx):
        """Skips the current song."""
        try:
            if self.voice_client and self.voice_client.is_connected():
                if self.music_player.is_playing():
                    self.music_player.stop()
                    await self.queue.put(self.current_song)  # Put the current song back in the queue
                    await self.play_next(ctx)

                else:
                    await ctx.send("No song is currently playing.")

        except Exception as e:
            print(f"Error in skip command: {e}")
            await ctx.send(f"An error occurred while skipping the song: {e}")

    @commands.command(name="stop", description="Stops the music and clears the queue.")
    async def stop(self, ctx):
        """Stops the music and clears the queue."""
        try:
            if self.voice_client and self.voice_client.is_connected():
                if self.music_player.is_playing():
                    self.music_player.stop()
                    await ctx.send("Music stopped.")
                    await self.voice_client.disconnect()
                    self.voice_client = None
                    self.queue = asyncio.Queue()  # Clear the queue

        except Exception as e:
            print(f"Error in stop command: {e}")
            await ctx.send(f"An error occurred while stopping the music: {e}")

    @commands.command(name="pause", description="Pauses the current song.")
    async def pause(self, ctx):
        """Pauses the current song."""
        try:
            if self.voice_client and self.voice_client.is_connected():
                if self.music_player.is_playing():
                    self.music_player.pause()
                    await ctx.send("Music paused.")
                else:
                    await ctx.send("No song is currently playing.")

        except Exception as e:
            print(f"Error in pause command: {e}")
            await ctx.send(f"An error occurred while pausing the music: {e}")

    @commands.command(name="resume", description="Resumes the current song.")
    async def resume(self, ctx):
        """Resumes the current song."""
        try:
            if self.voice_client and self.voice_client.is_connected():
                if self.music_player.is_paused():
                    self.music_player.resume()
                    await ctx.send("Music resumed.")
                else:
                    await ctx.send("No song is currently paused.")

        except Exception as e:
            print(f"Error in resume command: {e}")
            await ctx.send(f"An error occurred while resuming the music: {e}")

    @commands.command(name="queue", description="Shows the current song queue.")
    async def queue(self, ctx):
        """Shows the current song queue."""
        try:
            if self.queue.empty():
                await ctx.send("The queue is empty.")
                return

            queue_list = list(self.queue._queue)  # Get the queue contents
            queue_str = "**Queue:**\n"
            for i, song in enumerate(queue_list):
                queue_str += f"{i + 1}. {song['title']} by {song['artist']}\n"
            await ctx.send(queue_str)

        except Exception as e:
            print(f"Error in queue command: {e}")
            await ctx.send(f"An error occurred while displaying the queue: {e}")

    @commands.command(name="join", description="Joins the user's voice channel.")
    async def join(self, ctx):
        """Joins the user's voice channel."""
        try:
            if not ctx.author.voice:
                await ctx.send("You need to be in a voice channel to use this command.")
                return

            self.voice_client = await ctx.author.voice.channel.connect()
            await ctx.send(f"Joined {ctx.author.voice.channel.name}")

        except Exception as e:
            print(f"Error in join command: {e}")
            await ctx.send(f"An error occurred while joining the voice channel: {e}")

    @commands.command(name="leave", description="Leaves the current voice channel.")
    async def leave(self, ctx):
        """Leaves the current voice channel."""
        try:
            if self.voice_client and self.voice_client.is_connected():
                await self.voice_client.disconnect()
                self.voice_client = None
                await ctx.send("Left the voice channel.")

        except Exception as e:
            print(f"Error in leave command: {e}")
            await ctx.send(f"An error occurred while leaving the voice channel: {e}")

    @commands.command(name="volume", description="Adjusts the volume of the music.")
    async def volume(self, ctx, volume: int):
        """Adjusts the volume of the music.

        Args:
            ctx: The context of the command.
            volume: The desired volume (0-100).
        """
        try:
            if self.voice_client and self.voice_client.is_connected():
                if 0 <= volume <= 100:
                    self.music_player.set_volume(volume / 100)
                    await ctx.send(f"Volume set to {volume}%")
                else:
                    await ctx.send("Volume must be between 0 and 100.")

        except Exception as e:
            print(f"Error in volume command: {e}")
            await ctx.send(f"An error occurred while adjusting the volume: {e}")

def setup(bot):
    bot.add_cog(MusicCog(bot))