import time
import traceback
import numpy
import pygame as pg

from class_types.panel_types import SwitchViewButtonTypes
from components.button import Button
from events.event_manager import EventManager
from sounds.sounds import SoundManager
from .textures import Textures
from .world import World
from .utils import draw_text
from .map_controller import MapController
from .panel import Panel
from .game_controller import GameController
from threading import Thread, Event
from Online.multiplayer_connection import Multiplayer_connection
from Online.Room import Room

from compet_mode import Comp_mode

def my_thread(func, event: Event):
    fps_moyen = [0]
    try:
        while not event.is_set():
            func(fps_moyen)
    except Exception:
        event.set()
        print("\033[91m In render thread :")
        print("\033[91m" + traceback.format_exc())
        exit()

class Game:
    def __init__(self, screen,player, online=False, room : Room = None):
        self.is_running = False
        self.screen = screen
        self.paused = False
        self.game_controller = GameController.get_instance()
        self.width, self.height = self.screen.get_size()
        self.multplayer = None
        self.room = room
        self.start_time = time.time()

        #Gestion de la connexion multijoueur
        if online:
            self.multplayer = Multiplayer_connection(room,screen)

        # sound manager
        self.sound_manager = SoundManager()

        # panel has two sub_panel: ressource_panel for displaying Dn, Populations, etc and building_panel
        # for displaying available building in game
        self.panel = Panel(self.width, self.height, self.screen)

        # World contains populations or graphical objects like buildings, trees, grass
        self.world = World(self.width, self.height, self.panel, self.multplayer,player)

        self.thread_event = Event()
        self.draw_thread = Thread(None, my_thread, "1", [self.display, self.thread_event])

        self.pause_game = Button((self.width - 50, 490 + 46), (39, 26),
                                 image=Textures.get_texture(SwitchViewButtonTypes.PAUSE_GAME), )
        self.pause_game.on_click(self.toogle_pause)
        EventManager.register_component(self.pause_game)

        MapController.init_()

        # Exit the game when pressing <esc>
        EventManager.register_key_listener(pg.K_ESCAPE, self.exit_game)
        # Calls the event_handler of the World
        EventManager.add_hooked_function(self.world.event_handler)
        EventManager.register_key_listener(pg.K_SPACE, self.toogle_pause)
        self.draw_thread.start()

        

    # Game Loop
    def run(self):
        self.is_running = True
        # Main control
        try:
            while self.is_running and not self.thread_event.is_set():
                # We need to recalculate it every time, since it can change
                targeted_ticks_per_seconds = self.game_controller.get_current_speed() * 50
                if not self.paused:
                    self.game_controller.update()
                    for walker in GameController.get_instance().walkers:
                        walker.update()
                if self.game_controller.is_load_save():
                    self.load_save()

                #self.multplayer.receive()

                time.sleep(1/targeted_ticks_per_seconds)

        # Main programm exeption stop the thread and show the traceback
        except Exception:
            self.thread_event.set()
            self.draw_thread.join()
            print("\033[91m In logic main program :")
            print("\033[91m" + traceback.format_exc())
            exit()

        self.thread_event.set()
        self.draw_thread.join()
        exit()


    def toogle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_game.image = Textures.get_texture(SwitchViewButtonTypes.CONTINUE_GAME)
        else:
            self.pause_game.image = Textures.get_texture(SwitchViewButtonTypes.PAUSE_GAME)


    def draw(self, fps):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen)
        self.panel.draw(self.screen)
        month_number = self.game_controller.get_actual_month()

        draw_text('fps={}'.format(fps), self.screen, (self.width - 120, 10), size=22)
        draw_text('Chrono  {}'.format(int(time.time() - self.start_time)), self.screen, (self.width - 905, 10), size=22)
        draw_text('Score  {}'.format(self.game_controller.get_actual_citizen()+self.game_controller.actual_foods+int(self.game_controller.global_desirability)), self.screen, (self.width - 1200, 10), size=22)
        draw_text('Winner: '.format(self.game_controller.get_month(month_number)), self.screen, (self.width - 590, 10), color=pg.Color(255, 255, 0), size=22)
        draw_text('{} '.format(Comp_mode.get_instance().var), self.screen, (self.width - 500, 10), color=pg.Color(255, 255, 0), size=22)
        draw_text('Speed {}%'.format(int(100*self.game_controller.get_actual_speed())), self.screen, (self.width - 150, 510), color=pg.Color(60, 40, 25), size=16)



        self.pause_game.display(self.screen)
        pg.display.flip()

    def display(self,fps_moyen):
        start_render = time.process_time_ns()
        EventManager.handle_events()

        self.world.update()
        self.panel.update()
        self.draw(int(numpy.average(fps_moyen)))
        end_render = time.process_time_ns()
        time_diff = (end_render - start_render) / 1000000

        if len(fps_moyen) > 100:
            fps_moyen.pop(0)
        if time_diff:
            fps_moyen.append(1000 / time_diff)


    def exit_game(self):
        self.is_running = False
        self.multplayer.kill_thread()
        Comp_mode().get_instance().kill_chrono()

    def load_save(self):
        self.world.load_numpy_array()
        self.game_controller.game_reloaded()
