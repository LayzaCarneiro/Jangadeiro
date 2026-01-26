import pygame  # type: ignore
import sys
from menu import run_menu

# Placeholder do gameplay (será substituído pela lógica completa do jogo)
def run_gameplay_placeholder(tela):
    from menu import draw_text
    SEA = (0, 120, 170)
    w, h = tela.get_width(), tela.get_height()
    while True:
        tela.fill(SEA)
        n = len("JOGO EM BREVE")
        draw_text(tela, "JOGO EM BREVE", (w - n * 12) // 2, (h - 14) // 2, (255, 255, 255), scale=2)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return


def main():
    pygame.init()
    largura, altura = 1000, 1000
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Jangada das Estrelas")

    resultado = run_menu(tela)

    if resultado == "sair":
        pygame.quit()
        sys.exit(0)

    if resultado == "iniciar":
        run_gameplay_placeholder(tela)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
