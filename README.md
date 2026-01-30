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

### Descrição do fluxo:

1. **História** – Animação de abertura com texto e elementos gráficos (jangadas, mar, céu).  
2. **Intro** – Tela de introdução com efeitos visuais e música.  
3. **Menu** – Tela principal do jogo com opções:
   - **Iniciar** – Começa a partida.  
   - **Como Jogar** – Mostra instruções e controles.  
   - **Sair** – Fecha o jogo.  
4. **Gameplay** – Tela principal do jogo onde o jogador controla a jangada, coleta peixes e evita obstáculos.  
5. **Jogar de novo / Sair** – Tela final após a partida, permitindo reiniciar ou encerrar o jogo.

---

## Screenshots

Alguns exemplos de telas do jogo:

<img width="600" alt="Tela 1" src="https://github.com/user-attachments/assets/37bdb0bf-6d2b-4b4f-a523-83dc90df7d24" />
<img width="600" alt="Tela 2" src="https://github.com/user-attachments/assets/a59c54f0-3095-4144-8926-7eded7ac0cda" />
<img width="600" alt="Tela 3" src="https://github.com/user-attachments/assets/077da983-45d7-41a1-9fa8-105e2bdd4cde" />
<img width="600" alt="Tela 4" src="https://github.com/user-attachments/assets/68ab5fcf-947b-4289-a43b-26783f7d0769" />
<img width="600" alt="Tela 5" src="https://github.com/user-attachments/assets/f2dbf3bb-9d13-4068-a8a3-b0ef68a4d42a" />

## Vídeo Demonstrativo
📹 [Jangadeiro: Dragão do Mar](https://youtu.be/tAzGCbpE4CU)

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
├── README.md                  # Documentação geral do projeto, como instalar, rodar e fluxo do jogo
├── requirements.txt           # Lista de dependências do projeto (ex.: pygame)
├── main.py                    # Script principal que inicializa o jogo e gerencia a troca de telas
├── testes.py                  # Arquivo para testes manuais ou automatizados de funções da engine
│
├── engine/                    # Engine gráfica customizada (base do jogo)
│   ├── __init__.py            # Marca o diretório como pacote Python
│   │
│   ├── framebuffer.py         # Funções: set_pixel, limpar tela, pegar pixel
│   │
│   ├── collision.py           # Funções de detecção de colisão (jangada x obstáculos/peixes)
│   │
│   ├── raster/                # Algoritmos de rasterização de primitivas
│   │   ├── line.py            # Desenho de linhas (Bresenham e DDA)
│   │   ├── circle.py          # Desenho de círculos (Midpoint Circle)
│   │   └── ellipse.py         # Desenho de elipses (Midpoint Ellipse)
│   │
│   ├── fill/                  # Algoritmos de preenchimento
│   │   ├── flood_fill.py      # Flood Fill iterativo/recursivo
│   │   └── scanline.py        # Preenchimento de polígonos via Scanline
│   │
│   ├── geometry/              # Transformações geométricas e clipping
│   │   ├── transform.py       # Matrizes 3x3 para translação, escala e rotação
│   │   └── cohen_sutherland.py # Algoritmo de recorte de linhas (clipping)
│   │
│   └── math/
│       └── auxiliary.py       # Funções auxiliares de matemática (trigonometria, vetores, etc.)
│
├── app/                       # Código do jogo/simulação em si
│   │
│   ├── scenes/                # Telas e cenas do jogo
│   │   ├── menu.py            # Menu principal interativo
│   │   ├── auxiliary_functions.py # Funções utilitárias para desenhar textos, botões, etc.
│   │   ├── game_over.py       # Tela de fim de jogo
│   │   ├── history.py         # Tela de história/introdução do jogo
│   │   ├── instructions.py    # Tela de instruções e controles
│   │   ├── victory.py         # Tela de vitória
│   │   ├── intro.py           # Tela de abertura animada
│   │   └── gameplay.py        # Tela principal do jogo com lógica de movimentação, peixes e obstáculos
│   │
│   ├── entities/              # Entidades do jogo
│   │   ├── fish.py            # Desenho e comportamento dos peixes
│   │   ├── icons.py           # Ícones gráficos (ex.: vidas, coração)
│   │   ├── minimap.py         # Mini mapa com escala e viewport
│   │   ├── raft.py            # Desenho e movimentação da jangada
│   │   └── obstacle.py        # Desenho e posição dos obstáculos
│   │
│   └── constants.py           # Constantes do jogo (cores, dimensões, velocidades)
│
├── assets/                    # Recursos do jogo
│   ├── colors.py              # Paleta de cores utilizada no jogo
│   ├── music_manager.py       # Controle de música e efeitos sonoros
│   ├── textures/              # Texturas e imagens (se necessário para mapeamento manual)
│   └── music/                 # Arquivos de música e efeitos sonoros
│
└── docs/                      # Documentação técnica
    └── documentacao.md        # Explicação de implementação da engine, telas, fluxos e algoritmos
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

## Integrantes

Equipe responsável pelo desenvolvimento do projeto:

| Nome Completo              | GitHub                                     |
|----------------------------|-------------------------------------------|
| Layza Carneiro             | [https://github.com/LayzaCarneiro](https://github.com/LayzaCarneiro) |
| Samuel William             | [https://github.com/William-SWS](https://github.com/William-SWS)       |
| Samuel Valente             | [https://github.com/ValenteBy](https://github.com/ValenteBy) |

---

## Licença

Projeto acadêmico desenvolvido para a disciplina de Computação Gráfica.`
