import pygame
import random

pygame.init()

ancho_juego = 800
largo_juego = 1500
tamano_diana = 5

hay_diana = False

fase_lanzamiento = 1
array_proyectiles = []
array_obstaculos_g = []
array_obstaculos = []
array_dianas = []
nivel_actual = 0

posrx1 = 0
posry1 = 0
posrx2 = 0
posry2 = 0

screen = pygame.display.set_mode([largo_juego, ancho_juego])

gravedad = 9.81
masa_tierra = 10

white = (255, 255, 255)
gray = (100, 100, 100) 
black = (0, 0, 0)
dark_red = (200, 0, 0)

global diana

candado = pygame.image.load("candado.bmp")

lvl1 = pygame.image.load("lvl1.bmp")

lvl2 = pygame.image.load("lvl2.bmp")

lvl3 = pygame.image.load("lvl3.bmp")

lvl4 = pygame.image.load("lvl4.bmp")

lvl5 = pygame.image.load("lvl5.bmp")

lvl6 = pygame.image.load("lvl6.bmp")

lvl7 = pygame.image.load("lvl7.bmp")

lvl8 = pygame.image.load("lvl8.bmp")

lvl9 = pygame.image.load("lvl9.bmp")

lvl10 = pygame.image.load("lvl10.bmp")

lvl11 = pygame.image.load("lvl11.bmp")

lvl12 = pygame.image.load("lvl12.bmp")

diana = pygame.image.load("diana.bmp")

diana = pygame.transform.scale(diana,[9 * tamano_diana, 13 * tamano_diana])

class Obstaculo:
    def __init__(self, bizq, bder, bsup, binf):
        self.bizq = bizq
        self.bder = bder
        self.bsup = bsup
        self.binf = binf
        global array_obstaculos
        array_obstaculos.append([])
        array_obstaculos[len(array_obstaculos) - 1].append(self.bizq)
        array_obstaculos[len(array_obstaculos) - 1].append(self.bder)
        array_obstaculos[len(array_obstaculos) - 1].append(self.bsup)
        array_obstaculos[len(array_obstaculos) - 1].append(self.binf)
    
    def dibujar(self):
        pygame.draw.rect(screen,white,pygame.Rect(self.bizq, self.bsup, self.bder - self.bizq, self.binf - self.bsup))

class Obstaculo_g:
    def __init__(self, bizq, bder, bsup, binf, direccion):
        self.direccion = direccion
        self.bizq = bizq
        self.bder = bder
        self.bsup = bsup
        self.binf = binf
        global array_obstaculos_g
        array_obstaculos_g.append(self)


class Proyectil:
    def __init__(self, vratonx, vratony, masa, posx, posy, array_obstaculos):
        self.array_obstaculos = array_obstaculos
        self.vx = vratonx / 70
        self.sentido_gravedad = 1
        self.vy = vratony * (-1) / 70
        self.masa = masa
        self.x = posx
        self.y = posy
        self.fuerza_gravedad = gravedad * masa_tierra * self.masa / 400 ** 2

    def avanzar(self):
        for obs_g in array_obstaculos_g:
            if self.x > obs_g.bizq and self.x < obs_g.bder and self.y > obs_g.bsup and self.y < obs_g.binf:
                self.sentido_gravedad = obs_g.direccion
            else:
                self.sentido_gravedad = 1
        if self.sentido_gravedad == 1:
            self.vy = self.vy - self.fuerza_gravedad
        elif self.sentido_gravedad == 2:
            self.vx = self.vx - self.fuerza_gravedad
        elif self.sentido_gravedad == 3:
            self.vy = self.vy + self.fuerza_gravedad
        elif self.sentido_gravedad == 4:
            self.vx = self.vx + self.fuerza_gravedad
        for obstaculo in self.array_obstaculos:
            if self.x + self.vx > obstaculo[0] and self.x + self.vx < obstaculo[1] and self.y + self.vy > obstaculo[2] and self.y + self.vy < obstaculo[3]:
                self.vx = self.vx * (-1)
                self.vx = self.vx * 0.8
                self.vy = self.vy * 0.9
            if self.y - self.vy > obstaculo[2] and self.y - self.vy < obstaculo[3] and self.x + self.vx > obstaculo[0] and self.x + self.vx < obstaculo[1]:
                self.vy = self.vy * (-1)
                self.vy = self.vy * 0.8
                self.vx = self.vx * 0.9
        if self.x + self.vx > largo_juego - self.masa or self.x + self.vx < self.masa:
            self.vx = self.vx * (-1)
            self.vx = self.vx * 0.8
            self.vy = self.vy * 0.9
        if self.y - self.vy > ancho_juego - self.masa or self.y - self.vy < self.masa:
            self.vy = self.vy * (-1)
            self.vy = self.vy * 0.8
            self.vx = self.vx * 0.9
        self.x = self.x + self.vx
        self.y = self.y - self.vy
    
    def dibujar(self):
        pygame.draw.circle(screen, white, (self.x, self.y), self.masa, 0)

class Diana:
    def __init__(self, x, y, movimiento):
        self.diana = diana
        self.d_movimiento = movimiento
        self.velocidad = 1
        self.x = x
        self.y = y
        self.borde_superior = y
        self.borde_inferior = y + 13 * tamano_diana
        self.borde_lateral_izquierdo = x
        self.borde_lateral_derecho = x + 9 * tamano_diana
#        self.visible = True
        global hay_diana
        hay_diana = True
    
    def avanzar(self):
        if self.d_movimiento != 0:
            if self.y + (self.d_movimiento * self.velocidad + tamano_diana * 13 / 2) > ancho_juego * 3 / 4 or self.y + (self.d_movimiento * self.velocidad - tamano_diana * 13 / 2) < ancho_juego / 4:
                self.d_movimiento = self.d_movimiento * (-1)
            self.y = self.y + self.d_movimiento * self.velocidad
            self.borde_superior = self.y
            self.borde_inferior = self.y + 13 * tamano_diana

    def comprobar_choque(self):
        global array_proyectiles
        indice = 0
        for proyectil in array_proyectiles:
            if proyectil.x > self.borde_lateral_izquierdo and proyectil.x < self.borde_lateral_derecho and proyectil.y > self.borde_superior and proyectil.y < self.borde_inferior:
#                self.visible = False
                global nivel_actual
                array_botones[nivel_actual].desbloqueado = True
                #global array_proyectiles
                array_proyectiles = []
                nivel_actual = 0
                global array_dianas
                array_dianas = []
            indice = indice + 1
    
    def dibujar(self):
        screen.blit(self.diana, (self.x, self.y))

class Boton:
    def __init__(self, x, y, bder, bizq, bsup, binf, foto, nboton):
        global candado
        self.candado = candado
        self.desbloqueado = False
        self.nboton = nboton
        if self.nboton == 1:
            self.desbloqueado = True
        self.x = x
        self.y = y
        self.bder = bder
        self.bizq = bizq
        self.bsup = bsup
        self.binf = binf
        self.foto = foto
        

    def dibujar(self):
        anchurax = 0
        anchuray = 0
        posx = self.x
        posy = self.y
        anchurax = self.bder - self.bizq
        anchuray = self.binf - self.bsup
        posxp = posx + anchurax * 0.1 / 2
        posyp = posy + anchuray * 0.1 / 2
        anchuraxp = int(anchurax * 0.9)
        anchurayp = int(anchuray * 0.9)
        self.fotop = pygame.transform.scale(self.foto, [anchuraxp, anchurayp])
        self.candadop = pygame.transform.scale(self.candado, [anchuraxp, anchurayp])
        self.foto = pygame.transform.scale(self.foto, [anchurax, anchuray])
        self.candado = pygame.transform.scale(self.candado, [anchurax, anchuray])
        (posrx, posry) = pygame.mouse.get_pos()
        if posrx > self.bizq and posrx < self.bder and posry > self.bsup and posry < self.binf:
            if self.desbloqueado == False:
                screen.blit(self.candadop, (posxp, posyp))
            else:
                screen.blit(self.fotop, (posxp, posyp))
            return()
        if self.desbloqueado == False:
            screen.blit(self.candado, (posx, posy))
        else:
            screen.blit(self.foto, (posx, posy))

    def comprobar(self):
        if self.desbloqueado == True:      
            (posrx, posry) = pygame.mouse.get_pos()
            if posrx > self.bizq and posrx < self.bder and posry > self.bsup and posry < self.binf:
                global nivel_actual
                nivel_actual = self.nboton
                global hay_diana
                hay_diana = False
                return()

class Menu:
    def __init__(self, array_b):
        self.array_b = array_b

    def dibujar(self):
        screen.fill(black)
        for b in self.array_b:
            b.dibujar()
    
    def comprobar(self):
        for b in self.array_b:
            b.comprobar()
            

array_botones = [Boton(260, 250, 460, 260, 250, 450, lvl1, 1),
                 Boton(560, 250, 760, 560, 250, 450, lvl2, 2),
                 Boton(860, 250, 1060, 860, 250, 450, lvl3, 3),
                 Boton(1160, 250, 1360, 1160, 250, 450, lvl4, 4),
                 Boton(1460, 250, 1660, 1460, 250, 450, lvl5, 5),
                 Boton(260, 550, 460, 260, 550, 750, lvl6, 6),
                 Boton(560, 550, 760, 560, 550, 750, lvl7, 7),
                 Boton(860, 550, 1060, 860, 550, 750, lvl8, 8),
                 Boton(1160, 550, 1360, 1160, 550, 750, lvl9, 9),
                 Boton(1460, 550, 1660, 1460, 550, 750, lvl10, 10)]
                 #Boton(200, 500, 400, 200, 500, 700, lvl3, 11),
                 #Boton(200, 500, 400, 200, 500, 700, lvl2, 12)]

menu = Menu(array_botones)
def lvl1():
    global hay_diana
    if hay_diana == False:
        global array_dianas
        array_dianas.append(Diana(largo_juego - 9 * tamano_diana, ancho_juego / 2 - 13 * tamano_diana / 2, 0))
        hay_diana = True
        global array_obstaculos
        global array_obstaculos_g
        array_obstaculos_g = []
        array_obstaculos = []
    global fase_lanzamiento

    screen.fill(gray)
    pygame.draw.line(screen, dark_red, (largo_juego / 5, 0), (largo_juego / 5, ancho_juego), 5)

    if fase_lanzamiento == 2:
        pygame.draw.line(screen, white, (posrx1, posry1), pygame.mouse.get_pos())

    for proyectil in array_proyectiles:
        proyectil.avanzar()
        proyectil.dibujar()
    
#    if len(array_dianas) == 0:
 #       array_dianas.append(Diana(largo_juego - 9 * tamano_diana, random.randint(0, ancho_juego)))

    for d in array_dianas:
        d.avanzar()
        d.comprobar_choque()
        d.dibujar()

def lvl2():
    global hay_diana
    if hay_diana == False:
        global array_dianas
        array_dianas.append(Diana
        (largo_juego - 9 * tamano_diana, ancho_juego / 2 - 13 * tamano_diana / 2, 0))
        hay_diana = True
        global array_obstaculos
        global array_obstaculos_g
        array_obstaculos_g = []
        array_obstaculos = []
        global obs1
        obs1 = Obstaculo(900, 1100, 500, 1000)
    global fase_lanzamiento

    screen.fill(gray)
    pygame.draw.line(screen, dark_red, (largo_juego / 5, 0), (largo_juego / 5, ancho_juego), 5)
    obs1.dibujar()

    if fase_lanzamiento == 2:
        pygame.draw.line(screen, white, (posrx1, posry1), pygame.mouse.get_pos())

    for proyectil in array_proyectiles:
        proyectil.avanzar()
        proyectil.dibujar()
    
#    if len(array_dianas) == 0:
 #       array_dianas.append(Diana(largo_juego - 9 * tamano_diana, random.randint(0, ancho_juego)))

    for d in array_dianas:
        d.avanzar()
        d.comprobar_choque()       
        d.dibujar()

def lvl3():
    global hay_diana
    if hay_diana == False:
        global array_dianas
        array_dianas.append(Diana(largo_juego - 9 * tamano_diana, ancho_juego / 2 - 13 * tamano_diana / 2, 0))
        hay_diana = True
        global array_obstaculos
        global array_obstaculos_g
        array_obstaculos_g = []
        array_obstaculos = []
        global obs1
        global obs2
        obs1 = Obstaculo(900, 1100, 0, 700)
        obs2 = Obstaculo(900, 1100, 950, 1000)
    global fase_lanzamiento

    screen.fill(gray)
    pygame.draw.line(screen, dark_red, (largo_juego / 5, 0), (largo_juego / 5, ancho_juego), 5)
    obs1.dibujar()
    obs2.dibujar()

    if fase_lanzamiento == 2:
        pygame.draw.line(screen, white, (posrx1, posry1), pygame.mouse.get_pos())

    for proyectil in array_proyectiles:
        proyectil.avanzar()
        proyectil.dibujar()
    
#    if len(array_dianas) == 0:
 #       array_dianas.append(Diana(largo_juego - 9 * tamano_diana, random.randint(0, ancho_juego)))

    for d in array_dianas:
        d.avanzar()
        d.comprobar_choque()
        d.dibujar()

def lvl4():
    global hay_diana
    if hay_diana == False:
        global array_dianas
        array_dianas.append(Diana(largo_juego - 9 * tamano_diana, ancho_juego / 2 - 13 * tamano_diana / 2, 1))
        hay_diana = True
        global array_obstaculos
        global array_obstaculos_g
        array_obstaculos_g = []
        array_obstaculos = []
        global obs1
        obs1 = Obstaculo(900, 1100, 500, 1000)
    global fase_lanzamiento

    screen.fill(gray)
    pygame.draw.line(screen, dark_red, (largo_juego / 5, 0), (largo_juego / 5, ancho_juego), 5)
    obs1.dibujar()

    if fase_lanzamiento == 2:
        pygame.draw.line(screen, white, (posrx1, posry1), pygame.mouse.get_pos())

    for proyectil in array_proyectiles:
        proyectil.avanzar()
        proyectil.dibujar()
    
#    if len(array_dianas) == 0:
 #       array_dianas.append(Diana(largo_juego - 9 * tamano_diana, random.randint(0, ancho_juego)))

    for d in array_dianas:
        d.avanzar()
        d.comprobar_choque()       
        d.dibujar()

def lvl5():
    global hay_diana
    if hay_diana == False:
        global array_dianas
        array_dianas.append(Diana(largo_juego - 9 * tamano_diana, ancho_juego / 2 - 13 * tamano_diana / 2, 1))
        hay_diana = True
        global array_obstaculos
        global array_obstaculos_g
        array_obstaculos_g = []
        array_obstaculos = []
        obs_g1 = Obstaculo_g(largo_juego / 2, largo_juego, 0, ancho_juego, 3)
    global fase_lanzamiento

    screen.fill(gray)
    pygame.draw.line(screen, dark_red, (largo_juego / 5, 0), (largo_juego / 5, ancho_juego), 5)

    if fase_lanzamiento == 2:
        pygame.draw.line(screen, white, (posrx1, posry1), pygame.mouse.get_pos())

    for proyectil in array_proyectiles:
        proyectil.avanzar()
        proyectil.dibujar()
    
#    if len(array_dianas) == 0:
 #       array_dianas.append(Diana(largo_juego - 9 * tamano_diana, random.randint(0, ancho_juego)))

    for d in array_dianas:
        d.avanzar()
        d.comprobar_choque()       
        d.dibujar()

running = True
fase_lanzamiento = 1
posrx1 = 0
posry1 = 0
posrx2 = 0
posry2 = 0
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and fase_lanzamiento == 1:
            if nivel_actual != 0:
                posrx1, posry1 = pygame.mouse.get_pos()
                if posrx1 < largo_juego / 5:
                    fase_lanzamiento = 2
            if nivel_actual == 0:
                for b in array_botones:
                    b.comprobar()
        if event.type == pygame.MOUSEBUTTONUP and fase_lanzamiento == 2:
            if nivel_actual != 0:
                posrx2, posry2 = pygame.mouse.get_pos()
                array_proyectiles.append(Proyectil(posrx1 - posrx2, posry1 - posry2, 10, posrx1, posry1, array_obstaculos))
                fase_lanzamiento = 1
    if nivel_actual == 0:
        menu.dibujar()
    if nivel_actual == 1:
        lvl1()
    if nivel_actual == 2:
        lvl2()
    if nivel_actual == 3:
        lvl3()
    if nivel_actual == 4:
        lvl4()
    if nivel_actual == 5:
        lvl5()
    pygame.display.flip()
