#!/usr/bin/env python3
"""
Dungeon Explorer - Main Entry Point (Fully Modular)
A tabletop-style RPG dungeon crawler with character creation, inventory management, and exploration.
"""

import pygame
import sys
import json
import time
from pathlib import Path
from typing import Optional

# Add the project root to the Python path so we can import our modules
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import our modular components
from config.constants import *
from game.states import GameState
from data.player import Player
from game.dungeon_game import DungeonGame
from ui.character_creation import run_character_creation
from ui.gear_selection import run_gear_selection
from ui.inventory_ui import *
from graphics.tile_renderer import DungeonRenderer, calculate_viewport_parameters, create_fonts_for_zoom

class DungeonExplorer:
    """Main application class using fully modular architecture."""
    
    def __init__(self):
        pygame.init()
        
        # Initialize display
        self.screen_width = INITIAL_VIEWPORT_WIDTH * int(BASE_CELL_SIZE * DEFAULT_ZOOM)
        self.screen_height = INITIAL_VIEWPORT_HEIGHT * int(BASE_CELL_SIZE * DEFAULT_ZOOM) + HUD_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Dungeon Explorer")
        
        # Load dungeon data
        self.dungeon_data = self.load_dungeon_data()
        
        # Initialize fonts
        self.fonts = self.create_fonts()
        
        # Game state
        self.game_state = GameState.MAIN_MENU
        self.player = None
        self.dungeon_game = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        
        # Rendering system
        self.renderer = DungeonRenderer()
        self.zoom_level = DEFAULT_ZOOM
        
        # UI components
        self.inventory_ui = InventoryUI(self.screen_width, self.screen_height, FONT_FILE)
        self.container_view_ui = ContainerViewUI(self.screen_width, self.screen_height, FONT_FILE)
        self.item_action_ui = ItemActionUI(self.screen_width, self.screen_height, FONT_FILE)
        self.equipment_ui = EquipmentUI(self.screen_width, self.screen_height, FONT_FILE)
        self.equipment_selection_ui = EquipmentSelectionUI(self.screen_width, self.screen_height, FONT_FILE)
        
        # UI state
        self.current_containers = []
        self.current_container = None
        self.equipment_selection_mode = False
        self.equipment_available_items = []
        
        # Spell system
        self.current_spell = ""
        self.spell_target_pos = (0, 0)
    
    def load_dungeon_data(self) -> dict:
        """Load dungeon configuration from JSON file."""
        try:
            with open(JSON_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: '{JSON_FILE}' not found.")
            self.running = False
            return {}
    
    def create_fonts(self) -> dict:
        """Create and return font dictionary."""
        return {
            'large': pygame.font.Font(FONT_FILE, 28),
            'medium': pygame.font.Font(FONT_FILE, 20),
            'small': pygame.font.Font(FONT_FILE, 14),
            'coords': pygame.font.Font(FONT_FILE, 16),
            'timer': pygame.font.Font(FONT_FILE, 22),
            'spell_menu': pygame.font.Font(FONT_FILE, 20),
            'title': pygame.font.Font(FONT_FILE, 36)
        }
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    self.screen_width, self.screen_height = event.size
                    self._update_ui_components()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._handle_escape_key()
                
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                
                else:
                    self._handle_keydown(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GameState.MAIN_MENU:
                    self.handle_main_menu_click(event.pos)
    
    def _handle_escape_key(self):
        """Handle escape key based on current state."""
        if self.game_state == GameState.MAIN_MENU:
            self.running = False
        elif self.game_state == GameState.PLAYING:
            self.running = False
        elif self.game_state in [GameState.SPELL_MENU, GameState.SPELL_TARGETING]:
            self.game_state = GameState.PLAYING
        elif self.game_state == GameState.INVENTORY:
            self.game_state = GameState.PLAYING
        elif self.game_state == GameState.CONTAINER_VIEW:
            self.game_state = GameState.INVENTORY
        elif self.game_state == GameState.ITEM_ACTION:
            self.game_state = GameState.CONTAINER_VIEW
        elif self.game_state == GameState.EQUIPMENT:
            if self.equipment_selection_mode:
                self.equipment_selection_mode = False
            else:
                self.game_state = GameState.PLAYING
    
    def _handle_keydown(self, event):
        """Handle keyboard input based on game state."""
        if self.game_state == GameState.PLAYING:
            self._handle_playing_input(event)
        elif self.game_state == GameState.SPELL_MENU:
            self._handle_spell_menu_input(event)
        elif self.game_state == GameState.SPELL_TARGETING:
            self._handle_spell_targeting_input(event)
        elif self.game_state == GameState.INVENTORY:
            self._handle_inventory_input(event)
        elif self.game_state == GameState.CONTAINER_VIEW:
            self._handle_container_view_input(event)
        elif self.game_state == GameState.ITEM_ACTION:
            self._handle_item_action_input(event)
        elif self.game_state == GameState.EQUIPMENT:
            self._handle_equipment_input(event)
    
    def _handle_playing_input(self, event):
        """Handle input during gameplay."""
        if event.key in [pygame.K_PLUS, pygame.K_EQUALS]:
            self.zoom_level = min(self.zoom_level + ZOOM_STEP, MAX_ZOOM)
        elif event.key == pygame.K_MINUS:
            self.zoom_level = max(self.zoom_level - ZOOM_STEP, MIN_ZOOM)
        elif event.key == pygame.K_m:
            self.game_state = GameState.SPELL_MENU
            self.spell_target_pos = self.dungeon_game.get_player_position()
        elif event.key == pygame.K_i:
            self.game_state = GameState.INVENTORY
            self.current_containers = organize_player_inventory(self.player)
            self.inventory_ui.set_containers(self.current_containers)
        elif event.key == pygame.K_e:
            self.game_state = GameState.EQUIPMENT
            self.equipment_selection_mode = False
        elif event.key == pygame.K_SPACE:
            self.dungeon_game.handle_door_interaction()
        else:
            self._handle_movement_input(event)
    
    def _handle_movement_input(self, event):
        """Handle player movement input."""
        direction = None
        if event.key in [pygame.K_UP, pygame.K_w]:
            direction = (0, -1)
        elif event.key in [pygame.K_DOWN, pygame.K_s]:
            direction = (0, 1)
        elif event.key in [pygame.K_LEFT, pygame.K_a]:
            direction = (-1, 0)
        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
            direction = (1, 0)
        
        if direction:
            self.dungeon_game.handle_player_movement(direction)
    
    def _handle_spell_menu_input(self, event):
        """Handle spell menu input."""
        if event.key == pygame.K_1:
            self.current_spell = "Burning Hands"
            self.game_state = GameState.SPELL_TARGETING
    
    def _handle_spell_targeting_input(self, event):
        """Handle spell targeting input."""
        direction = None
        if event.key in [pygame.K_UP, pygame.K_w]:
            direction = (0, -1)
        elif event.key in [pygame.K_DOWN, pygame.K_s]:
            direction = (0, 1)
        elif event.key in [pygame.K_LEFT, pygame.K_a]:
            direction = (-1, 0)
        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
            direction = (1, 0)
        elif event.key == pygame.K_RETURN:
            self.dungeon_game.handle_spell_casting(self.current_spell, self.spell_target_pos)
            self.game_state = GameState.PLAYING
        
        if direction:
            self.dungeon_game.handle_spell_targeting_movement(direction, self.current_spell)
            self.spell_target_pos = self.dungeon_game.spell_target_pos
    
    def _handle_inventory_input(self, event):
        """Handle inventory screen input."""
        if event.key == pygame.K_UP:
            self.inventory_ui.handle_navigation(-1)
        elif event.key == pygame.K_DOWN:
            self.inventory_ui.handle_navigation(1)
        elif event.key == pygame.K_RETURN:
            self.current_container = self.inventory_ui.get_selected_container()
            if self.current_container:
                self.container_view_ui.selected_index = 0
                self.game_state = GameState.CONTAINER_VIEW
    
    def _handle_container_view_input(self, event):
        """Handle container view input."""
        if event.key == pygame.K_UP:
            self.container_view_ui.handle_navigation(-1, self.current_container)
        elif event.key == pygame.K_DOWN:
            self.container_view_ui.handle_navigation(1, self.current_container)
        elif event.key == pygame.K_RETURN:
            selected_item = self.container_view_ui.get_selected_item(self.current_container)
            if selected_item:
                self.item_action_ui.selected_action = 0
                self.game_state = GameState.ITEM_ACTION
    
    def _handle_item_action_input(self, event):
        """Handle item action input."""
        if event.key == pygame.K_UP:
            self.item_action_ui.handle_navigation(-1)
        elif event.key == pygame.K_DOWN:
            self.item_action_ui.handle_navigation(1)
        elif event.key == pygame.K_RETURN:
            selected_item = self.container_view_ui.get_selected_item(self.current_container)
            action = self.item_action_ui.get_selected_action()
            if selected_item:
                handle_item_action(self.player, selected_item, action, self.dungeon_game)
            self.game_state = GameState.CONTAINER_VIEW
    
    def _handle_equipment_input(self, event):
        """Handle equipment screen input."""
        if not self.equipment_selection_mode:
            if event.key == pygame.K_UP:
                self.equipment_ui.handle_slot_navigation(-1)
            elif event.key == pygame.K_DOWN:
                self.equipment_ui.handle_slot_navigation(1)
            elif event.key == pygame.K_RETURN:
                self.equipment_selection_mode = True
                self.equipment_selection_ui.selected_index = 0
        else:
            if event.key == pygame.K_UP:
                self.equipment_selection_ui.handle_navigation(-1, self.equipment_available_items)
            elif event.key == pygame.K_DOWN:
                self.equipment_selection_ui.handle_navigation(1, self.equipment_available_items)
            elif event.key == pygame.K_RETURN:
                selected_item = self.equipment_selection_ui.get_selected_item(self.equipment_available_items)
                slot = self.equipment_ui.get_selected_slot()
                
                if selected_item is None:
                    # Unequip
                    self.dungeon_game.unequip_item(slot)
                else:
                    # Equip
                    self.dungeon_game.equip_item(selected_item, slot)
                
                self.equipment_selection_mode = False
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            self.screen_width, self.screen_height = info.current_w, info.current_h
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        
        self._update_ui_components()
    
    def _update_ui_components(self):
        """Update UI components when screen size changes."""
        self.inventory_ui = InventoryUI(self.screen_width, self.screen_height, FONT_FILE)
        self.container_view_ui = ContainerViewUI(self.screen_width, self.screen_height, FONT_FILE)
        self.item_action_ui = ItemActionUI(self.screen_width, self.screen_height, FONT_FILE)
        self.equipment_ui = EquipmentUI(self.screen_width, self.screen_height, FONT_FILE)
        self.equipment_selection_ui = EquipmentSelectionUI(self.screen_width, self.screen_height, FONT_FILE)
    
    def handle_main_menu_click(self, pos: tuple):
        """Handle clicks on the main menu."""
        button_width = 300
        button_height = 60
        start_button_rect = pygame.Rect(
            (self.screen_width - button_width) / 2, 
            self.screen_height * 0.5, 
            button_width, 
            button_height
        )
        
        if start_button_rect.collidepoint(pos):
            self.start_character_creation()
    
    def start_character_creation(self):
        """Start the character creation process."""
        # Store current fullscreen state
        was_fullscreen = self.fullscreen
        current_width = self.screen_width
        current_height = self.screen_height
        
        # Hide current display for character creation
        pygame.display.quit()
        
        # Run character creation
        created_player = run_character_creation(current_width, current_height, FONT_FILE)
        
        if created_player is None:
            # Character creation was cancelled
            self.running = False
            return
        
        # Character creation successful - restore display with same fullscreen state
        if was_fullscreen:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            self.screen_width = info.current_w
            self.screen_height = info.current_h
            self.fullscreen = True
        else:
            self.screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
            self.screen_width = current_width
            self.screen_height = current_height
            self.fullscreen = False
        
        pygame.display.set_caption(f"{self.dungeon_data.get('title', 'Dungeon')}")
        
        self.player = created_player
        
        # Initialize dungeon game with new modular system
        self.dungeon_game = DungeonGame(self.dungeon_data, self.player)
        
        self.game_state = GameState.PLAYING
        
        print(f"✅ Character created: {self.player.name} the {self.player.race} {self.player.character_class}")
        print(f"✅ Using modular dungeon system")
    
    def draw_main_menu(self):
        """Draw the main menu screen."""
        self.screen.fill(COLOR_BLACK)  # Changed back to black background
        
        # Title
        title_surf = self.fonts['large'].render("Dungeon Explorer", True, COLOR_WHITE)  # White text on black background
        title_rect = title_surf.get_rect(centerx=self.screen_width/2, top=self.screen_height * 0.2)
        self.screen.blit(title_surf, title_rect)

        # Start button - make it a filled button with white text
        button_width = 300
        button_height = 60
        start_button_rect = pygame.Rect(
            (self.screen_width - button_width)/2, 
            self.screen_height * 0.5, 
            button_width, 
            button_height
        )
        
        # Fill button background
        pygame.draw.rect(self.screen, COLOR_BUTTON_NORMAL, start_button_rect)
        pygame.draw.rect(self.screen, COLOR_WHITE, start_button_rect, 2)
        
        button_text_surf = self.fonts['medium'].render("Create New Character", True, COLOR_WHITE)  # White text on button
        button_text_rect = button_text_surf.get_rect(center=start_button_rect.center)
        self.screen.blit(button_text_surf, button_text_rect)
        
        # Instructions
        inst_text = "Press ESC to quit | F11 for fullscreen"
        inst_surf = self.fonts['medium'].render(inst_text, True, COLOR_WHITE)  # White text on black background
        inst_rect = inst_surf.get_rect(centerx=self.screen_width/2, bottom=self.screen_height * 0.9)
        self.screen.blit(inst_surf, inst_rect)
    
    def draw_spell_menu(self):
        """Draw the spell selection menu."""
        menu_width = 300
        menu_height = 200
        screen_width, screen_height = self.screen.get_size()
        
        menu_rect = pygame.Rect((screen_width - menu_width) / 2, (screen_height - HUD_HEIGHT - menu_height) / 2, menu_width, menu_height)
        
        # Draw a solid black background box
        pygame.draw.rect(self.screen, COLOR_BLACK, menu_rect)
        pygame.draw.rect(self.screen, COLOR_WHITE, menu_rect, 1)
        
        # Draw title
        title_surf = self.fonts['spell_menu'].render("Choose a Spell", True, COLOR_WHITE)
        title_rect = title_surf.get_rect(centerx=menu_rect.centerx, top=menu_rect.top + 10)
        self.screen.blit(title_surf, title_rect)
        
        # Draw spell options (simplified for now)
        spells = ["Burning Hands"]
        for i, spell_name in enumerate(spells):
            text = f"{i+1}. {spell_name}"
            spell_surf = self.fonts['spell_menu'].render(text, True, COLOR_WHITE)
            spell_rect = spell_surf.get_rect(left=menu_rect.left + 20, top=title_rect.bottom + 10 + (i * 30))
            self.screen.blit(spell_surf, spell_rect)
    
    def draw_hud(self):
        """Draw the player information HUD at the bottom of the screen."""
        screen_width, screen_height = self.screen.get_size()
        hud_rect = pygame.Rect(0, screen_height - HUD_HEIGHT, screen_width, HUD_HEIGHT)
        
        # Draw outer black box
        pygame.draw.rect(self.screen, COLOR_BLACK, hud_rect)
        
        # Draw inner white box
        inner_margin = 4
        inner_rect = hud_rect.inflate(-inner_margin * 2, -inner_margin * 2)
        pygame.draw.rect(self.screen, COLOR_WHITE, inner_rect, width=1)
        
        # --- Left Section: Character Info ---
        left_padding = inner_rect.left + 20
        name_surf = self.fonts['large'].render(self.player.name, True, COLOR_WHITE)
        name_rect = name_surf.get_rect(left=left_padding, top=inner_rect.top + 10)
        self.screen.blit(name_surf, name_rect)

        title_surf = self.fonts['medium'].render(self.player.title, True, COLOR_WHITE)
        title_rect = title_surf.get_rect(left=left_padding, top=name_rect.bottom + 2)
        self.screen.blit(title_surf, title_rect)

        info_text = f"Lvl {self.player.level} {self.player.alignment} {self.player.race} {self.player.character_class}"
        info_surf = self.fonts['small'].render(info_text, True, COLOR_WHITE)
        info_rect = info_surf.get_rect(left=left_padding, bottom=inner_rect.bottom - 10)
        self.screen.blit(info_surf, info_rect)

        # --- Right Section: Vitals & Resources ---
        right_padding = inner_rect.right - 20
        bar_width = 150 
        bar_height = 15
        
        # HP Bar
        hp_y = inner_rect.top + 15
        
        hp_value_surf = self.fonts['medium'].render(f"{self.player.hp}/{self.player.max_hp}", True, COLOR_WHITE)
        hp_value_rect = hp_value_surf.get_rect(right=right_padding, centery=hp_y + bar_height/2)
        self.screen.blit(hp_value_surf, hp_value_rect)
        
        hp_bar_rect = pygame.Rect(hp_value_rect.left - bar_width - 10, hp_y, bar_width, bar_height)
        hp_ratio = self.player.hp / self.player.max_hp
        hp_bar_fill_width = int(bar_width * hp_ratio)
        pygame.draw.rect(self.screen, COLOR_BAR_BG, hp_bar_rect)
        pygame.draw.rect(self.screen, COLOR_HP_BAR, (hp_bar_rect.x, hp_bar_rect.y, hp_bar_fill_width, bar_height))

        hp_text_surf = self.fonts['medium'].render(f'{UI_ICONS["HEART"]} HP', True, COLOR_HP_BAR)
        hp_text_rect = hp_text_surf.get_rect(right=hp_bar_rect.left - 10, centery=hp_bar_rect.centery)
        self.screen.blit(hp_text_surf, hp_text_rect)

        # XP Bar
        xp_y = hp_y + bar_height + 10
        
        xp_bar_rect = pygame.Rect(hp_bar_rect.x, xp_y, bar_width, bar_height)
        xp_ratio = self.player.xp / self.player.xp_to_next_level
        xp_bar_fill_width = int(bar_width * xp_ratio)
        pygame.draw.rect(self.screen, COLOR_BAR_BG, xp_bar_rect)
        pygame.draw.rect(self.screen, COLOR_XP_BAR, (xp_bar_rect.x, xp_bar_rect.y, xp_bar_fill_width, bar_height))

        xp_text_surf = self.fonts['medium'].render("XP", True, COLOR_XP_BAR)
        xp_text_rect = xp_text_surf.get_rect(right=xp_bar_rect.left - 10, centery=xp_bar_rect.centery)
        self.screen.blit(xp_text_surf, xp_text_rect)

        # --- Bottom Right: Other Stats ---
        bottom_y = inner_rect.bottom - 10
        
        ac_icon_surf = self.fonts['large'].render(UI_ICONS["SHIELD"], True, COLOR_WHITE)
        ac_text_surf = self.fonts['medium'].render(f"{self.player.ac}", True, COLOR_WHITE)
        ac_text_rect = ac_text_surf.get_rect(right=right_padding, bottom=bottom_y)
        ac_icon_rect = ac_icon_surf.get_rect(right=ac_text_rect.left - 5, centery=ac_text_rect.centery)
        self.screen.blit(ac_icon_surf, ac_icon_rect)
        self.screen.blit(ac_text_surf, ac_text_rect)
        
        gold_icon_surf = self.fonts['large'].render(UI_ICONS["GOLD"], True, COLOR_GOLD)
        gold_text_surf = self.fonts['medium'].render(f"{self.player.gold:.0f}", True, COLOR_WHITE)
        gold_text_rect = gold_text_surf.get_rect(right=ac_icon_rect.left - 20, bottom=bottom_y)
        gold_icon_rect = gold_icon_surf.get_rect(right=gold_text_rect.left - 5, centery=gold_text_rect.centery)
        self.screen.blit(gold_icon_surf, gold_icon_rect)
        self.screen.blit(gold_text_surf, gold_text_rect)
    
    def update(self):
        """Update game logic."""
        if self.game_state == GameState.PLAYING and self.dungeon_game:
            self.dungeon_game.update_light_timer()
    
    def draw(self):
        """Draw the current game state."""
        if self.game_state == GameState.MAIN_MENU:
            self.draw_main_menu()
        
        elif self.game_state == GameState.PLAYING and self.dungeon_game:
            self._draw_game_screen()
        
        elif self.game_state == GameState.SPELL_MENU:
            self._draw_game_screen()
            self.draw_spell_menu()
        
        elif self.game_state == GameState.SPELL_TARGETING:
            self._draw_game_screen()
        
        elif self.game_state == GameState.INVENTORY:
            self.inventory_ui.draw_inventory_screen(self.screen, self.player)
        
        elif self.game_state == GameState.CONTAINER_VIEW:
            self.container_view_ui.draw_container_view_screen(self.screen, self.player, self.current_container)
        
        elif self.game_state == GameState.ITEM_ACTION:
            self.container_view_ui.draw_container_view_screen(self.screen, self.player, self.current_container)
            selected_item = self.container_view_ui.get_selected_item(self.current_container)
            if selected_item:
                self.item_action_ui.draw_item_action_screen(self.screen, selected_item.item)
        
        elif self.game_state == GameState.EQUIPMENT:
            if self.equipment_selection_mode:
                self.equipment_ui.draw_equipment_screen(self.screen, self.player)
                slot = self.equipment_ui.get_selected_slot()
                self.equipment_available_items = self.equipment_selection_ui.draw_equipment_selection(
                    self.screen, self.player, slot)
            else:
                self.equipment_ui.draw_equipment_screen(self.screen, self.player)
    
    def _draw_game_screen(self):
        """Draw the main game screen with dungeon and UI."""
        if not self.dungeon_game:
            return
        
        # Calculate viewport parameters
        viewport_params = calculate_viewport_parameters(
            self.screen_width, self.screen_height - HUD_HEIGHT, HUD_HEIGHT,
            self.dungeon_game.get_player_position(), self.zoom_level
        )
        
        # Create fonts for current zoom level
        zoom_fonts = create_fonts_for_zoom(FONT_FILE, self.zoom_level)
        
        # Create viewport surface that fills the entire game area
        viewport_surface = pygame.Surface((self.screen_width, self.screen_height - HUD_HEIGHT))
        
        # Render the dungeon viewport
        self.renderer.render_viewport(
            viewport_surface, self.dungeon_game, self.dungeon_game.get_player_position(),
            viewport_params['viewport_x'], viewport_params['viewport_y'], viewport_params['cell_size'],
            viewport_params['viewport_width_cells'], viewport_params['viewport_height_cells'],
            self.game_state, self.spell_target_pos, self.current_spell,
            zoom_fonts['player'], zoom_fonts['spell_cursor']
        )
        
        # Blit viewport to main screen (this should fill the entire game area)
        self.screen.blit(viewport_surface, (0, 0))
        
        # Draw coordinate display
        self.renderer.render_coordinates(self.screen, self.dungeon_game.get_player_position(), self.fonts['coords'])
        
        # Draw timer
        self.renderer.render_timer_box(self.screen, self.player, self.fonts['timer'])
        
        # Draw HUD
        self.draw_hud()
    
    def run(self):
        """Main game loop."""
        print("🚀 Starting Dungeon Explorer (Fully Modular)...")
        print(f"📖 Loaded dungeon: {self.dungeon_data.get('title', 'Unknown')}")
        print("✨ Using new modular architecture!")
        
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game logic
            self.update()
            
            # Draw everything
            self.draw()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
        
        # Cleanup
        pygame.quit()
        print("👋 Dungeon Explorer closed.")

def main():
    """Entry point for the application."""
    app = DungeonExplorer()
    app.run()

if __name__ == '__main__':
    main()