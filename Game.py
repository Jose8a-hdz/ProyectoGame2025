import pygame, random

class Game:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ANCHO, self.ALTO = ventana.get_width(), ventana.get_height()

        self.jugador_img = pygame.image.load("link.webp")
        self.jugador_img = pygame.transform.scale(self.jugador_img, (50, 50))
        self.jugador = self.jugador_img.get_rect(x=50, y=250)

        self.vel_y = 0
        self.en_suelo = False
        self.vida = 3
        self.experiencia = 0

        self.corazon = pygame.image.load("corazon.png")
        self.corazon = pygame.transform.scale(self.corazon, (25, 25))

        self.fondo = pygame.image.load("fondo.png")
        self.fondo = pygame.transform.scale(self.fondo, (self.ANCHO, self.ALTO))

        self.suelo = pygame.Rect(0, 310, self.ANCHO, 5)
        self.enemigos = [pygame.Rect(500, 270, 40, 40)]

        self.gravedad = 1
        self.velocidad = 5
        self.salto = -15

        self.fuente = pygame.font.Font(None, 36)

        self.intervalo = 1000
        self.ultimo = pygame.time.get_ticks()

    # Actualiza lógica y dibuja
    def actualizar(self):

        teclas = pygame.key.get_pressed()

        # Movimiento
        if teclas[pygame.K_LEFT]:
            self.jugador.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.jugador.x += self.velocidad
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = self.salto
            self.en_suelo = False

        # Gravedad
        self.vel_y += self.gravedad
        self.jugador.y += self.vel_y

        # Suelo
        if self.jugador.colliderect(self.suelo):
            self.jugador.bottom = self.suelo.top
            self.vel_y = 0
            self.en_suelo = True

        # Movimiento de enemigos
        for e in self.enemigos:
            e.x += random.choice([-1, 1])

        # Colisiones
        for e in self.enemigos[:]:

            if self.jugador.colliderect(e):

                # Salto sobre enemigo
                if self.vel_y > 0 and self.jugador.bottom - e.top < 20:
                    self.enemigos.remove(e)
                    self.experiencia += 1
                    self.vel_y = self.salto // 2

                    if self.experiencia >= 10:
                        return "ganaste"

                    continue

                # Golpe normal
                self.vida -= 1

                if self.vida <= 0:
                    return "perdiste"

        # Spawn enemigo
        tiempo = pygame.time.get_ticks()
        if tiempo - self.ultimo >= self.intervalo:
            self.enemigos.append(pygame.Rect(random.randint(200, 750), 270, 40, 40))
            self.ultimo = tiempo

        # Dibujar pantalla de juego
        self.ventana.blit(self.fondo, (0,0))
        self.ventana.blit(self.jugador_img, self.jugador.topleft)

        for e in self.enemigos:
            pygame.draw.rect(self.ventana, (200,0,0), e)

        # XP y vida
        xp = self.fuente.render(f"XP: {self.experiencia}", True, (0,0,0))
        self.ventana.blit(xp, (10,10))

        for i in range(self.vida):
            self.ventana.blit(self.corazon, (10 + i*35, 35))

        return None