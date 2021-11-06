import pygame
import pygame_menu, json
import pie3d

def launchMenu():
    pygame.init()
    surface = pygame.display.set_mode((600, 400))

    with open("config.json", "r") as f: config = json.load(f);f.close()

    def start_the_game():
        pie3d.menuPlayMap()

    menu = pygame_menu.Menu(config["gameSettings"]["title"], 400, 300,
                        theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)