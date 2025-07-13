import pygame
import sys
from ui.modern_components import Typography, LayoutSystem, ModernUITheme, ModernNotificationManager
from ui.modern_integration import upgrade_ui_system
from data.states import GameState

class DungeonExplorer:
    """Main game class, updated to manage the dynamic UI system."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Dungeon Explorer")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.CHAR_CREATION
        self.fullscreen = False
        
        # --- Design System Management ---
        self.theme = ModernUITheme('neutral') # Start with neutral theme
        self.layout = LayoutSystem(self.screen_width, self.screen_height)
        self.typography = Typography("RobotoSlab-VariableFont_wght.ttf", "JetBrainsMonoNL-Regular.ttf")
        self.fonts = self.typography.styles
        
        self.player = None
        self.active_ui = None
        self.notification_manager = ModernNotificationManager(self.screen_width, self.fonts, self.theme)
        self.modern_ui_creators = upgrade_ui_system(self)

    def set_theme(self, theme_name: str):
        """Changes the active UI theme and forces a UI rebuild."""
        print(f"UI Theme changed to: {theme_name}")
        self.theme = ModernUITheme(theme_name)
        self.notification_manager.theme = self.theme # Update the notifier's theme too
        if hasattr(self.active_ui, 'handle_resize'):
            self.active_ui.handle_resize(self.layout, self.theme)

    def run(self):
        self.active_ui = self.modern_ui_creators['character_creation']()
        
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.VIDEORESIZE and not self.fullscreen:
                    self.handle_resize(event)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        pygame.display.toggle_fullscreen()
                        self.handle_resize(None)
                    # Theme switching hotkeys
                    if event.key == pygame.K_F1: self.set_theme('lawful')
                    if event.key == pygame.K_F2: self.set_theme('neutral')
                    if event.key == pygame.K_F3: self.set_theme('chaotic')
                
                if self.active_ui:
                    if self.active_ui.handle_event(event) is True:
                        self.player = self.active_ui.create_player()
                        if self.player:
                            print(f"✅ Character created: {self.player.name}")
                            self.game_state = GameState.PLAYING
                            self.active_ui = None # Exit character creation
                        else:
                            # Creation failed, stay on screen. handle_event already showed notification
                            pass 
            
            # --- Main Draw Call ---
            self.screen.fill(self.theme.DARK_CATHODE)
            if self.active_ui:
                self.active_ui.draw(self.screen)
            
            self.notification_manager.draw(self.screen)
            pygame.display.flip()
            
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

    def handle_resize(self, event):
        self.screen_width, self.screen_height = self.screen.get_size()
        self.layout = LayoutSystem(self.screen_width, self.screen_height)
        self.notification_manager.screen_width = self.screen_width
        if hasattr(self.active_ui, 'handle_resize'):
            self.active_ui.handle_resize(self.layout, self.theme)

if __name__ == '__main__':
    game = DungeonExplorer()
    game.run()