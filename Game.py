import pygame, random
#162
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

        # --- ESPADA ---
        self.espada_img = pygame.image.load("espada.png")
        self.espada_img = pygame.transform.scale(self.espada_img, (40, 40))
        self.espada_img_izq = pygame.transform.flip(self.espada_img, True, False)
        self.espada = self.espada_img.get_rect()
        self.mirando_derecha = True
        self.atacando = False
        self.tiempo_ataque = 0
        self.duracion_ataque = 300  

        # --- ENEMIGOS ---
        self.Enemigo_img = pygame.image.load("enemigo.png")    
        self.Enemigo_img1 = pygame.image.load("enemigo1.png")
        self.Enemigo_img = pygame.transform.scale(self.Enemigo_img, (80, 70))
        self.Enemigo_img1 = pygame.transform.scale(self.Enemigo_img1, (80, 70))

        self.enemigos = [pygame.Rect(500, 270, 70, 70)]

        # --- JEFE (BOSS) ---
        self.boss_img = pygame.image.load("boss.png")
        self.boss_img = pygame.transform.scale(self.boss_img, (130, 120))
        self.boss = None
        self.boss_vida = 3
        self.boss_activo = False

        # --- FÍSICA ---
        self.vel_y = 5
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

        # --- SPAWN ---
        self.intervalo = 2500
        self.ultimo = pygame.time.get_ticks()

        # --- FUENTE ---
        self.fuente = pygame.font.Font(None, 36)

    # ----------------------------------------------------------
    # FUNCIÓN PARA CREAR BOSS
    # ----------------------------------------------------------
    def aparecer_boss(self):
        self.boss = pygame.Rect(700, 250, 130, 120)
        self.boss_vida = 3
        self.boss_activo = True

    # ----------------------------------------------------------
    # ACTUALIZAR JUEGO
    # ----------------------------------------------------------
    def actualizar(self):

        teclas = pygame.key.get_pressed()

        # MOVIMIENTO JUGADOR
        if teclas[pygame.K_LEFT]:
            self.imagen_jugador = self.jugador_img1
            self.jugador.x -= self.velocidad_jugador
            self.mirando_derecha = False

        if teclas[pygame.K_RIGHT]:
            self.imagen_jugador = self.jugador_img
            self.jugador.x += self.velocidad_jugador
            self.mirando_derecha = True

        if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
            self.velocidad_jugador = 8
        else:
            self.velocidad_jugador = 5

        if teclas[pygame.K_SPACE] and self.en_suelo:
            self.vel_y = self.salto
            self.en_suelo = False

        if teclas[pygame.K_z] and not self.atacando:
            self.atacando = True
            self.tiempo_ataque = pygame.time.get_ticks()

        # Pantalla envolvente
        if self.jugador.x < -50:
            self.jugador.x = self.ANCHO
        elif self.jugador.x > self.ANCHO:
            self.jugador.x = -50

        # GRAVEDAD
        self.vel_y += self.gravedad
        self.jugador.y += self.vel_y

        if self.jugador.colliderect(self.suelo):
            self.jugador.bottom = self.suelo.top
            self.vel_y = 0
            self.en_suelo = True

        # ACTUALIZAR ESPADA
        if self.mirando_derecha:
            self.espada.midleft = (self.jugador.right, self.jugador.centery)
        else:
            self.espada.midright = (self.jugador.left, self.jugador.centery)

        if self.atacando and pygame.time.get_ticks() - self.tiempo_ataque >= self.duracion_ataque:
            self.atacando = False

        # ----------------------------------------------------------
        # MOVIMIENTO ENEMIGOS NORMALES
        # ----------------------------------------------------------
        for e in self.enemigos:
            if self.jugador.x < e.x:
                e.x -= 2
            else:
                e.x += 2

            e.y += self.gravedad
            if e.colliderect(self.suelo):
                e.bottom = self.suelo.top

            if e.x < -40:
                e.x = self.ANCHO
            elif e.x > self.ANCHO:
                e.x = -40

        # ----------------------------------------------------------
        # COLISIONES CON ENEMIGOS
        # ----------------------------------------------------------
        for e in self.enemigos[:]:

            # Espada destruye enemigo
            if self.atacando and self.espada.colliderect(e):
                self.enemigos.remove(e)
                self.experiencia += 1

                if self.experiencia % 5 == 0 and not self.boss_activo: #10 para pruebas
                    self.aparecer_boss()

                continue

            # Jugador toca enemigo
            if self.jugador.colliderect(e):

                # Saltar sobre enemigo
                if self.vel_y > 0 and self.jugador.bottom - e.top < 20:
                    self.enemigos.remove(e)
                    self.experiencia += 1
                    self.vel_y = self.salto // 2

                    if self.experiencia % 5 == 0 and not self.boss_activo: #10 para pruebas
                        self.aparecer_boss()

                    continue

                # Daño
                self.vida -= 1
                self.enemigos.remove(e)
                if self.vida <= 0:
                    return "perdiste"

        # ----------------------------------------------------------
        # JEFE (BOSS)
        # ----------------------------------------------------------
        if self.boss_activo:

            # Movimiento hacia el jugador
            if self.jugador.x < self.boss.x:
                self.boss.x -= 1
            else:
                self.boss.x += 1

            # Gravedad
            self.boss.y += self.gravedad
            if self.boss.colliderect(self.suelo):
                self.boss.bottom = self.suelo.top

            # Espada golpea boss
            if self.atacando and self.espada.colliderect(self.boss):
                self.boss_vida -= 1

                if self.boss_vida <= 0:
                    self.boss_activo = False
                    self.boss = None
                    self.experiencia += 2
                    return None

            # Daño al jugador
            if self.jugador.colliderect(self.boss):
                self.vida -= 1
                self.jugador.x -= 50
                if self.vida <= 0:
                    return "perdiste"

        # SPAWN NUEVOS ENEMIGOS
        tiempo = pygame.time.get_ticks()
        if tiempo - self.ultimo >= self.intervalo:
            self.enemigos.append(
                pygame.Rect(random.randint(200, 750), 270, 80, 70)
            )
            self.ultimo = tiempo

        # ----------------------------------------------------------
        # DIBUJADO
        # ----------------------------------------------------------
        self.ventana.blit(self.fondo, (0, 0))
        self.ventana.blit(self.imagen_jugador, self.jugador)

        # Espada
        if self.atacando:
            espada_temporal = self.espada.copy()
            espada_temporal.width = 60
            if self.mirando_derecha:
                self.ventana.blit(pygame.transform.scale(self.espada_img, (60, 40)), espada_temporal)
            else:
                espada_temporal.x -= 20
                self.ventana.blit(pygame.transform.scale(self.espada_img_izq, (60, 40)), espada_temporal)
        else:
            if self.mirando_derecha:
                self.ventana.blit(self.espada_img, self.espada)
            else:
                self.ventana.blit(self.espada_img_izq, self.espada)

        # Enemigos
        for e in self.enemigos:
            if self.jugador.x < e.x:
                self.ventana.blit(self.Enemigo_img1, e)
            else:
                self.ventana.blit(self.Enemigo_img, e)

        # Jefe
        if self.boss_activo and self.boss:
            self.ventana.blit(self.boss_img, self.boss)

            hp_boss = self.fuente.render(f"Boss HP: {self.boss_vida}", True, (0,0,0))
            self.ventana.blit(hp_boss, (600, 10))

        # XP y vida
        xp = self.fuente.render(f"Puntos: {self.experiencia}", True, (0, 0, 0))
        self.ventana.blit(xp, (10, 10))

        for i in range(self.vida):
            self.ventana.blit(self.corazon, (10 + i * 35, 35))

        # CONDICIÓN DE VICTORIA: GANAR CUANDO SE ELIMINAN 20 ENEMIGOS
        if self.experiencia >= 15:
            return "ganaste"

        return None
