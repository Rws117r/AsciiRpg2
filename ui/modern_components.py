"""
Modern UI Component Library
This file contains a collection of reusable, modern-looking UI components for Pygame,
built according to the "Utilitarian-Symbolic" design system.
"""

import pygame
import math
from typing import Dict, List, Optional, Any, Callable
from utils.helpers import draw_glow_rect, AnimationTimer

# --- THEME AND DESIGN SYSTEM ---

class ModernUITheme:
    """A dynamic theme class that holds the active color palette."""
    def __init__(self, theme_name: str = 'neutral'):
        self.DARK_CATHODE = (26, 29, 33)
        self.LIGHT_CATHODE = (42, 47, 54)
        self.PARCHMENT_MAIN = (234, 230, 221)
        self.PARCHMENT_DIM = (168, 162, 148)
        self.ACCENT_GOLD = (255, 199, 89)
        self.SEMANTIC_SUCCESS = (74, 222, 128)
        self.SEMANTIC_ERROR = (248, 113, 113)
        self.BORDER_DIM = self.PARCHMENT_DIM
        self.BORDER_FOCUSED = self.ACCENT_GOLD
        self.set_theme(theme_name)

    def set_theme(self, theme_name: str):
        """Sets the interactive and accent colors based on the chosen theme."""
        if theme_name == 'lawful':
            self.INTERACTIVE = (96, 165, 250)
            self.INTERACTIVE_GLOW = (245, 158, 11)
        elif theme_name == 'chaotic':
            self.INTERACTIVE = (239, 68, 68)
            self.INTERACTIVE_GLOW = (217, 70, 239)
        else: # Default to neutral
            self.INTERACTIVE = (34, 197, 94)
            self.INTERACTIVE_GLOW = (109, 40, 217)

class Typography:
    """Manages the dual-font system and typographic scale."""
    def __init__(self, slab_font_path: str, mono_font_path: str):
        self.styles = {}
        scale = {
            'TITLE_MAIN':     {'family': slab_font_path, 'weight': 'bold', 'size': 48},
            'HEADING_CARD':   {'family': slab_font_path, 'weight': 'regular', 'size': 32},
            'LABEL_UI':       {'family': slab_font_path, 'weight': 'bold', 'size': 20},
            'BODY_TEXT':      {'family': slab_font_path, 'weight': 'regular', 'size': 20},
            'BODY_SMALL':     {'family': slab_font_path, 'weight': 'regular', 'size': 16},
            'MONO_LARGE':     {'family': mono_font_path, 'weight': 'regular', 'size': 24},
            'MONO_BODY':      {'family': mono_font_path, 'weight': 'regular', 'size': 18},
            'MONO_LABEL':     {'family': mono_font_path, 'weight': 'bold', 'size': 18},
        }
        for name, spec in scale.items():
            try:
                font = pygame.font.Font(spec['family'], spec['size'])
                if spec['weight'] == 'bold': font.set_bold(True)
                self.styles[name] = font
            except FileNotFoundError:
                print(f"Warning: Font file '{spec['family']}' not found. Using default font.")
                font = pygame.font.Font(None, spec['size'])
                if spec['weight'] == 'bold': font.set_bold(True)
                self.styles[name] = font

class LayoutSystem:
    """Manages grid, spacing, and layout dimensions."""
    def __init__(self, screen_width: int, screen_height: int):
        self.BASE_UNIT = 8
        self.screen_width, self.screen_height = screen_width, screen_height
        self.margin = 6 * self.BASE_UNIT
        self.gutter = 8 * self.BASE_UNIT
        available_width = screen_width - (self.margin * 2)
        self.left_column_width = int(available_width * 0.60)
        self.right_column_width = int(available_width * 0.35)

# --- UI COMPONENTS ---

class ModernNotificationManager:
    """Displays temporary, non-blocking notifications."""
    def __init__(self, screen_width: int, fonts: Dict[str, pygame.font.Font], theme: ModernUITheme):
        self.screen_width = screen_width
        self.notifications = []
        self.font = fonts['BODY_SMALL']
        self.theme = theme

    def add_notification(self, text: str, n_type: str = 'info', duration: float = 3.0):
        color_map = {'success': self.theme.SEMANTIC_SUCCESS, 'error': self.theme.SEMANTIC_ERROR}
        self.notifications.append({
            'text': text, 'color': color_map.get(n_type, self.theme.INTERACTIVE),
            'alpha': 255, 'duration': duration, 'start_time': pygame.time.get_ticks()})

    def update(self):
        current_time = pygame.time.get_ticks()
        for n in self.notifications[:]:
            elapsed = (current_time - n['start_time']) / 1000.0
            if elapsed > n['duration']:
                fade_progress = (elapsed - n['duration']) / 0.5
                n['alpha'] = max(0, 255 * (1 - fade_progress))
                if n['alpha'] == 0: self.notifications.remove(n)

    def draw(self, surface: pygame.Surface):
        y_pos = 24
        for n in self.notifications:
            text_surf = self.font.render(n['text'], True, self.theme.DARK_CATHODE)
            bg_rect = pygame.Rect(0, 0, text_surf.get_width() + 32, text_surf.get_height() + 16)
            bg_rect.centerx = self.screen_width / 2
            bg_rect.y = y_pos
            bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            color = n['color']
            bg_surf.fill((*color, int(n['alpha'])))
            surface.blit(bg_surf, bg_rect)
            text_rect = text_surf.get_rect(center=bg_rect.center)
            surface.blit(text_surf, text_rect)
            y_pos += bg_rect.height + 8
        self.update()


class ModernButton:
    """A button updated for the 'Utilitarian-Symbolic' system."""
    def __init__(self, rect, text, font_style, theme, variant='primary', callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font_style
        self.theme = theme
        self.callback = callback
        self.variant = variant
        self.state = 'normal'

    def handle_event(self, event):
        if event.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return False
            
        if event.type == pygame.MOUSEMOTION:
            self.state = 'hover' if self.rect.collidepoint(event.pos) else 'normal'
        elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if event.button == 1:
                self.state = 'active'
                if self.callback: self.callback()
                return True
        elif event.type == pygame.MOUSEBUTTONUP and self.state == 'active':
            self.state = 'hover' if self.rect.collidepoint(event.pos) else 'normal'
        return False

    def draw(self, surface):
        if self.variant == 'primary':
            bg_color = self.theme.INTERACTIVE
            text_color = self.theme.DARK_CATHODE
            if self.state == 'hover': bg_color = tuple(min(255, c + 20) for c in self.theme.INTERACTIVE)
            pygame.draw.rect(surface, bg_color, self.rect, border_radius=6)
        else: # secondary
            text_color = self.theme.PARCHMENT_DIM
            if self.state == 'hover':
                text_color = self.theme.PARCHMENT_MAIN
                pygame.draw.rect(surface, self.theme.LIGHT_CATHODE, self.rect, border_radius=6)
            pygame.draw.rect(surface, self.theme.BORDER_DIM, self.rect, 2, border_radius=6)
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class AdaptiveList:
    """A list that now correctly supports scrolling and animations."""
    def __init__(self, rect, items, fonts, theme, multi_select=False, max_selection=1):
        self.rect = pygame.Rect(rect)
        self.items = items
        self.fonts = fonts
        self.theme = theme
        self.multi_select = multi_select
        self.max_selection = max_selection
        self.selected_indices = []
        self.on_selection_changed = None
        self.item_height = self.fonts['BODY_TEXT'].get_height() + 16
        self.hovered_index = -1
        self.selection_anim = AnimationTimer(200)

        # Scrolling attributes
        self.scroll_offset = 0
        self.scroll_speed = 40
        self.content_height = len(self.items) * self.item_height
        self.max_scroll = self.content_height - self.rect.height
        if self.max_scroll < 0: self.max_scroll = 0

    def handle_event(self, event):
        # Scrolling logic
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_offset += event.y * self.scroll_speed
                self.scroll_offset = max(-self.max_scroll, min(0, self.scroll_offset))
                return True
        
        # Hover logic
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                relative_y = event.pos[1] - self.rect.y - self.scroll_offset
                self.hovered_index = int(relative_y // self.item_height)
                if not (0 <= self.hovered_index < len(self.items)): self.hovered_index = -1
            else: self.hovered_index = -1
        
        # Click logic
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and event.button == 1 and self.hovered_index != -1:
                index = self.hovered_index
                if self.multi_select:
                    if index in self.selected_indices: self.selected_indices.remove(index)
                    elif len(self.selected_indices) < self.max_selection: self.selected_indices.append(index)
                else: self.selected_indices = [index]
                
                self.selection_anim.start()
                if self.on_selection_changed: self.on_selection_changed([self.items[i] for i in self.selected_indices])
                return True
        return False

    def select_item(self, index):
        if 0 <= index < len(self.items):
            self.selected_indices = [index]
            self.selection_anim.start()
            if self.on_selection_changed: self.on_selection_changed([self.items[i] for i in self.selected_indices])

    def draw(self, surface):
        pygame.draw.rect(surface, self.theme.LIGHT_CATHODE, self.rect, border_radius=8)
        
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            track_width = 8
            track_height = self.rect.height - 16
            track_x = self.rect.right - track_width - 8
            track_rect = pygame.Rect(track_x, self.rect.y + 8, track_width, track_height)
            
            thumb_height = max(20, (self.rect.height / self.content_height) * track_height)
            scroll_percentage = (-self.scroll_offset) / self.max_scroll
            thumb_y = track_rect.y + scroll_percentage * (track_height - thumb_height)
            thumb_rect = pygame.Rect(track_x, thumb_y, track_width, thumb_height)

            pygame.draw.rect(surface, self.theme.DARK_CATHODE, track_rect, border_radius=4)
            pygame.draw.rect(surface, self.theme.PARCHMENT_DIM, thumb_rect, border_radius=4)

        # Set clipping area for list items
        original_clip = surface.get_clip()
        list_items_area = self.rect.inflate(-16, -4)
        surface.set_clip(list_items_area)

        y_pos = self.rect.y + 8 + self.scroll_offset
        for i, item_text in enumerate(self.items):
            item_rect = pygame.Rect(self.rect.x + 8, y_pos, self.rect.width - 24, self.item_height - 8)
            
            if item_rect.bottom > self.rect.top and item_rect.top < self.rect.bottom:
                if i == self.hovered_index and i not in self.selected_indices:
                    draw_glow_rect(surface, item_rect, self.theme.INTERACTIVE_GLOW, radius=8, steps=10)

                if i in self.selected_indices:
                    color = self.theme.INTERACTIVE
                    if self.selection_anim.is_running:
                        alpha = int(255 * self.selection_anim.get_progress())
                        selection_surf = pygame.Surface(item_rect.size, pygame.SRCALPHA)
                        pygame.draw.rect(selection_surf, (*color, alpha), selection_surf.get_rect(), border_radius=6)
                        surface.blit(selection_surf, item_rect.topleft)
                    else:
                        pygame.draw.rect(surface, color, item_rect, border_radius=6)
                
                text_color = self.theme.DARK_CATHODE if i in self.selected_indices else self.theme.PARCHMENT_MAIN
                text_surf = self.fonts['BODY_TEXT'].render(item_text, True, text_color)
                surface.blit(text_surf, (self.rect.x + 24, item_rect.centery - text_surf.get_height() // 2))
            
            y_pos += self.item_height
        
        surface.set_clip(original_clip)

class TextInput:
    """A text input with a clear focus state."""
    def __init__(self, rect, fonts, theme):
        self.rect = pygame.Rect(rect)
        self.fonts = fonts
        self.theme = theme
        self.text = ""
        self.placeholder = ""
        self.is_active = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_active = self.rect.collidepoint(event.pos)
        if self.is_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            elif event.key not in (pygame.K_RETURN, pygame.K_ESCAPE):
                 self.text += event.unicode
            return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.theme.LIGHT_CATHODE, self.rect, border_radius=6)
        border_color = self.theme.BORDER_FOCUSED if self.is_active else self.theme.BORDER_DIM
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=6)

        display_text, text_color = (self.text, self.theme.PARCHMENT_MAIN) if self.text else (self.placeholder, self.theme.PARCHMENT_DIM)
        text_surf = self.fonts['BODY_TEXT'].render(display_text, True, text_color)
        surface.blit(text_surf, (self.rect.x + 16, self.rect.centery - text_surf.get_height() // 2))

        if self.is_active and (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = self.rect.x + 16 + self.fonts['BODY_TEXT'].size(self.text)[0]
            pygame.draw.line(surface, self.theme.ACCENT_GOLD, (cursor_x, self.rect.y + 8), (cursor_x, self.rect.bottom - 8), 2)

class InfoCard:
    """A container for information, styled with typography and negative space."""
    def __init__(self, rect, title, description, fonts, theme):
        self.rect = pygame.Rect(rect)
        self.title = title
        self.description = description
        self.fonts = fonts
        self.theme = theme
        self.padding = 24
        self._render_text()

    def _render_text(self):
        self.title_surfs = self._wrap_text(self.title, self.fonts['HEADING_CARD'], self.theme.PARCHMENT_MAIN, self.rect.width - (self.padding * 2))
        self.desc_surfs = self._wrap_text(self.description, self.fonts['BODY_TEXT'], self.theme.PARCHMENT_MAIN, self.rect.width - (self.padding * 2))
        title_h = sum(s.get_height() for s in self.title_surfs)
        desc_h = sum(s.get_height() for s in self.desc_surfs)
        self.rect.height = title_h + desc_h + (self.padding * 2) + (16 if desc_h > 0 else 0)

    def _wrap_text(self, text, font, color, max_width):
        lines = []
        for line in text.splitlines():
            words = line.split(' ')
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if font.size(test_line)[0] <= max_width: current_line = test_line
                else:
                    lines.append(font.render(current_line.strip(), True, color))
                    current_line = word + " "
            if current_line: lines.append(font.render(current_line.strip(), True, color))
        return lines

    def draw(self, surface):
        pygame.draw.rect(surface, self.theme.LIGHT_CATHODE, self.rect, border_radius=8)
        y_offset = self.rect.y + self.padding
        for surf in self.title_surfs:
            surface.blit(surf, (self.rect.x + self.padding, y_offset))
            y_offset += surf.get_height()
        y_offset += 16
        for surf in self.desc_surfs:
            surface.blit(surf, (self.rect.x + self.padding, y_offset))
            y_offset += surf.get_height()

class CharacterSummaryCard(InfoCard):
    """A specialized InfoCard for the diegetic Character Summary panel."""
    def _render_text(self):
        self.title_surf = self.fonts['HEADING_CARD'].render(self.title, True, self.theme.PARCHMENT_MAIN)
        self.lines = []
        
        temp_labels = [line.split('|')[0] for line in self.description.splitlines() if '|' in line]
        max_label_w = max(self.fonts['MONO_LABEL'].size(lbl)[0] for lbl in temp_labels) if temp_labels else 0
        value_max_width = self.rect.width - max_label_w - (self.padding * 2) - 16

        total_height = 0
        for line in self.description.splitlines():
            if not line.strip() or '|' not in line:
                self.lines.append(('', []))
                total_height += self.fonts['MONO_LABEL'].get_height() * 0.75
                continue
            
            label, value = line.split('|', 1)
            label_surf = self.fonts['MONO_LABEL'].render(label, True, self.theme.PARCHMENT_DIM)
            value_surfs = self._wrap_text(value, self.fonts['MONO_BODY'], self.theme.PARCHMENT_MAIN, value_max_width)
            self.lines.append((label_surf, value_surfs))
            
            total_height += max(label_surf.get_height(), sum(s.get_height() for s in value_surfs)) + 4
        
        self.max_label_width = max_label_w
        self.rect.height = self.title_surf.get_height() + total_height + (self.padding * 2) + 16

    def draw(self, surface):
        pygame.draw.rect(surface, self.theme.LIGHT_CATHODE, self.rect, border_radius=8)
        surface.blit(self.title_surf, (self.rect.x + self.padding, self.rect.y + self.padding))
        
        y_offset = self.rect.y + self.padding + self.title_surf.get_height() + 24
        
        for label_surf, value_surfs in self.lines:
            if not label_surf:
                y_offset += self.fonts['MONO_LABEL'].get_height() * 0.75
                continue

            surface.blit(label_surf, (self.rect.x + self.padding, y_offset))
            value_x = self.rect.x + self.padding + self.max_label_width + 16
            line_y = y_offset
            for value_surf in value_surfs:
                surface.blit(value_surf, (value_x, line_y))
                line_y += value_surf.get_height()
            
            y_offset += max(label_surf.get_height(), line_y - y_offset) + 4

class StatDisplay:
    """Displays a stat with the new typographic hierarchy."""
    def __init__(self, rect, name, value, fonts, theme):
        self.rect = pygame.Rect(rect)
        self.name = name
        self.value = value
        self.fonts = fonts
        self.theme = theme

    def draw(self, surface):
        name_surf = self.fonts['LABEL_UI'].render(f"{self.name}:", True, self.theme.PARCHMENT_DIM)
        value_surf = self.fonts['MONO_LARGE'].render(str(self.value), True, self.theme.PARCHMENT_MAIN)
        
        surface.blit(name_surf, (self.rect.x, self.rect.centery - name_surf.get_height() // 2))
        surface.blit(value_surf, (self.rect.right - value_surf.get_width(), self.rect.centery - value_surf.get_height() // 2))

class ModernInventoryGrid:
    """A grid for displaying inventory items, updated for the new theme."""
    def __init__(self, rect, fonts, theme, grid_size=(5, 8)):
        self.rect = pygame.Rect(rect)
        self.fonts = fonts
        self.theme = theme
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
                else: self.hovered_slot = None
            else: self.hovered_slot = None

    def draw(self, surface):
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell_rect = pygame.Rect(
                    self.rect.x + c * self.cell_size, self.rect.y + r * self.cell_size,
                    self.cell_size, self.cell_size
                )
                cell_rect.inflate_ip(-8, -8)
                
                bg_color = self.theme.DARK_CATHODE
                border_color = self.theme.BORDER_DIM
                if (c, r) == self.hovered_slot:
                    bg_color = self.theme.LIGHT_CATHODE
                    border_color = self.theme.ACCENT_GOLD
                
                pygame.draw.rect(surface, bg_color, cell_rect, border_radius=4)
                pygame.draw.rect(surface, border_color, cell_rect, 1, border_radius=4)

                if (c, r) in self.items:
                    item = self.items[(c, r)]
                    char = getattr(item.item, 'char', '?')
                    item_surf = self.fonts['MONO_LARGE'].render(char, True, self.theme.PARCHMENT_MAIN)
                    item_rect = item_surf.get_rect(center=cell_rect.center)
                    surface.blit(item_surf, item_rect)


class SmartTooltip:
    """A tooltip that positions itself intelligently, styled for the new theme."""
    def __init__(self, anchor_rect, content, fonts, theme):
        self.anchor_rect = anchor_rect
        self.content = content
        self.fonts = fonts
        self.theme = theme
        self.visible = False
        self._build_surface()

    def _build_surface(self):
        padding = 16
        title_surf = self.fonts['BODY_TEXT'].render(self.content.get('title', ''), True, self.theme.ACCENT_GOLD)
        subtitle_surf = self.fonts['BODY_SMALL'].render(self.content.get('subtitle', ''), True, self.theme.PARCHMENT_DIM)
        desc_surf = self.fonts['BODY_SMALL'].render(self.content.get('description', ''), True, self.theme.PARCHMENT_MAIN)
        
        width = max(title_surf.get_width(), subtitle_surf.get_width(), desc_surf.get_width()) + (padding * 2)
        height = title_surf.get_height() + subtitle_surf.get_height() + desc_surf.get_height() + (padding * 2) + 8
        
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((*self.theme.DARK_CATHODE, 240))
        
        y_offset = padding
        self.surface.blit(title_surf, (padding, y_offset))
        y_offset += title_surf.get_height() + 4
        self.surface.blit(subtitle_surf, (padding, y_offset))
        y_offset += subtitle_surf.get_height() + 8
        self.surface.blit(desc_surf, (padding, y_offset))
        
        self.rect = self.surface.get_rect()

    def show(self):
        self.visible = True

    def draw(self, surface):
        if not self.visible: return
        self.rect.topleft = self.anchor_rect.bottomright
        if self.rect.right > surface.get_width() - 16:
            self.rect.right = self.anchor_rect.left
        if self.rect.bottom > surface.get_height() - 16:
            self.rect.bottom = self.anchor_rect.top
        
        surface.blit(self.surface, self.rect)