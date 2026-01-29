import pygame  # type: ignore
import sys
from app.scenes.intro import run_intro
import app.scenes.jangada2 as jangada2


def main():
    pygame.init()
    largura, altura = 1000, 800
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Jangada das Estrelas")

    resultado = run_intro(tela)

    if resultado == "sair":
        pygame.quit()
        sys.exit(0)

    if resultado == "iniciar":
        pygame.quit()
        jangada2.main()
        return

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()