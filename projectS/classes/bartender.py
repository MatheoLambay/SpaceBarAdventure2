import pygame
from utility.eventChangeTile import eventChangeTile
from utility.eventMove import MoveEvent
from utility.eventManager import EventManager
from utility.eventWait import WaitEvent
from utility.eventLookAt import LookAtEvent


class Bartender(pygame.sprite.Sprite):
    def __init__(self,frames_walk,pos,dialogues):
        super().__init__()

        self.frames = frames_walk
        self.direction = "S"
        self.image = self.frames[self.direction][0]
        x,y = pos
        
        self.frame_index = 0
        self.rect = self.image.get_rect(center=(x*64+32,y*64+32))
        self.animation_speed = 2

        self.interaction_img = pygame.image.load("assets/pnj/interaction.png").convert_alpha()
        self.panel = pygame.image.load("assets/pnj/talkpanel.png").convert_alpha()
        self.panel_rect = self.panel.get_rect(center = (400,450))
        
        self.control_enabled = True
        self.text_index = 0
        self.current_displayed_text = ""
        self.talk_index = 0
        self.last_talk = 0
        self.in_talk = 0

        self.last_frame_time = 0
        self.frame_interval = 40

        self.index = 0

        self.step = 1
        
        self.dialogues = dialogues

        
        self.event_list = []
        self.events = EventManager(self)
        self.completed_steps = set()
        




    def update(self,player,keys,screen,camera,inventory,event_tile,map,dt,event_tp):
       
        self.events.update(dt)

        if not self.control_enabled:
            return 
        
        if self.in_talk:
            screen.blit(self.panel,self.panel_rect)
            my_font = pygame.font.SysFont('Comic Sans MS', 20)
            text_surface = my_font.render(self.current_displayed_text, False, (0, 0, 0))
            screen.blit(text_surface, (self.panel_rect.topleft[0]+20,self.panel_rect.topleft[1]+10))
    
            # --- display letter one by one
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_interval:
                if self.talk_index != len(self.dialogues[self.step]['text'][self.text_index]):
                    self.current_displayed_text += self.dialogues[self.step]['text'][self.text_index][self.talk_index]
                    self.talk_index+=1
                
                self.last_frame_time = current_time

            # --- skip animation
            if keys[pygame.K_RETURN] and self.last_talk == 0:
                if self.talk_index != len(self.dialogues[self.step]['text'][self.text_index]):
                    self.current_displayed_text = self.dialogues[self.step]['text'][self.text_index]
                    self.talk_index = len(self.dialogues[self.step]['text'][self.text_index])
                else: # ---

                    self.index += 1
                    self.text_index +=1
                    self.current_displayed_text = ""
                    self.talk_index = 0

                
                self.last_talk = 1

            elif not keys[pygame.K_RETURN] and self.last_talk == 1:
                self.last_talk = 0

        if self.index == 0 and len(self.dialogues[self.step]['text']) > 0:
            if self.rect.colliderect(player.hitbox):
                interaction_rect = self.interaction_img.get_rect(topright=self.rect.topright)
                screen.blit(self.interaction_img, camera.apply(interaction_rect))
                if keys[pygame.K_RETURN] and self.last_talk == 0:
                    player.control_enabled = False
                    self.in_talk = 1
                    self.index = self.text_index

                elif not keys[pygame.K_RETURN] and self.last_talk == 1:
                    self.last_talk = 0

        
        elif self.index == len(self.dialogues[self.step]['text']):
            # --- Fin du dialogue courant ---
            self.in_talk = 0
            player.control_enabled = True
            self.index = 0
            self.current_displayed_text = ""
            self.talk_index = 0
            self.text_index = 0

            # --- Exécuter l’unlock du step actuel (si pas déjà fait)
            if self.step not in self.completed_steps:
                current_unlock = self.dialogues[self.step].get("unlock", "None")

                if current_unlock != "None":
                    for u in current_unlock:
                        if u[0] == "door":
                            tile1 = u[1]
                            tile2 = u[2]
                            event_tile.append(eventChangeTile(tile1, tile2, map))

                        if u[0] == "event":
                            self.event_list.clear()
                            for e in u[1:]:
                                if e[0] == "move":
                                    print("move")
                                    x, y, distance, can_move = e[1], e[2], e[3], e[4]
                                    self.event_list.append(MoveEvent(self, x, y, 64 * distance, can_move))
                                elif e[0] == "wait":
                                    time = e[1]
                                    self.event_list.append(WaitEvent(time))
                                elif e[0] == "TP":
                                    event_tp.append(e[1])
                                elif e[0] == "look_at":
                                    print("look_at")
                                    self.event_list.append(LookAtEvent(self, e[1]))

                            self.events.start_event(self.event_list.copy())

                        if u[0] == "inventory":
                            if u[1] not in inventory:
                                inventory.append(u[1])

                    # if current_unlock[0] == "door":
                    #     tile1 = current_unlock[1]
                    #     tile2 = current_unlock[2]
                    #     event_tile.append(eventChangeTile(tile1, tile2, map))

                    # elif current_unlock[0] == "event":
                    #     self.event_list.clear()
                    #     for e in current_unlock[1:]:
                    #         if e[0] == "move":
                    #             x, y, distance, can_move = e[1], e[2], e[3], e[4]
                    #             self.event_list.append(MoveEvent(self, x, y, 64 * distance, can_move))
                    #         elif e[0] == "wait":
                    #             time = e[1]
                    #             self.event_list.append(WaitEvent(time))
                    #         elif e[0] == "TP":
                    #             event_tp.append(e[1])

                    #     self.events.start_event(self.event_list.copy())

                    # elif current_unlock[0] == "inventory":
                    #     if current_unlock[1] not in inventory:
                    #         inventory.append(current_unlock[1])

                # 🔒 Marquer ce step comme complété
                self.completed_steps.add(self.step)

            # --- 2️⃣ Passer au step suivant si l’objectif est rempli
            if self.step + 1 <= len(self.dialogues):
                next_objectif = self.dialogues[self.step + 1]["objectif"]
                if next_objectif != "None":
                    for i in inventory:
                        if i == next_objectif:
                            self.step += 1
                            break
                else:
                    self.step += 1



        



           