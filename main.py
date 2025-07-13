import pygame
import json
import sys
import os

# --- Core Game Imports ---
# Absolute imports starting from the project root
from config.constants import *
from data.states import GameState
from data.player import Player
from data.containers import organize_inventory_into_containers
# NOTE: Assuming a DungeonGame class exists to handle game logic
# from dungeon.dungeon_game import DungeonGame 

# --- Classic UI Imports (as fallback) ---
# NOTE: Assuming these are your existing UI files
# from ui.character_creation import run_enhanced_character_creation_with_existing_display
# from ui.inventory_ui import InventoryUI

# --- Modern UI Imports (Absolute Paths) ---
from ui.modern_components import ModernNotificationManager
from ui.modern_integration import (
    ModernizedCharacterCreation, 
    ModernizedInventoryUI, 
    upgrade_ui_system
)


class DungeonExplorer:
    """
    Main game class, updated to integrate the modern UI system.
    """
    def __init__(self):
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Dungeon Explorer")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        self.game_state = GameState.CHAR_CREATION # Start with character creation
        
        self.font_file = FONT_FILE

        # --- Load Game Data ---
        try:
            with open(JSON_FILE, 'r') as f:
                self.dungeon_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading dungeon data: {e}")
            self.running = False
            return

        # --- Player and Game Logic Initialization ---
        self.player = None
        # self.dungeon_game = None # Will be initialized after character creation

        # --- Classic UI Initialization (as fallback) ---
        # self.inventory_ui = InventoryUI(self.screen_width, self.screen_height, self.font_file)
        self.current_containers = []

        # --- Modern UI Integration ---
        self.modern_ui_enabled = MODERN_UI_ENABLED
        self.use_modern_character_creation = USE_MODERN_CHARACTER_CREATION
        self.use_modern_inventory = USE_MODERN_INVENTORY
        
        # This holds the creator functions for modern UI screens
        self.modern_ui_creators = upgrade_ui_system(self)
        
        # Initialize the notification manager, which will be used everywhere
        self.notification_manager = ModernNotificationManager(self.screen_width)
        
        # This will hold the active modern inventory UI instance
        self.modern_inventory_ui = None


    def run(self):
        """Main game loop."""
        self.start_character_creation()
        
        if not self.player: # If character creation was cancelled
            self.running = False

        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def start_character_creation(self):
        """
        REPLACED METHOD
        Starts the character creation process, using the modern UI if enabled.
        """
        pygame.display.set_caption("Character Creation")

        created_player = None
        if self.use_modern_character_creation:
            try:
                modern_creator = self.modern_ui_creators['character_creation']()
                created_player = self.run_modern_character_creation(modern_creator)
                if created_player:
                    self.notification_manager.add_notification(
                        f"Welcome, {created_player.name}!", 'success', duration=3.0
                    )
            except Exception as e:
                print(f"Modern UI failed, falling back to classic: {e}")
                self.notification_manager.add_notification(
                    "UI Error. Using fallback.", 'error', duration=4.0
                )
                # Fallback to original system (assuming it exists)
                # created_player = run_enhanced_character_creation_with_existing_display(self.screen, self.font_file)
        else:
            # Use original character creation
            # created_player = run_enhanced_character_creation_with_existing_display(self.screen, self.font_file)
            pass # Placeholder for your classic character creation call

        if created_player is None:
            self.running = False
            return

        self.player = created_player
        # self.dungeon_game = DungeonGame(self.dungeon_data, self.player) # Initialize game logic
        self.game_state = GameState.PLAYING
        pygame.display.set_caption(f"{self.dungeon_data.get('title', 'Dungeon')}")
        print(f"✅ Character created: {self.player.name} the {self.player.race} {self.player.character_class}")


    def run_modern_character_creation(self, creator: ModernizedCharacterCreation) -> Player:
        """
        NEW METHOD
        Runs the dedicated game loop for the modern character creation screen.
        """
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                # The creator's handle_event returns True when done
                result = creator.handle_event(event)
                if result is True:
                    # Final check before creating player
                    player = creator.create_player()
                    if player:
                        return player
                    else: # If creation fails (e.g., empty name), stay on screen
                        continue
                elif result is None and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None # Allow escaping

            # Update UI animations and notifications
            creator.notification_manager.update(dt)
            
            # Draw the UI
            creator.draw(self.screen)
            pygame.display.flip()
        
        return None


    def handle_input(self):
        """Handles user input for the entire game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self.fullscreen = not self.fullscreen
                pygame.display.toggle_fullscreen()

            if self.game_state == GameState.PLAYING:
                self._handle_playing_input(event)
            elif self.game_state == GameState.INVENTORY:
                self._handle_inventory_input(event)


    def _handle_playing_input(self, event):
        """
        UPDATED METHOD
        Handles input during the main gameplay state.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False # Or open a main menu
            
            # --- MODIFIED: Open Inventory ---
            if event.key == pygame.K_i:
                if self.use_modern_inventory:
                    try:
                        self.modern_inventory_ui = self.modern_ui_creators['inventory']()
                        self.modern_inventory_ui.update_inventory(self.player)
                        self.game_state = GameState.INVENTORY
                        self.notification_manager.add_notification(
                            "Inventory opened", 'info', duration=1.5
                        )
                    except Exception as e:
                        print(f"Modern inventory failed, using classic: {e}")
                        # Fallback to original
                        # self.game_state = GameState.INVENTORY
                        # self.current_containers = organize_inventory_into_containers(self.player)
                        # self.inventory_ui.set_containers(self.current_containers)
                else:
                    # Use original inventory
                    # self.game_state = GameState.INVENTORY
                    # self.current_containers = organize_inventory_into_containers(self.player)
                    # self.inventory_ui.set_containers(self.current_containers)
                    pass # Placeholder for classic inventory call

    def _handle_inventory_input(self, event):
        """Handles input when the inventory is open."""
        if self.use_modern_inventory and self.modern_inventory_ui:
            self.modern_inventory_ui.handle_event(event)
        # else:
            # self.inventory_ui.handle_event(event)
        
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_i or event.key == pygame.K_ESCAPE):
            self.game_state = GameState.PLAYING
            self.modern_inventory_ui = None # Clear the modern UI instance


    def update(self):
        """
        UPDATED METHOD
        Updates game logic based on the current state.
        """
        # --- NEW: Update notification manager globally ---
        self.notification_manager.update(self.clock.get_time() / 1000.0)

        if self.game_state == GameState.PLAYING:
            # if self.dungeon_game:
            #     self.dungeon_game.update()
            pass


    def draw(self):
        """
        UPDATED METHOD
        Draws everything to the screen.
        """
        self.screen.fill(COLOR_BG)

        if self.game_state == GameState.PLAYING:
            # if self.dungeon_game:
            #     self.dungeon_game.draw(self.screen)
            pass
        
        # --- NEW: Handle modern inventory drawing ---
        elif self.game_state == GameState.INVENTORY:
            if self.use_modern_inventory and self.modern_inventory_ui:
                try:
                    self.modern_inventory_ui.draw_inventory_screen(self.screen, self.player)
                except Exception as e:
                    print(f"Modern inventory draw failed: {e}")
                    # Fallback to original drawing
                    # self.inventory_ui.draw_inventory_screen(self.screen, self.player)
            # else:
                # self.inventory_ui.draw_inventory_screen(self.screen, self.player)
                pass # Placeholder for classic inventory draw

        # --- NEW: Draw notification manager on top of everything ---
        self.notification_manager.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    game = DungeonExplorer()
    if game.running:
        game.run()
