# Clase para los jugadores de Texas Hold'em
from typing import List
from core.card import Card

class Player:
    """
    Representa a un jugador de póker, siguiendo principios SOLID y POO.
    """
    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.hand: List[Card] = []
        self.active: bool = True  # Activo en la mano actual
        self.chips: int = chips   # Fichas disponibles
        self.current_bet: int = 0 # Apuesta actual en la ronda
        self.folded: bool = False # Si el jugador se ha retirado

    def receive_cards(self, cards: List[Card]):
        self.hand = cards

    def reset_hand(self):
        self.hand = []
        self.active = True
        self.current_bet = 0
        self.folded = False

    def bet(self, amount: int):
        if amount > self.chips:
            raise ValueError(f"{self.name} no tiene suficientes fichas para apostar {amount}.")
        self.chips -= amount
        self.current_bet += amount

    def fold(self):
        self.folded = True
        self.active = False

    def is_active(self) -> bool:
        return self.active and not self.folded

    def get_state(self) -> dict:
        return {
            "name": self.name,
            "chips": self.chips,
            "current_bet": self.current_bet,
            "hand": [card.to_dict() for card in self.hand],
            "active": self.active,
            "folded": self.folded,
        }
