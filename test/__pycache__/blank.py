currents_frames = self.frames_fight[self.direction][1:]
self.frame_fight_index += self.animation_speed
if self.frame_fight_index >= len(currents_frames):
    self.frame_fight_index = 0
self.image = currents_frames[int(self.frame_fight_index)]