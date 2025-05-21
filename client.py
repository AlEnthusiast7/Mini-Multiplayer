import pygame
from network import Network
from player import player
from laser import laser
from settings import*

width = 500
height = 500
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Client")

def redrawWindow(win,players,alllasers,image):
    win.fill((255,255,255))
    colours = ["red", "black","blue","yellow"]

    for x in players:
            players[x].draw(win, colours[x%len(colours)])

    for x in alllasers:
        if alllasers[x]:
            for laser in alllasers[x]:
                laser.draw(win,image)

                if not laser.update():
                    alllasers[x].remove(laser)

    pygame.display.update()



def main ():
    run = True
    n = Network()
    clock = pygame.time.Clock()
    player1 = n.getP()
    print(player1)
    lasers = []
    laserspng = pygame.image.load("laser.png").convert_alpha()

    while run:
        dt = clock.tick(60)
        k = pygame.key.get_pressed()
        kk = {"right": k[pygame.K_d],
              "up": k[pygame.K_w],
              "left": k[pygame.K_a],
              "down": k[pygame.K_s]}
        big_ass_dict = { "keys": kk,
                         "mouse": pygame.mouse.get_just_pressed(),
                         "mpos": pygame.mouse.get_pos(),
                         "lasers": lasers,
                         "player": player1
        }

        dainfo = n.send(big_ass_dict)
        pid  = dainfo["pid"]
        lasers = dainfo["alllasers"][pid]
        player1 = dainfo["players"][pid]

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run = False
                n.client.close()
                pygame.quit()



        redrawWindow(win, dainfo["players"],dainfo["alllasers"],laserspng)


if __name__ == "__main__":
    main()
