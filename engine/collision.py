# -*- coding: utf-8 -*-
"""
Colisão: jangada × obstáculos (pedras).
Usa apenas lógica matemática (AABB); sem funções de bibliotecas gráficas.
"""


def check_collision_raft_obstacle(raft_x, raft_y, raft_w, raft_h, obs_x, obs_y, obs_radius):
    """
    Verifica colisão entre a jangada (retângulo AABB) e um obstáculo (círculo).
    Retorna True se houver sobreposição.

    Parâmetros:
        raft_x, raft_y: canto superior esquerdo da jangada
        raft_w, raft_h: largura e altura da jangada
        obs_x, obs_y: centro do obstáculo
        obs_radius: raio do obstáculo (aproximado como retângulo para AABB)
    """
    raft_left = raft_x
    raft_right = raft_x + raft_w
    raft_top = raft_y
    raft_bottom = raft_y + raft_h

    obs_left = obs_x - obs_radius
    obs_right = obs_x + obs_radius
    obs_top = obs_y - obs_radius
    obs_bottom = obs_y + obs_radius

    return not (
        raft_right < obs_left
        or raft_left > obs_right
        or raft_bottom < obs_top
        or raft_top > obs_bottom
    )


def check_collision_raft_fish(raft_x, raft_y, fish_x, fish_y):
    """
    Verifica colisão entre jangada e peixe.
    Jangada: aproximadamente 50x85 pixels (incluindo proa)
    Peixe: aproximadamente 28x12 pixels (corpo + cauda + barbatanas)
    """
    # Área aproximada da jangada
    raft_w = 50
    raft_h = 85  # altura_proa (15) + comprimento (70)
    raft_left = raft_x
    raft_top = raft_y
    raft_right = raft_x + raft_w
    raft_bottom = raft_top + raft_h
    
    # Área aproximada do peixe (corpo 20x12 + cauda ~8 pixels)
    fish_w = 28
    fish_h = 12
    fish_left = fish_x - fish_w // 2
    fish_right = fish_x + fish_w // 2
    fish_top = fish_y - fish_h // 2
    fish_bottom = fish_y + fish_h // 2
    
    # Verifica sobreposição de retângulos (AABB)
    return not (raft_right < fish_left or 
                raft_left > fish_right or 
                raft_bottom < fish_top or 
                raft_top > fish_bottom)

