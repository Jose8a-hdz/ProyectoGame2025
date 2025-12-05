import pygame
from Game import Game   # Importamos la clase Game

pygame.init()
pygame.mixer.init()  # Inicializar el mixer de audio

ANCHO, ALTO = 800, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("The legend of Mario")

fondo = pygame.image.load("fondo.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

fuente = pygame.font.SysFont("Comic Sans MS", 32)
fuente_ganar = pygame.font.SysFont("Times New Roman", 60)

NEGRO = (0, 0, 0)
DORADO = (255, 215, 0)
BLANCO = (255, 255, 255)

# ====================================================
#  CARGAR MÚSICA DE FONDO
# ====================================================
try:
    pygame.mixer.music.load("audio.mp3")  # audio del fondo del juego
    pygame.mixer.music.set_volume(0.5)  # Volumen al 50%
    pygame.mixer.music.play(-1)  # -1 = repetir infinitamente
except:
    print("No se pudo cargar la música de fondo")

# Opcional: Cargar efectos de sonido
try:
    sonido_ganar = pygame.mixer.Sound("ganar.mp3")
    sonido_perder = pygame.mixer.Sound("perder.mp3")
    sonido_inicio = pygame.mixer.Sound("inicio.mp3")
except:
    sonido_ganar = None
    sonido_perder = None
    sonido_inicio = None
    print("No se pudieron cargar los efectos de sonido")

estado = "inicio"
reloj = pygame.time.Clock()
ejecutando = True
sonido_reproducido = False  # Para controlar que el sonido final se reproduzca una sola vez

# ====================================================
#  FUNCIÓN PARA RENDERIZAR TEXTO CON BORDE
# ====================================================
def render_text_outlined(font, text, color, outline_color, outline_width=2):
    """Renderiza texto con borde negro"""
    base = font.render(text, True, color)
    outline = font.render(text, True, outline_color)
    
    w, h = base.get_size()
    surface = pygame.Surface((w + outline_width * 2, h + outline_width * 2), pygame.SRCALPHA)
    
    # Renderizar el borde en 8 direcciones para un mejor efecto
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                surface.blit(outline, (dx + outline_width, dy + outline_width))
    
    # Texto principal en el centro
    surface.blit(base, (outline_width, outline_width))
    
    return surface

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
        
        # Título con borde negro
        titulo = render_text_outlined(fuente_ganar, "THE LEGEND OF MARIO", DORADO, NEGRO, 3)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 120))
        
        # Texto de inicio con borde negro
        texto_inicio = render_text_outlined(fuente, "Presiona ENTER para comenzar", BLANCO, NEGRO, 2)
        ventana.blit(texto_inicio, (ANCHO//2 - texto_inicio.get_width()//2, 250))
        
        # Cambiar a juego
        if teclas[pygame.K_RETURN]:
            if sonido_inicio:
                sonido_inicio.play()
            juego = Game(ventana)     # Crear objeto Game
            estado = "juego"
            sonido_reproducido = False  # Resetear para la pantalla final
    
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
        # Reproducir sonido de victoria/derrota solo una vez
        if not sonido_reproducido:
            if fin == "ganaste" and sonido_ganar:
                sonido_ganar.play()
            elif fin == "perdiste" and sonido_perder:
                sonido_perder.play()
            sonido_reproducido = True
        
        ventana.blit(fondo, (0, 0))
        
        # Texto final con borde
        if fin == "ganaste":
            texto = render_text_outlined(fuente_ganar, "¡HAS GANADO!", DORADO, NEGRO, 3)
        else:
            texto = render_text_outlined(fuente_ganar, "HAS PERDIDO", DORADO, NEGRO, 3)
        
        ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 150))
        
        # Texto de reinicio con borde
        texto2 = render_text_outlined(fuente, "Presiona ENTER para volver al menú", BLANCO, NEGRO, 2)
        ventana.blit(texto2, (ANCHO//2 - texto2.get_width()//2, 250))
        
        if teclas[pygame.K_RETURN]:
            estado = "inicio"
    
    pygame.display.flip()

pygame.quit()