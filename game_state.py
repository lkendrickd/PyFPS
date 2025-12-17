from enum import Enum, auto


class GameState(Enum):
    """Enumeration of possible game states."""
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()


class GameStateManager:
    """Manages game state transitions and state-specific callbacks."""
    
    def __init__(self, initial_state=GameState.MENU):
        self._current_state = initial_state
        self._previous_state = None
        self._callbacks = {
            'on_enter': {},
            'on_exit': {}
        }
    
    @property
    def current_state(self) -> GameState:
        """Get the current game state."""
        return self._current_state
    
    @property
    def previous_state(self) -> GameState | None:
        """Get the previous game state."""
        return self._previous_state
    
    def transition(self, new_state: GameState) -> bool:
        """
        Transition to a new game state.
        
        Args:
            new_state: The state to transition to
            
        Returns:
            True if transition was successful, False otherwise
        """
        if new_state == self._current_state:
            return False
        
        # Execute exit callback for current state
        if self._current_state in self._callbacks['on_exit']:
            self._callbacks['on_exit'][self._current_state]()
        
        # Update states
        self._previous_state = self._current_state
        self._current_state = new_state
        
        # Execute enter callback for new state
        if new_state in self._callbacks['on_enter']:
            self._callbacks['on_enter'][new_state]()
        
        return True
    
    def register_callback(self, callback_type: str, state: GameState, callback):
        """
        Register a callback for state transitions.
        
        Args:
            callback_type: 'on_enter' or 'on_exit'
            state: The state to trigger the callback
            callback: The function to call
        """
        if callback_type not in self._callbacks:
            raise ValueError(f"Invalid callback type: {callback_type}")
        
        self._callbacks[callback_type][state] = callback
    
    def is_state(self, state: GameState) -> bool:
        """Check if the current state matches the given state."""
        return self._current_state == state
