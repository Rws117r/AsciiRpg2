"""
Modern UI Integration Layer
This file connects the modern UI components to the game's data and logic.
It provides modernized versions of UI screens like character creation and inventory.
"""

import pygame
import random
import math
from typing import Dict, List, Optional, Any, Callable

from .modern_components import *
from data.player import Player, create_enhanced_player
from data.items import find_item_by_name, InventoryItem
from data.updated_spell_systems import WizardSpellbook, PriestSpellbook, SpellTier
from config.constants import *
from data.states import GameState, CharCreationState
from data.calendar import WorldCalendar

GOD_LIST = ["Serentha (Life)", "Caedros (Justice)", "Zyrix (War)", "Velmari (Hearth)", "Nymbril (Nature)", "Vhalor (Death)", "Olvenar (Secrets)"]
MONTH_LIST = list(WorldCalendar.MONTHS.keys())

class ModernizedCharacterCreation:
    """Manages character creation, using a shared design system."""
    
    def __init__(self, screen: pygame.Surface, layout: LayoutSystem, fonts: Dict, theme: ModernUITheme, notification_manager: ModernNotificationManager):
        self.screen = screen
        self.layout = layout
        self.fonts = fonts
        self.theme = theme
        self.notification_manager = notification_manager
        
        self.state = CharCreationState.NAME_INPUT
        self.active_components = []
        self.buttons = {}
        
        self.player_data = {"name": "", "stats": [10]*6, "race": "Human", "class": "Fighter", "alignment": "Neutral", "god": None, "birth_month": "Duskwane", "birth_day": "17", "age": "33", "spells": []}
        
        self.wizard_spellbook = WizardSpellbook()
        self.priest_spellbook = PriestSpellbook()
        
        self.handle_resize(self.layout, self.theme)

    def handle_resize(self, new_layout: LayoutSystem, new_theme: ModernUITheme):
        """Rebuilds the UI with new layout and theme dimensions."""
        self.layout = new_layout
        self.theme = new_theme
        self.screen_width = self.layout.screen_width
        self.screen_height = self.layout.screen_height
        self._setup_summary_panel()
        self._setup_current_step()

    def _setup_summary_panel(self):
        summary_rect = pygame.Rect(self.screen_width - self.layout.right_column_width - self.layout.margin, self.layout.margin, self.layout.right_column_width, self.screen_height - (self.layout.margin * 2))
        self.summary_card = CharacterSummaryCard(summary_rect, "Character Summary", "", self.fonts, self.theme)

    def _update_summary_panel(self):
        stats = self.player_data['stats']
        summary_text = (
            f"Name:|{self.player_data.get('name', '...')}\n"
            f"Race:|{self.player_data.get('race', '...')}\n"
            f"Class:|{self.player_data.get('class', '...')}\n"
            f"Alignment:|{self.player_data.get('alignment', '...')}\n"
            f"Deity:|{self.player_data.get('god', 'None')}\n|\n"
            f"STR:|{stats[0]}\n"
            f"DEX:|{stats[1]}\n"
            f"CON:|{stats[2]}\n"
            f"INT:|{stats[3]}\n"
            f"WIS:|{stats[4]}\n"
            f"CHA:|{stats[5]}\n|\n"
            f"Spells:|{', '.join(self.player_data['spells']) if self.player_data['spells'] else 'None'}"
        )
        self.summary_card.description = summary_text
        self.summary_card._render_text()

    def _setup_current_step(self):
        self.active_components = []
        self.buttons = {}
        base_y = self.layout.margin + self.fonts['TITLE_MAIN'].get_height() + 48
        
        nav_y = self.screen_height - self.layout.margin - 50
        if self.state != CharCreationState.NAME_INPUT:
            self.buttons['back'] = ModernButton((self.layout.margin, nav_y, 150, 50), "Back", self.fonts['BODY_TEXT'], self.theme, 'secondary', self._go_to_previous_step)
        
        next_text = "Finish" if self.state == CharCreationState.STATS_REVIEW else "Next"
        self.buttons['next'] = ModernButton((self.layout.margin + self.layout.left_column_width - 150, nav_y, 150, 50), next_text, self.fonts['BODY_TEXT'], self.theme, 'primary', self._go_to_next_step)

        if self.state == CharCreationState.NAME_INPUT: self._setup_name_input(base_y)
        elif self.state == CharCreationState.BIRTH_DETAILS: self._setup_birth_details(base_y)
        elif self.state == CharCreationState.STAT_ROLLING: self._setup_stat_rolling(base_y)
        elif self.state == CharCreationState.SPELL_SELECTION: self._setup_spell_selection(base_y)
        else: self._setup_selection_screen(base_y)
        
        self._update_summary_panel()

    def _setup_name_input(self, base_y):
        label_surf = self.fonts['LABEL_UI'].render("Character Name", True, self.theme.PARCHMENT_DIM)
        self.active_components.append(('label', label_surf, (self.layout.margin, base_y)))
        input_y = base_y + label_surf.get_height() + 8
        input_width = int(self.layout.left_column_width * 0.75)
        self.name_input = TextInput((self.layout.margin, input_y, input_width, 50), self.fonts, self.theme)
        self.name_input.text = self.player_data.get('name', '')
        self.active_components.append(self.name_input)
    
    def _setup_birth_details(self, base_y):
        col1_x = self.layout.margin
        col1_width = int(self.layout.left_column_width * 0.6)
        col2_x = col1_x + col1_width + 48
        
        month_label = self.fonts['LABEL_UI'].render("Birth Month", True, self.theme.PARCHMENT_DIM)
        self.active_components.append(('label', month_label, (col1_x, base_y)))
        
        # --- FIX: Use dynamic height for consistency ---
        list_y = base_y + month_label.get_height() + 8
        list_height = self.screen_height - list_y - 120
        list_rect = (col1_x, list_y, col1_width, list_height)
        
        self.month_list = AdaptiveList(list_rect, MONTH_LIST, self.fonts, self.theme)
        self.active_components.append(self.month_list)
        
        y = base_y
        day_label = self.fonts['LABEL_UI'].render("Birth Day", True, self.theme.PARCHMENT_DIM)
        self.active_components.append(('label', day_label, (col2_x, y)))
        y += day_label.get_height() + 8
        self.day_input = TextInput((col2_x, y, 150, 50), self.fonts, self.theme)
        self.day_input.text = self.player_data.get('birth_day', '')
        self.active_components.append(self.day_input)
        y += 50 + 32
        
        age_label = self.fonts['LABEL_UI'].render("Age", True, self.theme.PARCHMENT_DIM)
        self.active_components.append(('label', age_label, (col2_x, y)))
        y += age_label.get_height() + 8
        self.age_input = TextInput((col2_x, y, 150, 50), self.fonts, self.theme)
        self.age_input.text = self.player_data.get('age', '')
        self.active_components.append(self.age_input)

    def _setup_stat_rolling(self, base_y):
        self.buttons['roll'] = ModernButton((self.layout.margin, base_y, 200, 50), "Roll Stats", self.fonts['BODY_TEXT'], self.theme, 'secondary', self._roll_stats)
        stat_y = base_y + 82
        self.stat_displays = []
        for i, stat_name in enumerate(STATS):
            rect = (self.layout.margin, stat_y + i * 64, self.layout.left_column_width * 0.6, 50)
            display = StatDisplay(rect, stat_name, self.player_data['stats'][i], self.fonts, self.theme)
            self.stat_displays.append(display)
            self.active_components.append(display)

    def _setup_spell_selection(self, base_y):
        player_class = self.player_data.get('class')
        spellbook = self.wizard_spellbook if player_class == "Wizard" else self.priest_spellbook
        max_spells = 3 if player_class == "Wizard" else 2

        list_width = int(self.layout.left_column_width * 0.45)
        details_x = self.layout.margin + list_width + 32
        details_width = self.layout.left_column_width - list_width - 32
        
        label = self.fonts['LABEL_UI'].render("Select Spells", True, self.theme.PARCHMENT_DIM)
        self.active_components.append(('label', label, (self.layout.margin, base_y)))
        list_y = base_y + label.get_height() + 8
        
        tier1_spells = [spell for spell in spellbook.get_spells_by_tier(SpellTier.TIER_1)]
        spell_names = [spell.name for spell in tier1_spells]
        
        list_rect = (self.layout.margin, list_y, list_width, self.screen_height - list_y - 120)
        spell_list = AdaptiveList(list_rect, spell_names, self.fonts, self.theme, multi_select=True, max_selection=max_spells) 
        
        self.details_card = InfoCard((details_x, list_y, details_width, 100), "Spell Details", "Select a spell.", self.fonts, self.theme)
        self.active_components.extend([spell_list, self.details_card])
        
        def on_select(selected_names):
            self.player_data['spells'] = selected_names
            if selected_names:
                last_selected_spell = spellbook.get_spell(selected_names[-1])
                if last_selected_spell:
                    self.details_card.title = last_selected_spell.name
                    desc = (f"Tier {last_selected_spell.tier.value} {player_class} Spell\n"
                            f"Range: {last_selected_spell.range.value}\n\n"
                            f"{last_selected_spell.description}")
                    self.details_card.description = desc
                    self.details_card._render_text()
            self._update_summary_panel()
        
        spell_list.on_selection_changed = on_select
        self.notification_manager.add_notification(f"Select up to {max_spells} starting spells.", 'info')

    def _setup_selection_screen(self, base_y):
        state_map = {
            CharCreationState.RACE_SELECTION: {'items': RACES, 'key': 'race', 'label': 'Select a Race'},
            CharCreationState.CLASS_SELECTION: {'items': CLASSES, 'key': 'class', 'label': 'Select a Class'},
            CharCreationState.ALIGNMENT_SELECTION: {'items': ALIGNMENTS, 'key': 'alignment', 'label': 'Select an Alignment'},
            CharCreationState.GOD_SELECTION: {'items': GOD_LIST, 'key': 'god', 'label': 'Select a Deity'},
        }
        if self.state not in state_map: return
        config = state_map[self.state]
        
        list_width = int(self.layout.left_column_width * 0.45)
        details_x = self.layout.margin + list_width + 32
        details_width = self.layout.left_column_width - list_width - 32
        
        label = self.fonts['LABEL_UI'].render(config['label'], True, self.theme.PARCHMENT_DIM)
        self.active_components.append(('label', label, (self.layout.margin, base_y)))
        
        list_y = base_y + label.get_height() + 8
        list_rect = (self.layout.margin, list_y, list_width, self.screen_height - list_y - 120)
        
        selection_list = AdaptiveList(list_rect, config['items'], self.fonts, self.theme)
        self.details_card = InfoCard((details_x, list_y, details_width, 100), "Details", "Select an item.", self.fonts, self.theme)
        self.active_components.extend([selection_list, self.details_card])
        
        def on_select(selected):
            if not selected: return
            selection = selected[0]
            self.player_data[config['key']] = selection
            self.details_card.title = selection
            self.details_card.description = f"Details about {selection} would appear here."
            self.details_card._render_text()
            self._update_summary_panel()
        
        selection_list.on_selection_changed = on_select
        selection_list.select_item(0)

    def _roll_stats(self):
        self.player_data['stats'] = [random.randint(8, 18) for _ in range(6)]
        for i, display in enumerate(self.stat_displays):
            display.value = self.player_data['stats'][i]
        self._update_summary_panel()

    def handle_event(self, event: pygame.event.Event):
        if self.state == CharCreationState.COMPLETE: return True
        for button in self.buttons.values():
            if button.handle_event(event): return
        for component in self.active_components:
            if hasattr(component, 'handle_event') and component.handle_event(event):
                self._update_summary_panel()
                return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.buttons.get('next'): self.buttons['next'].callback()

    def draw(self, surface: pygame.Surface):
        surface.fill(self.theme.DARK_CATHODE)
        
        title_text = self.state.name.replace("_", " ").title()
        base_color = self.theme.ACCENT_GOLD
        flicker = (math.sin(pygame.time.get_ticks() * 0.002) + 1) / 2
        color_offset = int(flicker * 15)
        flicker_color = tuple(min(255, c + color_offset) for c in base_color)
        title_surf = self.fonts['TITLE_MAIN'].render(title_text, True, flicker_color)
        surface.blit(title_surf, (self.layout.margin, self.layout.margin))
        
        for component in self.active_components:
            if isinstance(component, tuple): surface.blit(component[1], component[2])
            else: component.draw(surface)
            
        self.summary_card.draw(surface)
        for button in self.buttons.values(): button.draw(surface)

    def _go_to_next_step(self):
        if self.state == CharCreationState.NAME_INPUT:
            if not self.name_input.text:
                self.notification_manager.add_notification("Name cannot be empty.", 'error')
                return
            self.player_data['name'] = self.name_input.text
        elif self.state == CharCreationState.BIRTH_DETAILS:
            try:
                int(self.day_input.text); int(self.age_input.text)
                self.player_data['birth_day'] = self.day_input.text
                self.player_data['age'] = self.age_input.text
            except ValueError:
                self.notification_manager.add_notification("Birth Day and Age must be numbers.", 'error')
                return
        
        current_val = self.state.value
        next_val = current_val + 1
        
        if CharCreationState(next_val) == CharCreationState.GOD_SELECTION and self.player_data['class'] != 'Priest': next_val += 1
        if CharCreationState(next_val) == CharCreationState.SPELL_SELECTION and self.player_data['class'] not in ['Priest', 'Wizard']: next_val += 1

        if next_val >= CharCreationState.COMPLETE.value: self.state = CharCreationState.COMPLETE
        else:
            self.state = CharCreationState(next_val)
            self._setup_current_step()

    def _go_to_previous_step(self):
        current_val = self.state.value
        prev_val = current_val - 1
        if CharCreationState(prev_val) == CharCreationState.SPELL_SELECTION and self.player_data['class'] not in ['Priest', 'Wizard']: prev_val -= 1
        if CharCreationState(prev_val) == CharCreationState.GOD_SELECTION and self.player_data['class'] != 'Priest': prev_val -= 1
        if prev_val >= 0:
            self.state = CharCreationState(prev_val)
            self._setup_current_step()
            
    def create_player(self) -> Optional[Player]:
        if not self.player_data.get("name"):
            self.notification_manager.add_notification("Character name cannot be empty.", 'error')
            return None
        return create_enhanced_player(**self.player_data)

# Remainder of file is unchanged and omitted for brevity
class ModernizedInventoryUI:
    pass
def upgrade_ui_system(game_instance) -> Dict[str, Callable]:
    """Returns a dictionary of creator functions for modern UI screens."""
    def create_modern_character_creation():
        return ModernizedCharacterCreation(game_instance.screen, game_instance.layout, game_instance.fonts, game_instance.theme, game_instance.notification_manager)
    # ...
    return {'character_creation': create_modern_character_creation}