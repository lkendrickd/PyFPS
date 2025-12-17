import pygame as pg
from typing import List
from game_state import GameState


class DevConsole:
    """Lightweight in-game console for debug commands."""

    def __init__(self, game):
        self.game = game
        self.active = False
        self.buffer = ''
        self.messages: List[str] = []
        self.surface: pg.Surface | None = None
        self.god_mode = False

        # styling
        self.bg_color = (0, 0, 0, 180)
        self.text_color = (230, 230, 230)
        self.hint_color = (200, 180, 120)

    def handle_event(self, event) -> bool:
        """
        Returns True if the event was consumed by the console.
        Toggle with the backquote key.
        """
        if event.type == pg.KEYDOWN and event.key == pg.K_BACKQUOTE:
            self.toggle()
            return True

        if not self.active:
            return False

        if event.type == pg.TEXTINPUT:
            self.buffer += event.text
            return True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.execute(self.buffer.strip())
                self.buffer = ''
                return True
            if event.key == pg.K_BACKSPACE:
                self.buffer = self.buffer[:-1]
                return True
            if event.key == pg.K_ESCAPE:
                self.toggle()
                return True

        return False

    def toggle(self):
        self.active = not self.active
        if self.active:
            self.buffer = ''
            pg.key.start_text_input()
            pg.event.set_grab(False)
            pg.mouse.set_visible(True)
            self._push_message("Console opened. Type 'god' to enable god mode.")
        else:
            pg.key.stop_text_input()
            self._push_message("Console closed.")
            if self.game.state_manager.is_state(GameState.PLAYING):
                pg.event.set_grab(True)
                pg.mouse.set_visible(False)

    def execute(self, command: str):
        if not command:
            return

        cmd = command.lower()
        if cmd == 'god':
            self.set_god_mode(True)
            self._push_message('God mode enabled.')
        elif cmd in ('god off', 'nogod', 'ungod'):
            self.set_god_mode(False)
            self._push_message('God mode disabled.')
        else:
            self._push_message(f'Unknown command: {command}')

    def set_god_mode(self, enabled: bool):
        self.god_mode = enabled
        if self.game.engine:
            self.game.engine.set_god_mode(enabled)

    def sync_with_engine(self):
        """Reapply cheats after (re)creating the engine."""
        self.set_god_mode(self.god_mode)

    def render(self):
        if not self.active:
            return

        if self.surface is None or self.surface.get_size() != self.game.current_resolution:
            self.surface = pg.Surface(self.game.current_resolution, pg.SRCALPHA)

        self.surface.fill(self.bg_color)

        renderer = self.game.menu_renderer
        font = renderer.small_font
        line_height = font.get_linesize()
        padding = 18
        y = padding

        # recent messages
        for msg in self.messages[-6:]:
            renderer.render_text(
                self.surface, msg, (padding, y), font=font, color=self.text_color
            )
            y += line_height

        # input line
        renderer.render_text(
            self.surface, f'> {self.buffer}', (padding, y + line_height),
            font=renderer.menu_font, color=self.hint_color
        )

        renderer.render_to_screen(self.surface)

    def _push_message(self, msg: str):
        self.messages.append(msg)
        if len(self.messages) > 20:
            self.messages = self.messages[-20:]
