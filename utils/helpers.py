import pygame
import math

def draw_glow_rect(surface, rect, glow_color, radius=10, steps=15):
    """
    Draws a soft glow effect around a rectangle.

    Args:
        surface: The pygame.Surface to draw on.
        rect: The pygame.Rect to draw the glow around.
        glow_color: The RGB color of the glow.
        radius: The maximum size of the glow effect.
        steps: The number of layers for the glow. More steps = smoother glow.
    """
    for i in range(steps, 0, -1):
        alpha = int(255 * (i / steps) ** 2)  # Use a squared falloff for a softer edge
        if alpha < 5: continue # Skip very faint layers

        glow_surf = pygame.Surface((rect.width + radius * 2, rect.height + radius * 2), pygame.SRCALPHA)
        glow_rect = glow_surf.get_rect()
        
        # Draw a rounded rectangle onto the glow surface
        pygame.draw.rect(glow_surf, (*glow_color, alpha // steps), glow_rect, border_radius=radius)

        # Blit the blurred glow surface, centering it on the original rect
        surface.blit(glow_surf, (rect.centerx - glow_rect.width // 2, rect.centery - glow_rect.height // 2))


class AnimationTimer:
    """A helper class to manage the state of a timed animation."""
    def __init__(self, duration_ms):
        self.duration = duration_ms
        self.start_time = 0
        self.is_running = False

    def start(self):
        """Starts the animation timer."""
        self.start_time = pygame.time.get_ticks()
        self.is_running = True

    def get_progress(self) -> float:
        """
        Returns the animation's progress as a value from 0.0 to 1.0.
        Stops the animation and returns 1.0 if the duration has passed.
        """
        if not self.is_running:
            return 0.0
        
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.is_running = False
            return 1.0
        
        return elapsed / self.duration