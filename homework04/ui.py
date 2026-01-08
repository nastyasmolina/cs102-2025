"""
Базовый класс UI для игры "Жизнь".
"""
from abc import ABC, abstractmethod


class UI(ABC):
    """Абстрактный базовый класс для интерфейсов игры "Жизнь"."""
    
    def __init__(self, life) -> None:
        """
        Инициализация UI.
        
        Parameters
        ----------
        life : GameOfLife
            Объект игры "Жизнь"
        """
        self.life = life
    
    @abstractmethod
    def run(self) -> None:
        """Запустить интерфейс."""
        pass