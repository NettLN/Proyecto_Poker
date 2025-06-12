from typing import List
import random
from core.card import Card, Rank, Suit

class Deck:
    """Mazo de cartas"""
    
    def __init__(self):
        self.cards = []
        self.dealt_cards = []
        self.reset()
    
    def reset(self):
        """Reinicia el mazo con todas las cartas"""
        self.cards = [Card(rank, suit) for rank in Rank for suit in Suit]
        self.dealt_cards = []
        self.shuffle()
    
    def shuffle(self):
        """Baraja el mazo"""
        random.shuffle(self.cards)
    
    def deal_card(self) -> Card:
        """Reparte una carta del mazo"""
        if not self.cards:
            raise ValueError("No quedan cartas en el mazo")
        card = self.cards.pop()
        self.dealt_cards.append(card)
        return card
    
    def deal_cards(self, count: int) -> List[Card]:
        """Reparte múltiples cartas"""
        return [self.deal_card() for _ in range(count)]
    
    def remaining_cards(self) -> List[Card]:
        """Devuelve las cartas que quedan en el mazo"""
        return self.cards.copy()
    
    def cards_left(self) -> int:
        """Número de cartas restantes"""
        return len(self.cards)
