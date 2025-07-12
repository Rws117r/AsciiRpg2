"""
Enhanced Modern UI Components
Implementing the responsive, minimalist UI system from your design plan.
This builds on your existing modular structure with modern UX principles.
"""

import pygame
import math
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

# Import your existing systems
from config.constants import *
from ui.base_ui import wrap_text
from data.items import GearItem
from data.calendar import get_world_calendar

class ModernUITheme:
    """Modern minimalist color scheme and styling."""
    
    # Enhanced color palette (building on your existing colors)
    SURFACE_PRIMARY = (20, 20, 20)        # Dark panels
    SURFACE_SECONDARY = (30, 30, 30)      # Slightly lighter panels
    SURFACE_ELEVATED = (40, 40, 40)       # Elevated elements
    
    TEXT_PRIMARY = COLOR_WHITE             # Main text
    TEXT_SECONDARY = (180, 180, 180)      # Secondary text
    TEXT_ACCENT = COLOR_GOLD              # Highlighted text
    TEXT_MUTED = (120, 120, 120)          # Disabled/muted text
    
    INTERACTIVE_NORMAL = (60, 60, 60)     # Normal interactive elements
    INTERACTIVE_HOVER = (80, 80, 80)      # Hovered elements
    INTERACTIVE_ACTIVE = COLOR_GOLD       # Active/selected elements
    
    BORDER_SUBTLE = (60, 60, 60)          # Subtle borders
    BORDER_STRONG = COLOR_WHITE           # Strong borders
    
    SUCCESS = (76, 175, 80)               # Success states
    WARNING = (255, 193, 7)               # Warning states  
    ERROR = (244, 67, 54)                 # Error states
    INFO = (33, 150, 243)                 # Information states
    
    # Spacing system (8px base unit)
    SPACING_XS = 4
    SPACING_SM = 8
    SPACING_MD = 16
    SPACING_LG = 24
    SPACING_XL = 32
    SPACING_XXL = 48

class ResponsiveLayout:
    """Responsive layout system that adapts to screen size."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Calculate scale factor
        self.scale_factor = max(0.8, min(1.5, screen_width / 1200))
        
        # Typography scale
        self.font_sizes = self._calculate_font_sizes()
        
        # Layout properties
        self.margin = max(16, int(32 * self.scale_factor))
        self.gutter = max(12, int(24 * self.scale_factor))
        
        # Determine layout mode
        if screen_width < 800:
            self.layout_mode = 'compact'
            self.columns = 1
        elif screen_width < 1200:
            self.layout_mode = 'normal'
            self.columns = 2
        else:
            self.layout_mode = 'spacious'
            self.columns = 3
        
        # Calculate content areas
        self.content_width = screen_width - (self.margin * 2)
        self.content_height = screen_height - (self.margin * 2)
        
        # Column calculations
        if self.columns > 1:
            self.column_width = (self.content_width - (self.gutter * (self.columns - 1))) // self.columns
        else:
            self.column_width = self.content_width
    
    def _calculate_font_sizes(self) -> Dict[str, int]:
        """Calculate responsive font sizes."""
        base_sizes = {
            'title': 28,
            'heading': 22,
            'subheading': 18,
            'body': 16,
            'small': 14,
            'caption': 12
        }
        
        return {
            name: max(10, int(size * self.scale_factor))
            for name, size in base_sizes.items()
        }
    
    def get_fonts(self, font_path: str) -> Dict[str, pygame.font.Font]:
        """Create font objects with responsive sizes."""
        return {
            name: pygame.font.Font(font_path, size)
            for name, size in self.font_sizes.items()
        }

class ModernCard:
    """Modern card component with elevation and clean styling."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 elevated: bool = True, padding: int = ModernUITheme.SPACING_MD):
        self.rect = pygame.Rect(x, y, width, height)
        self.elevated = elevated
        self.padding = padding
        self.content_rect = pygame.Rect(
            x + padding, y + padding, 
            width - 2 * padding, height - 2 * padding
        )
        
        # Visual properties
        self.border_radius = 8
        self.shadow_offset = 4 if elevated else 0
        
    def draw_background(self, surface: pygame.Surface):
        """Draw card background with shadow."""
        # Shadow
        if self.shadow_offset > 0:
            shadow_rect = self.rect.copy()
            shadow_rect.x += self.shadow_offset
            shadow_rect.y += self.shadow_offset
            shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 60))
            surface.blit(shadow_surface, shadow_rect)
        
        # Main card
        color = ModernUITheme.SURFACE_ELEVATED if self.elevated else ModernUITheme.SURFACE_PRIMARY
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, ModernUITheme.BORDER_SUBTLE, self.rect, 1)

class InfoCard(ModernCard):
    """Information card with progressive disclosure."""
    
    def __init__(self, x: int, y: int, width: int, title: str, content: str,
                 fonts: Dict[str, pygame.font.Font], expandable: bool = True):
        super().__init__(x, y, width, 100)  # Start with base height
        
        self.title = title
        self.content = content
        self.fonts = fonts
        self.expandable = expandable
        self.expanded = False
        self.hovered = False
        
        # Calculate content layout
        self.header_height = fonts['heading'].get_height() + ModernUITheme.SPACING_MD
        self.content_lines = self._wrap_text(content, fonts['body'], width - 2 * self.padding)
        self.preview_lines = self.content_lines[:2] if len(self.content_lines) > 2 else self.content_lines
        
        # Calculate heights
        self.collapsed_height = self.header_height + (fonts['body'].get_height() * len(self.preview_lines)) + ModernUITheme.SPACING_LG
        self.expanded_height = self.header_height + (fonts['body'].get_height() * len(self.content_lines)) + ModernUITheme.SPACING_LG
        
        # Update rect height
        self.update_height()
    
    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def update_height(self):
        """Update card height based on expanded state."""
        new_height = self.expanded_height if self.expanded else self.collapsed_height
        self.rect.height = new_height
        self.content_rect.height = new_height - 2 * self.padding
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events. Returns True if event was consumed."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.expandable:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                self.update_height()
                return True
        return False
    
    def draw(self, surface: pygame.Surface):
        """Draw the info card."""
        # Background with hover effect
        if self.hovered and self.expandable:
            hover_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            hover_surface.fill((*ModernUITheme.INTERACTIVE_HOVER, 30))
            surface.blit(hover_surface, self.rect)
        
        self.draw_background(surface)
        
        y_offset = self.content_rect.y
        
        # Title with accent color
        title_surf = self.fonts['heading'].render(self.title, True, ModernUITheme.TEXT_ACCENT)
        surface.blit(title_surf, (self.content_rect.x, y_offset))
        
        # Expand/collapse icon if expandable
        if self.expandable:
            icon = "▼" if self.expanded else "▶"
            icon_surf = self.fonts['body'].render(icon, True, ModernUITheme.TEXT_SECONDARY)
            icon_x = self.content_rect.right - icon_surf.get_width()
            surface.blit(icon_surf, (icon_x, y_offset))
        
        y_offset += self.fonts['heading'].get_height() + ModernUITheme.SPACING_SM
        
        # Content
        lines_to_show = self.content_lines if self.expanded else self.preview_lines
        for line in lines_to_show:
            line_surf = self.fonts['body'].render(line, True, ModernUITheme.TEXT_PRIMARY)
            surface.blit(line_surf, (self.content_rect.x, y_offset))
            y_offset += self.fonts['body'].get_height() + 2
        
        # Show "..." if content is truncated
        if not self.expanded and len(self.content_lines) > len(self.preview_lines):
            dots_surf = self.fonts['body'].render("...", True, ModernUITheme.TEXT_SECONDARY)
            surface.blit(dots_surf, (self.content_rect.x, y_offset))

class SmartTooltip:
    """Rich tooltip system with intelligent positioning."""
    
    def __init__(self, target_rect: pygame.Rect, content: Dict[str, Any], 
                 fonts: Dict[str, pygame.font.Font]):
        self.target_rect = target_rect
        self.content = content
        self.fonts = fonts
        self.visible = False
        self.rect = None
        
        # Tooltip configuration
        self.max_width = 400
        self.padding = ModernUITheme.SPACING_MD
        
        # Calculate tooltip size and position
        self._calculate_layout()
    
    def _calculate_layout(self):
        """Calculate tooltip size and optimal position."""
        lines = []
        total_height = 0
        max_width = 0
        
        # Title
        if 'title' in self.content:
            title_surf = self.fonts['heading'].render(self.content['title'], True, ModernUITheme.TEXT_ACCENT)
            lines.append(('title', title_surf))
            total_height += title_surf.get_height() + ModernUITheme.SPACING_SM
            max_width = max(max_width, title_surf.get_width())
        
        # Subtitle  
        if 'subtitle' in self.content:
            subtitle_surf = self.fonts['small'].render(self.content['subtitle'], True, ModernUITheme.TEXT_SECONDARY)
            lines.append(('subtitle', subtitle_surf))
            total_height += subtitle_surf.get_height() + ModernUITheme.SPACING_SM
            max_width = max(max_width, subtitle_surf.get_width())
        
        # Description
        if 'description' in self.content:
            desc_lines = wrap_text(self.content['description'], self.max_width - self.padding * 2, self.fonts['body'])
            for line in desc_lines:
                line_surf = self.fonts['body'].render(line, True, ModernUITheme.TEXT_PRIMARY)
                lines.append(('description', line_surf))
                total_height += line_surf.get_height() + 2
                max_width = max(max_width, line_surf.get_width())
        
        # Effects list
        if 'effects' in self.content and self.content['effects']:
            total_height += ModernUITheme.SPACING_SM
            for effect in self.content['effects']:
                effect_surf = self.fonts['small'].render(f"• {effect}", True, ModernUITheme.TEXT_PRIMARY)
                lines.append(('effect', effect_surf))
                total_height += effect_surf.get_height() + 2
                max_width = max(max_width, effect_surf.get_width())
        
        # Store layout info
        self.lines = lines
        self.tooltip_width = min(self.max_width, max_width + self.padding * 2)
        self.tooltip_height = total_height + self.padding * 2
        
        # Calculate position (prefer right, fallback to left)
        x = self.target_rect.right + ModernUITheme.SPACING_SM
        y = self.target_rect.y
        
        # Keep on screen
        screen = pygame.display.get_surface()
        if screen:
            if x + self.tooltip_width > screen.get_width():
                x = self.target_rect.left - self.tooltip_width - ModernUITheme.SPACING_SM
            if y + self.tooltip_height > screen.get_height():
                y = screen.get_height() - self.tooltip_height - ModernUITheme.SPACING_SM
            if y < 0:
                y = ModernUITheme.SPACING_SM
        
        self.rect = pygame.Rect(x, y, self.tooltip_width, self.tooltip_height)
    
    def show(self):
        """Show the tooltip."""
        self.visible = True
    
    def hide(self):
        """Hide the tooltip."""
        self.visible = False
    
    def draw(self, surface: pygame.Surface):
        """Draw the tooltip."""
        if not self.visible or not self.rect:
            return
        
        # Shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0, 100))
        surface.blit(shadow_surface, shadow_rect)
        
        # Background
        pygame.draw.rect(surface, ModernUITheme.SURFACE_ELEVATED, self.rect)
        pygame.draw.rect(surface, ModernUITheme.BORDER_STRONG, self.rect, 2)
        
        # Content
        y_offset = self.padding
        for line_type, line_surf in self.lines:
            x_pos = self.rect.x + self.padding
            y_pos = self.rect.y + y_offset
            surface.blit(line_surf, (x_pos, y_pos))
            y_offset += line_surf.get_height() + (ModernUITheme.SPACING_SM if line_type == 'title' else 2)

class AdaptiveList:
    """Modern list component with smooth scrolling."""
    
    def __init__(self, rect: pygame.Rect, items: List[Any], 
                 fonts: Dict[str, pygame.font.Font], item_height: int = None):
        self.rect = rect
        self.items = items
        self.fonts = fonts
        self.item_height = item_height or (fonts['body'].get_height() + ModernUITheme.SPACING_MD)
        
        # Selection and scrolling
        self.selected_index = -1
        self.scroll_offset = 0
        self.smooth_scroll_target = 0
        self.smooth_scroll_current = 0
        
        # Calculate visible items
        self.visible_count = max(1, rect.height // self.item_height)
        self.can_scroll = len(items) > self.visible_count
        
        # Visual properties
        self.border_radius = 6
        self.show_scrollbar = True
        self.scrollbar_width = 8
        self.content_width = rect.width - (self.scrollbar_width if self.show_scrollbar and self.can_scroll else 0)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle list events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Calculate clicked item
                local_y = event.pos[1] - self.rect.y
                clicked_index = int((local_y + self.smooth_scroll_current) // self.item_height)
                
                if 0 <= clicked_index < len(self.items):
                    self.selected_index = clicked_index
                    self.on_selection_changed(clicked_index)
                return True
        
        elif event.type == pygame.MOUSEWHEEL and self.can_scroll:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.smooth_scroll_target = max(0, min(
                    (len(self.items) - self.visible_count) * self.item_height,
                    self.smooth_scroll_target - event.y * 30
                ))
                return True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.select_previous()
                return True
            elif event.key == pygame.K_DOWN:
                self.select_next()
                return True
        
        return False
    
    def select_previous(self):
        """Select previous item."""
        if self.items:
            self.selected_index = max(0, self.selected_index - 1)
            self._ensure_visible(self.selected_index)
            self.on_selection_changed(self.selected_index)
    
    def select_next(self):
        """Select next item."""
        if self.items:
            self.selected_index = min(len(self.items) - 1, self.selected_index + 1)
            self._ensure_visible(self.selected_index)
            self.on_selection_changed(self.selected_index)
    
    def _ensure_visible(self, index: int):
        """Ensure the given index is visible in the viewport."""
        item_y = index * self.item_height
        viewport_top = self.smooth_scroll_target
        viewport_bottom = viewport_top + self.rect.height
        
        if item_y < viewport_top:
            self.smooth_scroll_target = item_y
        elif item_y + self.item_height > viewport_bottom:
            self.smooth_scroll_target = item_y + self.item_height - self.rect.height
    
    def update(self, dt: float):
        """Update animations."""
        # Smooth scrolling
        if abs(self.smooth_scroll_target - self.smooth_scroll_current) > 1:
            self.smooth_scroll_current += (self.smooth_scroll_target - self.smooth_scroll_current) * 0.2
        else:
            self.smooth_scroll_current = self.smooth_scroll_target
    
    def on_selection_changed(self, index: int):
        """Override in subclasses."""
        pass
    
    def get_selected_item(self):
        """Get the currently selected item."""
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None
    
    def draw(self, surface: pygame.Surface):
        """Draw the list."""
        # Background
        pygame.draw.rect(surface, ModernUITheme.SURFACE_PRIMARY, self.rect)
        pygame.draw.rect(surface, ModernUITheme.BORDER_SUBTLE, self.rect, 1)
        
        # Create content clipping surface
        content_surface = pygame.Surface((self.content_width, self.rect.height))
        content_surface.fill(ModernUITheme.SURFACE_PRIMARY)
        
        # Draw items
        start_index = max(0, int(self.smooth_scroll_current // self.item_height))
        end_index = min(len(self.items), start_index + self.visible_count + 2)
        
        for i in range(start_index, end_index):
            item_y = i * self.item_height - self.smooth_scroll_current
            
            if item_y > self.rect.height or item_y + self.item_height < 0:
                continue
            
            item_rect = pygame.Rect(0, int(item_y), self.content_width, self.item_height)
            
            # Selection highlight with rounded corners
            if i == self.selected_index:
                highlight_rect = item_rect.inflate(-4, -4)
                highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
                highlight_surface.fill(ModernUITheme.INTERACTIVE_ACTIVE)
                content_surface.blit(highlight_surface, (highlight_rect.x, highlight_rect.y))
            
            # Item content
            self.draw_item(content_surface, self.items[i], item_rect, i)
        
        # Blit content to main surface
        surface.blit(content_surface, self.rect)
        
        # Draw scrollbar
        if self.can_scroll and self.show_scrollbar:
            self._draw_scrollbar(surface)
    
    def draw_item(self, surface: pygame.Surface, item: Any, rect: pygame.Rect, index: int):
        """Override in subclasses to customize item drawing."""
        # Default implementation: draw item as string
        text_color = ModernUITheme.TEXT_PRIMARY
        text_surf = self.fonts['body'].render(str(item), True, text_color)
        
        text_y = rect.y + (rect.height - text_surf.get_height()) // 2
        surface.blit(text_surf, (rect.x + ModernUITheme.SPACING_SM, text_y))
    
    def _draw_scrollbar(self, surface: pygame.Surface):
        """Draw modern scrollbar."""
        scrollbar_rect = pygame.Rect(
            self.rect.right - self.scrollbar_width,
            self.rect.y,
            self.scrollbar_width,
            self.rect.height
        )
        
        # Scrollbar background
        pygame.draw.rect(surface, ModernUITheme.SURFACE_SECONDARY, scrollbar_rect)
        
        # Scrollbar thumb
        if len(self.items) > 0:
            total_height = len(self.items) * self.item_height
            thumb_height = max(20, (self.rect.height / total_height) * scrollbar_rect.height)
            thumb_y = scrollbar_rect.y + (self.smooth_scroll_current / total_height) * (scrollbar_rect.height - thumb_height)
            
            thumb_rect = pygame.Rect(
                scrollbar_rect.x + 2,
                thumb_y,
                scrollbar_rect.width - 4,
                thumb_height
            )
            
            pygame.draw.rect(surface, ModernUITheme.INTERACTIVE_NORMAL, thumb_rect)

# Utility functions for creating spell tooltips and other content
def create_spell_tooltip_content(spell) -> Dict[str, Any]:
    """Create rich tooltip content for spells using the new system."""
    content = {
        'title': spell.name,
        'subtitle': f"Tier {spell.tier} • {spell.range} Range",
        'description': spell.description
    }
    
    # Add effects if available
    if hasattr(spell, 'base_effect') and spell.base_effect:
        effects = []
        if spell.base_effect.damage:
            effects.append(f"Damage: {spell.base_effect.damage} {spell.base_effect.damage_type}")
        if spell.base_effect.healing:
            effects.append(f"Healing: {spell.base_effect.healing}")
        if spell.base_effect.duration:
            effects.append(f"Duration: {spell.base_effect.duration} rounds")
        if spell.base_effect.area_of_effect:
            effects.append(f"Area: {spell.base_effect.area_of_effect} cells")
        
        content['effects'] = effects
    
    # Add lore enhancement if available
    if hasattr(spell, 'lore_condition_text') and spell.lore_condition_text:
        if 'effects' not in content:
            content['effects'] = []
        content['effects'].append(f"🌟 Lore Enhancement: {spell.lore_condition_text}")
    
    return content

def create_modern_fonts(font_path: str, layout: ResponsiveLayout) -> Dict[str, pygame.font.Font]:
    """Create responsive font set for modern UI."""
    return layout.get_fonts(font_path)

class ModernCharacterSheet:
    """Modern character sheet with responsive layout."""
    
    def __init__(self, screen_width: int, screen_height: int, font_file: str):
        self.layout = ResponsiveLayout(screen_width, screen_height)
        self.fonts = create_modern_fonts(font_file, self.layout)
        
        # Cards for different sections
        self.cards = []
        self._setup_cards()
    
    def _setup_cards(self):
        """Setup character sheet cards."""
        card_width = self.layout.column_width
        card_height = 200
        
        # Basic info card
        basic_info_card = InfoCard(
            self.layout.margin, self.layout.margin,
            card_width, "Character Info", 
            "Name, race, class, and basic character information",
            self.fonts, expandable=True
        )
        self.cards.append(basic_info_card)
        
        # Stats card
        stats_card = InfoCard(
            self.layout.margin, self.layout.margin + card_height + self.layout.gutter,
            card_width, "Abilities", 
            "Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma",
            self.fonts, expandable=True
        )
        self.cards.append(stats_card)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for all cards."""
        for card in self.cards:
            if card.handle_event(event):
                return True
        return False
    
    def draw(self, surface: pygame.Surface, player):
        """Draw the modern character sheet."""
        surface.fill(ModernUITheme.SURFACE_PRIMARY)
        
        for card in self.cards:
            card.draw(surface)

# Integration with your existing spell system
class ModernSpellBrowser(AdaptiveList):
    """Modern spell browser with rich tooltips."""
    
    def __init__(self, rect: pygame.Rect, spells: List, fonts: Dict[str, pygame.font.Font]):
        super().__init__(rect, spells, fonts)
        self.current_tooltip = None
        self.tooltip_timer = 0
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events including tooltip display."""
        result = super().handle_event(event)
        
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                # Show tooltip after hover delay
                self.tooltip_timer += 1
                if self.tooltip_timer > 30:  # ~0.5 seconds at 60fps
                    hovered_item = self._get_hovered_item(event.pos)
                    if hovered_item:
                        self._show_spell_tooltip(hovered_item, event.pos)
            else:
                self._hide_tooltip()
                self.tooltip_timer = 0
        
        return result
    
    def _get_hovered_item(self, mouse_pos):
        """Get the item being hovered over."""
        local_y = mouse_pos[1] - self.rect.y
        item_index = int((local_y + self.smooth_scroll_current) // self.item_height)
        
        if 0 <= item_index < len(self.items):
            return self.items[item_index]
        return None
    
    def _show_spell_tooltip(self, spell, mouse_pos):
        """Show tooltip for a spell."""
        if not self.current_tooltip:
            content = create_spell_tooltip_content(spell)
            target_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
            self.current_tooltip = SmartTooltip(target_rect, content, self.fonts)
            self.current_tooltip.show()
    
    def _hide_tooltip(self):
        """Hide current tooltip."""
        if self.current_tooltip:
            self.current_tooltip.hide()
            self.current_tooltip = None
        self.tooltip_timer = 0
    
    def update(self, dt: float):
        """Update animations and tooltips."""
        super().update(dt)
    
    def draw(self, surface: pygame.Surface):
        """Draw spell browser with tooltips."""
        super().draw(surface)
        
        if self.current_tooltip:
            self.current_tooltip.draw(surface)
    
    def draw_item(self, surface: pygame.Surface, spell, rect: pygame.Rect, index: int):
        """Draw spell item with enhanced information."""
        # Spell name
        name_surf = self.fonts['body'].render(spell.name, True, ModernUITheme.TEXT_PRIMARY)
        surface.blit(name_surf, (rect.x + ModernUITheme.SPACING_SM, rect.y + 4))
        
        # Spell tier and type
        tier_text = f"Tier {spell.tier}"
        tier_surf = self.fonts['small'].render(tier_text, True, ModernUITheme.TEXT_ACCENT)
        surface.blit(tier_surf, (rect.x + ModernUITheme.SPACING_SM, rect.y + rect.height - 18))
        
        # Lore enhancement indicator
        if hasattr(spell, 'lore_condition_text') and spell.lore_condition_text:
            # Check if lore condition is currently active
            calendar = get_world_calendar()
            is_enhanced = spell.check_lore_condition() if hasattr(spell, 'check_lore_condition') else False
            
            if is_enhanced:
                star_surf = self.fonts['small'].render("✨", True, ModernUITheme.TEXT_ACCENT)
                surface.blit(star_surf, (rect.right - 30, rect.y + 4))

class ModernInventoryGrid:
    """Modern grid-based inventory with drag and drop."""
    
    def __init__(self, rect: pygame.Rect, fonts: Dict[str, pygame.font.Font], 
                 grid_size: Tuple[int, int] = (8, 6)):
        self.rect = rect
        self.fonts = fonts
        self.grid_cols, self.grid_rows = grid_size
        
        # Calculate cell size
        self.cell_size = min(
            (rect.width - ModernUITheme.SPACING_MD * 2) // self.grid_cols,
            (rect.height - ModernUITheme.SPACING_MD * 2) // self.grid_rows
        )
        
        # Grid layout
        self.grid_rect = pygame.Rect(
            rect.x + (rect.width - self.grid_cols * self.cell_size) // 2,
            rect.y + ModernUITheme.SPACING_MD,
            self.grid_cols * self.cell_size,
            self.grid_rows * self.cell_size
        )
        
        # State
        self.items = {}  # {(x, y): item}
        self.selected_slot = None
        self.hovered_slot = None
        self.dragging_item = None
        self.drag_offset = (0, 0)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle inventory interactions."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered_slot = self._get_slot_at_pos(event.pos)
            
            if self.dragging_item:
                self.drag_offset = (
                    event.pos[0] - self.dragging_item['start_pos'][0],
                    event.pos[1] - self.dragging_item['start_pos'][1]
                )
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                slot = self._get_slot_at_pos(event.pos)
                if slot and slot in self.items:
                    self.selected_slot = slot
                    self.dragging_item = {
                        'item': self.items[slot],
                        'start_slot': slot,
                        'start_pos': event.pos
                    }
                    return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging_item:
                target_slot = self._get_slot_at_pos(event.pos)
                if target_slot and target_slot != self.dragging_item['start_slot']:
                    self._move_item(self.dragging_item['start_slot'], target_slot)
                
                self.dragging_item = None
                self.drag_offset = (0, 0)
                return True
        
        return False
    
    def _get_slot_at_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Get grid slot at mouse position."""
        if not self.grid_rect.collidepoint(pos):
            return None
        
        local_x = pos[0] - self.grid_rect.x
        local_y = pos[1] - self.grid_rect.y
        
        grid_x = local_x // self.cell_size
        grid_y = local_y // self.cell_size
        
        if 0 <= grid_x < self.grid_cols and 0 <= grid_y < self.grid_rows:
            return (grid_x, grid_y)
        
        return None
    
    def _move_item(self, from_slot: Tuple[int, int], to_slot: Tuple[int, int]):
        """Move item between slots."""
        if from_slot in self.items:
            item = self.items[from_slot]
            del self.items[from_slot]
            
            # Handle slot swapping if target occupied
            if to_slot in self.items:
                displaced_item = self.items[to_slot]
                self.items[from_slot] = displaced_item
            
            self.items[to_slot] = item
    
    def add_item(self, item, slot: Tuple[int, int] = None) -> bool:
        """Add item to inventory grid."""
        if slot is None:
            slot = self._find_empty_slot()
        
        if slot and slot not in self.items:
            self.items[slot] = item
            return True
        
        return False
    
    def _find_empty_slot(self) -> Optional[Tuple[int, int]]:
        """Find first empty slot."""
        for y in range(self.grid_rows):
            for x in range(self.grid_cols):
                if (x, y) not in self.items:
                    return (x, y)
        return None
    
    def draw(self, surface: pygame.Surface):
        """Draw the inventory grid."""
        # Background
        pygame.draw.rect(surface, ModernUITheme.SURFACE_PRIMARY, self.rect)
        pygame.draw.rect(surface, ModernUITheme.BORDER_SUBTLE, self.rect, 2)
        
        # Grid cells
        for y in range(self.grid_rows):
            for x in range(self.grid_cols):
                cell_rect = pygame.Rect(
                    self.grid_rect.x + x * self.cell_size,
                    self.grid_rect.y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                # Cell background
                cell_color = ModernUITheme.SURFACE_SECONDARY
                
                # Hover effect
                if self.hovered_slot == (x, y):
                    cell_color = ModernUITheme.INTERACTIVE_HOVER
                
                # Selection effect
                if self.selected_slot == (x, y):
                    cell_color = ModernUITheme.INTERACTIVE_ACTIVE
                
                pygame.draw.rect(surface, cell_color, cell_rect)
                pygame.draw.rect(surface, ModernUITheme.BORDER_SUBTLE, cell_rect, 1)
                
                # Item in slot
                if (x, y) in self.items and (not self.dragging_item or self.dragging_item['start_slot'] != (x, y)):
                    self._draw_item_in_slot(surface, self.items[(x, y)], cell_rect)
        
        # Draw dragging item
        if self.dragging_item:
            mouse_pos = pygame.mouse.get_pos()
            drag_rect = pygame.Rect(
                mouse_pos[0] - self.cell_size // 2,
                mouse_pos[1] - self.cell_size // 2,
                self.cell_size,
                self.cell_size
            )
            
            # Semi-transparent background
            drag_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            drag_surface.fill((*ModernUITheme.INTERACTIVE_ACTIVE, 180))
            surface.blit(drag_surface, drag_rect)
            
            self._draw_item_in_slot(surface, self.dragging_item['item'], drag_rect)
    
    def _draw_item_in_slot(self, surface: pygame.Surface, item, rect: pygame.Rect):
        """Draw an item within a slot."""
        # Item icon/representation
        if hasattr(item, 'icon'):
            # If item has icon, draw it
            icon_surf = self.fonts['body'].render(item.icon, True, ModernUITheme.TEXT_PRIMARY)
        else:
            # Fallback to first letter of item name
            first_letter = item.name[0].upper() if hasattr(item, 'name') else '?'
            icon_surf = self.fonts['body'].render(first_letter, True, ModernUITheme.TEXT_PRIMARY)
        
        icon_rect = icon_surf.get_rect(center=rect.center)
        surface.blit(icon_surf, icon_rect)
        
        # Quantity indicator
        if hasattr(item, 'quantity') and item.quantity > 1:
            qty_surf = self.fonts['caption'].render(str(item.quantity), True, ModernUITheme.TEXT_ACCENT)
            surface.blit(qty_surf, (rect.right - 12, rect.bottom - 12))

class ModernProgressBar:
    """Modern progress bar with smooth animations."""
    
    def __init__(self, rect: pygame.Rect, max_value: float, current_value: float = 0,
                 color: Tuple[int, int, int] = ModernUITheme.SUCCESS,
                 background_color: Tuple[int, int, int] = ModernUITheme.SURFACE_SECONDARY):
        self.rect = rect
        self.max_value = max_value
        self.current_value = current_value
        self.target_value = current_value
        self.color = color
        self.background_color = background_color
        
        # Animation
        self.animation_speed = 0.1
        self.border_radius = 4
    
    def set_value(self, value: float):
        """Set target value with animation."""
        self.target_value = max(0, min(self.max_value, value))
    
    def update(self, dt: float):
        """Update animation."""
        if abs(self.target_value - self.current_value) > 0.1:
            self.current_value += (self.target_value - self.current_value) * self.animation_speed
        else:
            self.current_value = self.target_value
    
    def draw(self, surface: pygame.Surface, show_text: bool = True):
        """Draw the progress bar."""
        # Background
        pygame.draw.rect(surface, self.background_color, self.rect)
        
        # Fill
        if self.max_value > 0:
            fill_ratio = self.current_value / self.max_value
            fill_width = int(self.rect.width * fill_ratio)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(surface, self.color, fill_rect)
        
        # Border
        pygame.draw.rect(surface, ModernUITheme.BORDER_SUBTLE, self.rect, 1)
        
        # Text overlay
        if show_text:
            text = f"{int(self.current_value)}/{int(self.max_value)}"
            font = pygame.font.Font(None, max(16, self.rect.height - 4))
            text_surf = font.render(text, True, ModernUITheme.TEXT_PRIMARY)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

class ModernButton:
    """Modern button with hover effects and variants."""
    
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font,
                 variant: str = 'primary', callback: Callable = None):
        self.rect = rect
        self.text = text
        self.font = font
        self.callback = callback
        
        # Visual state
        self.hovered = False
        self.pressed = False
        self.disabled = False
        
        # Style variants
        self.variants = {
            'primary': {
                'normal': ModernUITheme.INTERACTIVE_ACTIVE,
                'hover': (255, 235, 59),  # Lighter gold
                'pressed': (255, 193, 7),  # Darker gold
                'text': ModernUITheme.SURFACE_PRIMARY
            },
            'secondary': {
                'normal': ModernUITheme.SURFACE_SECONDARY,
                'hover': ModernUITheme.INTERACTIVE_HOVER,
                'pressed': ModernUITheme.INTERACTIVE_NORMAL,
                'text': ModernUITheme.TEXT_PRIMARY
            },
            'danger': {
                'normal': ModernUITheme.ERROR,
                'hover': (255, 87, 74),
                'pressed': (244, 67, 54),
                'text': ModernUITheme.TEXT_PRIMARY
            }
        }
        
        self.style = self.variants.get(variant, self.variants['primary'])
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle button events."""
        if self.disabled:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed:
                self.pressed = False
                if self.rect.collidepoint(event.pos) and self.callback:
                    self.callback()
                return True
        
        return False
    
    def draw(self, surface: pygame.Surface):
        """Draw the button."""
        # Determine color based on state
        if self.disabled:
            bg_color = ModernUITheme.SURFACE_SECONDARY
            text_color = ModernUITheme.TEXT_MUTED
        elif self.pressed:
            bg_color = self.style['pressed']
            text_color = self.style['text']
        elif self.hovered:
            bg_color = self.style['hover']
            text_color = self.style['text']
        else:
            bg_color = self.style['normal']
            text_color = self.style['text']
        
        # Background with rounded corners effect
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, ModernUITheme.BORDER_SUBTLE, self.rect, 1)
        
        # Text
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class ModernNotification:
    """Modern notification/toast system."""
    
    def __init__(self, message: str, notification_type: str = 'info', 
                 duration: float = 3.0, font: pygame.font.Font = None):
        self.message = message
        self.type = notification_type
        self.duration = duration
        self.timer = 0
        self.font = font or pygame.font.Font(None, 16)
        
        # Visual properties
        self.alpha = 0
        self.target_alpha = 255
        self.slide_y = -50
        self.target_y = 20
        
        # Colors by type
        self.colors = {
            'info': ModernUITheme.INFO,
            'success': ModernUITheme.SUCCESS,
            'warning': ModernUITheme.WARNING,
            'error': ModernUITheme.ERROR
        }
        
        self.color = self.colors.get(notification_type, ModernUITheme.INFO)
        
        # Calculate size
        text_surf = self.font.render(message, True, ModernUITheme.TEXT_PRIMARY)
        self.width = text_surf.get_width() + ModernUITheme.SPACING_LG * 2
        self.height = text_surf.get_height() + ModernUITheme.SPACING_MD * 2
    
    def update(self, dt: float) -> bool:
        """Update notification. Returns False when it should be removed."""
        self.timer += dt
        
        # Fade in
        if self.timer < 0.3:
            self.alpha = int((self.timer / 0.3) * 255)
            self.slide_y = self.target_y - 30 + (self.timer / 0.3) * 30
        
        # Stay visible
        elif self.timer < self.duration - 0.5:
            self.alpha = 255
            self.slide_y = self.target_y
        
        # Fade out
        elif self.timer < self.duration:
            fade_progress = (self.timer - (self.duration - 0.5)) / 0.5
            self.alpha = int(255 * (1 - fade_progress))
        
        # Remove
        else:
            return False
        
        return True
    
    def draw(self, surface: pygame.Surface, x: int):
        """Draw notification."""
        if self.alpha <= 0:
            return
        
        # Create notification surface
        notification_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Background
        bg_color = (*ModernUITheme.SURFACE_ELEVATED, self.alpha)
        notification_surface.fill(bg_color)
        
        # Colored left border
        border_color = (*self.color, self.alpha)
        pygame.draw.rect(notification_surface, border_color, (0, 0, 4, self.height))
        
        # Text
        text_color = (*ModernUITheme.TEXT_PRIMARY, min(255, self.alpha))
        text_surf = self.font.render(self.message, True, text_color)
        text_rect = text_surf.get_rect(
            x=ModernUITheme.SPACING_MD,
            centery=self.height // 2
        )
        notification_surface.blit(text_surf, text_rect)
        
        # Border
        border_color = (*ModernUITheme.BORDER_SUBTLE, self.alpha // 2)
        pygame.draw.rect(notification_surface, border_color, (0, 0, self.width, self.height), 1)
        
        # Draw to main surface
        surface.blit(notification_surface, (x, int(self.slide_y)))

class ModernNotificationManager:
    """Manages multiple notifications."""
    
    def __init__(self, screen_width: int):
        self.screen_width = screen_width
        self.notifications = []
        self.font = pygame.font.Font(None, 16)
    
    def add_notification(self, message: str, notification_type: str = 'info', duration: float = 3.0):
        """Add a new notification."""
        notification = ModernNotification(message, notification_type, duration, self.font)
        self.notifications.append(notification)
    
    def update(self, dt: float):
        """Update all notifications."""
        self.notifications = [notif for notif in self.notifications if notif.update(dt)]
    
    def draw(self, surface: pygame.Surface):
        """Draw all notifications."""
        for i, notification in enumerate(self.notifications):
            x = self.screen_width - notification.width - ModernUITheme.SPACING_MD
            y_offset = i * (notification.height + ModernUITheme.SPACING_SM)
            notification.slide_y = ModernUITheme.SPACING_MD + y_offset
            notification.draw(surface, x)

# Integration helpers for your existing systems
class ModernCharacterCreationManager:
    """Modern character creation with the new UI components."""
    
    def __init__(self, screen_width: int, screen_height: int, font_file: str):
        self.layout = ResponsiveLayout(screen_width, screen_height)
        self.fonts = create_modern_fonts(font_file, self.layout)
        self.notification_manager = ModernNotificationManager(screen_width)
        
        # UI components
        self.cards = []
        self.buttons = []
        self.current_step = 0
        
    def setup_name_input_step(self):
        """Setup modern name input interface."""
        # Create elegant input card
        input_card = ModernCard(
            x=(self.layout.screen_width - 400) // 2,
            y=(self.layout.screen_height - 200) // 2,
            width=400,
            height=200,
            elevated=True
        )
        
        return input_card
    
    def setup_spell_selection(self, available_spells):
        """Setup modern spell selection with rich tooltips."""
        spell_list_rect = pygame.Rect(
            self.layout.margin,
            self.layout.margin + 60,
            self.layout.column_width,
            self.layout.content_height - 120
        )
        
        spell_browser = ModernSpellBrowser(spell_list_rect, available_spells, self.fonts)
        return spell_browser
    
    def draw_progress_indicator(self, surface: pygame.Surface, current_step: int, total_steps: int):
        """Draw modern progress indicator."""
        progress_width = min(400, self.layout.content_width - 100)
        progress_rect = pygame.Rect(
            (self.layout.screen_width - progress_width) // 2,
            20,
            progress_width,
            4
        )
        
        # Background
        pygame.draw.rect(surface, ModernUITheme.SURFACE_SECONDARY, progress_rect)
        
        # Progress
        progress_ratio = current_step / total_steps
        fill_width = int(progress_width * progress_ratio)
        fill_rect = pygame.Rect(progress_rect.x, progress_rect.y, fill_width, progress_rect.height)
        pygame.draw.rect(surface, ModernUITheme.INTERACTIVE_ACTIVE, fill_rect)
        
        # Step indicators
        step_radius = 8
        for i in range(total_steps + 1):
            step_x = progress_rect.x + (i / total_steps) * progress_width
            step_y = progress_rect.centery
            
            if i <= current_step:
                color = ModernUITheme.INTERACTIVE_ACTIVE
            else:
                color = ModernUITheme.SURFACE_SECONDARY
            
            pygame.draw.circle(surface, color, (int(step_x), step_y), step_radius)
            pygame.draw.circle(surface, ModernUITheme.BORDER_SUBTLE, (int(step_x), step_y), step_radius, 2)

# Example usage of the new modern UI system
def create_modern_inventory_ui(screen_width: int, screen_height: int, font_file: str):
    """Create a modern inventory interface."""
    layout = ResponsiveLayout(screen_width, screen_height)
    fonts = create_modern_fonts(font_file, layout)
    
    # Main inventory grid
    grid_rect = pygame.Rect(
        layout.margin,
        layout.margin + 60,
        layout.column_width,
        layout.content_height - 120
    )
    
    inventory_grid = ModernInventoryGrid(grid_rect, fonts)
    
    # Equipment panel
    equipment_rect = pygame.Rect(
        layout.margin + layout.column_width + layout.gutter,
        layout.margin + 60,
        layout.column_width,
        layout.content_height - 120
    )
    
    equipment_card = InfoCard(
        equipment_rect.x, equipment_rect.y, equipment_rect.width,
        "Equipment", "Currently equipped items and their stats",
        fonts, expandable=True
    )
    
    return {
        'inventory_grid': inventory_grid,
        'equipment_card': equipment_card,
        'layout': layout,
        'fonts': fonts
    }

def create_modern_spell_interface(screen_width: int, screen_height: int, font_file: str, spells: List):
    """Create a modern spell selection interface."""
    layout = ResponsiveLayout(screen_width, screen_height)
    fonts = create_modern_fonts(font_file, layout)
    
    # Spell browser
    browser_rect = pygame.Rect(
        layout.margin,
        layout.margin + 60,
        layout.column_width,
        layout.content_height - 120
    )
    
    spell_browser = ModernSpellBrowser(browser_rect, spells, fonts)
    
    # Spell details card
    details_rect = pygame.Rect(
        layout.margin + layout.column_width + layout.gutter,
        layout.margin + 60,
        layout.column_width,
        layout.content_height - 120
    )
    
    details_card = InfoCard(
        details_rect.x, details_rect.y, details_rect.width,
        "Spell Details", "Detailed information about the selected spell",
        fonts, expandable=False
    )
    
    return {
        'spell_browser': spell_browser,
        'details_card': details_card,
        'layout': layout,
        'fonts': fonts
    }