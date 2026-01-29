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
