import pygame  # type: ignore
import sys
from app.scenes.intro import run_intro
import app.scenes.gameplay as gameplay


def main():
    """
    Ponto de entrada principal do jogo "Jangadeiro: Dragão do Mar".

    Fluxo:
        1. Inicializa o pygame.
        2. Cria a janela do jogo com tamanho fixo (1000x800).
        3. Executa a cena de introdução (run_intro).
        4. Dependendo do resultado da introdução:
            - "sair": encerra o jogo.
            - "iniciar": fecha a janela atual e chama a função principal de `gameplay`.
        5. Fecha o pygame e encerra o programa em qualquer outro caso.

    Observações:
        - A função run_intro retorna uma string que indica a ação seguinte.
        - `gameplay.main()` deve conter o loop principal do jogo em si.
    """
        
    pygame.init()
    largura, altura = 1000, 800
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Jangadeiro: Dragão do Mar")

    resultado = run_intro(tela)

    if resultado == "sair":
        pygame.quit()
        sys.exit(0)

    if resultado == "iniciar":
        pygame.quit()
        gameplay.main()
        return

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()