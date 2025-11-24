import pygame, random

class Game:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ANCHO, self.ALTO = ventana.get_width(), ventana.get_height()

        # --- IMÁGENES DEL JUGADOR ---
        self.jugador_img = pygame.image.load("link1.png")    
        self.jugador_img1 = pygame.image.load("link.png")
 
        self.jugador_img = pygame.transform.scale(self.jugador_img, (50, 50))
        self.jugador_img1 = pygame.transform.scale(self.jugador_img1, (50, 50))

        self.imagen_jugador = self.jugador_img
        self.jugador = self.jugador_img.get_rect(x=50, y=250)

        # --- FÍSICA ---
        self.vel_y = 0
        self.en_suelo = False
        self.gravedad = 1
        self.velocidad_jugador = 5
        self.salto = -15

        # --- STATS ---
        self.vida = 3
        self.experiencia = 0

        # --- UI ---
        self.corazon = pygame.image.load("corazon.png")
        self.corazon = pygame.transform.scale(self.corazon, (25, 25))

        # --- FONDO ---
        self.fondo = pygame.image.load("fondo.png")
        self.fondo = pygame.transform.scale(self.fondo, (self.ANCHO, self.ALTO))

        # --- SUELO ---
        self.suelo = pygame.Rect(0, 310, self.ANCHO, 5)

        # --- ENEMIGOS ---
        self.enemigos = [pygame.Rect(500, 270, 40, 40)]

        self.intervalo = 4000       # Tiempo entre enemigos
        self.ultimo = pygame.time.get_ticks()

        # --- FUENTE ---
        self.fuente = pygame.font.Font(None, 36)


    def actualizar(self):

        teclas = pygame.key.get_pressed()

        # =====================================================
        # MOVIMIENTO DEL JUGADOR
        # =====================================================
        if teclas[pygame.K_LEFT]:
            self.imagen_jugador = self.jugador_img1
            self.jugador.x -= self.velocidad_jugador

        if teclas[pygame.K_RIGHT]:
            self.imagen_jugador = self.jugador_img
            self.jugador.x += self.velocidad_jugador

        # SALTO
        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = self.salto
            self.en_suelo = False
        
        # --- Pantalla envolvente jugador ---
        if self.jugador.x < -50:
            self.jugador.x = self.ANCHO
        elif self.jugador.x > self.ANCHO:
            self.jugador.x = -50


        # =====================================================
        # GRAVEDAD
        # =====================================================
        self.vel_y += self.gravedad
        self.jugador.y += self.vel_y

        # Colisión con suelo
        if self.jugador.colliderect(self.suelo):
            self.jugador.bottom = self.suelo.top
            self.vel_y = 0
            self.en_suelo = True

        # =====================================================
        # ENEMIGOS
        # =====================================================
        # Movimiento aleatorio
        for e in self.enemigos:

            # --- Movimiento inteligente hacia el jugador ---
            if self.jugador.x < e.x:
                e.x -= 2   # enemigo se mueve a la izquierda
            elif self.jugador.x > e.x:
                e.x += 2   # enemigo se mueve a la derecha

            # --- Gravedad del enemigo ---
            e.y += self.gravedad
            if e.colliderect(self.suelo):
                e.bottom = self.suelo.top

            # --- Pantalla envolvente ---
            if e.x < -40:
                e.x = self.ANCHO
            elif e.x > self.ANCHO:
                e.x = -40



        # Colisiones
        for e in self.enemigos[:]:

            if self.jugador.colliderect(e):

                # Saltar encima del enemigo para destruirlo
                if self.vel_y > 0 and self.jugador.bottom - e.top < 20:
                    self.enemigos.remove(e)
                    self.experiencia += 1
                    self.vel_y = self.salto // 2

                    if self.experiencia >= 10:
                        return "ganaste"
                    continue

                # Daño al jugador
                self.vida -= 1

                if self.vida <= 0:
                    return "perdiste"


        # SPAWN de enemigos nuevos
        tiempo = pygame.time.get_ticks()
        if tiempo - self.ultimo >= self.intervalo:
            self.enemigos.append(
                pygame.Rect(random.randint(200, 750), 270, 40, 40)
            )
            self.ultimo = tiempo

        # =====================================================
        # DIBUJAR TODO
        # =====================================================
        self.ventana.blit(self.fondo, (0, 0))
        self.ventana.blit(self.imagen_jugador, (self.jugador.x, self.jugador.y))

        # Enemigos
        for e in self.enemigos:
            pygame.draw.rect(self.ventana, (200, 0, 0), e)

        # XP y vida
        xp = self.fuente.render(f"XP: {self.experiencia}", True, (0, 0, 0))
        self.ventana.blit(xp, (10, 10))

        for i in range(self.vida):
            self.ventana.blit(self.corazon, (10 + i * 35, 35))

        return None
