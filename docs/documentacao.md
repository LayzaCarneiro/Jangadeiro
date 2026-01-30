# Documentação Técnica Detalhada — Jangadeiro: Dragão do Mar

Documentação focada no código: parâmetros, retornos e comportamento dos métodos da engine, dos renderizadores baseados em `set_pixel` e das transformações geométricas.

---

## 1. Framebuffer (`engine/framebuffer.py`)

Todas as funções de desenho da engine terminam em `set_pixel`, que usa `superficie.set_at((x, y), color)` do Pygame. O framebuffer é a única camada que escreve pixels na superfície.

### 1.1 `set_pixel(superficie, x, y, color)`

- **Parâmetros:**
  - `superficie`: superfície Pygame (ex.: tela)
  - `x`, `y`: coordenadas inteiras do pixel
  - `color`: tupla RGB `(R, G, B)`, 0–255
- **Retorno:** nenhum (`None`).
- **Comportamento:** só desenha se `0 <= x < largura` e `0 <= y < altura`; caso contrário não faz nada. É a primitiva usada por todos os algoritmos de rasterização.

### 1.2 `getPixel(superficie, x, y)`

- **Parâmetros:** `superficie`, `x`, `y` (inteiros).
- **Retorno:** cor do pixel em `(x, y)` como retorno de `get_at`, ou `None` se fora dos limites.
- **Uso:** leitura de pixel (ex.: flood fill para saber cor atual).

### 1.3 `clear(superficie)`

- **Parâmetros:** `superficie`.
- **Retorno:** nenhum.
- **Comportamento:** percorre todos os pixels e chama `set_at` com preto `(0, 0, 0)`.

### 1.4 `clear_color(superficie, cor)`

- **Parâmetros:** `superficie`, `cor` (tupla RGB).
- **Retorno:** nenhum.
- **Comportamento:** igual a `clear`, mas usa a cor `cor` em vez de preto.

---

## 2. Renderizadores de primitivas (usando apenas `set_pixel`)

### 2.1 Retas — `engine/raster/line.py`

#### `dda(superficie, x0, y0, x1, y1, cor)`

- **Parâmetros:**
  - `superficie`: onde desenhar
  - `x0`, `y0`: início do segmento
  - `x1`, `y1`: fim do segmento
  - `cor`: tupla RGB
- **Retorno:** nenhum.
- **Comportamento:** Digital Differential Analyzer. Calcula `passos = max(|dx|, |dy|)` e incrementa `x` e `y` em passos iguais; em cada passo chama `set_pixel(round(x), round(y), cor)`. Se `passos == 0`, desenha só o ponto `(x0, y0)`.

#### `bresenham(superficie, x0, y0, x1, y1, cor)`

- **Parâmetros:** mesmos de `dda`.
- **Retorno:** nenhum.
- **Comportamento:** Algoritmo de Bresenham para retas. Usa variável de decisão inteira `d = 2*dy - dx`; em cada passo avança em `x` e eventualmente em `y`, atualizando `d` com `incE = 2*dy` ou `incNE = 2*(dy-dx)`. Se `|dy| > |dx|`, troca papéis de x e y (“steep”) e desenha `set_pixel(y, x, cor)` para manter continuidade. Só usa inteiros e `set_pixel`.

#### `desenhar_poligono(tela, pontos, cor)`

- **Parâmetros:**
  - `tela`: superfície
  - `pontos`: lista de tuplas `(x, y)` com pelo menos 3 vértices, em ordem (fechando no primeiro)
  - `cor`: tupla RGB
- **Retorno:** nenhum. Não faz nada se `len(pontos) < 3`.
- **Comportamento:** para cada par de vértices consecutivos `pontos[i]` e `pontos[(i+1) % n]` chama `bresenham`, desenhando apenas o contorno do polígono (sem preenchimento).

---

### 2.2 Circunferência — `engine/raster/circle.py`

#### `get_circle_points(superficie, xc, yc, x, y, cor)`

- **Parâmetros:** `superficie`, centro `(xc, yc)`, ponto no primeiro octante `(x, y)`, `cor`.
- **Retorno:** nenhum.
- **Comportamento:** desenha os 8 pontos simétricos da circunferência usando `set_pixel`: `(xc±x, yc±y)`, `(xc±y, yc±x)` (4 combinações de sinais).

#### `draw_circle(superficie, xc, yc, raio, cor)`

- **Parâmetros:**
  - `superficie`: superfície
  - `xc`, `yc`: centro
  - `raio`: raio inteiro
  - `cor`: tupla RGB
- **Retorno:** nenhum.
- **Comportamento:** Midpoint Circle. Inicia em `(0, raio)`; variável de decisão `d = 1 - raio`. Enquanto `x < y`, incrementa `x` e, se `d < 0`, faz `d += 2*x+1`, senão decrementa `y` e `d += 2*(x-y)+1`. Em cada passo chama `get_circle_points`, que por sua vez usa apenas `set_pixel`.

---

### 2.3 Elipse — `engine/raster/elipse.py`

#### `get_elipse_points(superficie, xc, yc, x, y, cor)`

- **Parâmetros:** centro `(xc, yc)`, ponto no primeiro quadrante `(x, y)`, `cor`.
- **Retorno:** nenhum.
- **Comportamento:** desenha 4 pontos por simetria: `(xc±x, yc±y)` via `set_pixel`.

#### `draw_elipse(superficie, xc, yc, rx, ry, cor)`

- **Parâmetros:**
  - `superficie`, centro `(xc, yc)`
  - `rx`, `ry`: semi-eixos horizontal e vertical
  - `cor`: tupla RGB
- **Retorno:** nenhum.
- **Comportamento:** Midpoint Ellipse em duas regiões. Região 1: parte mais horizontal; decisão `p1 = ry² - rx²*ry + rx²/4`; atualiza `x` e eventualmente `y`. Região 2: parte mais vertical; decisão `p2` em função de `(x+0.5)²` e `(y-1)²`. Todas as saídas gráficas passam por `get_elipse_points` → `set_pixel`.

---

## 3. Preenchimento (todos os pixels via `set_pixel`)

### 3.1 Scanline — `engine/fill/scanline.py`

#### `scanline_fill(superficie, pontos, cor_preenchimento)`

- **Parâmetros:**
  - `superficie`: superfície
  - `pontos`: lista de tuplas `(x, y)` formando um polígono fechado (vértices consecutivos)
  - `cor_preenchimento`: tupla RGB
- **Retorno:** nenhum.
- **Comportamento:** para cada linha de varredura `y` entre `y_min` e `y_max-1`, calcula as interseções da reta horizontal `y` com cada aresta do polígono. Regra: só considera aresta se `y0 <= y < y1` (após normalizar para `y0 < y1`). Interseção: `x = x0 + (y - y0)*(x1 - x0)/(y1 - y0)`. Ordena as interseções em `x` e, entre pares consecutivos, desenha todos os pixels com `set_pixel(superficie, x, y, cor_preenchimento)`.

#### `scanline_fill_gradiente(superficie, pontos, cor_inicio, cor_fim, direcao='vertical')`

- **Parâmetros:**
  - `superficie`, `pontos`: como em `scanline_fill`
  - `cor_inicio`, `cor_fim`: tuplas RGB para os extremos do gradiente
  - `direcao`: `'vertical'` ou `'horizontal'`
- **Retorno:** nenhum.
- **Comportamento:** mesmo algoritmo de scanline (interseções e preenchimento entre pares), mas a cor de cada pixel não é fixa: é obtida por interpolação linear entre `cor_inicio` e `cor_fim`. Se `direcao == 'vertical'`, `t = (y - y_min)/(y_max - y_min)` (ou 0.5 se `y_max == y_min`). Se `direcao == 'horizontal'`, `t = (x - x_min)/(x_max - x_min)`. A cor é `interpolar_cor(cor_inicio, cor_fim, t)` e cada pixel é desenhado com `set_pixel`.

---

### 3.2 Flood Fill — `engine/fill/flood_fill.py`

#### `flood_fill_iterativo(superficie, x, y, cor_preenchimento, cor_borda)`

- **Parâmetros:**
  - `superficie`: superfície (usa `get_at` para ler e `set_pixel` para escrever)
  - `x`, `y`: semente (pixel inicial)
  - `cor_preenchimento`: cor com que preencher
  - `cor_borda`: cor que delimita a região (não preenche)
- **Retorno:** nenhum.
- **Comportamento:** preenchimento 4-conectado com pilha. Enquanto a pilha não estiver vazia, desempilha `(x, y)`; se estiver dentro dos limites e a cor atual não for borda nem preenchimento, chama `set_pixel(superficie, x, y, cor_preenchimento)` e empilha os 4 vizinhos `(x±1, y)`, `(x, y±1)`. Assim, todo o preenchimento é feito apenas com `set_pixel`.

---

## 4. Transformações geométricas (`engine/geometry/transform.py`)

Coordenadas 2D são tratadas em forma homogênea: ponto `(x, y)` como vetor `[x, y, 1]`. Transformações são matrizes 3×3 aplicadas a esses vetores; o resultado é interpretado como novo `(x', y')` (ignorando a terceira coordenada, que permanece 1).

### 4.1 Matrizes básicas

#### `identidade()`

- **Parâmetros:** nenhum.
- **Retorno:** matriz 3×3 identidade `[[1,0,0],[0,1,0],[0,0,1]]`.

#### `translacao(tx, ty)`

- **Parâmetros:** `tx`, `ty` (reais ou inteiros).
- **Retorno:** matriz 3×3 de translação.
- **Efeito:** `(x', y') = (x + tx, y + ty)`.

#### `escala(sx, sy)`

- **Parâmetros:** `sx`, `sy` (fatores de escala).
- **Retorno:** matriz 3×3 de escala.
- **Efeito:** `(x', y') = (sx*x, sy*y)`.

#### `rotacao(theta)`

- **Parâmetros:** `theta` em radianos (sentido anti-horário positivo).
- **Retorno:** matriz 3×3 de rotação em torno da origem.
- **Fórmula:**  
  `x' = x*cos(theta) - y*sin(theta)`  
  `y' = x*sin(theta) + y*cos(theta)`.

### 4.2 Composição e aplicação

#### `multiplica_matrizes(a, b)`

- **Parâmetros:** `a`, `b`: matrizes 3×3 (listas de listas).
- **Retorno:** matriz 3×3 produto `a * b` (ordem: aplicar `b` primeiro, depois `a`).
- **Uso:** compor translação, rotação e escala em uma única matriz.

#### `aplica_transformacao(m, pontos)`

- **Parâmetros:**
  - `m`: matriz 3×3
  - `pontos`: lista de tuplas `(x, y)`
- **Retorno:** lista de tuplas `(x_novo, y_novo)` com valores arredondados.
- **Cálculo:** para cada `(x, y)`, `x_novo = m[0][0]*x + m[0][1]*y + m[0][2]`, `y_novo = m[1][0]*x + m[1][1]*y + m[1][2]`.

#### `rotacionar_pontos_em_torno_de(pontos, cx, cy, theta)`

- **Parâmetros:**
  - `pontos`: lista de tuplas `(x, y)`
  - `cx`, `cy`: centro de rotação (pivô)
  - `theta`: ângulo em radianos
- **Retorno:** nova lista de tuplas `(x', y')` (inteiros por arredondamento).
- **Matemática:** rotação em torno de `(cx, cy)` é a composição  
  `T(cx, cy) * R(theta) * T(-cx, -cy)`.  
  Ou seja: translada `(-cx, -cy)`, aplica `R(theta)`, translada `(cx, cy)`.  
  Fórmula explícita:  
  `x' = cx + (x-cx)*cos(theta) - (y-cy)*sin(theta)`  
  `y' = cy + (x-cx)*sin(theta) + (y-cy)*cos(theta)`.

---

## 5. Matemática auxiliar (`engine/math/auxiliary.py`)

#### `interpolar_cor(cor1, cor2, t)`

- **Parâmetros:**
  - `cor1`, `cor2`: tuplas RGB `(R, G, B)`
  - `t`: real em `[0, 1]`
- **Retorno:** tupla RGB `(R, G, B)` com componentes inteiras.
- **Fórmula:** por canal, `c = c1 + (c2 - c1)*t`, truncado/arredondado para inteiro. Usado em gradientes (ex.: `scanline_fill_gradiente`).

---

## 6. Colisão (`engine/collision.py`)

#### `check_collision_raft_obstacle(raft_x, raft_y, raft_w, raft_h, obs_x, obs_y, obs_radius)`

- **Parâmetros:**
  - `raft_x`, `raft_y`: canto superior esquerdo do retângulo da jangada
  - `raft_w`, `raft_h`: largura e altura do retângulo
  - `obs_x`, `obs_y`: centro do obstáculo
  - `obs_radius`: “raio” do obstáculo (para AABB vira metade do lado do quadrado envolvente)
- **Retorno:** `True` se há sobreposição dos dois retângulos (AABB), `False` caso contrário.
- **Lógica:** retângulo da jangada: `[raft_x, raft_x+raft_w]` x `[raft_y, raft_y+raft_h]`. Retângulo do obstáculo: `[obs_x-obs_radius, obs_x+obs_radius]` x `[obs_y-obs_radius, obs_y+obs_radius]`. Retorna `not (separação em x ou em y)`; não usa funções gráficas, só comparações numéricas.

---

## 7. Resumo: fluxo de desenho com `set_pixel`

- **Framebuffer:** toda escrita na tela é feita por `set_pixel` (que usa `set_at`).
- **Retas:** `dda` e `bresenham` chamam apenas `set_pixel`; `desenhar_poligono` chama `bresenham` para cada aresta.
- **Círculo/elipse:** `get_circle_points` e `get_elipse_points` desenham pontos simétricos com `set_pixel`; `draw_circle` e `draw_elipse` usam só essas funções e aritmética inteira.
- **Preenchimento:** `scanline_fill` e `scanline_fill_gradiente` preenchem intervalos horizontais pixel a pixel com `set_pixel`; `flood_fill_iterativo` propaga com `set_pixel` e leitura via `get_at`.
- **Transformações:** não desenham; apenas produzem novas listas de pontos (ou matrizes). Quem desenha são as funções de rasterização e preenchimento aplicadas aos pontos transformados, sempre terminando em `set_pixel`.

Este documento cobre parâmetros, retornos e papel de cada método da engine e das transformações, com foco no uso de `set_pixel` em todos os renderizadores.

---

## 8. Sistema de Telas e Navegação

O jogo "Jangadeiro: Dragão do Mar" possui um sistema de telas interconectadas. Todas as telas utilizam renderização exclusiva via `set_pixel`, exceto o preenchimento de fundo (por performance).

### 8.1 Diagrama de Navegação

```
main.py
  │
  └─> run_intro() ─────────────────────────────────────┐
        │ (animação automática)                        │
        ▼                                              │
      run_menu() ◄─────────────────────────────────────┤
        │                                              │
        ├─> "INICIAR" ──> jangada2.main() (gameplay)   │
        │                     │                        │
        │                     ├─> Vitória (5 peixes)   │
        │                     │     │                  │
        │                     │     └─> run_victory()  │
        │                     │           │            │
        │                     │           ├─> "JOGAR NOVAMENTE" ─┐
        │                     │           └─> "SAIR" ──> exit    │
        │                     │                                  │
        │                     └─> Game Over (0 vidas)            │
        │                           │                            │
        │                           └─> run_game_over()          │
        │                                 │                      │
        │                                 ├─> "JOGAR NOVAMENTE" ─┘
        │                                 └─> "SAIR" ──> exit
        │
        ├─> "COMO JOGAR" ──> run_instructions()
        │                         │
        │                         └─> "VOLTAR" ─┐
        │                                       │
        │◄──────────────────────────────────────┘
        │
        └─> "SAIR" ──> exit
```

---

### 8.2 Tela de Introdução (`app/scenes/intro.py`)

**Função principal:** `run_intro(tela)`

**Descrição:**
Animação inicial que mostra um jangadeiro caminhando em direção a uma jangada na praia. Após a animação, transiciona automaticamente para o menu principal.

**Elementos renderizados:**

| Elemento | Algoritmo | Função |
|----------|-----------|--------|
| Céu | `fill()` | Fundo azul (performance) |
| Mar | `scanline_fill()` | Polígono preenchido |
| Areia | `scanline_fill()` | Polígono preenchido |
| Sol | `draw_circle()` + `flood_fill_iterativo()` | Circunferência preenchida |
| Ondas | `bresenham()` | Linhas horizontais paralelas |
| Jangada | `scanline_fill()` + `desenhar_poligono()` | Polígono com contorno |
| Jangadeiro (cabeça) | `draw_circle()` + `flood_fill_iterativo()` | Circunferência preenchida |
| Jangadeiro (corpo) | `draw_line_clipped()` / `bresenham()` | Linhas com clipping Cohen-Sutherland |

**Animações:**
- **Jangadeiro:** Translação horizontal (`dx += vel_x`) e vertical (`dy += vel_y`) até atingir a jangada
- **Jangada:** Oscilação horizontal via `sin(frame * frequencia) * amplitude`
- **Transição:** Fade escuro com `Surface.set_alpha()` + elevação do mar (translação vertical)

**Fluxo:**
1. Animação executa automaticamente (60 FPS)
2. Quando jangadeiro atinge a jangada → inicia transição
3. Após fade completo → chama `run_menu(tela)`

**Retorno:**
- `"sair"` → Se usuário fechar a janela durante a animação

---

### 8.3 Tela de Menu (`app/scenes/menu.py`)

**Função principal:** `run_menu(superficie)`

**Descrição:**
Menu principal do jogo com cenário decorativo (sol, horizonte) e três botões interativos.

**Elementos renderizados:**

| Elemento | Algoritmo | Função |
|----------|-----------|--------|
| Céu | `fill()` | Fundo azul claro (performance) |
| Sol | `draw_circle()` | Circunferência Midpoint |
| Título | `draw_text()` | Fonte bitmap 5×7 via `set_pixel()` |
| Botões | `scanline_fill()` + `desenhar_poligono()` + `draw_text()` | Polígono preenchido com borda e texto |

**Botões e destinos:**

| Botão | Posição (Y) | Retorno/Ação |
|-------|-------------|--------------|
| "INICIAR" | 45% da altura | Retorna `"iniciar"` → inicia gameplay |
| "COMO JOGAR" | 45% + 70px | Chama `run_instructions()` (modal) |
| "SAIR" | 45% + 140px | Retorna `"sair"` → encerra programa |

**Detecção de clique:**
- Algoritmo AABB via `ponto_em_retangulo(px, py, rx, ry, rw, rh)`
- Evento: `pygame.MOUSEBUTTONDOWN` com `button == 1`

**Retorno:**
- `"iniciar"` → Usuário clicou em "INICIAR"
- `"sair"` → Usuário clicou em "SAIR", pressionou ESC ou fechou janela

---

### 8.4 Tela de Instruções (`app/scenes/instructions.py`)

**Função principal:** `run_instructions(superficie)`

**Descrição:**
Tela modal que exibe as instruções do jogo. Apresenta objetivo, controles e elementos decorativos.

**Elementos renderizados:**

| Elemento | Algoritmo | Função |
|----------|-----------|--------|
| Fundo gradiente | Loop + `pygame.draw.line()` | Gradiente vertical (céu noturno) |
| Ondas animadas | `bresenham()` + `sin()` | Linhas onduladas na parte inferior |
| Peixinhos decorativos | `draw_circle()` | Círculos decorativos |
| Título "COMO JOGAR" | `draw_text()` | Fonte bitmap 5×7 (scale=3) |
| Caixas de instrução | `scanline_fill()` + `bresenham()` | Retângulos preenchidos com borda |
| Texto das instruções | `draw_text()` | Fonte bitmap 5×7 (scale=2) |
| Botão "VOLTAR" | `draw_button()` | Polígono com texto |

**Conteúdo das instruções:**
1. **OBJETIVO:** Coletar peixes e navegar, evitar pedras
2. **CONTROLES:** W/A/S/D para mover, ESC para sair

**Botão e destino:**

| Botão | Ação |
|-------|------|
| "VOLTAR" | Retorna ao menu (`return`) |
| ESC | Retorna ao menu |

**Animações:**
- Ondas na parte inferior oscilam via `sin((x + offset) * 0.05)`
- Frame incrementa a cada ciclo para animar

**Retorno:** Nenhum (função retorna `None`, voltando ao loop do menu)

---

### 8.5 Tela de Gameplay (`app/scenes/jangada2.py`)

**Função principal:** `main()`

**Descrição:**
Tela principal de jogo onde o jogador controla a jangada, coleta peixes e evita obstáculos.

**Elementos renderizados:**

| Elemento | Algoritmo | Função |
|----------|-----------|--------|
| Mar | `fill()` | Fundo azul (performance) |
| Jangada (corpo) | `scanline_fill_gradiente()` | Gradiente marrom vertical |
| Jangada (proa) | `scanline_fill_gradiente()` | Triângulo com gradiente |
| Jangada (detalhes) | `bresenham()` / `draw_line()` | Linhas das tábuas |
| Jangada (contorno) | `desenhar_poligono()` | Contorno Bresenham |
| Peixe (corpo) | Loop + `interpolar_cor()` | Elipse com gradiente simétrico |
| Peixe (cauda/barbatanas) | `scanline_fill_gradiente()` | Triângulos com gradiente |
| Peixe (olho) | Loop circular | Círculo preto com centro branco |
| Ondas ao redor do peixe | `bresenham()` + `sin()` | Círculos concêntricos ondulados |
| Obstáculos (rochas) | Loop circular | Círculos cinza |
| HUD - Ícone peixe | `draw_fish_icon()` | Elipse + triângulo pequenos |
| HUD - Ícone coração | `draw_heart_icon()` | Equação paramétrica de coração |
| HUD - Números | `draw_simple_text()` | Fonte bitmap 3×5 |
| Minimapa | Loops + `set_pixel()` | Representação miniatura do mundo |

**Controles:**

| Tecla | Ação |
|-------|------|
| W | Move jangada para cima |
| A | Move jangada para esquerda |
| S | Move jangada para baixo |
| D | Move jangada para direita |
| ESC | Encerra o jogo |

**Sistema de mundo:**
- **Viewport (tela):** 1000×800 pixels
- **Mundo:** 3000×3000 pixels
- **Câmera:** Segue a jangada com centralização

**Condições de término:**

| Condição | Resultado | Próxima tela |
|----------|-----------|--------------|
| Coletar 5 peixes | `resultado = "VITORIA"` | `run_victory()` |
| Perder 3 vidas | `resultado = "GAME OVER"` | `run_game_over()` |

**Sistema de colisão:**
- **Jangada × Peixe:** AABB → incrementa pontuação, reposiciona peixe
- **Jangada × Obstáculo:** `check_collision_raft_obstacle()` → decrementa vida, rotaciona jangada

---

### 8.6 Tela de Vitória (`app/scenes/victory.py`)

**Função principal:** `run_victory(superficie)`

**Descrição:**
Exibida quando o jogador coleta 5 peixes. Mostra mensagem de vitória e opções.

**Elementos renderizados:**

| Elemento | Algoritmo | Função |
|----------|-----------|--------|
| Fundo | `fill()` | Azul claro (mesmo do menu) |
| Mensagem "VOCE VENCEU" | `draw_text()` | Fonte bitmap 5×7 em verde |
| Botões | `draw_button()` | Polígonos amarelos com texto |

**Como chegar nesta tela:**
1. Iniciar jogo pelo menu → "INICIAR"
2. Durante gameplay, coletar 5 peixes
3. Sistema detecta `pontos >= 5` → `resultado = "VITORIA"`
4. Loop do gameplay termina → chama `run_victory(screen)`

**Botões e destinos:**

| Botão | Posição (Y) | Retorno |
|-------|-------------|---------|
| "JOGAR NOVAMENTE" | 52% da altura | `"jogar_novamente"` → reinicia gameplay |
| "SAIR" | 52% + 70px | `"sair"` → encerra programa |

**Paleta de cores:**
- Fundo: `SKY = (135, 206, 235)` (azul claro)
- Mensagem: `MESSAGE_COLOR = (50, 160, 80)` (verde)
- Botões: Mesmo padrão do menu (amarelo/marrom)

**Retorno:**
- `"jogar_novamente"` → Volta ao início do loop em `jangada2.main()`, resetando estado
- `"sair"` → Encerra o programa

---

### 8.7 Tela de Game Over (`app/scenes/game_over.py`)

**Função principal:** `run_game_over(superficie)`

**Descrição:**
Exibida quando o jogador perde todas as 3 vidas (colidindo com obstáculos).

**Elementos renderizados:**

| Elemento | Algoritmo | Função |
|----------|-----------|--------|
| Fundo | `fill()` | Azul claro (mesmo do menu) |
| Mensagem "VOCE PERDEU" | `draw_text()` | Fonte bitmap 5×7 em vermelho |
| Botões | `draw_button()` | Polígonos amarelos com texto |

**Como chegar nesta tela:**
1. Iniciar jogo pelo menu → "INICIAR"
2. Durante gameplay, colidir com 3 obstáculos (pedras)
3. Sistema detecta `vidas <= 0` → `resultado = "GAME OVER"`
4. Loop do gameplay termina → chama `run_game_over(screen)`

**Botões e destinos:**

| Botão | Posição (Y) | Retorno |
|-------|-------------|---------|
| "JOGAR NOVAMENTE" | 52% da altura | `"jogar_novamente"` → reinicia gameplay |
| "SAIR" | 52% + 70px | `"sair"` → encerra programa |

**Paleta de cores:**
- Fundo: `SKY = (135, 206, 235)` (azul claro)
- Mensagem: `MESSAGE_COLOR = (200, 50, 50)` (vermelho)
- Botões: Mesmo padrão do menu (amarelo/marrom)

**Retorno:**
- `"jogar_novamente"` → Volta ao início do loop em `jangada2.main()`, resetando estado
- `"sair"` → Encerra o programa

---

### 8.8 Funções Auxiliares Compartilhadas (`app/scenes/auxiliary_functions.py`)

Funções reutilizadas por todas as telas para renderização consistente.

#### `draw_text(surf, texto, x, y, cor, scale=2)`

- **Descrição:** Renderiza texto usando fonte bitmap 5×7 via `set_pixel()`
- **Parâmetros:**
  - `surf`: superfície Pygame
  - `texto`: string a renderizar
  - `x`, `y`: posição inicial
  - `cor`: tupla RGB
  - `scale`: fator de escala (2 = cada pixel da fonte vira 2×2)
- **Caracteres suportados:** A-Z, 0-9, espaço, ":", "-", "."

#### `draw_button(surf, x, y, larg, alt, texto, cor_fundo, cor_borda, cor_texto)`

- **Descrição:** Renderiza botão interativo com preenchimento, borda e texto centralizado
- **Algoritmos utilizados:**
  1. `scanline_fill()` → preenchimento do retângulo
  2. `desenhar_poligono()` → contorno via Bresenham
  3. `draw_text()` → texto centralizado

#### `ponto_em_retangulo(px, py, rx, ry, rw, rh)`

- **Descrição:** Teste AABB para detecção de clique em botões
- **Retorno:** `True` se ponto `(px, py)` está dentro do retângulo

---

### 8.9 Resumo do Fluxo Completo

```
1. main.py inicia Pygame e chama run_intro()
2. Animação de introdução → transição para run_menu()
3. Menu:
   ├── "INICIAR" → pygame.quit() + jangada2.main()
   ├── "COMO JOGAR" → run_instructions() → retorna ao menu
   └── "SAIR" → encerra programa

4. Gameplay (jangada2.main()):
   ├── Loop: controle WASD, coleta peixes, evita obstáculos
   ├── 5 peixes coletados → run_victory()
   │   ├── "JOGAR NOVAMENTE" → reinicia gameplay
   │   └── "SAIR" → encerra
   └── 0 vidas → run_game_over()
       ├── "JOGAR NOVAMENTE" → reinicia gameplay
       └── "SAIR" → encerra
```

---

### 8.10 Paleta de Cores Global

| Cor | RGB | Uso |
|-----|-----|-----|
| `SKY` | `(135, 206, 235)` | Fundo do menu, vitória, game over |
| `SEA_COLOR` | `(0, 120, 170)` | Mar no gameplay |
| `SUN` | `(255, 204, 92)` | Sol, botões |
| `WAVE` | `(90, 180, 200)` | Ondas decorativas |
| `BTN_FILL` | `(255, 204, 92)` | Preenchimento de botões |
| `BTN_BORDER` | `(180, 140, 50)` | Borda de botões |
| `BTN_TEXT` | `(60, 50, 40)` | Texto de botões |
| `MESSAGE_COLOR` (vitória) | `(50, 160, 80)` | Verde para sucesso |
| `MESSAGE_COLOR` (derrota) | `(200, 50, 50)` | Vermelho para falha |
