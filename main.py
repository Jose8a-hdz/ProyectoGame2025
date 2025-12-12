import pygame
import sqlite3
from datetime import datetime
from Game import Game

pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 800, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("The legend of Mario")

fondo = pygame.image.load("fondo.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

fuente = pygame.font.SysFont("Comic Sans MS", 32)
fuente_ganar = pygame.font.SysFont("Times New Roman", 60)
fuente_pequeña = pygame.font.SysFont("Comic Sans MS", 24)

NEGRO = (0, 0, 0)
DORADO = (255, 215, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (100, 150, 255)

# ====================================================
#  INICIALIZAR BASE DE DATOS SQLite3
# ====================================================
def inicializar_db():
    conn = sqlite3.connect('mario_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS puntuaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            puntos INTEGER NOT NULL,
            resultado TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def guardar_puntuacion(nombre, puntos, resultado):
    conn = sqlite3.connect('mario_scores.db')
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO puntuaciones (nombre, puntos, resultado, fecha)
        VALUES (?, ?, ?, ?)
    ''', (nombre, puntos, resultado, fecha))
    conn.commit()
    conn.close()

def obtener_mejores_puntuaciones(limite=10):
    conn = sqlite3.connect('mario_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nombre, puntos, resultado, fecha
        FROM puntuaciones
        ORDER BY puntos DESC, fecha DESC
        LIMIT ?
    ''', (limite,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

inicializar_db()

# ====================================================
#  CARGAR MÚSICA Y SONIDOS
# ====================================================
try:
    pygame.mixer.music.load("audio.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
except:
    print("No se pudo cargar la música de fondo")

try:
    sonido_ganar = pygame.mixer.Sound("ganar.mp3")
    sonido_perder = pygame.mixer.Sound("perder.mp3")
    sonido_inicio = pygame.mixer.Sound("inicio.mp3")
except:
    sonido_ganar = None
    sonido_perder = None
    sonido_inicio = None
    print("No se pudieron cargar los efectos de sonido")

# ====================================================
#  VARIABLES GLOBALES
# ====================================================
estado = "inicio"
reloj = pygame.time.Clock()
ejecutando = True
sonido_reproducido = False
nombre_jugador = ""
puntos_finales = 0

# ====================================================
#  FUNCIÓN PARA RENDERIZAR TEXTO CON BORDE
# ====================================================
def render_text_outlined(font, text, color, outline_color, outline_width=2):
    base = font.render(text, True, color)
    outline = font.render(text, True, outline_color)
    
    w, h = base.get_size()
    surface = pygame.Surface((w + outline_width * 2, h + outline_width * 2), pygame.SRCALPHA)
    
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                surface.blit(outline, (dx + outline_width, dy + outline_width))
    
    surface.blit(base, (outline_width, outline_width))
    return surface

# ====================================================
#  BUCLE PRINCIPAL
# ====================================================
while ejecutando:
    reloj.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
        
        # Capturar entrada de texto en la pantalla de nombre
        if estado == "ingresar_nombre" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(nombre_jugador) > 0:
                # Guardar puntuación y pasar a la pantalla final
                guardar_puntuacion(nombre_jugador, puntos_finales, fin)
                estado = "final_guardado"
            elif event.key == pygame.K_BACKSPACE:
                nombre_jugador = nombre_jugador[:-1]
            elif len(nombre_jugador) < 15 and event.unicode.isprintable():
                nombre_jugador += event.unicode
    
    teclas = pygame.key.get_pressed()
    
    # ====================================================
    #  PANTALLA DE INICIO
    # ====================================================
    if estado == "inicio":
        ventana.blit(fondo, (0, 0))
        
        titulo = render_text_outlined(fuente_ganar, "THE LEGEND OF MARIO", DORADO, NEGRO, 3)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 80))
        
        texto_inicio = render_text_outlined(fuente, "Presiona ENTER para comenzar", BLANCO, NEGRO, 2)
        ventana.blit(texto_inicio, (ANCHO//2 - texto_inicio.get_width()//2, 200))
        
        texto_scores = render_text_outlined(fuente_pequeña, "Presiona S para ver puntuaciones", BLANCO, NEGRO, 2)
        ventana.blit(texto_scores, (ANCHO//2 - texto_scores.get_width()//2, 250))
        
        if teclas[pygame.K_RETURN]:
            if sonido_inicio:
                sonido_inicio.play()
            juego = Game(ventana)
            estado = "juego"
            sonido_reproducido = False
            nombre_jugador = ""
        
        if teclas[pygame.K_s]:
            estado = "ver_puntuaciones"
    
    # ====================================================
    #  PANTALLA DEL JUEGO
    # ====================================================
    elif estado == "juego":
        resultado = juego.actualizar()
        if resultado is not None:
            fin = resultado
            # Obtener puntos desde el atributo 'experiencia' de Game
            puntos_finales = juego.experiencia
            estado = "ingresar_nombre"
    
    # ====================================================
    #  PANTALLA PARA INGRESAR NOMBRE
    # ====================================================
    elif estado == "ingresar_nombre":
        if not sonido_reproducido:
            if fin == "ganaste" and sonido_ganar:
                sonido_ganar.play()
            elif fin == "perdiste" and sonido_perder:
                sonido_perder.play()
            sonido_reproducido = True
        
        ventana.blit(fondo, (0, 0))
        
        if fin == "ganaste":
            texto = render_text_outlined(fuente_ganar, "¡HAS GANADO!", DORADO, NEGRO, 3)
        else:
            texto = render_text_outlined(fuente_ganar, "HAS PERDIDO", DORADO, NEGRO, 3)
        
        ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 80))
        
        # Mostrar puntos
        texto_puntos = render_text_outlined(fuente, f"Puntos: {puntos_finales}", BLANCO, NEGRO, 2)
        ventana.blit(texto_puntos, (ANCHO//2 - texto_puntos.get_width()//2, 160))
        
        # Instrucciones
        texto_nombre = render_text_outlined(fuente_pequeña, "Ingresa tu nombre (máx 15 caracteres):", BLANCO, NEGRO, 2)
        ventana.blit(texto_nombre, (ANCHO//2 - texto_nombre.get_width()//2, 220))
        
        # Caja de texto
        caja_rect = pygame.Rect(ANCHO//2 - 150, 260, 300, 40)
        pygame.draw.rect(ventana, BLANCO, caja_rect, 2)
        
        texto_input = fuente.render(nombre_jugador, True, BLANCO)
        ventana.blit(texto_input, (caja_rect.x + 10, caja_rect.y + 5))
        
        # Cursor parpadeante
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = caja_rect.x + 10 + texto_input.get_width()
            pygame.draw.line(ventana, BLANCO, (cursor_x, caja_rect.y + 5), 
                           (cursor_x, caja_rect.y + 35), 2)
        
        # Instrucción final
        texto_enter = render_text_outlined(fuente_pequeña, "Presiona ENTER para guardar", 
                                          VERDE if len(nombre_jugador) > 0 else ROJO, NEGRO, 2)
        ventana.blit(texto_enter, (ANCHO//2 - texto_enter.get_width()//2, 320))
    
    # ====================================================
    #  PANTALLA FINAL CON PUNTUACIÓN GUARDADA
    # ====================================================
    elif estado == "final_guardado":
        ventana.blit(fondo, (0, 0))
        
        texto = render_text_outlined(fuente_ganar, "¡PUNTUACIÓN GUARDADA!", DORADO, NEGRO, 3)
        ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, 100))
        
        texto_info = render_text_outlined(fuente, f"{nombre_jugador}: {puntos_finales} puntos", BLANCO, NEGRO, 2)
        ventana.blit(texto_info, (ANCHO//2 - texto_info.get_width()//2, 200))
        
        texto2 = render_text_outlined(fuente_pequeña, "Presiona ENTER para volver al menú", BLANCO, NEGRO, 2)
        ventana.blit(texto2, (ANCHO//2 - texto2.get_width()//2, 260))
        
        texto3 = render_text_outlined(fuente_pequeña, "Presiona S para ver puntuaciones", BLANCO, NEGRO, 2)
        ventana.blit(texto3, (ANCHO//2 - texto3.get_width()//2, 300))
        
        if teclas[pygame.K_RETURN]:
            estado = "inicio"
        if teclas[pygame.K_s]:
            estado = "ver_puntuaciones"
    
    # ====================================================
    #  PANTALLA DE MEJORES PUNTUACIONES
    # ====================================================
    elif estado == "ver_puntuaciones":
        ventana.blit(fondo, (0, 0))
        
        titulo = render_text_outlined(fuente_ganar, "MEJORES PUNTUACIONES", DORADO, NEGRO, 3)
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 20))
        
        mejores = obtener_mejores_puntuaciones(8)
        
        if len(mejores) == 0:
            texto_vacio = render_text_outlined(fuente, "No hay puntuaciones aún", BLANCO, NEGRO, 2)
            ventana.blit(texto_vacio, (ANCHO//2 - texto_vacio.get_width()//2, 150))
        else:
            y_pos = 100
            for i, (nombre, puntos, resultado, fecha) in enumerate(mejores, 1):
                # Color según resultado
                color = DORADO if resultado == "ganaste" else NEGRO
                
                # Posición y medalla
                medalla = ""
                if i == 1:
                    medalla = " PRIMER LUGAR "
                elif i == 2:
                    medalla = " SEGUNDO LUGAR "
                elif i == 3:
                    medalla = " TERCER LUGAR "
                else:
                    medalla = f"{i}. "
                
                # Formatear fecha (solo día y hora)
                fecha_corta = fecha.split()[0] if ' ' in fecha else fecha
                
                texto_score = fuente_pequeña.render(
                    f"{medalla}{nombre}: {puntos} pts - {resultado}", True, color)
                ventana.blit(texto_score, (50, y_pos))
                y_pos += 30
        
        texto_volver = render_text_outlined(fuente_pequeña, "Presiona ESC para volver", BLANCO, NEGRO, 2)
        ventana.blit(texto_volver, (ANCHO//2 - texto_volver.get_width()//2, 360))
        
        if teclas[pygame.K_ESCAPE]:
            estado = "inicio"
    
    pygame.display.flip()

pygame.quit()