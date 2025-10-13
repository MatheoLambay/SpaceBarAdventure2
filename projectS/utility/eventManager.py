class EventManager:
    def __init__(self, player):
        self.player = player
        self.events = []
        self.active = False
        self.current_event = None
        self.timer = 0

    def start_event(self, event_list):
        """Lance une séquence d’events"""
        self.events = event_list
        self.active = True
        self.player.control_enabled = False
        self.current_event = None
        self.timer = 0

    def update(self, dt):
        if not self.active:
            return

        # Si aucun event actif, on en prend un nouveau
        if self.current_event is None and self.events:
            self.current_event = self.events.pop(0)
            self.timer = 0

        if self.current_event:
            done = self.current_event.update(dt)
            if done:
                self.current_event = None  # passer au suivant

        # Si plus d'event => fin de la séquence
        if not self.current_event and not self.events:
            self.active = False
            self.player.control_enabled = True