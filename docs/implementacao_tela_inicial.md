# Documentação Técnica: Implementação da Tela Inicial

## 1. Visão Geral

A tela inicial do jogo "Jangada das Estrelas" foi implementada seguindo o requisito de **renderização exclusiva via `set_pixel`**, utilizando os algoritmos de rasterização desenvolvidos no engine do projeto. Todos os elementos visuais (sol, horizonte, ondas, título, botões) são desenhados através de primitivas gráficas implementadas manualmente, sem uso de funções de alto nível do Pygame (exceto `fill()` para o fundo, por questões de performance).

---

## 2. Arquitetura e Estrutura

### 2.1 Módulos Envolvidos

```
menu.py
├── engine/framebuffer.py      → set_pixel()
├── engine/raster/line.py       → bresenham(), desenhar_poligono()
├── engine/raster/circle.py    → draw_circle()
└── engine/fill/scanline.py    → scanline_fill()
```

### 2.2 Fluxo de Execução

```
main.py
  └─> run_menu(tela)
        ├─> draw_title_scene()    → Cenário (sol, horizonte, ondas)
        ├─> draw_text()            → Título do jogo
        └─> draw_button()          → Botões interativos
              └─> Retorna "iniciar" ou "sair"
```

---

## 3. Algoritmos Utilizados

### 3.1 Rasterização de Reta (Bresenham)

**Localização:** `engine/raster/line.py`

**Uso na tela inicial:**
- **Horizonte:** Linha horizontal que separa céu e mar
- **Ondas:** Múltiplas linhas horizontais paralelas
- **Contorno dos botões:** Polígono retangular desenhado aresta por aresta

**Implementação:**
```python
bresenham(superficie, x0, y0, x1, y1, cor)
```

**Características:**
- Algoritmo de Bresenham otimizado para retas
- Suporta inclinações arbitrárias (incluindo casos especiais: horizontal, vertical, diagonal)
- Usa apenas operações inteiras, garantindo eficiência

---

### 3.2 Rasterização de Circunferência (Midpoint Circle)

**Localização:** `engine/raster/circle.py`

**Uso na tela inicial:**
- **Sol:** Circunferência amarela no canto superior direito

**Implementação:**
```python
draw_circle(superficie, xc, yc, raio, cor)
```

**Algoritmo:**
- Baseado no algoritmo de Midpoint Circle
- Aproveita simetria de 8 pontos para desenhar apenas 1/8 da circunferência
- Usa decisão incremental para determinar próximo pixel

**Parâmetros na tela inicial:**
- Centro: `(w * 0.85, h * 0.15)` → 85% da largura, 15% da altura
- Raio: `50` pixels
- Cor: `SUN = (255, 204, 92)`

---

### 3.3 Preenchimento por Scanline

**Localização:** `engine/fill/scanline.py`

**Uso na tela inicial:**
- **Botões:** Preenchimento do polígono retangular dos botões

**Implementação:**
```python
scanline_fill(superficie, pontos, cor_preenchimento)
```

**Algoritmo:**
1. Determina `y_min` e `y_max` do polígono
2. Para cada scanline `y` entre `y_min` e `y_max`:
   - Calcula interseções da scanline com todas as arestas do polígono
   - Ignora arestas horizontais
   - Aplica regra: `y_min ≤ y < y_max` (exclui vértice superior)
3. Ordena interseções em X
4. Preenche pixels entre pares de interseções

**Vantagens:**
- Eficiente para polígonos convexos e côncavos
- Funciona com qualquer número de vértices
- Preenche corretamente mesmo com arestas complexas

---

### 3.4 Desenho de Polígonos

**Localização:** `engine/raster/line.py`

**Uso na tela inicial:**
- **Contorno dos botões:** Desenha as 4 arestas do retângulo

**Implementação:**
```python
desenhar_poligono(superficie, pontos, cor)
```

**Funcionamento:**
- Conecta cada vértice ao próximo usando `bresenham()`
- Fecha o polígono conectando o último ao primeiro vértice
- Requer mínimo de 3 pontos

---

## 4. Componentes da Tela Inicial

### 4.1 Sistema de Texto (Fonte 5x7)

**Localização:** `menu.py` → `_FONT`, `_draw_char()`, `draw_text()`

**Conceito:**
Implementação de uma fonte bitmap customizada onde cada caractere é representado por uma matriz 5×7 pixels. Apenas os caracteres necessários foram implementados: `A, B, C, D, E, G, I, J, L, M, N, O, R, S, T, V` e espaço.

**Estrutura de Dados:**
```python
_FONT = {
    "A": ["  X  ",  # Linha 0
          " X X ",  # Linha 1
          "X   X",  # Linha 2
          "XXXXX",  # Linha 3
          "X   X",  # Linha 4
          "X   X",  # Linha 5
          "X   X"], # Linha 6
    # ... outros caracteres
}
```

**Renderização:**
1. `_draw_char()`: Desenha um único caractere
   - Itera sobre cada linha e coluna da matriz
   - Para cada `'X'`, desenha um bloco `scale×scale` pixels usando `set_pixel()`
   - Suporta escala (padrão: `scale=2` → cada pixel da fonte vira 2×2 pixels na tela)

2. `draw_text()`: Desenha uma string completa
   - Chama `_draw_char()` para cada caractere
   - Espaçamento horizontal: `6 * scale` pixels entre caracteres

**Características:**
- **Escalabilidade:** Fator de escala configurável (usado `scale=2` na tela inicial)
- **Renderização pura:** Cada pixel é desenhado individualmente via `set_pixel()`
- **Otimização:** Apenas caracteres necessários são definidos

---

### 4.2 Cenário (Sol, Horizonte, Ondas)

**Função:** `draw_title_scene(superficie, largura, altura)`

**Elementos:**

#### 4.2.1 Sol
- **Algoritmo:** `draw_circle()`
- **Posição:** `(w * 0.85, h * 0.15)` → canto superior direito
- **Raio:** `50` pixels
- **Cor:** `SUN = (255, 204, 92)` (amarelo)

#### 4.2.2 Horizonte
- **Algoritmo:** `bresenham()`
- **Posição:** `y = h * 0.65` (65% da altura)
- **Extensão:** De `x=0` até `x=w` (largura total)
- **Cor:** `SEA = (0, 120, 170)` (azul marinho)

#### 4.2.3 Ondas
- **Algoritmo:** `bresenham()` (múltiplas chamadas)
- **Quantidade:** 5 ondas
- **Posicionamento:** 
  - Primeira onda: `y = horizonte + 15`
  - Espaçamento: `12` pixels entre ondas
  - Fórmula: `y = horizonte + 15 + i * 12` para `i ∈ [0, 4]`
- **Cor:** `WAVE = (90, 180, 200)` (azul claro)

---

### 4.3 Botões Interativos

**Função:** `draw_button(superficie, x, y, largura, altura, texto, cor_fundo, cor_borda, cor_texto)`

**Estrutura:**
1. **Polígono:** Retângulo definido por 4 vértices
   ```python
   pts = [(x, y), (x + larg, y), (x + larg, y + alt), (x, y + alt)]
   ```

2. **Preenchimento:**
   - Algoritmo: `scanline_fill(superficie, pts, cor_fundo)`
   - Preenche o interior do retângulo

3. **Contorno:**
   - Algoritmo: `desenhar_poligono(superficie, pts, cor_borda)`
   - Desenha as 4 arestas usando `bresenham()`

4. **Texto:**
   - Algoritmo: `draw_text()` (fonte 5x7)
   - Centralização aproximada:
     - Horizontal: `tx = x + (larg - largura_texto) // 2`
     - Vertical: `ty = y + (alt - altura_texto) // 2`

**Parâmetros na tela inicial:**
- **Dimensões:** `180×50` pixels
- **Posição:** Centralizado horizontalmente, verticalmente em `55%` e `62%` da altura
- **Cores:**
  - Fundo: `BTN_FILL = (255, 204, 92)` (amarelo)
  - Borda: `BTN_BORDER = (180, 140, 50)` (marrom)
  - Texto: `BTN_TEXT = (60, 50, 40)` (marrom escuro)

---

### 4.4 Detecção de Colisão (Clique)

**Função:** `ponto_em_retangulo(px, py, rx, ry, rw, rh)`

**Algoritmo:**
Teste de ponto dentro de retângulo axis-aligned (AABB - Axis-Aligned Bounding Box).

```python
return rx <= px <= rx + rw and ry <= py <= ry + rh
```

**Uso:**
- Verifica se a posição do mouse (`mx, my`) está dentro dos limites de cada botão
- Acionado no evento `pygame.MOUSEBUTTONDOWN` com botão esquerdo (`button == 1`)

---

## 5. Loop Principal do Menu

**Função:** `run_menu(superficie)`

**Fluxo:**

```python
while True:
    # 1. Limpar tela
    superficie.fill(SKY)
    
    # 2. Desenhar cenário
    draw_title_scene(superficie, w, h)
    
    # 3. Desenhar título
    draw_text(superficie, "JANGADA DAS ESTRELAS", ...)
    
    # 4. Desenhar botões
    draw_button(..., "INICIAR", ...)
    draw_button(..., "SAIR", ...)
    
    # 5. Atualizar display
    pygame.display.flip()
    
    # 6. Processar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return "sair"
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Verificar clique nos botões
            if ponto_em_retangulo(...):
                return "iniciar" ou "sair"
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return "sair"
```

**Retorno:**
- `"iniciar"` → Usuário clicou em "INICIAR"
- `"sair"` → Usuário clicou em "SAIR", pressionou ESC, ou fechou a janela

---

## 6. Integração com main.py

### 6.1 Fluxo de Navegação Menu → Gameplay (`jangada2.py`)

```python
import pygame
import sys
from menu import run_menu
import jangada2


def main():
    pygame.init()
    largura, altura = 1000, 1000
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Jangada das Estrelas")

    resultado = run_menu(tela)  # Exibe menu, aguarda escolha

    if resultado == "sair":
        pygame.quit()
        sys.exit(0)

    if resultado == "iniciar":
        # Encerra o contexto atual e delega para o gameplay da jangada
        pygame.quit()
        jangada2.main()  # Executa a cena de gameplay definida em jangada2.py
        return

    pygame.quit()
    sys.exit(0)
```

### 6.2 Resumo da Navegação

- `main.py` inicializa Pygame e exibe o **menu inicial** (`run_menu`).
- Botão **“Sair”** ou tecla **ESC** → encerra o programa.
- Botão **“Iniciar”** → fecha o contexto gráfico atual e chama `jangada2.main()`,
  que renderiza:
  - a **jangada animada** e controlável (WASD),
  - os **peixes animados** com gradiente,
  - o **sistema de ondas** e **contador de peixes**.

---

## 7. Paleta de Cores

| Elemento | Variável | RGB | Descrição |
|----------|----------|-----|-----------|
| Céu | `SKY` | `(135, 206, 235)` | Azul claro (sky blue) |
| Mar | `SEA` | `(0, 120, 170)` | Azul marinho |
| Sol | `SUN` | `(255, 204, 92)` | Amarelo dourado |
| Ondas | `WAVE` | `(90, 180, 200)` | Azul claro |
| Título | `TITLE` | `(40, 50, 100)` | Azul escuro |
| Botão (fundo) | `BTN_FILL` | `(255, 204, 92)` | Amarelo |
| Botão (borda) | `BTN_BORDER` | `(180, 140, 50)` | Marrom |
| Botão (texto) | `BTN_TEXT` | `(60, 50, 40)` | Marrom escuro |

---

## 8. Requisitos Atendidos

### 8.1 Algoritmos de Rasterização
- ✅ **Rasterização de reta:** Bresenham (horizonte, ondas, contornos)
- ✅ **Rasterização de circunferência:** Midpoint Circle (sol)
- ✅ **Preenchimento:** Scanline Fill (botões)

### 8.2 Elementos Visuais
- ✅ **Sol:** Circunferência
- ✅ **Mar/Horizonte:** Retas
- ✅ **Título:** Texto renderizado via set_pixel (fonte bitmap)
- ✅ **Botões:** Polígonos preenchidos

### 8.3 Interatividade
- ✅ **Menu inicial:** Botões "Iniciar" e "Sair"
- ✅ **Input:** Mouse (clique) e teclado (ESC)
- ✅ **Navegação:** Transição para gameplay ou saída

---

## 9. Considerações de Performance

### 9.1 Otimizações Implementadas

1. **Fundo:** Usa `superficie.fill()` do Pygame para limpar a tela (não usa `set_pixel` em loop, por questões de performance). Todos os elementos visuais (sol, ondas, texto, botões) são desenhados via `set_pixel`.

2. **Fonte:** Apenas caracteres necessários são definidos no dicionário `_FONT`, reduzindo uso de memória.

3. **Scanline:** Algoritmo eficiente para preenchimento de polígonos, especialmente para formas convexas como retângulos.

### 9.2 Limitações

- **Fonte bitmap:** Escalabilidade limitada; para tamanhos muito grandes, pode haver pixelização.
- **Renderização por pixel:** Mais lenta que primitivas nativas do Pygame, mas atende ao requisito de usar apenas `set_pixel`.

---

## 10. Extensibilidade

### 10.1 Adicionar Novos Caracteres

Para adicionar um novo caractere à fonte, basta incluir no dicionário `_FONT`:

```python
_FONT["P"] = ["XXXX ", "X   X", "X   X", "XXXX ", "X    ", "X    ", "X    "]
```

### 10.2 Adicionar Novos Botões

```python
draw_button(superficie, x, y, larg, alt, "NOVO", cor_fundo, cor_borda, cor_texto)
```

### 10.3 Modificar Cenário

A função `draw_title_scene()` pode ser estendida para incluir:
- Nuvens (usando `draw_elipse()`)
- Aves (usando `draw_circle()` ou polígonos)
- Outros elementos decorativos

---

## 11. Implementação da Jangada Animada e Sistema de Peixes

### 11.1 Arquivo: `jangada2.py`

Implementação do gameplay principal com jangada controlável e peixes animados, utilizando exclusivamente `set_pixel` para renderização.

---

### 11.2 Jangada Controlável

#### 11.2.1 Renderização da Jangada

**Função:** `draw_raft(superficie, x, y)`

A jangada é composta por:
- **Corpo principal:** Retângulo alongado (50×70 pixels) preenchido com gradiente vertical marrom escuro → claro
- **Proa:** Triângulo na frente (30 pixels de largura) também com gradiente
- **Detalhes:** Linhas horizontais simulando tábuas e estrutura central

**Algoritmos utilizados:**
- `scanline_fill_gradiente()`: Preenchimento com gradiente de duas cores marrons
- `desenhar_poligono()`: Contornos usando Bresenham
- `bresenham()`: Linhas de detalhes (tábuas)

#### 11.2.2 Sistema de Controle (WASD)

**Implementação:**
```python
keys = pygame.key.get_pressed()
if keys[pygame.K_w]: raft_y -= speed  # Move para cima
if keys[pygame.K_s]: raft_y += speed  # Move para baixo
if keys[pygame.K_a]: raft_x -= speed  # Move para esquerda
if keys[pygame.K_d]: raft_x += speed  # Move para direita
```

**Características:**
- **Velocidade:** 4 pixels por frame (60 FPS)
- **Limites:** Jangada não sai da tela (`max(0, min(WIDTH - 50, raft_x))`)
- **Atualização contínua:** Movimento suave a cada frame

---

### 11.3 Sistema de Peixes Animados

#### 11.3.1 Renderização do Peixe

**Função:** `draw_fish(superficie, x, y)`

**Estrutura do peixe:**
- **Corpo:** Elipse alongada (20×12 pixels) com gradiente azul → branco → azul
- **Cauda:** Triângulo traseiro com gradiente
- **Barbatanas:** Superior e inferior com gradiente
- **Olho:** Círculo preto com centro branco
- **Contorno:** Linha azul escura para destaque

**Gradiente simétrico:**
```python
t = (dy + b) / (2 * b)  # Normaliza de 0 a 1
if t < 0.5:
    t_grad = t * 2  # Topo → meio: azul → branco
else:
    t_grad = (1 - t) * 2  # Meio → base: branco → azul
cor = interpolar_cor(FISH_BLUE, FISH_WHITE, t_grad)
```

#### 11.3.2 Animação Vertical (Subir/Descer)

**Implementação:**
```python
fish_animation_offset += fish_animation_speed  # Incrementa offset
fish_y = fish_y_base + math.sin(fish_animation_offset) * fish_animation_range
```

**Parâmetros:**
- **Velocidade:** `0.15` radianos por frame
- **Amplitude:** `8` pixels (variação vertical)
- **Função:** `sin()` para movimento suave e cíclico
- **Posição base:** `fish_y_base` (centro da animação)

**Características:**
- Movimento contínuo em loop infinito
- Sempre mantém parte do peixe fora da água
- Sincronizado com as ondas ao redor

#### 11.3.3 Sistema de Ondas ao Redor do Peixe

**Função:** `draw_waves_around_fish(superficie, x, y, offset_y)`

**Implementação:**
- Desenha círculos concêntricos com variação senoidal
- Raio: 25 pixels (ajustável)
- Variação: `sin(angulo * 3 + offset_y * 0.1) * 2` para ondas irregulares
- Cor: Azul claro (`WAVE_COLOR`) para contraste com a água

**Algoritmo:**
1. Para cada raio de onda (17 a 25 pixels):
   - Gera 32 pontos em círculo
   - Aplica variação senoidal baseada no `offset_y`
   - Conecta pontos com `bresenham()`

**Efeito visual:** Ondas animadas que acompanham o movimento do peixe, simulando perturbação na superfície da água.

---

### 11.4 Sistema de Colisão

**Função:** `check_collision(raft_x, raft_y, fish_x, fish_y)`

**Algoritmo:** AABB (Axis-Aligned Bounding Box)

**Implementação:**
```python
# Verifica sobreposição de retângulos
return not (raft_right < fish_left or 
            raft_left > fish_right or 
            raft_bottom < fish_top or 
            raft_top > fish_bottom)
```

**Características:**
- Usa posição base do peixe (`fish_y_base`) para consistência
- Jangada: 50×85 pixels
- Peixe: 28×12 pixels (incluindo cauda e barbatanas)

**Comportamento:**
- Ao detectar colisão: incrementa pontuação e reposiciona peixe aleatoriamente
- Reset da animação: `fish_animation_offset = 0.0`

---

### 11.5 Interface de Pontuação

**Componentes:**
- **Ícone de peixe:** `draw_fish_icon()` - Pequeno peixe estilizado (8×6 pixels)
- **Números:** `draw_simple_text()` - Fonte bitmap 3×5

**Renderização:**
```python
draw_fish_icon(screen, 10, 10, tamanho=10)
draw_simple_text(screen, str(pontos), 25, 10, (255, 255, 255))
```

**Posicionamento:** Canto superior esquerdo (x=10, y=10)

---

### 11.6 Loop Principal

**Fluxo de execução:**

```python
while running:
    # 1. Limpa tela
    screen.fill(SEA_COLOR)
    
    # 2. Processa input (WASD)
    # 3. Atualiza posição da jangada
    # 4. Atualiza animação do peixe
    # 5. Verifica colisão
    # 6. Renderiza (ordem importante):
    #    - Ondas (fundo)
    #    - Peixe (meio)
    #    - Jangada (frente)
    #    - Pontuação (UI)
    
    pygame.display.flip()
    clock.tick(60)  # 60 FPS
```

**Ordem de renderização:**
1. Ondas ao redor do peixe (fundo)
2. Peixe animado (meio)
3. Jangada (frente, sobrepõe peixe se colidir)
4. Pontuação (UI, sempre visível)

---

### 11.7 Algoritmos Utilizados

| Elemento | Algoritmo | Função |
|----------|-----------|--------|
| Jangada (corpo) | Scanline Fill com Gradiente | `scanline_fill_gradiente()` |
| Jangada (contorno) | Bresenham | `desenhar_poligono()` |
| Peixe (corpo) | Elipse com Gradiente | Loop + `interpolar_cor()` |
| Peixe (barbatanas) | Scanline Fill com Gradiente | `scanline_fill_gradiente()` |
| Ondas | Bresenham (círculos) | `bresenham()` |
| Animação | Função Seno | `math.sin()` |
| Colisão | AABB | Teste de retângulos |

---

### 11.8 Considerações Técnicas

**Performance:**
- Renderização por pixel pode ser custosa, mas garante controle total
- Animação suave a 60 FPS
- Gradientes calculados em tempo real (interpolação RGB)

**Extensibilidade:**
- Fácil adicionar múltiplos peixes (array de posições)
- Sistema de ondas pode ser expandido para diferentes padrões
- Colisão pode ser refinada para formas mais complexas

---

## 12. Referências Técnicas

- **Bresenham Line Algorithm:** [Wikipedia - Bresenham's line algorithm](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm)
- **Midpoint Circle Algorithm:** [Wikipedia - Midpoint circle algorithm](https://en.wikipedia.org/wiki/Midpoint_circle_algorithm)
- **Scanline Fill:** Técnica clássica de preenchimento de polígonos em rasterização
- **AABB Collision Detection:** Detecção de colisão por retângulos alinhados aos eixos

---

## 13. Conclusão

A implementação da tela inicial demonstra o uso prático dos algoritmos de rasterização desenvolvidos no engine do projeto, atendendo ao requisito de renderização exclusiva via `set_pixel`. Todos os elementos visuais são desenhados através de primitivas gráficas de baixo nível, garantindo controle total sobre o processo de renderização e servindo como base para a implementação completa do jogo.
