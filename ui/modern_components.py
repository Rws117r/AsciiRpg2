"""
Modern UI Component Library
This file contains a collection of reusable, modern-looking UI components for Pygame.
"""

import pygame
from typing import Dict, List, Optional, Any, Callable

# --- Core Theme and Layout ---

class ModernUITheme:
    """Defines the color palette for all modern UI components."""
    # Primary Colors
    SURFACE_PRIMARY = (23, 24, 28)    # Dark background
    SURFACE_SECONDARY = (38, 40, 46)  # Lighter cards, inputs
    TEXT_PRIMARY = (230, 230, 230)    # Main text
    TEXT_SECONDARY = (160, 160, 160)  # Dimmer text
    TEXT_ACCENT = (76, 175, 80)       # Green for titles, highlights

    # Interactive States
    INTERACTIVE_NORMAL = (54, 57, 63) # Buttons, list items
    INTERACTIVE_HOVER = (64, 68, 75)
    INTERACTIVE_ACTIVE = (88, 101, 242) # Blue for active/selected
    
    # Semantic Colors
    SUCCESS = (76, 175, 80)
    ERROR = (244, 67, 54)
    WARNING = (255, 193, 7)
    
    # Border and Shadow
    BORDER = (64, 68, 75)
    SHADOW = (10, 10, 10, 100)

class ResponsiveLayout:
    """Manages responsive design breakpoints and font sizes."""
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Define breakpoints
        if screen_width < 800:
            self.layout_mode = 'mobile'
            self.columns = 1
            self.margin = 15
            self.gutter = 10
            self.font_sizes = {'title': 28, 'heading': 22, 'body': 16, 'small': 12}
        elif screen_width < 1280:
            self.layout_mode = 'tablet'
            self.columns = 2
            self.margin = 30
            self.gutter = 20
            self.font_sizes = {'title': 36, 'heading': 26, 'body': 18, 'small': 14}
        else:
            self.layout_mode = 'desktop'
            self.columns = 3
            self.margin = 50
            self.gutter = 30
            self.font_sizes = {'title': 48, 'heading': 32, 'body': 20, 'small': 16}
            
        self.column_width = (screen_width - (self.margin * 2) - (self.gutter * (self.columns - 1))) / self.columns
        self.content_height = screen_height - (self.margin * 2)

    def get_fonts(self, font_file: str) -> Dict[str, pygame.font.Font]:
        """Creates and returns a dictionary of Pygame fonts."""
        fonts = {}
        for name, size in self.font_sizes.items():
            try:
                fonts[name] = pygame.font.Font(font_file, size)
            except FileNotFoundError:
                print(f"Warning: Font file '{font_file}' not found. Using default font.")
                fonts[name] = pygame.font.Font(None, size)
        return fonts

# --- UI Components ---

class ModernNotificationManager:
    """Displays temporary, non-blocking notifications."""
    def __init__(self, screen_width: int):
        self.screen_width = screen_width
        self.notifications = []
        try:
            self.font = pygame.font.Font(None, 20)
        except:
            self.font = pygame.font.Font(None, 24)

    def add_notification(self, text: str, n_type: str = 'info', duration: float = 3.0):
        color_map = {
            'info': ModernUITheme.INTERACTIVE_ACTIVE,
            'success': ModernUITheme.SUCCESS,
            'error': ModernUITheme.ERROR,
            'warning': ModernUITheme.WARNING
        }
        self.notifications.append({
            'text': text, 'color': color_map.get(n_type, ModernUITheme.TEXT_SECONDARY),
            'alpha': 255, 'duration': duration, 'start_time': pygame.time.get_ticks()
        })

    def update(self, dt: float):
        for n in self.notifications[:]:
            elapsed = (pygame.time.get_ticks() - n['start_time']) / 1000.0
            if elapsed > n['duration']:
                n['alpha'] -= 255 * dt * 2 # Fade out
                if n['alpha'] <= 0:
                    self.notifications.remove(n)

    def draw(self, surface: pygame.Surface):
        y_pos = 20
        for n in self.notifications:
            text_surf = self.font.render(n['text'], True, ModernUITheme.TEXT_PRIMARY)
            bg_rect = pygame.Rect(0, 0, text_surf.get_width() + 20, text_surf.get_height() + 10)
            bg_rect.centerx = self.screen_width / 2
            bg_rect.y = y_pos
            
            bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surf.fill((*n['color'], int(n['alpha'])))
            
            surface.blit(bg_surf, bg_rect)
            surface.blit(text_surf, (bg_rect.x + 10, bg_rect.y + 5))
            y_pos += bg_rect.height + 10

class InfoCard:
    """A card for displaying formatted information."""
    def __init__(self, x, y, width, title, description, fonts, expandable=True):
        self.rect = pygame.Rect(x, y, width, 100) # Height is dynamic
        self.title = title
        self.description = description
        self.fonts = fonts
        self.is_expanded = not expandable
        self.expandable = expandable
        self._render_text()

    def _render_text(self):
        """ Wraps both title and description text and recalculates card height. """
        padding = 20
        # Wrap title text
        self.title_surfs = self._wrap_text(self.title, self.fonts['heading'], ModernUITheme.TEXT_ACCENT, self.rect.width - padding)
        
        # Wrap description text
        self.desc_surfs = self._wrap_text(self.description, self.fonts['body'], ModernUITheme.TEXT_PRIMARY, self.rect.width - padding)
        
        # Calculate height needed for all text surfaces
        title_height = sum(s.get_height() for s in self.title_surfs)
        desc_height = sum(s.get_height() for s in self.desc_surfs) if self.is_expanded else 0
        
        # Update the card's main rect height with appropriate padding
        if self.is_expanded and desc_height > 0:
            padding += 5  # Add padding between title and description
        
        self.rect.height = title_height + desc_height + padding

    # --- TEXT WRAPPING FIX IS HERE ---
    def _wrap_text(self, text, font, color, max_width):
        """ A generic text wrapper that correctly wraps long lines. """
        lines = []
        # Process each line from the input text (e.g., text with \n)
        for line in text.splitlines():
            words = line.split(' ')
            current_line = ""
            for word in words:
                # Test if adding the new word exceeds the width
                test_line = current_line + word + " "
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    # The line is full. Render it and start a new one.
                    lines.append(font.render(current_line.strip(), True, color))
                    current_line = word + " "
            # Add the last remaining line
            if current_line:
                lines.append(font.render(current_line.strip(), True, color))
        return lines

    def draw(self, surface: pygame.Surface):
        """Draws the card by first rendering to a local surface to ensure correct clipping."""
        card_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(card_surface, ModernUITheme.SURFACE_SECONDARY, card_surface.get_rect(), border_radius=8)

        y_offset = 10
        # Draw each line of the wrapped title
        for title_surf in self.title_surfs:
            card_surface.blit(title_surf, (10, y_offset))
            y_offset += title_surf.get_height()
        
        # Draw each line of the wrapped description
        if self.is_expanded:
            y_offset += 5 # Padding between title and description
            for line_surf in self.desc_surfs:
                card_surface.blit(line_surf, (10, y_offset))
                y_offset += line_surf.get_height()
        
        # Blit the final composed card onto the main screen
        surface.blit(card_surface, self.rect.topleft)
    
    def handle_event(self, event):
        if self.expandable and event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.is_expanded = not self.is_expanded
            self._render_text() # Recalculate height on expand/collapse
            return True
        return False

class ModernButton:
    """A stylish, interactive button."""
    def __init__(self, rect, text, font, variant='primary', callback=None):
        self.rect = rect
        self.text = text
        self.font = font
        self.callback = callback
        self.variant = variant
        self.state = 'normal' # normal, hover, active

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.state = 'hover'
            else:
                self.state = 'normal'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = 'active'
                if self.callback:
                    self.callback()
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.state == 'active':
                self.state = 'hover' if self.rect.collidepoint(event.pos) else 'normal'
        return False

    def draw(self, surface):
        color = ModernUITheme.INTERACTIVE_NORMAL
        if self.state == 'hover':
            color = ModernUITheme.INTERACTIVE_HOVER
        elif self.state == 'active':
            color = ModernUITheme.INTERACTIVE_ACTIVE
        
        if self.variant == 'secondary':
            pygame.draw.rect(surface, color, self.rect, 2, border_radius=8)
            text_color = ModernUITheme.TEXT_PRIMARY
        else: # primary
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            text_color = ModernUITheme.TEXT_PRIMARY
        
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class TextInput:
    """A component for user text input."""
    def __init__(self, rect, fonts, placeholder="", initial_text=""):
        self.rect = rect
        self.fonts = fonts
        self.placeholder = placeholder
        self.text = initial_text
        self.is_active = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_active = self.rect.collidepoint(event.pos)
        if self.is_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.is_active = False
            else:
                self.text += event.unicode
            return True
        return False

    def draw(self, surface):
        self.cursor_timer = (self.cursor_timer + 1) % 60
        self.cursor_visible = self.cursor_timer < 30

        bg_color = ModernUITheme.INTERACTIVE_ACTIVE if self.is_active else ModernUITheme.SURFACE_SECONDARY
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, ModernUITheme.BORDER, self.rect, 2, border_radius=8)

        display_text = self.text if self.text else self.placeholder
        text_color = ModernUITheme.TEXT_PRIMARY if self.text else ModernUITheme.TEXT_SECONDARY
        text_surf = self.fonts['body'].render(display_text, True, text_color)
        
        surface.blit(text_surf, (self.rect.x + 10, self.rect.centery - text_surf.get_height() // 2))

        if self.is_active and self.cursor_visible:
            cursor_x = self.rect.x + 10 + self.fonts['body'].size(self.text)[0]
            cursor_y1 = self.rect.centery - self.fonts['body'].get_height() // 2
            cursor_y2 = self.rect.centery + self.fonts['body'].get_height() // 2
            pygame.draw.line(surface, ModernUITheme.TEXT_PRIMARY, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)

class StatDisplay:
    """Displays a single stat with its name and value."""
    def __init__(self, rect, name, value, fonts):
        self.rect = rect
        self.name = name
        self.value = value
        self.fonts = fonts

    def draw(self, surface):
        name_surf = self.fonts['body'].render(f"{self.name}:", True, ModernUITheme.TEXT_SECONDARY)
        value_surf = self.fonts['heading'].render(str(self.value), True, ModernUITheme.TEXT_PRIMARY)
        
        surface.blit(name_surf, (self.rect.x, self.rect.centery - name_surf.get_height() // 2))
        surface.blit(value_surf, (self.rect.right - value_surf.get_width(), self.rect.centery - value_surf.get_height() // 2))

class AdaptiveList:
    """A scrollable list that adapts its layout and supports multi-selection."""
    def __init__(self, rect, items, fonts, multi_select=False, max_selection=1):
        self.rect = rect
        self.items = items
        self.fonts = fonts
        self.multi_select = multi_select
        self.max_selection = max_selection if multi_select else 1
        self.selected_indices = []
        self.on_selection_changed = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            relative_y = event.pos[1] - self.rect.y
            item_height = self.fonts['body'].get_height() + 10
            index = int(relative_y // item_height)
            
            if 0 <= index < len(self.items):
                if self.multi_select:
                    if index in self.selected_indices:
                        self.selected_indices.remove(index)
                    elif len(self.selected_indices) < self.max_selection:
                        self.selected_indices.append(index)
                else:
                    self.selected_indices = [index]
                
                if self.on_selection_changed:
                    selected_items = [self.items[i] for i in self.selected_indices]
                    self.on_selection_changed(selected_items)
                return True
        return False
        
    def select_item(self, index):
        if 0 <= index < len(self.items):
            if self.multi_select:
                if index not in self.selected_indices and len(self.selected_indices) < self.max_selection:
                    self.selected_indices.append(index)
            else:
                self.selected_indices = [index]
            
            if self.on_selection_changed:
                selected_items = [self.items[i] for i in self.selected_indices]
                self.on_selection_changed(selected_items)

    def draw(self, surface):
        pygame.draw.rect(surface, ModernUITheme.SURFACE_SECONDARY, self.rect, border_radius=8)
        
        # Save the current clipping region
        original_clip = surface.get_clip()
        
        # Set the clipping region to the list's rectangle to prevent overflow
        surface.set_clip(self.rect)

        y_pos = self.rect.y + 5
        item_height = self.fonts['body'].get_height() + 10
        for i, item_text in enumerate(self.items):
            item_rect = pygame.Rect(self.rect.x, y_pos, self.rect.width, item_height)
            if i in self.selected_indices:
                pygame.draw.rect(surface, ModernUITheme.INTERACTIVE_ACTIVE, item_rect, border_radius=6)
            
            text_surf = self.fonts['body'].render(item_text, True, ModernUITheme.TEXT_PRIMARY)
            surface.blit(text_surf, (self.rect.x + 10, y_pos + 5))
            y_pos += item_height

        # Restore the original clipping region
        surface.set_clip(original_clip)

class ModernInventoryGrid:
    """A grid for displaying inventory items."""
    def __init__(self, rect, fonts, grid_size=(5, 8)):
        self.rect = rect
        self.fonts = fonts
        self.grid_cols, self.grid_rows = grid_size
        self.cell_size = min(rect.width // self.grid_cols, rect.height // self.grid_rows)
        self.items = {} # (col, row): InventoryItem
        self.hovered_slot = None

    def add_item(self, inv_item):
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                if (c, r) not in self.items:
                    self.items[(c, r)] = inv_item
                    return

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                rel_x, rel_y = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
                col, row = rel_x // self.cell_size, rel_y // self.cell_size
                if 0 <= col < self.grid_cols and 0 <= row < self.grid_rows:
                    self.hovered_slot = (col, row)
                else:
                    self.hovered_slot = None
            else:
                self.hovered_slot = None

    def draw(self, surface):
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell_rect = pygame.Rect(
                    self.rect.x + c * self.cell_size,
                    self.rect.y + r * self.cell_size,
                    self.cell_size, self.cell_size
                )
                bg_color = ModernUITheme.SURFACE_SECONDARY
                if (c, r) == self.hovered_slot:
                    bg_color = ModernUITheme.INTERACTIVE_HOVER
                
                pygame.draw.rect(surface, bg_color, cell_rect, border_radius=4)
                pygame.draw.rect(surface, ModernUITheme.BORDER, cell_rect, 1, border_radius=4)

                if (c, r) in self.items:
                    pygame.draw.circle(surface, ModernUITheme.SUCCESS, cell_rect.center, 10)

class SmartTooltip:
    """A tooltip that positions itself intelligently."""
    def __init__(self, anchor_rect, content, fonts):
        self.anchor_rect = anchor_rect
        self.content = content
        self.fonts = fonts
        self.visible = False
        self._build_surface()

    def _build_surface(self):
        title_surf = self.fonts['body'].render(self.content.get('title', ''), True, ModernUITheme.TEXT_ACCENT)
        subtitle_surf = self.fonts['small'].render(self.content.get('subtitle', ''), True, ModernUITheme.TEXT_SECONDARY)
        desc_surf = self.fonts['small'].render(self.content.get('description', ''), True, ModernUITheme.TEXT_PRIMARY)
        
        width = max(title_surf.get_width(), subtitle_surf.get_width(), desc_surf.get_width()) + 20
        height = title_surf.get_height() + subtitle_surf.get_height() + desc_surf.get_height() + 20
        
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((*ModernUITheme.SURFACE_PRIMARY, 220))
        
        self.surface.blit(title_surf, (10, 5))
        self.surface.blit(subtitle_surf, (10, 10 + title_surf.get_height()))
        self.surface.blit(desc_surf, (10, 15 + title_surf.get_height() + subtitle_surf.get_height()))
        
        self.rect = self.surface.get_rect()

    def show(self):
        self.visible = True

    def draw(self, surface):
        if not self.visible: return
        self.rect.topleft = self.anchor_rect.bottomright
        if self.rect.right > surface.get_width():
            self.rect.right = self.anchor_rect.left
        if self.rect.bottom > surface.get_height():
            self.rect.bottom = self.anchor_rect.top
        
        surface.blit(self.surface, self.rect)