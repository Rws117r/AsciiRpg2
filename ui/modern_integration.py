"""
Modern UI Integration Layer
This file connects the modern UI components to the game's data and logic.
It provides modernized versions of UI screens like character creation and inventory.
"""

import pygame
import random
from typing import Dict, List, Optional, Any, Callable

# Import new modern components and existing systems
from .modern_components import (
    ModernUITheme,
    ResponsiveLayout,
    ModernNotificationManager,
    InfoCard,
    ModernButton,
    TextInput,
    StatDisplay,
    AdaptiveList,
    ModernInventoryGrid,
    SmartTooltip
)
from data.player import Player, create_enhanced_player, get_stat_modifier
from data.items import find_item_by_name, InventoryItem
from data.updated_spell_systems import WizardSpellbook, PriestSpellbook, SpellTier
from data.birth_sign_system import BirthSignCalculator, format_birth_sign_for_display
from config.constants import *
from data.states import GameState, CharCreationState
from data.calendar import WorldCalendar

# --- Constants ---
GOD_LIST = ["Serentha (Life)", "Caedros (Justice)", "Zyrix (War)", "Velmari (Hearth)", "Nymbril (Nature)", "Vhalor (Death)", "Olvenar (Secrets)"]
MONTH_LIST = list(WorldCalendar.MONTHS.keys())

class ModernizedCharacterCreation:
    """
    Manages the entire character creation process using modern UI components.
    This class is driven by an external game loop.
    """
    
    def __init__(self, screen: pygame.Surface, font_file: str):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font_file = font_file
        
        self.layout = ResponsiveLayout(self.screen_width, self.screen_height)
        self.fonts = self.layout.get_fonts(font_file)
        
        self.state = CharCreationState.NAME_INPUT
        
        self.notification_manager = ModernNotificationManager(self.screen_width)
        self.active_components = []
        self.buttons = {}
        self.details_card = None 
        self._setup_summary_panel()
        
        self.player_data = {
            "name": "", "stats": [10, 10, 10, 10, 10, 10], "race": "Human",
            "class": "Fighter", "alignment": "Neutral", "god": None,
            "birth_month": "Duskwane", "birth_day": "17", "age": "33",
            "spells": [], "gold": 0, "inventory": []
        }
        
        self.wizard_spellbook = WizardSpellbook()
        self.priest_spellbook = PriestSpellbook()
        
        self._setup_current_step()

    def _setup_summary_panel(self):
        summary_width = self.layout.column_width * 0.8
        summary_rect = pygame.Rect(
            self.screen_width - summary_width - self.layout.margin,
            self.layout.margin, summary_width, self.screen_height - (self.layout.margin * 2)
        )
        self.summary_card = InfoCard(
            summary_rect.x, summary_rect.y, summary_rect.width,
            "Character Summary", "", self.fonts, expandable=False
        )

    def _update_summary_panel(self):
        spells_str = ", ".join(self.player_data['spells']) if self.player_data['spells'] else "None"
        summary_text = (
            f"Name: {self.player_data.get('name', '...')}\n"
            f"Race: {self.player_data.get('race', '...')}\n"
            f"Class: {self.player_data.get('class', '...')}\n"
            f"Alignment: {self.player_data.get('alignment', '...')}\n"
            f"Deity: {self.player_data.get('god', 'None')}\n\n"
            f"--- Stats ---\n"
            f"STR: {self.player_data['stats'][0]} | DEX: {self.player_data['stats'][1]}\n"
            f"CON: {self.player_data['stats'][2]} | INT: {self.player_data['stats'][3]}\n"
            f"WIS: {self.player_data['stats'][4]} | CHA: {self.player_data['stats'][5]}\n\n"
            f"--- Spells ---\n{spells_str}"
        )
        self.summary_card.description = summary_text
        self.summary_card._render_text()

    def _setup_current_step(self):
        self.active_components = []
        self.buttons = {}
        self.details_card = None
        
        content_width = self.layout.column_width * 1.5
        content_x = self.layout.margin

        if self.state != CharCreationState.NAME_INPUT:
            back_button = ModernButton(
                pygame.Rect(content_x, self.screen_height - 60, 120, 40),
                "Back", self.fonts['body'], variant='secondary', callback=self._go_to_previous_step
            )
            self.buttons['back'] = back_button

        next_text = "Next"
        if self.state == CharCreationState.STATS_REVIEW:
            next_text = "Finish"
        
        next_button = ModernButton(
            pygame.Rect(content_x + content_width - 120, self.screen_height - 60, 120, 40),
            next_text, self.fonts['body'], variant='primary', callback=self._go_to_next_step
        )
        self.buttons['next'] = next_button

        if self.state == CharCreationState.NAME_INPUT: self._setup_name_input(content_x, content_width)
        elif self.state == CharCreationState.BIRTH_DETAILS: self._setup_birth_details(content_x, content_width)
        elif self.state == CharCreationState.STAT_ROLLING: self._setup_stat_rolling(content_x, content_width)
        elif self.state == CharCreationState.RACE_SELECTION: self._setup_selection_list(RACES, 'race', content_x, content_width)
        elif self.state == CharCreationState.CLASS_SELECTION: self._setup_selection_list(CLASSES, 'class', content_x, content_width)
        elif self.state == CharCreationState.ALIGNMENT_SELECTION: self._setup_selection_list(ALIGNMENTS, 'alignment', content_x, content_width)
        elif self.state == CharCreationState.GOD_SELECTION: self._setup_selection_list(GOD_LIST, 'god', content_x, content_width)
        elif self.state == CharCreationState.SPELL_SELECTION: self._setup_spell_selection(content_x, content_width)
        elif self.state == CharCreationState.GEAR_SELECTION: self._setup_gear_selection(content_x, content_width)
        elif self.state == CharCreationState.STATS_REVIEW: self._setup_review_display(content_x, content_width)
        
        self._update_summary_panel()

    def _setup_name_input(self, content_x, content_width):
        self.notification_manager.add_notification("Enter your character's name.", 'info')
        input_rect = pygame.Rect(content_x, 200, content_width, 50)
        self.name_input = TextInput(input_rect, self.fonts, placeholder="Character Name")
        self.active_components.append(self.name_input)

    def _setup_birth_details(self, content_x, content_width):
        self.notification_manager.add_notification("Describe your character's origin.", 'info')
        
        # Starting y-coordinate
        y_pos = 150
        
        # --- Birth Month List ---
        month_label = self.fonts['body'].render("Birth Month", True, ModernUITheme.TEXT_SECONDARY)
        self.active_components.append(('label', month_label, (content_x, y_pos)))
        y_pos += month_label.get_height() + 5
        
        month_list_rect = pygame.Rect(content_x, y_pos, content_width, 250)
        self.month_list = AdaptiveList(month_list_rect, MONTH_LIST, self.fonts)
        def on_month_select(selected): self.player_data['birth_month'] = selected[0] if selected else None
        self.month_list.on_selection_changed = on_month_select
        self.month_list.select_item(MONTH_LIST.index(self.player_data['birth_month']))
        self.active_components.append(self.month_list)
        
        # --- Day & Age Inputs (Robust Approach) ---
        # Position the next elements relative to the bottom of the month list.
        
        # 1. Calculate the Y position for the row with the labels.
        label_row_y = self.month_list.rect.bottom + 25

        day_label = self.fonts['body'].render("Birth Day", True, ModernUITheme.TEXT_SECONDARY)
        age_label = self.fonts['body'].render("Age", True, ModernUITheme.TEXT_SECONDARY)
        input_width = (content_width // 2) - 10
        
        # 2. Place the labels at the newly calculated Y position.
        self.active_components.append(('label', day_label, (content_x, label_row_y)))
        self.active_components.append(('label', age_label, (content_x + input_width + 20, label_row_y)))
        
        # 3. Calculate the Y position for the input boxes, placing them below the labels.
        input_row_y = label_row_y + day_label.get_height() + 5

        # 4. Create and place the input boxes.
        day_input_rect = pygame.Rect(content_x, input_row_y, input_width, 50)
        self.day_input = TextInput(day_input_rect, self.fonts, placeholder="e.g., 17", initial_text=self.player_data['birth_day'])
        self.active_components.append(self.day_input)

        age_input_rect = pygame.Rect(content_x + input_width + 20, input_row_y, input_width, 50)
        self.age_input = TextInput(age_input_rect, self.fonts, placeholder="e.g., 33", initial_text=self.player_data['age'])
        self.active_components.append(self.age_input)

    def _setup_stat_rolling(self, content_x, content_width):
        self.notification_manager.add_notification("Roll for your stats.", 'info')
        roll_button = ModernButton(pygame.Rect(content_x, 150, 150, 40), "Roll Stats", self.fonts['body'], callback=self._roll_stats)
        self.buttons['roll'] = roll_button
        self.stat_displays = []
        y_pos = 220
        for i, stat_name in enumerate(STATS):
            stat_rect = pygame.Rect(content_x, y_pos, content_width, 40)
            stat_display = StatDisplay(stat_rect, stat_name, self.player_data['stats'][i], self.fonts)
            self.stat_displays.append(stat_display)
            self.active_components.append(stat_display)
            y_pos += 50

    def _roll_stats(self):
        self.player_data['stats'] = [random.randint(8, 18) for _ in range(6)]
        for i, display in enumerate(self.stat_displays): display.value = self.player_data['stats'][i]
        self.notification_manager.add_notification("Stats rolled!", 'success', duration=2.0)
        self._update_summary_panel()

    def _setup_selection_list(self, items: List[str], data_key: str, content_x, content_width):
        list_rect = pygame.Rect(content_x, 150, content_width / 2 - 10, self.screen_height - 250)
        selection_list = AdaptiveList(list_rect, items, self.fonts, multi_select=False)
        
        details_rect = pygame.Rect(content_x + list_rect.width + 20, 150, content_width - list_rect.width - 20, self.screen_height - 250)
        self.details_card = InfoCard(details_rect.x, details_rect.y, details_rect.width, "Details", "Select an item to see details.", self.fonts, expandable=False)
        
        def on_select(selected_items):
            if not selected_items: return
            selection = selected_items[0]
            self.player_data[data_key] = selection
            self.details_card.title = selection
            self.details_card.description = f"Details about {selection} would appear here."
            self.details_card._render_text()
            self._update_summary_panel()

        selection_list.on_selection_changed = on_select
        self.active_components.append(selection_list)
        self.active_components.append(self.details_card)
        selection_list.select_item(0)

    def _setup_spell_selection(self, content_x, content_width):
        player_class = self.player_data.get('class')
        spellbook = self.wizard_spellbook if player_class == "Wizard" else self.priest_spellbook
        
        if not spellbook: 
            self._setup_placeholder_step("Spell Selection", "This class does not select spells at creation.", content_x, content_width)
            return

        tier1_spells = [spell for spell in spellbook.get_spells_by_tier(SpellTier.TIER_1)]
        spell_names = [spell.name for spell in tier1_spells]
        
        list_rect = pygame.Rect(content_x, 150, content_width / 2 - 10, self.screen_height - 250)
        spell_list = AdaptiveList(list_rect, spell_names, self.fonts, multi_select=True, max_selection=3)
        
        details_rect = pygame.Rect(content_x + list_rect.width + 20, 150, content_width - list_rect.width - 20, self.screen_height - 250)
        self.details_card = InfoCard(details_rect.x, details_rect.y, details_rect.width, "Spell Details", "Select a spell to see details.", self.fonts, expandable=False)

        def on_select(selected_names):
            self.player_data['spells'] = selected_names
            if selected_names:
                last_selected_spell = spellbook.get_spell(selected_names[-1])
                if last_selected_spell:
                    self.details_card.title = last_selected_spell.name
                    desc = (f"Tier {last_selected_spell.tier.value} {player_class} Spell\n"
                            f"Range: {last_selected_spell.range.value}\n\n"
                            f"{last_selected_spell.description}\n\n"
                            f"LORE-FUELED:\n{last_selected_spell.lore_condition_text}")
                    self.details_card.description = desc
                    self.details_card._render_text()
            self._update_summary_panel()

        spell_list.on_selection_changed = on_select
        self.active_components.append(spell_list)
        self.active_components.append(self.details_card)
        self.notification_manager.add_notification("Select up to 3 starting spells.", 'info')

    def _setup_gear_selection(self, content_x, content_width):
        player_class = self.player_data['class']
        gold = STARTING_GOLD.get(player_class, 0)
        text = (f"As a {player_class}, you begin your journey with:\n\n"
                f"- {gold} gold pieces\n"
                f"- A 'Crawling Kit' with essential supplies.\n\n"
                "An interactive shop is planned for a future update.")
        card = InfoCard(content_x, 150, content_width, "Starting Gear", text, self.fonts, expandable=False)
        self.active_components.append(card)

    def _get_day_of_year(self, month_name, day):
        day_of_year = 0
        for m, d in WorldCalendar.MONTHS.items():
            if m == month_name:
                day_of_year += day
                break
            day_of_year += d
        return day_of_year

    def _setup_review_display(self, content_x, content_width):
        player = self.create_player(finalize=False)
        if not player: 
            self._setup_placeholder_step("Error", "Could not generate character preview.", content_x, content_width)
            return
        
        try:
            day_of_year = self._get_day_of_year(player.birth_month, player.birth_day)
            birth_sign = BirthSignCalculator.calculate_birth_sign(player.birth_year, day_of_year)
            review_text = "\n".join(format_birth_sign_for_display(birth_sign))
        except (ValueError, TypeError):
             review_text = "Invalid birth date provided.\nPlease go back and correct it."

        review_card = InfoCard(content_x, 150, content_width, f"The Story of {player.name}", review_text, self.fonts)
        self.active_components.append(review_card)

    def _go_to_next_step(self):
        current_state_val = self.state.value
        
        if self.state == CharCreationState.NAME_INPUT:
            self.player_data['name'] = self.name_input.text
            if not self.player_data['name']:
                self.notification_manager.add_notification("Name cannot be empty.", 'error'); return
        elif self.state == CharCreationState.BIRTH_DETAILS:
            self.player_data['birth_day'] = self.day_input.text
            self.player_data['age'] = self.age_input.text
            try:
                int(self.player_data['birth_day']); int(self.player_data['age'])
            except ValueError:
                self.notification_manager.add_notification("Day and Age must be numbers.", 'error'); return

        if self.state == CharCreationState.STATS_REVIEW:
            self.state = CharCreationState.COMPLETE; return

        next_state_val = current_state_val + 1
        
        if CharCreationState(next_state_val) == CharCreationState.GOD_SELECTION and self.player_data['class'] != 'Priest': next_state_val += 1
        if CharCreationState(next_state_val) == CharCreationState.SPELL_SELECTION and self.player_data['class'] not in ['Priest', 'Wizard']: next_state_val += 1

        if next_state_val >= CharCreationState.COMPLETE.value: self.state = CharCreationState.STATS_REVIEW
        else: self.state = CharCreationState(next_state_val)
        
        self._setup_current_step()

    def _go_to_previous_step(self):
        current_state_val = self.state.value
        prev_state_val = current_state_val - 1

        if CharCreationState(prev_state_val) == CharCreationState.SPELL_SELECTION and self.player_data['class'] not in ['Priest', 'Wizard']: prev_state_val -= 1
        if CharCreationState(prev_state_val) == CharCreationState.GOD_SELECTION and self.player_data['class'] != 'Priest': prev_state_val -= 1
        
        if prev_state_val >= 0:
            self.state = CharCreationState(prev_state_val)
            self._setup_current_step()

    def handle_event(self, event: pygame.event.Event) -> Optional[bool]:
        if self.state == CharCreationState.COMPLETE: return True

        for component in self.active_components:
            if isinstance(component, tuple) and component[0] == 'label': continue
            if hasattr(component, 'handle_event') and component.handle_event(event):
                self._update_summary_panel(); return
        
        for button in self.buttons.values():
            if button.handle_event(event): return
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.buttons.get('next'):
                self.buttons['next'].callback()
                if self.state == CharCreationState.COMPLETE: return True
                return
            
        return None

    def create_player(self, finalize=True) -> Optional[Player]:
        try:
            player = create_enhanced_player(
                name=self.player_data['name'], race=self.player_data['race'],
                character_class=self.player_data['class'], alignment=self.player_data['alignment'],
                stats=self.player_data['stats'], birth_month=self.player_data['birth_month'],
                birth_day=int(self.player_data['birth_day']), age=int(self.player_data['age'])
            )
        except (ValueError, TypeError):
            if finalize: self.notification_manager.add_notification("Invalid birth date.", 'error')
            return None

        if finalize:
            day_of_year = self._get_day_of_year(player.birth_month, player.birth_day)
            birth_sign = BirthSignCalculator.calculate_birth_sign(player.birth_year, day_of_year)
            player.apply_birth_sign_bonuses(birth_sign)
            player.known_spells = self.player_data['spells']
            player.god = self.player_data['god']
            player.gold = STARTING_GOLD.get(player.character_class, 0)
            kit_item = find_item_by_name("Crawling Kit")
            if kit_item:
                player.inventory.append(InventoryItem(item=kit_item, quantity=1))
        return player

    def draw(self, surface: pygame.Surface):
        surface.fill(ModernUITheme.SURFACE_PRIMARY)
        
        title_text = self.state.name.replace("_", " ").title()
        title_surf = self.fonts['title'].render(title_text, True, ModernUITheme.TEXT_ACCENT)
        title_rect = title_surf.get_rect(centerx=(self.screen_width - self.summary_card.rect.width) / 2, y=self.layout.margin)
        surface.blit(title_surf, title_rect)

        for component in self.active_components:
            if isinstance(component, tuple) and component[0] == 'label':
                surface.blit(component[1], component[2])
            else:
                component.draw(surface)
        
        for button in self.buttons.values(): button.draw(surface)
        
        self.summary_card.draw(surface)
        self.notification_manager.draw(surface)

class ModernizedInventoryUI:
    """Manages the modern inventory screen."""
    
    def __init__(self, screen_width: int, screen_height: int, font_file: str):
        self.layout = ResponsiveLayout(screen_width, screen_height)
        self.fonts = self.layout.get_fonts(font_file)
        self.notification_manager = ModernNotificationManager(screen_width)
        
        self.grid_rect = pygame.Rect(self.layout.margin, 100, self.layout.column_width, self.layout.content_height - 150)
        self.inventory_grid = ModernInventoryGrid(self.grid_rect, self.fonts)
        
        self.details_card = InfoCard(self.layout.margin + self.layout.column_width + self.layout.gutter, 100,
                                     self.layout.column_width, "Item Details", "Hover over an item to see details.",
                                     self.fonts, expandable=False)
        self.tooltip = None

    def update_inventory(self, player: Player):
        self.inventory_grid.items = {}
        for inv_item in player.inventory: self.inventory_grid.add_item(inv_item)

    def handle_event(self, event: pygame.event.Event):
        self.inventory_grid.handle_event(event)
        
        if event.type == pygame.MOUSEMOTION:
            slot = self.inventory_grid.hovered_slot
            if slot and slot in self.inventory_grid.items:
                item = self.inventory_grid.items[slot]
                content = {'title': f"{item.item.name} (x{item.quantity})",
                           'subtitle': f"Category: {item.item.category}",
                           'description': item.item.description}
                self.tooltip = SmartTooltip(pygame.Rect(event.pos[0] + 15, event.pos[1] + 15, 1, 1), content, self.fonts)
                self.tooltip.show()
            else:
                self.tooltip = None

    def draw_inventory_screen(self, surface: pygame.Surface, player: Player):
        surface.fill(ModernUITheme.SURFACE_PRIMARY)
        
        title_surf = self.fonts['title'].render("Inventory", True, ModernUITheme.TEXT_ACCENT)
        surface.blit(title_surf, (self.layout.margin, self.layout.margin))
        
        self.inventory_grid.draw(surface)
        self.details_card.draw(surface)
        
        if self.tooltip: self.tooltip.draw(surface)
        self.notification_manager.draw(surface)

def upgrade_ui_system(game_instance) -> Dict[str, Callable]:
    """Returns a dictionary of creator functions for modern UI screens."""
    def create_modern_character_creation():
        return ModernizedCharacterCreation(game_instance.screen, game_instance.font_file)
    def create_modern_inventory():
        return ModernizedInventoryUI(game_instance.screen_width, game_instance.screen_height, game_instance.font_file)
    return {'character_creation': create_modern_character_creation, 'inventory': create_modern_inventory}