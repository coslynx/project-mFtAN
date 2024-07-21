import asyncio
import subprocess
import logging

logger = logging.getLogger(__name__)

class MusicPlayer:
    """Manages music playback using ffmpeg."""

    def __init__(self):
        self.player = None
        self.current_stream = None
        self.volume = 0.5  # Default volume

    async def play(self, stream_url, voice_client):
        """Starts playing the provided audio stream."""
        try:
            # Stop any existing playback
            if self.player:
                await self.stop()

            self.current_stream = stream_url

            # ffmpeg command for playing audio
            self.player = await asyncio.create_subprocess_exec(
                "ffmpeg",
                "-loglevel", "panic",  # Suppress ffmpeg logging
                "-i", stream_url,
                "-vn",  # Disable video output
                "-af", f"volume={self.volume}",  # Apply volume
                "-f", "s16le",
                "-ar", "48000",
                "-ac", "2",
                "pipe:1",
                stdout=subprocess.PIPE,
            )

            # Send audio data to Discord voice client
            while True:
                audio_data = await self.player.stdout.read(1024)
                if not audio_data:
                    break
                voice_client.play(discord.PCMVolumeTransformer(discord.Audio(audio_data), volume=self.volume))

            # Wait for ffmpeg to finish
            await self.player.wait()
            logger.info("Music playback finished.")
        except Exception as e:
            logger.error(f"Error playing music: {e}")

    async def stop(self):
        """Stops the current music playback."""
        try:
            if self.player:
                self.player.kill()
                self.player = None
                self.current_stream = None
                logger.info("Music playback stopped.")
        except Exception as e:
            logger.error(f"Error stopping music: {e}")

    async def pause(self):
        """Pauses the current music playback."""
        try:
            if self.player:
                self.player.stdin.write(b'pause\n')
                self.player.stdin.flush()
                logger.info("Music playback paused.")
        except Exception as e:
            logger.error(f"Error pausing music: {e}")

    async def resume(self):
        """Resumes the music playback."""
        try:
            if self.player:
                self.player.stdin.write(b'resume\n')
                self.player.stdin.flush()
                logger.info("Music playback resumed.")
        except Exception as e:
            logger.error(f"Error resuming music: {e}")

    def is_playing(self):
        """Returns True if music is currently playing, False otherwise."""
        return self.player is not None and self.player.returncode is None

    def is_paused(self):
        """Returns True if music is currently paused, False otherwise."""
        return self.player is not None and self.player.returncode is None

    def set_volume(self, volume):
        """Sets the volume for music playback."""
        if 0 <= volume <= 1:
            self.volume = volume
            if self.player:
                self.player.stdin.write(f'volume={volume}\n'.encode())
                self.player.stdin.flush()
            logger.info(f"Volume set to {volume}")
        else:
            logger.error(f"Invalid volume: {volume} (must be between 0 and 1).")