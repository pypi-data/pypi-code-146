import logging
import pygame

logger = logging.getLogger(__name__)


class Announcer:
    """Announcer encapsulates the pygame functionality to play sounds.

    Author:  Michael J. Swenson
    """

    def __init__(self):
        """Initialize the pygame mixer.  This must be done once.
        """
        try:
            pygame.mixer.init()
            pygame.mixer.music.load('./sound/complete.wav')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
            logger.debug(f'Pygame sound mixer initialized.')
            self.initialized = True
        except Exception as e:
            logger.error(f'Error initializing Announcer.\n   {e}')
            raise

    def _play_message(self, logmsg: str, soundfile: str):
        """Logs an informational message to the logger and plays the sound
        file passed as soundfile.

        :param self:
        :param logmsg: str: Informational message posted to the logger before the message is played.
        :param soundfile: str:  The sound file to play
        :return: nothing
        """
        try:
            logger.info(logmsg)
            pygame.mixer.music.load(soundfile)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
            logger.info(f'Played {soundfile}')
        except Exception as e:
            logger.error(f'Error in Announcer playing message .\n   {e}')
            raise

    def announce_message(self, message_minutes: int):
        """

        :param self:
        :param message_minutes: int: number of minutes before the range closes.
        :return: nothing
        """
        if message_minutes == 0:  # Play we are closed message
            self._play_message('About to play closing message.', './sound/closed.mp3')
        elif message_minutes == 5:  # Play closing in 5 minutes message
            self._play_message('About to play 5 minutes to close message.', './sound/5_minutes.mp3')
        elif message_minutes == 15:
            self._play_message('About to play 15 minutes to close message.', './sound/15_minutes.mp3')
        elif message_minutes == 30:
            self._play_message('About to play 30 minutes to close message.', './sound/30_minutes.mp3')
        elif message_minutes == 60:
            self._play_message('About to play 1 hour to close message.', './sound/one_hour.mp3')
        else:
            logger.debug('Invalid message ID sent to announce_message.')
            return
        logger.info('Completed playing message.')
