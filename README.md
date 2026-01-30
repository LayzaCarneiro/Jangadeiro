# Jangada das Estrelas 🚣

Jogo 2D desenvolvido em Python com Pygame, utilizando exclusivamente algoritmos de rasterização via `set_pixel`. Projeto acadêmico da disciplica de Computação Gráfica.

---

## Requisitos do Sistema

- **Python:** 3.8 ou superior
- **Sistema Operacional:** Windows, Linux ou macOS
- **Pygame:** 2.5.0 ou superior

---

## Instalação

### 1. Clone ou baixe o projeto

```bash
git clone <url-do-repositorio>
cd CG_Trabalho_1
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
   - Evite **obstáculos (rochas)** – você tem 3 vidas

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
