# -*- coding: utf-8 -*-
"""
Jangada renderizada com set_pixel e gradiente de duas cores marrons.
Controle WASD e coleta de peixes.
"""

import pygame
import sys
import random
import math
import assets.colors as color
import app.constants as constant
import app.entities.fish as fish
import app.entities.obstacle as obstacle
import app.entities.icons as icon
import app.entities.raft as raft
import app.entities.minimap as minimap
from app.scenes.auxiliary_functions import draw_simple_text
from engine.collision import check_collision_raft_obstacle, check_collision_raft_fish
from app.scenes.game_over import run_game_over
from app.scenes.victory import run_victory
from assets.music_manager import music_manager

def main():
    pygame.init()
    
    # ===== VIEWPORT (TELA) =====
    WIDTH, HEIGHT = 1000, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jangadeiro: Dragão do Mar")
    
    clock = pygame.time.Clock()

    # ===== JANELA (MUNDO) =====
    WORLD_WIDTH = 3000
    WORLD_HEIGHT = 3000

    # Inicia música do gameplay
    music_manager.play("gameplay")
    
    while True:
        # ===== POSIÇÕES NO MUNDO (reset a cada "jogar novamente") =====
        raft_x = WORLD_WIDTH // 2
        raft_y = WORLD_HEIGHT // 2
        speed = 4

        fish_x = random.randint(100, WORLD_WIDTH - 100)
        fish_y_base = random.randint(100, WORLD_HEIGHT - 100)
        fish_y = fish_y_base

        fish_animation_offset = 0.0
        fish_animation_speed = 0.15
        fish_animation_range = 8

        # Spawnar obstáculos: 5 de cada tipo (0=rocha, 1=alga, 2=coral)
        NUM_OBSTACULOS_POR_TIPO = 5
        obstaculos = []
        
        for tipo in range(3):  # 0=rocha, 1=alga, 2=coral
            for _ in range(NUM_OBSTACULOS_POR_TIPO):
                while True:
                    ox = random.randint(100, WORLD_WIDTH - 100)
                    oy = random.randint(100, WORLD_HEIGHT - 100)
                    if abs(ox - fish_x) < 80 and abs(oy - fish_y_base) < 80:
                        continue
                    if any(abs(ox - obs[0]) < 80 and abs(oy - obs[1]) < 80 for obs in obstaculos):
                        continue
                    obstaculos.append([ox, oy, tipo])
                    break

        pontos = 0
        vidas = 3

        rotation_frames_left = 0
        ROTATION_TOTAL_FRAMES = 60

        hud_scale_effect_frames = 0
        HUD_SCALE_EFFECT_FRAMES = 60

        running = True
        while running:
            screen.fill(color.SEA_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # ===== INPUT (MOVE NO MUNDO) — desabilitado durante rotação =====
            if rotation_frames_left <= 0:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    raft_y -= speed
                if keys[pygame.K_s]:
                    raft_y += speed
                if keys[pygame.K_a]:
                    raft_x -= speed
                if keys[pygame.K_d]:
                    raft_x += speed

            # Limites do MUNDO
            raft_x = max(0, min(WORLD_WIDTH - constant.RAFT_LARGURA, raft_x))
            raft_y = max(0, min(WORLD_HEIGHT - constant.RAFT_ALTURA, raft_y))

            # ===== CÂMERA (VIEWPORT) =====
            camera_x = raft_x - WIDTH // 2
            camera_y = raft_y - HEIGHT // 2

            camera_x = max(0, min(WORLD_WIDTH - WIDTH, camera_x))
            camera_y = max(0, min(WORLD_HEIGHT - HEIGHT, camera_y))

            viewport = (camera_x, camera_y, WIDTH, HEIGHT)

            # ===== ANIMAÇÃO DO PEIXE =====
            fish_animation_offset += fish_animation_speed
            fish_y = fish_y_base + math.sin(fish_animation_offset) * fish_animation_range

            # ===== COLISÕES (EM COORDENADAS DO MUNDO) =====
            if check_collision_raft_fish(raft_x, raft_y, fish_x, fish_y_base):
                pontos += 1
                fish_x = random.randint(100, WORLD_WIDTH - 100)
                fish_y_base = random.randint(100, WORLD_HEIGHT - 100)
                fish_animation_offset = 0.0
                hud_scale_effect_frames = HUD_SCALE_EFFECT_FRAMES  # Reação: HUD em escala maior

            # Colisão jangada × pedra (engine): perde vida e inicia rotação 360°
            if rotation_frames_left <= 0:
                for obs in obstaculos[:]:
                    if check_collision_raft_obstacle(
                        raft_x, raft_y, constant.RAFT_LARGURA, constant.RAFT_ALTURA,
                        obs[0], obs[1], constant.OBSTACLE_RADIUS
                    ):
                        vidas -= 1
                        rotation_frames_left = ROTATION_TOTAL_FRAMES
                        hud_scale_effect_frames = HUD_SCALE_EFFECT_FRAMES
                        # bloqueia movimento até sair do obstáculo
                        if keys[pygame.K_w]: raft_y += speed
                        if keys[pygame.K_s]: raft_y -= speed
                        if keys[pygame.K_a]: raft_x += speed
                        if keys[pygame.K_d]: raft_x -= speed
                        break

            # Avanço da animação de rotação (0 → 2π)
            if rotation_frames_left > 0:
                rotation_frames_left -= 1

            # Avanço do efeito de escala do HUD (~1 s)
            if hud_scale_effect_frames > 0:
                hud_scale_effect_frames -= 1

            if vidas <= 0:
                running = False
                resultado = "GAME OVER"
            elif pontos >= 5:
                running = False
                resultado = "VITORIA"

            # ===== DESENHO (MUNDO → VIEWPORT) =====
            fish.draw_waves_around_fish(
                screen,
                fish_x - camera_x,
                fish_y_base - camera_y,
                fish_animation_offset
            )

            fish.draw_fish(
                screen,
                fish_x - camera_x,
                int(fish_y - camera_y)
            )

            for obs in obstaculos:
                obstacle.draw_obstacle(
                    screen,
                    obs[0] - camera_x,
                    obs[1] - camera_y,
                    tipo=obs[2]
                )

            # Ângulo de rotação ao colidir com pedra (0 → 2π)
            raft_angle = 0.0
            if rotation_frames_left > 0:
                raft_angle = (ROTATION_TOTAL_FRAMES - rotation_frames_left) / ROTATION_TOTAL_FRAMES * 2 * math.pi
            raft.draw_raft(
                screen,
                raft_x - camera_x,
                raft_y - camera_y,
                viewport,
                angle=raft_angle
            )

            minimap.draw_minimap(
                screen,
                raft_x, raft_y,
                fish_x, fish_y_base,
                obstaculos,
                camera_x, camera_y,
                WORLD_WIDTH, WORLD_HEIGHT,
                WIDTH, HEIGHT
            )

            # ===== HUD CENTRALIZADO (PARTE SUPERIOR) =====
            center_x = WIDTH // 2
            hud_scale = 3 if hud_scale_effect_frames > 0 else 2
            
            # Definir posição base alinhada
            icon_x = center_x - 50  # Posição X dos ícones
            text_x = center_x - 10  # Posição X do texto (mais próximo)
            
            # Pontos com ícone (primeira linha)
            # Peixe: desenha de y-b até y+b, com tamanho=8, b=8//3=2
            # Centro real está em y, ajustando texto para alinhar melhor
            fish_y = 18
            icon.draw_fish_icon(screen, icon_x, fish_y, tamanho=8, scale=hud_scale)
            draw_simple_text(screen, f"{pontos}/5", text_x, fish_y - 3, (255, 215, 0), scale=hud_scale)
            
            # Vidas com ícone (segunda linha, alinhado)
            # X diminuído e movido para esquerda para alinhar com o peixe
            heart_y = 40
            icon.draw_heart_icon(screen, icon_x - 5, heart_y, tamanho=4, scale=hud_scale)
            draw_simple_text(screen, f"{vidas}/3", text_x, heart_y + 3, (255, 100, 100), scale=hud_scale)

            pygame.display.flip()
            clock.tick(60)

        # ===== TELA FINAL: Game Over ou Vitória =====
        if resultado == "GAME OVER":
            escolha = run_game_over(screen)
        else:
            escolha = run_victory(screen)

        if escolha == "sair":
            break
        # "jogar_novamente" → loop continua e estado é resetado no início do while True

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
