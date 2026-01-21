## Folder Structure

```bash
project-name/
│
├── README.md
├── requirements.txt
├── main.py
│
├── engine/
│   ├── __init__.py
│   │
│   ├── framebuffer.py      # set_pixel, clear, buffer
│   │
│   ├── raster/
│   │   ├── __init__.py
│   │   ├── line.py         # Bresenham / DDA
│   │   ├── circle.py       # Midpoint Circle
│   │   └── ellipse.py      # Midpoint Ellipse
│   │
│   ├── fill/
│   │   ├── __init__.py
│   │   ├── flood_fill.py
│   │   ├── boundary_fill.py
│   │   └── scanline.py
│   │
│   ├── geometry/
│   │   ├── __init__.py
│   │   ├── polygon.py      # vértices, edges
│   │   ├── transform.py    # matrizes 3x3
│   │   └── clipping.py     # Cohen-Sutherland
│   │
│   ├── viewport/
│   │   ├── __init__.py
│   │   └── viewport.py     # janela -> viewport
│   │
│   ├── texture/
│   │   ├── __init__.py
│   │   └── texture.py      # mapeamento UV
│   │
│   └── math/
│       ├── __init__.py
│       └── matrix.py       # operações auxiliares
│
├── app/                    # JOGO / SIMULAÇÃO
│   ├── __init__.py
│   │
│   ├── scenes/
│   │   ├── menu.py
│   │   ├── intro.py        # tela de abertura
│   │   └── game.py
│   │
│   ├── entities/
│   │   ├── entity.py
│   │   ├── player.py
│   │   └── obstacle.py
│   │
│   ├── input/
│   │   └── input_handler.py
│   │
│   └── state_manager.py
│
├── assets/
│   ├── textures/
│   └── screenshots/
│
└── docs/
    ├── design.md
    ├── algorithms.md
    └── presentation.md
````
