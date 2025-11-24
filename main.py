import pygame
from Game import Game   # Importamos la clase Game

pygame.init()

ANCHO, ALTO = 800, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("The legend of Mario")

fondo = pygame.image.load("fondo.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

fuente = pygame.font.SysFont("Comic Sans MS", 36)
fuente_ganar = pygame.font.SysFont("Times New Roman", 72)

NEGRO = (0, 0, 0)

estado = "inicio"
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    reloj.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()

    # ====================================================
    #  PANTALLA DE INICIO
    # ====================================================
    if estado == "inicio":

        ventana.blit(fondo, (0, 0))

        titulo = fuente_ganar.render("THE LEGEND OF MARIO", True, NEGRO)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 120))

        texto_inicio = fuente.render("Presiona ENTER para comenzar", True, NEGRO)
        ventana.blit(texto_inicio, (ANCHO//2 - texto_inicio.get_width()//2, 250))

        # Cambiar a juego
        if teclas[pygame.K_RETURN]:
            juego = Game(ventana)     # Crear objeto Game
            estado = "juego"

    # ====================================================
    #  PANTALLA DEL JUEGO (ESTÁ EN game.py)
    # ====================================================
    elif estado == "juego":
        resultado = juego.actualizar()   # Game retorna "ganaste", "perdiste" o None

        if resultado is not None:
            estado = "final"
            fin = resultado

    # ====================================================
    #  PANTALLA FINAL
    # ====================================================
    elif estado == "final":

        ventana.blit(fondo, (0, 0))

        if fin == "ganaste":
            texto = fuente_ganar.render("¡HAS GANADO!", True, NEGRO)
        else:
            texto = fuente_ganar.render("HAS PERDIDO", True, NEGRO)

        ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 150))

        texto2 = fuente.render("Presiona ENTER para volver al menú", True, NEGRO)
        ventana.blit(texto2, (ANCHO//2 - texto2.get_width()//2, 250))

        if teclas[pygame.K_RETURN]:
            estado = "inicio"

    pygame.display.flip()

pygame.quit()