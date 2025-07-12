"""
UI Modernization Integration Guide
Shows how to integrate the new modern UI components with your existing systems.
This file demonstrates upgrading your current UI screens to use the modern components.
"""

import pygame
from typing import Dict, List, Optional, Tuple

# Import your existing systems
from ui.character_creation import EnhancedCharacterCreator
from ui.inventory_ui import InventoryUI, ContainerViewUI, EquipmentUI
from ui.gear_selection import GearSelector
from game.states import GameState, CharCreationState

# Import the new modern components
from modern_ui_components import (
    ModernUITheme, ResponsiveLayout, ModernCard, InfoCard, SmartTooltip,
    AdaptiveList, ModernInventoryGrid, ModernProgressBar, ModernButton,
    ModernNotificationManager, ModernSpellBrowser, create_modern_fonts
)

class ModernizedCharacterCreation(EnhancedCharacterCreator):
    """Modernized version of your character creation using new UI components."""
    
    def __init__(self, screen: pygame.Surface, font_file: str):
        # Initialize the base class
        super().__init__(screen, font_file)
        
        # Add modern UI components
        self.layout = ResponsiveLayout(self.screen_width, self.screen_height)
        self.modern_fonts = create_modern_fonts(font_file, self.layout)
        self.notification_manager = ModernNotificationManager(self.screen_width)
        
        # Modern UI elements
        self.info_cards = {}
        self.progress_bars = {}
        self.modern_buttons = []
        
        self._setup_modern_components()
    
    def _setup_modern_components(self):
        """Setup modern UI components for character creation."""
        # Progress indicator for character creation steps
        progress_rect = pygame.Rect(
            (self.screen_width - 400) // 2, 20, 400, 6
        )
        self.creation_progress = ModernProgressBar(
            progress_rect, max_value=10, 
            color=ModernUITheme.INTERACTIVE_ACTIVE
        )
        
        # Race selection card
        race_card_width = self.layout.column_width
        self.info_cards['race'] = InfoCard(
            self.layout.margin, 120, race_card_width,
            "Choose Your Ancestry", "Select your character's race and heritage",
            self.modern_fonts, expandable=False
        )
        
        # Class selection card  
        class_card_x = self.layout.margin + race_card_width + self.layout.gutter
        self.info_cards['class'] = InfoCard(
            class_card_x, 120, race_card_width,
            "Choose Your Path", "Select your character's class and profession",
            self.modern_fonts, expandable=False
        )
        
        # Spell selection with modern browser
        if self.layout.columns >= 2:
            spell_rect = pygame.Rect(
                class_card_x, 400, race_card_width, 300
            )
            self.spell_browser = ModernSpellBrowser(spell_rect, [], self.modern_fonts)
    
    def draw(self, surface: pygame.Surface):
        """Enhanced draw method with modern UI."""
        # Modern background
        surface.fill(ModernUITheme.SURFACE_PRIMARY)
        
        # Update progress based on current state
        progress_value = {
            CharCreationState.NAME_INPUT: 1,
            CharCreationState.STAT_ROLLING: 2,
            CharCreationState.RACE_SELECTION: 3,
            CharCreationState.CLASS_SELECTION: 4,
            CharCreationState.ALIGNMENT_SELECTION: 5,
            CharCreationState.BIRTH_DATE_INPUT: 6,
            CharCreationState.BIRTH_SIGN_REVIEW: 7,
            CharCreationState.GOD_SELECTION: 8,
            CharCreationState.SPELL_SELECTION: 9,
            CharCreationState.STATS_REVIEW: 10
        }.get(self.state, 0)
        
        self.creation_progress.set_value(progress_value)
        self.creation_progress.update(1/60)  # Assuming 60 FPS
        self.creation_progress.draw(surface, show_text=False)
        
        # Modern title
        title = self._get_title()
        title_surf = self.modern_fonts['title'].render(title, True, ModernUITheme.TEXT_ACCENT)
        title_rect = title_surf.get_rect(centerx=self.screen_width // 2, top=50)
        surface.blit(title_surf, title_rect)
        
        # State-specific modern rendering
        if self.state == CharCreationState.RACE_SELECTION:
            self._draw_modern_race_selection(surface)
        elif self.state == CharCreationState.CLASS_SELECTION:
            self._draw_modern_class_selection(surface)
        elif self.state == CharCreationState.SPELL_SELECTION:
            self._draw_modern_spell_selection(surface)
        elif self.state == CharCreationState.BIRTH_SIGN_REVIEW:
            self._draw_modern_birth_sign(surface)
        else:
            # Fall back to original drawing for other states
            super().draw(surface)
            return
        
        # Modern notifications
        self.notification_manager.update(1/60)
        self.notification_manager.draw(surface)
        
        # Modern instructions
        self._draw_modern_instructions(surface)
    
    def _draw_modern_race_selection(self, surface: pygame.Surface):
        """Modern race selection interface."""
        # Race list with modern styling
        races = list(self._get_current_options())
        
        # Left panel - race list
        list_rect = pygame.Rect(
            self.layout.margin, 150, 
            self.layout.column_width, 400
        )
        
        race_list = AdaptiveList(list_rect, races, self.modern_fonts)
        race_list.selected_index = self.selected_index
        race_list.draw(surface)
        
        # Right panel - race details card
        if self.selected_index < len(races):
            selected_race = races[self.selected_index]
            race_details = self._get_current_details()
            
            details_rect = pygame.Rect(
                self.layout.margin + self.layout.column_width + self.layout.gutter,
                150, self.layout.column_width, 400
            )
            
            details_card = ModernCard(
                details_rect.x, details_rect.y, 
                details_rect.width, details_rect.height,
                elevated=True
            )
            details_card.draw_background(surface)
            
            # Race details content
            self._draw_race_details_content(surface, details_card.content_rect, race_details)
    
    def _draw_race_details_content(self, surface: pygame.Surface, rect: pygame.Rect, details: dict):
        """Draw race details with modern styling."""
        current_y = rect.y + ModernUITheme.SPACING_MD
        
        # Race name with accent color
        race_name = details.get('description', 'Unknown Race').split('.')[0]
        name_surf = self.modern_fonts['heading'].render(race_name, True, ModernUITheme.TEXT_ACCENT)
        surface.blit(name_surf, (rect.x + ModernUITheme.SPACING_MD, current_y))
        current_y += name_surf.get_height() + ModernUITheme.SPACING_SM
        
        # Description
        description = details.get('description', '')
        desc_lines = wrap_text(description, rect.width - ModernUITheme.SPACING_LG, self.modern_fonts['body'])
        for line in desc_lines:
            line_surf = self.modern_fonts['body'].render(line, True, ModernUITheme.TEXT_PRIMARY)
            surface.blit(line_surf, (rect.x + ModernUITheme.SPACING_MD, current_y))
            current_y += line_surf.get_height() + 3
        
        current_y += ModernUITheme.SPACING_MD
        
        # Traits section
        traits_surf = self.modern_fonts['subheading'].render("Traits", True, ModernUITheme.TEXT_ACCENT)
        surface.blit(traits_surf, (rect.x + ModernUITheme.SPACING_MD, current_y))
        current_y += traits_surf.get_height() + ModernUITheme.SPACING_SM
        
        traits = details.get('traits', '')
        trait_surf = self.modern_fonts['small'].render(traits, True, ModernUITheme.TEXT_SECONDARY)
        surface.blit(trait_surf, (rect.x + ModernUITheme.SPACING_MD, current_y))
        current_y += trait_surf.get_height() + ModernUITheme.SPACING_MD
        
        # Abilities section
        if 'abilities' in details:
            abilities_surf = self.modern_fonts['subheading'].render("Abilities", True, ModernUITheme.TEXT_ACCENT)
            surface.blit(abilities_surf, (rect.x + ModernUITheme.SPACING_MD, current_y))
            current_y += abilities_surf.get_height() + ModernUITheme.SPACING_SM
            
            for ability in details['abilities']:
                ability_surf = self.modern_fonts['small'].render(f"• {ability}", True, ModernUITheme.TEXT_PRIMARY)
                surface.blit(ability_surf, (rect.x + ModernUITheme.SPACING_MD, current_y))
                current_y += ability_surf.get_height() + 2
    
    def _draw_modern_class_selection(self, surface: pygame.Surface):
        """Modern class selection interface."""
        classes = list(self._get_current_options())
        
        # Similar layout to race selection but with class-specific styling
        list_rect = pygame.Rect(
            self.layout.margin, 150, 
            self.layout.column_width, 400
        )
        
        class_list = AdaptiveList(list_rect, classes, self.modern_fonts)
        class_list.selected_index = self.selected_index
        class_list.draw(surface)
        
        # Class details with different accent color
        if self.selected_index < len(classes):
            details_rect = pygame.Rect(
                self.layout.margin + self.layout.column_width + self.layout.gutter,
                150, self.layout.column_width, 400
            )
            
            details_card = ModernCard(
                details_rect.x, details_rect.y, 
                details_rect.width, details_rect.height,
                elevated=True
            )
            details_card.draw_background(surface)
            
            class_details = self._get_current_details()
            self._draw_class_details_content(surface, details_card.content_rect, class_details)
    
    def _draw_class_details_content(self, surface: pygame.Surface, rect: pygame.Rect, details: dict):
        """Draw class details with modern styling."""
        current_y = rect.y + ModernUITheme.SPACING_MD
        
        # Class name
        class_name = details.get('description', 'Unknown Class').split('.')[0]
        name_surf = self.modern_fonts['heading'].render(class_name, True, ModernUITheme.INFO)
        surface.blit(name_surf, (rect.x + ModernUITheme.SPACING_MD, current_y))
        current_y += name_surf.get_height() + ModernUITheme.SPACING_SM
        
        # Description and abilities (similar to race but with different colors)
        description = details.get('description', '')
        desc_lines = wrap_text(description, rect.width - ModernUITheme.SPACING_LG, self.modern_fonts['body'])
        for line in desc_lines:
            line_surf = self.modern_fonts['body'].render(line, True, ModernUITheme.TEXT_PRIMARY)
            surface.blit(line_surf, (rect.x + ModernUITheme.SPACING_MD, current_y))
            current_y += line_surf.get_height() + 3
        
        # Add class-specific visual indicators
        if 'Wizard' in class_name or 'Priest' in class_name:
            magic_indicator = self.modern_fonts['small'].render("🔮 Spellcaster", True, ModernUITheme.TEXT_ACCENT)
            surface.blit(magic_indicator, (rect.x + ModernUITheme.SPACING_MD, current_y + ModernUITheme.SPACING_SM))
    
    def _draw_modern_spell_selection(self, surface: pygame.Surface):
        """Modern spell selection interface."""
        if hasattr(self, 'spell_browser'):
            self.spell_browser.draw(surface)
            
            # Selected spells indicator
            progress_text = f"Selected: {len(self.selected_spells)}/{self.spells_to_select}"
            progress_surf = self.modern_fonts['subheading'].render(progress_text, True, ModernUITheme.TEXT_ACCENT)
            surface.blit(progress_surf, (self.layout.margin, 100))
            
            # Modern spell selection progress bar
            if self.spells_to_select > 0:
                spell_progress_rect = pygame.Rect(
                    self.layout.margin, 125, 300, 8
                )
                spell_progress = ModernProgressBar(
                    spell_progress_rect, 
                    max_value=self.spells_to_select,
                    current_value=len(self.selected_spells),
                    color=ModernUITheme.SUCCESS
                )
                spell_progress.draw(surface)
    
    def _draw_modern_birth_sign(self, surface: pygame.Surface):
        """Modern birth sign review interface."""
        # Cosmic background effect
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Create a mystical card for birth sign
        sign_card = ModernCard(
            center_x - 300, center_y - 200,
            600, 400, elevated=True
        )
        sign_card.draw_background(surface)
        
        # Cosmic title
        title_surf = self.modern_fonts['title'].render("Your Cosmic Destiny", True, ModernUITheme.TEXT_ACCENT)
        title_rect = title_surf.get_rect(centerx=center_x, top=sign_card.rect.y + ModernUITheme.SPACING_LG)
        surface.blit(title_surf, title_rect)
        
        # Birth sign content with mystical styling
        if hasattr(self, 'birth_sign') and self.birth_sign:
            content_y = title_rect.bottom + ModernUITheme.SPACING_LG
            
            # Birth sign title with special formatting
            sign_title = f"✨ {self.birth_sign.combined_title} ✨"
            sign_surf = self.modern_fonts['heading'].render(sign_title, True, ModernUITheme.WARNING)
            sign_rect = sign_surf.get_rect(centerx=center_x, top=content_y)
            surface.blit(sign_surf, sign_rect)
            
            # Prophecy text with mystical styling
            prophecy_y = sign_rect.bottom + ModernUITheme.SPACING_MD
            prophecy_lines = wrap_text(self.birth_sign.prophecy_text, 500, self.modern_fonts['body'])
            
            for line in prophecy_lines:
                line_surf = self.modern_fonts['body'].render(line, True, ModernUITheme.TEXT_PRIMARY)
                line_rect = line_surf.get_rect(centerx=center_x, top=prophecy_y)
                surface.blit(line_surf, line_rect)
                prophecy_y += line_surf.get_height() + 3
    
    def _draw_modern_instructions(self, surface: pygame.Surface):
        """Modern instruction display."""
        instructions = self._get_instructions_for_state()
        
        if instructions:
            # Create semi-transparent instruction panel
            panel_height = len(instructions) * 25 + ModernUITheme.SPACING_MD
            panel_rect = pygame.Rect(
                ModernUITheme.SPACING_MD, 
                self.screen_height - panel_height - ModernUITheme.SPACING_MD,
                400, panel_height
            )
            
            # Semi-transparent background
            panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
            panel_surface.fill((*ModernUITheme.SURFACE_ELEVATED, 200))
            surface.blit(panel_surface, panel_rect)
            
            # Instructions
            inst_y = panel_rect.y + ModernUITheme.SPACING_SM
            for instruction in instructions:
                inst_surf = self.modern_fonts['small'].render(instruction, True, ModernUITheme.TEXT_PRIMARY)
                surface.blit(inst_surf, (panel_rect.x + ModernUITheme.SPACING_SM, inst_y))
                inst_y += 20
    
    def _get_instructions_for_state(self) -> List[str]:
        """Get instructions for current state."""
        instruction_map = {
            CharCreationState.RACE_SELECTION: ["↑↓ Navigate races", "ENTER Select", "ESC Back"],
            CharCreationState.CLASS_SELECTION: ["↑↓ Navigate classes", "ENTER Select", "ESC Back"],
            CharCreationState.SPELL_SELECTION: ["↑↓ Navigate spells", "ENTER Select/Deselect", "ESC Back"],
            CharCreationState.BIRTH_SIGN_REVIEW: ["ENTER Continue", "ESC Recalculate"],
        }
        return instruction_map.get(self.state, [])
    
    def handle_event(self, event: pygame.event.Event) -> Optional[bool]:
        """Enhanced event handling with modern UI feedback."""
        # Handle modern UI events first
        for card in self.info_cards.values():
            if card.handle_event(event):
                return False
        
        # Handle spell browser if active
        if hasattr(self, 'spell_browser') and self.state == CharCreationState.SPELL_SELECTION:
            if self.spell_browser.handle_event(event):
                return False
        
        # Add notifications for state transitions
        old_state = self.state
        result = super().handle_event(event)
        
        if old_state != self.state:
            self._add_transition_notification(old_state, self.state)
        
        return result
    
    def _add_transition_notification(self, old_state, new_state):
        """Add notifications for smooth state transitions."""
        state_names = {
            CharCreationState.NAME_INPUT: "Name Input",
            CharCreationState.RACE_SELECTION: "Race Selection", 
            CharCreationState.CLASS_SELECTION: "Class Selection",
            CharCreationState.SPELL_SELECTION: "Spell Selection",
            CharCreationState.BIRTH_SIGN_REVIEW: "Birth Sign Review"
        }
        
        if new_state in state_names:
            message = f"Entering {state_names[new_state]}"
            self.notification_manager.add_notification(message, 'info', duration=2.0)

class ModernizedInventoryUI(InventoryUI):
    """Modernized inventory interface."""
    
    def __init__(self, screen_width: int, screen_height: int, font_file: str):
        super().__init__(screen_width, screen_height, font_file)
        
        # Add modern components
        self.layout = ResponsiveLayout(screen_width, screen_height)
        self.modern_fonts = create_modern_fonts(font_file, self.layout)
        
        # Modern inventory grid
        grid_rect = pygame.Rect(
            self.layout.margin, 100,
            self.layout.column_width, 500
        )
        self.inventory_grid = ModernInventoryGrid(grid_rect, self.modern_fonts)
        
        # Equipment preview card
        equipment_rect = pygame.Rect(
            self.layout.margin + self.layout.column_width + self.layout.gutter,
            100, self.layout.column_width, 300
        )
        self.equipment_card = InfoCard(
            equipment_rect.x, equipment_rect.y, equipment_rect.width,
            "Equipment", "Currently equipped items and stats",
            self.modern_fonts, expandable=True
        )
        
        # Stats preview card
        stats_rect = pygame.Rect(
            equipment_rect.x, equipment_rect.bottom + ModernUITheme.SPACING_MD,
            equipment_rect.width, 200
        )
        self.stats_card = InfoCard(
            stats_rect.x, stats_rect.y, stats_rect.width,
            "Character Stats", "Current health, mana, and other vital statistics",
            self.modern_fonts, expandable=True
        )
    
    def draw_inventory_screen(self, surface: pygame.Surface, player):
        """Enhanced inventory with modern components."""
        surface.fill(ModernUITheme.SURFACE_PRIMARY)
        
        # Modern title
        title_surf = self.modern_fonts['title'].render(f"{player.name}'s Inventory", True, ModernUITheme.TEXT_ACCENT)
        title_rect = title_surf.get_rect(centerx=self.screen_width // 2, top=20)
        surface.blit(title_surf, title_rect)
        
        # Modern inventory grid
        self.inventory_grid.draw(surface)
        
        # Equipment and stats cards
        self.equipment_card.draw(surface)
        self.stats_card.draw(surface)
        
        # Modern progress bars for stats
        self._draw_modern_stat_bars(surface, player)
        
        # Modern instructions
        self._draw_modern_inventory_instructions(surface)
    
    def _draw_modern_stat_bars(self, surface: pygame.Surface, player):
        """Draw modern health/mana bars."""
        bar_width = 200
        bar_height = 8
        bar_x = self.stats_card.content_rect.x
        bar_y = self.stats_card.content_rect.y + 50
        
        # Health bar
        hp_bar = ModernProgressBar(
            pygame.Rect(bar_x, bar_y, bar_width, bar_height),
            max_value=player.max_hp,
            current_value=player.hp,
            color=ModernUITheme.ERROR if player.hp < player.max_hp * 0.3 else ModernUITheme.SUCCESS
        )
        hp_bar.draw(surface)
        
        # HP label
        hp_text = f"Health: {player.hp}/{player.max_hp}"
        hp_surf = self.modern_fonts['small'].render(hp_text, True, ModernUITheme.TEXT_PRIMARY)
        surface.blit(hp_surf, (bar_x, bar_y - 20))
        
        # Experience bar
        if hasattr(player, 'xp') and hasattr(player, 'xp_to_next_level'):
            xp_bar_y = bar_y + 40
            xp_bar = ModernProgressBar(
                pygame.Rect(bar_x, xp_bar_y, bar_width, bar_height),
                max_value=player.xp_to_next_level,
                current_value=player.xp,
                color=ModernUITheme.INFO
            )
            xp_bar.draw(surface)
            
            xp_text = f"Experience: {player.xp}/{player.xp_to_next_level}"
            xp_surf = self.modern_fonts['small'].render(xp_text, True, ModernUITheme.TEXT_PRIMARY)
            surface.blit(xp_surf, (bar_x, xp_bar_y - 20))
    
    def _draw_modern_inventory_instructions(self, surface: pygame.Surface):
        """Modern instruction panel."""
        instructions = [
            "Drag items to rearrange",
            "Right-click for actions", 
            "ESC to return to game"
        ]
        
        panel_rect = pygame.Rect(
            ModernUITheme.SPACING_MD,
            self.screen_height - 80,
            300, 60
        )
        
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel_surface.fill((*ModernUITheme.SURFACE_ELEVATED, 180))
        surface.blit(panel_surface, panel_rect)
        
        inst_y = panel_rect.y + ModernUITheme.SPACING_SM
        for instruction in instructions:
            inst_surf = self.modern_fonts['small'].render(instruction, True, ModernUITheme.TEXT_PRIMARY)
            surface.blit(inst_surf, (panel_rect.x + ModernUITheme.SPACING_SM, inst_y))
            inst_y += 18

class ModernizedGearSelection(GearSelector):
    """Modernized gear selection with better UX."""
    
    def __init__(self, player, screen: pygame.Surface, font_file: str):
        super().__init__(player, screen, font_file)
        
        # Add modern components
        self.layout = ResponsiveLayout(self.screen_width, self.screen_height)
        self.modern_fonts = create_modern_fonts(font_file, self.layout)
        self.notification_manager = ModernNotificationManager(self.screen_width)
        
        # Modern category cards
        self.category_cards = self._create_category_cards()
        
        # Modern shopping cart
        cart_rect = pygame.Rect(
            self.screen_width - 300 - ModernUITheme.SPACING_MD,
            100, 280, 400
        )
        self.shopping_cart = InfoCard(
            cart_rect.x, cart_rect.y, cart_rect.width,
            "Shopping Cart", "Items ready for purchase",
            self.modern_fonts, expandable=True
        )
    
    def _create_category_cards(self):
        """Create modern category selection cards."""
        categories = self._get_categories()
        cards = {}
        
        cards_per_row = min(3, len(categories))
        card_width = (self.layout.content_width - (cards_per_row - 1) * self.layout.gutter) // cards_per_row
        card_height = 120
        
        for i, category in enumerate(categories):
            if category == "Review & Finish":
                continue
                
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = self.layout.margin + col * (card_width + self.layout.gutter)
            y = 120 + row * (card_height + self.layout.gutter)
            
            cards[category] = InfoCard(
                x, y, card_width, category,
                self._get_category_description(category),
                self.modern_fonts, expandable=False
            )
        
        return cards
    
    def _get_category_description(self, category: str) -> str:
        """Get description for category."""
        descriptions = {
            "General": "Basic supplies and tools",
            "Weapons": "Combat equipment", 
            "Armor": "Protective gear",
            "Kits": "Complete equipment sets"
        }
        return descriptions.get(category, "Equipment category")
    
    def draw(self, surface: pygame.Surface):
        """Enhanced gear selection with modern UI."""
        surface.fill(ModernUITheme.SURFACE_PRIMARY)
        
        # Modern title
        title_surf = self.modern_fonts['title'].render("Equip Your Adventure", True, ModernUITheme.TEXT_ACCENT)
        title_rect = title_surf.get_rect(centerx=self.screen_width // 2, top=20)
        surface.blit(title_surf, title_rect)
        
        # Draw category cards
        if self.state == GearSelectionState.CATEGORY_SELECTION:
            for category, card in self.category_cards.items():
                # Highlight selected category
                if category == self.current_category:
                    highlight_surface = pygame.Surface((card.rect.width, card.rect.height), pygame.SRCALPHA)
                    highlight_surface.fill((*ModernUITheme.INTERACTIVE_ACTIVE, 50))
                    surface.blit(highlight_surface, card.rect)
                
                card.draw(surface)
        
        # Shopping cart
        self.shopping_cart.draw(surface)
        
        # Player info with modern styling
        self._draw_modern_player_info(surface)
        
        # Modern notifications
        self.notification_manager.update(1/60)
        self.notification_manager.draw(surface)
    
    def _draw_modern_player_info(self, surface: pygame.Surface):
        """Modern player information panel."""
        info_rect = pygame.Rect(
            ModernUITheme.SPACING_MD, 
            self.screen_height - 120,
            350, 100
        )
        
        info_card = ModernCard(
            info_rect.x, info_rect.y,
            info_rect.width, info_rect.height,
            elevated=True
        )
        info_card.draw_background(surface)
        
        content_y = info_card.content_rect.y
        
        # Player name
        name_surf = self.modern_fonts['heading'].render(self.player.name, True, ModernUITheme.TEXT_ACCENT)
        surface.blit(name_surf, (info_card.content_rect.x, content_y))
        content_y += name_surf.get_height() + 5
        
        # Class
        class_surf = self.modern_fonts['body'].render(f"{self.player.character_class}", True, ModernUITheme.TEXT_PRIMARY)
        surface.blit(class_surf, (info_card.content_rect.x, content_y))
        content_y += class_surf.get_height() + 10
        
        # Gold with progress bar showing spending
        gold_text = f"Gold: {self.gold:.1f} gp"
        gold_surf = self.modern_fonts['body'].render(gold_text, True, ModernUITheme.WARNING)
        surface.blit(gold_surf, (info_card.content_rect.x, content_y))
        
        # Gear capacity bar
        capacity_y = content_y + 25
        capacity_bar = ModernProgressBar(
            pygame.Rect(info_card.content_rect.x, capacity_y, 200, 6),
            max_value=self.max_gear_slots,
            current_value=self.used_gear_slots,
            color=ModernUITheme.WARNING if self.used_gear_slots > self.max_gear_slots * 0.8 else ModernUITheme.SUCCESS
        )
        capacity_bar.draw(surface)

# Integration function to upgrade existing UI systems
def upgrade_ui_system(main_app):
    """Upgrade the main application to use modern UI components."""
    
    # Replace character creation
    def create_modern_character_creation():
        return ModernizedCharacterCreation(main_app.screen, main_app.font_file)
    
    # Replace inventory UI
    def create_modern_inventory():
        return ModernizedInventoryUI(main_app.screen_width, main_app.screen_height, main_app.font_file)
    
    # Replace gear selection
    def create_modern_gear_selection(player):
        return ModernizedGearSelection(player, main_app.screen, main_app.font_file)
    
    # Add notification system to main app
    main_app.notification_manager = ModernNotificationManager(main_app.screen_width)
    
    # Return the new creators
    return {
        'character_creation': create_modern_character_creation,
        'inventory_ui': create_modern_inventory,
        'gear_selection': create_modern_gear_selection
    }

# Usage example for integrating with your main.py
"""
To integrate these modern UI components into your existing main.py:

1. In DungeonExplorer.__init__():
   # Add this after creating existing UI components
   self.modern_ui_creators = upgrade_ui_system(self)
   
2. In start_character_creation():
   # Replace the old character creation with:
   modern_creator = self.modern_ui_creators['character_creation']()
   created_player = run_enhanced_character_creation_with_modern_ui(modern_creator, self.screen)

3. In handle_events() for inventory:
   # Replace old inventory with:
   if event.key == pygame.K_i:
       self.modern_inventory_ui = self.modern_ui_creators['inventory_ui']()
       self.game_state = GameState.INVENTORY

4. Add notification support:
   # In your main game loop update():
   if hasattr(self, 'notification_manager'):
       self.notification_manager.update(1/60)
   
   # In your main draw loop:
   if hasattr(self, 'notification_manager'):
       self.notification_manager.draw(self.screen)
"""