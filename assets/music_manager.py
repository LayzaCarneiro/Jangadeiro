# -*- coding: utf-8 -*-
"""
Gerenciador de música para o jogo.
Controla a reprodução de músicas de fundo em diferentes cenas.
"""

import pygame
import os

class MusicManager:
    """
    Classe para gerenciar músicas de fundo do jogo.
    """
    
    def __init__(self):
        """Inicializa o mixer de áudio do pygame."""
        pygame.mixer.init()
        self.current_music = None
        self.music_volume = 0.5  # Volume padrão (0.0 a 1.0)
        
        # Caminhos das músicas
        self.base_path = os.path.join(os.path.dirname(__file__), "music")
        self.music_files = {
            "menu": self._find_music_file("menu"),
            "gameplay": self._find_music_file("gameplay")
        }
    
    def _find_music_file(self, name):
        """
        Procura um arquivo de música com o nome dado.
        Tenta encontrar formatos: .ogg, .mp3, .wav
        
        Args:
            name: nome base do arquivo (sem extensão)
            
        Returns:
            Caminho completo do arquivo ou None se não encontrado
        """
        extensions = [".ogg", ".mp3", ".wav"]
        for ext in extensions:
            filepath = os.path.join(self.base_path, name + ext)
            if os.path.exists(filepath):
                return filepath
        return None
    
    def play(self, music_name, loops=-1, fade_ms=1000):
        """
        Toca uma música.
        
        Args:
            music_name: nome da música ("menu" ou "gameplay")
            loops: número de repetições (-1 para loop infinito)
            fade_ms: tempo de fade in em milissegundos
        """
        if music_name == self.current_music:
            # Já está tocando esta música
            return
        
        music_path = self.music_files.get(music_name)
        
        if music_path is None:
            print(f"Músiquinha '{music_name}' não encontrada. Coloque o arquivo em assets/music/ a coloque o titulo do arquivo que estar na pasta")
            return
        
        try:
            # Para a música atual com fade out
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(500)
            
            # Carrega e toca a nova música
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            self.current_music = music_name
            print(f"♪ Tocando: {music_name}")
            
        except pygame.error as e:
            print(f"Erro ao tocar música '{music_name}' verifique o tipo de arquivo e veja se estar em MP3 como preferencia do projeto: {e}")
    
    def stop(self, fade_ms=500):
        """
        Para a música atual.
        
        Args:
            fade_ms: tempo de fade out em milissegundos
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)
            self.current_music = None
    
    def pause(self):
        """Pausa a música atual."""
        pygame.mixer.music.pause()
    
    def unpause(self):
        """Retoma a música pausada."""
        pygame.mixer.music.unpause()
    
    def set_volume(self, volume):
        """
        Ajusta o volume da música.
        
        Args:
            volume: valor entre 0.0 (mudo) e 1.0 (volume máximo)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)


# Instância global do gerenciador de música
music_manager = MusicManager()
