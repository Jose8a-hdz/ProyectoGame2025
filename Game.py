import pygame
import random
pygame.init()

# --- Configuración de ventana ---
ANCHO, ALTO = 800, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mini Mario Bros con XP y Enemigos Dinámicos")

# --- Colores ---
AZUL = (100, 149, 237)
VERDE = (34, 177, 76)
ROJO = (200, 0, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# --- Jugador ---
jugador = pygame.Rect(100, 300, 40, 40)
vel_y = 0
en_suelo = False

# --- Suelo ---
suelo = pygame.Rect(0, 360, ANCHO, 40)

# --- Enemigos iniciales ---
enemigos = []
for i in range(1):
    x = random.randint(200, 750)
    enemigo = pygame.Rect(x, 320, 40, 40)
    enemigos.append(enemigo)

# --- Físicas ---
gravedad = 1
velocidad = 5
salto = -15

# --- Experiencia ---
experiencia = 0
fuente = pygame.font.Font(None, 36)
fuente_ganar = pygame.font.Font(None, 72)

# --- Timers ---
tiempo_inicial = pygame.time.get_ticks()  # tiempo total del juego
intervalo_enemigo = 1000  # 10 segundos (en milisegundos)
ultimo_enemigo = tiempo_inicial  # última vez que apareció un enemigo

# --- Juego ---
reloj = pygame.time.Clock()
ejecutando = True
ganado = False

while ejecutando:
    reloj.tick(60)
    tiempo_actual = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False

    if not ganado:
        # --- Movimiento del jugador ---
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jugador.x -= velocidad
        if teclas[pygame.K_RIGHT]:
            jugador.x += velocidad
        if teclas[pygame.K_SPACE] and en_suelo:
            vel_y = salto
            en_suelo = False

        # --- Gravedad ---
        vel_y += gravedad
        jugador.y += vel_y

        # --- Colisión con el suelo ---
        if jugador.colliderect(suelo):
            jugador.bottom = suelo.top
            vel_y = 0
            en_suelo = True

        # --- Movimiento simple de enemigos ---
        for enemigo in enemigos:
            enemigo.x += random.choice([-1, 1])
            enemigo.x = max(0, min(ANCHO - enemigo.width, enemigo.x))

        # --- Colisión con enemigos ---
        for enemigo in enemigos[:]:
            if jugador.colliderect(enemigo):
                # Si cae sobre el enemigo (parte superior)
                if vel_y > 0 and jugador.bottom - enemigo.top < 20:
                    enemigos.remove(enemigo)
                    experiencia += 1
                    vel_y = salto / 2  # Rebota

                    # ✅ Condición de victoria
                    if experiencia >= 10:
                        ganado = True
                else:
                    print("¡Has perdido!")
                    ejecutando = False

        # --- 👾 Aparición automática de enemigos cada 10 segundos ---
        if tiempo_actual - ultimo_enemigo >= intervalo_enemigo:
            x = random.randint(200, 750)
            nuevo_enemigo = pygame.Rect(x, 320, 40, 40)
            enemigos.append(nuevo_enemigo)
            ultimo_enemigo = tiempo_actual  # reiniciar temporizador

    # --- Dibujar ---
    ventana.fill(AZUL)
    pygame.draw.rect(ventana, VERDE, suelo)
    pygame.draw.rect(ventana, BLANCO, jugador)
    for enemigo in enemigos:
        pygame.draw.rect(ventana, ROJO, enemigo)

    # Texto de experiencia
    texto_xp = fuente.render(f"Experiencia: {experiencia}", True, NEGRO)
    ventana.blit(texto_xp, (10, 10))

    # --- Pantalla de victoria ---
    if ganado:
        mensaje = fuente_ganar.render("🎉 ¡HAS GANADO! 🎉", True, NEGRO)
        ventana.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2 - 50))

    pygame.display.flip()

pygame.quit()
