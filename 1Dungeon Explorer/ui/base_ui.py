"""
Base UI components and utilities shared across the application.
"""

import pygame
from typing import List
from config.constants import *

class Button:
    """Generic button UI component."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
        self.clicked = False
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events. Returns True if button was clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
        return False
    
    def draw(self, surface: pygame.Surface):
        """Draw the button to the surface."""
        if self.clicked:
            color = COLOR_BUTTON_ACTIVE
        elif self.hovered:
            color = COLOR_BUTTON_HOVER
        else:
            color = COLOR_BUTTON_NORMAL
        
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, COLOR_BLACK, self.rect, 2)
        
        text_surf = self.font.render(self.text, True, COLOR_WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class TextInput:
    """Text input field UI component."""
    
    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font.Font, max_length: int = 20):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.max_length = max_length
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events. Returns True if Enter was pressed."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            elif len(self.text) < self.max_length:
                char = event.unicode
                if char.isalpha() or char == " ":
                    self.text += char
        return False
    
    def update(self, dt: float):
        """Update cursor blinking."""
        self.cursor_timer += dt
        if self.cursor_timer >= 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, surface: pygame.Surface):
        """Draw the text input field."""
        pygame.draw.rect(surface, COLOR_TEXT_INPUT, self.rect)
        pygame.draw.rect(surface, COLOR_TEXT_INPUT_BORDER, self.rect, 2)
        
        text_surf = self.font.render(self.text, True, COLOR_BLACK)
        text_rect = text_surf.get_rect(left=self.rect.left + 5, centery=self.rect.centery)
        surface.blit(text_surf, text_rect)
        
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            cursor_y = self.rect.centery
            pygame.draw.line(surface, COLOR_BLACK, 
                           (cursor_x, cursor_y - 10), (cursor_x, cursor_y + 10), 2)

# --- UI Utility Functions ---

def wrap_text(text: str, max_width: int, font: pygame.font.Font) -> List[str]:
    """Wrap text to fit within max_width."""
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        test_width = font.size(test_line)[0]
        
        if test_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines

def draw_outlined_box(surface: pygame.Surface, rect: pygame.Rect, 
                     fill_color: tuple, border_color: tuple, border_width: int = 2):
    """Draw a box with fill and border."""
    pygame.draw.rect(surface, fill_color, rect)
    pygame.draw.rect(surface, border_color, rect, border_width)

def draw_separator_line(surface: pygame.Surface, x: int, y1: int, y2: int, color: tuple = COLOR_WHITE, width: int = 2):
    """Draw a vertical separator line."""
    pygame.draw.line(surface, color, (x, y1), (x, y2), width)

def center_text(surface: pygame.Surface, text: str, font: pygame.font.Font, 
                color: tuple, y: int, x: int = None):
    """Draw centered text. If x is None, centers horizontally on surface."""
    text_surf = font.render(text, True, color)
    if x is None:
        x = surface.get_width() // 2
    text_rect = text_surf.get_rect(centerx=x, y=y)
    surface.blit(text_surf, text_rect)
    return text_rect

def create_highlight_rect(x: int, y: int, width: int, height: int, 
                         color: tuple = COLOR_SELECTED_ITEM) -> pygame.Rect:
    """Create a highlight rectangle for selected items."""
    return pygame.Rect(x - 5, y - 5, width, height)

def draw_progress_bar(surface: pygame.Surface, x: int, y: int, width: int, height: int,
                     current: int, maximum: int, 
                     fill_color: tuple = COLOR_GREEN, bg_color: tuple = COLOR_BAR_BG):
    """Draw a progress bar."""
    # Background
    pygame.draw.rect(surface, bg_color, (x, y, width, height))
    
    # Fill
    if maximum > 0:
        fill_ratio = min(current / maximum, 1.0)
        fill_width = int(width * fill_ratio)
        fill_color_actual = COLOR_RED if current > maximum else fill_color
        pygame.draw.rect(surface, fill_color_actual, (x, y, fill_width, height))

class SelectionList:
    """Generic selection list component."""
    
    def __init__(self, x: int, y: int, width: int, font: pygame.font.Font):
        self.x = x
        self.y = y
        self.width = width
        self.font = font
        self.selected_index = 0
        self.items = []
        self.item_height = 50
    
    def set_items(self, items: List[str]):
        """Set the list of items."""
        self.items = items
        self.selected_index = 0
    
    def handle_navigation(self, event: pygame.event.Event) -> bool:
        """Handle up/down navigation. Returns True if selection changed."""
        if event.type == pygame.KEYDOWN and self.items:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
                return True
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
                return True
        return False
    
    def get_selected_item(self) -> str:
        """Get the currently selected item."""
        if self.items and 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None
    
    def draw(self, surface: pygame.Surface, additional_info: dict = None):
        """Draw the selection list. additional_info can contain extra text per item."""
        current_y = self.y
        
        for i, item in enumerate(self.items):
            # Highlight selected item
            if i == self.selected_index:
                highlight_rect = create_highlight_rect(self.x, current_y, self.width - 30, 40)
                pygame.draw.rect(surface, COLOR_SELECTED_ITEM, highlight_rect)
                pygame.draw.rect(surface, COLOR_WHITE, highlight_rect, 2)
            
            # Item text color
            color = COLOR_BLACK if i == self.selected_index else COLOR_WHITE
            
            # Main item text
            item_surf = self.font.render(item, True, color)
            surface.blit(item_surf, (self.x, current_y))
            
            # Additional info if provided
            if additional_info and item in additional_info:
                info_text = additional_info[item]
                info_surf = self.font.render(info_text, True, color)
                surface.blit(info_surf, (self.x, current_y + 25))
            
            current_y += self.item_height