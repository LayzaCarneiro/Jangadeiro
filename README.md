# Jangadeiro: Dragão do Mar 🚣

**Jogo 2D desenvolvido em Python com Pygame**, utilizando exclusivamente algoritmos de rasterização via `set_pixel`.

Projeto acadêmico da disciplina de **Computação Gráfica**, desenvolvido para explorar técnicas de rasterização, transformações geométricas, recorte e animação.

---

## Descrição do Projeto

O jogo simula a vida dos **jangadeiros do Ceará**, com elementos históricos e desafios de navegação:

* Tela de abertura com introdução animada mostrando o **Dragão do Mar**.
* Jogo baseado em **coleta de peixes**, evitando obstáculos.
* Polígonos, gradientes e preenchimentos são renderizados com **algoritmos manuais**.
* Interação via teclado (W-A-S-D) e mouse para menus.

---

**Recursos Implementados (Atendem os requisitos do trabalho):**

| Requisito                                 | Implementação no jogo                                                                                                            |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Set Pixel**                             | Todas as primitivas gráficas utilizam `set_pixel`.                                                                               |
| **Rasterização**                          | Linhas (Bresenham/DDA), círculos (Midpoint Circle) e elipses (Midpoint Ellipse).                                                 |
| **Preenchimento de regiões**              | Flood Fill para mar e céu, Scanline para polígonos e jangadas.                                                                   |
| **Transformações geométricas**            | Translação, escala e rotação aplicadas em sprites e polígonos.                                                                   |
| **Animação 2D**                           | Movimentação do peixe, ondas e estrelas na tela inicial.                                                                         |
| **Janela e Viewport**                     | Minimapa com escalas de mundo → dispositivo; transformação de coordenadas aplicada; viewport desenhando câmera sobre o minimapa. |
| **Recorte Cohen-Sutherland**              | Implementado para recorte de obstáculos e movimentação da jangada na tela de jogo.                                               |
| **Mapeamento de textura**                 | Gradientes e texturas básicas aplicadas em areia e água.                                                                         |
| **Input (Teclado/Mouse)**                 | Menu interativo, movimento da jangada e ações no jogo.                                                                           |
| **Menus e interações gráficas avançadas** | Tela de abertura animada, menu interativo, instruções e tela de vitória/game over.                                               |

---

## Screenshots

Alguns exemplos de telas do jogo:

<img width="600" alt="Tela 1" src="https://github.com/user-attachments/assets/37bdb0bf-6d2b-4b4f-a523-83dc90df7d24" />
<img width="600" alt="Tela 2" src="https://github.com/user-attachments/assets/a59c54f0-3095-4144-8926-7eded7ac0cda" />
<img width="600" alt="Tela 3" src="https://github.com/user-attachments/assets/077da983-45d7-41a1-9fa8-105e2bdd4cde" />
<img width="600" alt="Tela 4" src="https://github.com/user-attachments/assets/68ab5fcf-947b-4289-a43b-26783f7d0769" />
<img width="600" alt="Tela 5" src="https://github.com/user-attachments/assets/f2dbf3bb-9d13-4068-a8a3-b0ef68a4d42a" />

## Vídeo Demonstrativo

Assista a execução completa do jogo no YouTube:

[Jangadeiro: Dragão do Mar](https://youtu.be/tAzGCbpE4CU)

---

## Requisitos do Sistema

- **Python:** 3.8 ou superior
- **Sistema Operacional:** Windows, Linux ou macOS
- **Pygame:** 2.5.0 ou superior

---

## Instalação

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/LayzaCarneiro/Jangadeiro
cd Jangadeiro
```

### 2. (Opcional) Crie um ambiente virtual

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

> **Alternativas:** `pip3 install -r requirements.txt` ou `python -m pip install -r requirements.txt`

---

## Como Rodar

1. Execute o jogo:
   ```bash
   python main.py
   ```
   (ou `python3 main.py` no Linux/macOS)

2. Execute o jogo:
   ```bash
   python main.py
   ```
   (ou `python3 main.py`)

2. Na tela inicial (após animação de introdução):
   - **INICIAR** – inicia o jogo
   - **COMO JOGAR** – exibe instruções e controles
   - **SAIR** – encerra o programa

3. Controles do jogo:
   - **W/A/S/D** – mover a jangada
   - **ESC** – sair do jogo

4. Objetivo:
   - Colete **5 peixes** para vencer
   - Evite **obstáculos** – você tem 3 vidas

---

## Como Visualizar a Documentação (arquivos .md)

A documentação técnica completa está em `docs/documentacao.md`. Para visualizar arquivos Markdown formatados:

### Visual Studio Code (Recomendado)

1. **Visualização nativa:** Abra o arquivo `.md` e pressione `Ctrl+Shift+V` (ou `Cmd+Shift+V` no macOS) para abrir o preview.

2. **Preview lado a lado:** Pressione `Ctrl+K V` para abrir o preview ao lado do código.

3. **Extensão recomendada:** Instale a extensão **Markdown Preview Enhanced** para recursos avançados:
   - Abra a paleta de comandos (`Ctrl+Shift+P`)
   - Digite `Extensions: Install Extensions`
   - Pesquise por `Markdown Preview Enhanced`
   - Clique em **Install**
   - Use `Ctrl+Shift+V` para preview aprimorado com suporte a diagramas e tabelas

### Outros Editores

| Editor | Como visualizar Markdown |
|--------|-------------------------|
| **PyCharm** | Clique direito no arquivo → *Open in* → *Markdown Preview* |
| **Sublime Text** | Instale o pacote `MarkdownPreview` via Package Control |
| **Atom** | Pressione `Ctrl+Shift+M` (preview nativo) |
| **Vim/Neovim** | Instale o plugin `vim-markdown-preview` ou `markdown-preview.nvim` |
| **Navegador** | Instale extensões como *Markdown Viewer* (Chrome/Firefox) e abra o arquivo |

### Linha de Comando

```bash
# Usando grip (GitHub Readme Instant Preview)
pip install grip
grip docs/documentacao.md
# Acesse http://localhost:6419
```

---

## Folder Structure

```bash
project-name/
│
├── README.md
├── requirements.txt
├── main.py
├── testes.py
│
├── engine/
│   ├── __init__.py
│   │
│   ├── framebuffer.py      # set_pixel, clear, clear_color, getPixel
│   │
│   ├── collision.py      # check_collision_raft_obstacle, check_collision_raft_fish
│   │
│   ├── raster/
│   │   ├── line.py         # Bresenham / DDA
│   │   ├── circle.py       # Midpoint Circle
│   │   └── ellipse.py      # Midpoint Ellipse
│   │
│   ├── fill/
│   │   ├── flood_fill.py
│   │   └── scanline.py
│   │
│   ├── geometry/
│   │   ├── transform.py    # matrizes 3x3
│   │   └── cohen_sutherland.py     # Cohen-Sutherland
│   │
│   └── math/
│       └── auxiliary.py       # operações auxiliares
│
├── app/                    # JOGO / SIMULAÇÃO
│   │
│   ├── scenes/
│   │   ├── menu.py
│   │   ├── auxiliary_functions.py
│   │   ├── game_over.py
│   │   ├── history.py
│   │   ├── instructions.py
│   │   ├── victory.py
│   │   ├── intro.py        # tela de abertura
│   │   └── gameplay.py
│   │
│   ├── entities/
│   │   ├── fish.py
│   │   ├── icons.py
│   │   ├── minimap.py
│   │   ├── raft.py
│   │   └── obstacle.py
│   │
│   └── constants.py
│
├── assets/
│   ├── colors.py
│   ├── music_manager.py
│   ├── textures/
│   └── music/
│
└── docs/
    └── documentacao.md
```

---

## Dependências

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| `pygame` | ≥ 2.5.0 | Biblioteca para desenvolvimento de jogos em Python |

> **Nota:** Todas as dependências estão listadas em `requirements.txt`.

---

## Documentação Técnica

A documentação completa do projeto está disponível em:

- **[docs/documentacao.md](docs/documentacao.md)** – Documentação técnica da engine e sistema de telas
- **[docs/implementacao_tela_inicial.md](docs/implementacao_tela_inicial.md)** – Detalhes da implementação das telas

---

## Licença

Projeto acadêmico desenvolvido para a disciplina de Computação Gráfica.`
