import sys
import moderngl as mgl
from engine import Engine
from settings import *
from game_state import GameState, GameStateManager
from config_manager import ConfigManager
from menu.menu_renderer import MenuRenderer
from menu.main_menu import MainMenu
from menu.settings_menu import SettingsMenu


class Game:
    def __init__(self):
        pg.init()
        
        # Load configuration
        self.config = ConfigManager()
        
        # Setup OpenGL context
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, MAJOR_VERSION)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, MINOR_VERSION)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, DEPTH_SIZE)

        # Get resolution from config
        config_resolution = self.config.get('video', 'resolution', default=[1280, 720])
        
        # Auto-detect if resolution is [0, 0] or None
        if config_resolution is None or config_resolution == [0, 0]:
            # Get native display resolution
            display_info = pg.display.Info()
            resolution = (display_info.current_w, display_info.current_h)
        else:
            resolution = tuple(config_resolution)
        
        self.current_resolution = resolution
        
        # Get display mode
        display_mode = self.config.get('video', 'display_mode', default='windowed')
        flags = pg.OPENGL | pg.DOUBLEBUF
        if display_mode == 'fullscreen':
            flags |= pg.FULLSCREEN
        elif display_mode == 'borderless':
            flags |= pg.NOFRAME
        
        pg.display.set_mode(resolution, flags=flags)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.BLEND)  # type: ignore
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        self.is_running = True
        self.fps_value = 0
        
        # Initialize game state management
        self.state_manager = GameStateManager(initial_state=GameState.MENU)
        
        # Initialize menu system
        self.menu_renderer = MenuRenderer(self.ctx, self.current_resolution)
        self.main_menu = MainMenu(
            self.menu_renderer,
            on_new_game=self._start_new_game,
            on_settings=self._show_settings,
            on_exit=self._exit_game
        )
        self.settings_menu = SettingsMenu(
            self.menu_renderer,
            self.config,
            on_back=self._show_main_menu,
            on_apply_settings=self._apply_video_settings
        )
        self.current_menu = self.main_menu
        
        # Menu surface for rendering
        self.menu_surface = self.menu_renderer.create_menu_surface()
        
        # Engine (will be initialized when starting new game)
        self.engine: Engine | None = None

        self.anim_trigger = False
        self.anim_event = pg.USEREVENT + 0
        pg.time.set_timer(self.anim_event, SYNC_PULSE)

        self.sound_trigger = False
        self.sound_event = pg.USEREVENT + 1
        pg.time.set_timer(self.sound_event, 750)
    
    def _start_new_game(self):
        """Start a new game."""
        self.state_manager.transition(GameState.PLAYING)
        # Initialize engine if not already done
        if self.engine is None:
            pg.event.set_grab(True)
            pg.mouse.set_visible(False)
            self.engine = Engine(self)
    
    def _show_settings(self):
        """Show settings menu."""
        self.current_menu = self.settings_menu
    
    def _show_main_menu(self):
        """Show main menu."""
        self.current_menu = self.main_menu
    
    def _exit_game(self):
        """Exit the game."""
        self.is_running = False
    
    def _apply_video_settings(self):
        """Apply video settings (resolution, display mode)."""
        # Get new settings
        config_resolution = self.config.get('video', 'resolution', default=[1280, 720])
        
        # Auto-detect if resolution is [0, 0] or None
        if config_resolution is None or config_resolution == [0, 0]:
            display_info = pg.display.Info()
            new_resolution = (display_info.current_w, display_info.current_h)
        else:
            new_resolution = tuple(config_resolution)
        
        display_mode = self.config.get('video', 'display_mode', default='windowed')
        
        # Check if resolution changed
        if new_resolution != self.current_resolution:
            self.current_resolution = new_resolution
            
            # Build flags
            flags = pg.OPENGL | pg.DOUBLEBUF
            if display_mode == 'fullscreen':
                flags |= pg.FULLSCREEN
            elif display_mode == 'borderless':
                flags |= pg.NOFRAME
            
            # Recreate display
            pg.display.set_mode(new_resolution, flags=flags)
            
            # Recreate OpenGL context
            self.ctx = mgl.create_context()
            self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.BLEND)  # type: ignore
            self.ctx.gc_mode = 'auto'
            
            # Recreate menu renderer with new resolution
            old_renderer = self.menu_renderer
            self.menu_renderer = MenuRenderer(self.ctx, new_resolution)
            old_renderer.cleanup()
            
            # Update menus with new renderer
            self.main_menu.renderer = self.menu_renderer
            self.settings_menu.renderer = self.menu_renderer
            
            # Recreate menu surface
            self.menu_surface = self.menu_renderer.create_menu_surface()
            
            # If engine exists, need to recreate it with new context
            if self.engine is not None:
                # This is complex - for now just set to None and let user restart game
                self.engine = None

    def update(self):
        if self.state_manager.is_state(GameState.PLAYING):
            assert self.engine is not None
            self.engine.update()
        elif self.state_manager.is_state(GameState.MENU):
            self.current_menu.update(self.delta_time)
        #
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        self.fps_value = int(self.clock.get_fps())
        pg.display.set_caption(f'{self.fps_value}')

    def render(self):
        self.ctx.clear(color=(*BG_COLOR, 1.0))
        
        if self.state_manager.is_state(GameState.PLAYING):
            assert self.engine is not None
            self.engine.render()
        elif self.state_manager.is_state(GameState.MENU):
            # Render menu to surface
            self.current_menu.render(self.menu_surface)
            # Render surface to OpenGL screen
            self.menu_renderer.render_to_screen(self.menu_surface)
        
        pg.display.flip()

    def handle_events(self):
        self.anim_trigger, self.sound_trigger = False, False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            
            # Handle ESC key based on state
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                if self.state_manager.is_state(GameState.PLAYING):
                    # Return to menu
                    self.state_manager.transition(GameState.MENU)
                    pg.event.set_grab(False)
                    pg.mouse.set_visible(True)
                elif self.state_manager.is_state(GameState.MENU):
                    # Exit from main menu
                    if self.current_menu == self.main_menu:
                        self.is_running = False
            #
            if event.type == self.anim_event:
                self.anim_trigger = True
            #
            if event.type == self.sound_event:
                self.sound_trigger = True
            
            # Route events based on state
            if self.state_manager.is_state(GameState.PLAYING):
                assert self.engine is not None
                self.engine.handle_events(event=event)
            elif self.state_manager.is_state(GameState.MENU):
                self.current_menu.handle_event(event)

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
