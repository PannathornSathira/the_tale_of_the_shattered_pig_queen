import pygame
import cv2
from abc import ABC, abstractmethod
from src.constants import *
from src.Dependency import *
from src.resources import *
from src.Util import *


class StartStoryState:
    def __init__(self, screen, font):
        # Initialize Pygame and its mixer
        pygame.init()
        pygame.mixer.init()
        self.play_check = False
        self.bg_image = pygame.image.load(resource_path("graphics/Backgrounds/Enter_tutorial.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        # Set up the screen with specified width and height
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Start Story")

        # Set up video capture and audio
        self.cap = cv2.VideoCapture(resource_path("video/My_Movie_11.mov"))
        self.audio_path = resource_path("video/My_Movie_1_audio.mp3")
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.set_volume(1.7)

        # Get video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.clock = pygame.time.Clock()  # Control frame rate
        
        self.ask_skip_popup = False
        self.ask_skip_timer = 0
        self.ask_skip_time = 5
        self.dt = 0
        
        self.font = font
    def Enter(self, params):
        self.play_check = params.get("play_check")

    def render(self, screen):
        if self.play_check:   
            pygame.mixer.music.play()  # Start audio playback

            # Main loop for video playback
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break  # Exit if there are no frames left

                # Resize frame to fit the screen dimensions
                frame = cv2.resize(frame, (WIDTH, HEIGHT))

                # Convert color from BGR (OpenCV default) to RGB (Pygame compatible)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

                # Clear the screen and display the current frame
                self.screen.fill((0, 0, 0))
                self.screen.blit(frame_surface, (0, 0))

                if self.ask_skip_popup:
                    render_text("Press Enter to skip", 900, 600, self.font, screen)
                    
                pygame.display.update()

                if self.ask_skip_popup:
                    self.ask_skip_timer += self.dt
                    if self.ask_skip_timer >= self.ask_skip_time:
                        self.ask_skip_timer = 0
                        self.ask_skip_popup = False

                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.cleanup()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if self.ask_skip_popup and event.key == pygame.K_RETURN:
                            # Stop the video and show end screen
                            pygame.mixer.music.stop()
                            self.cap.release()
                            self.show_end_screen(screen)
                            return
                        
                        if not self.ask_skip_popup:
                            self.ask_skip_popup = True
                            self.ask_skip_timer = 0

                self.dt = self.clock.tick(self.fps) / 1000  # Control frame rate to match the video's fps

            self.show_end_screen(screen)  # Show end screen when the video is finished

    def show_end_screen(self, screen):
        # Fill screen with white and display end message
        screen.blit(self.bg_image, (0, 0))
        pygame.display.update()

        # Wait for Enter key to continue
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        g_state_manager.Change("Tutorial", {})
                        waiting = False
    def update(self, dt, events):
        # Handle global events (e.g., quit)
        pass
    
    def Exit(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.set_volume(1/1.7)
       
    def cleanup(self):
        pygame.mixer.music.stop()
        self.cap.release()
        pygame.quit()

