from enum import Enum
from typing import List, Tuple, Dict, Optional
from collections import Counter
import itertools

class Suit(Enum):
    """Palos de las cartas"""
    HEARTS = "♥"    # Corazones
    DIAMONDS = "♦"  # Diamantes
    CLUBS = "♣"     # Tréboles
    SPADES = "♠"    # Picas

class Rank(Enum):
    """Valores de las cartas"""
    TWO = 2, "2"
    THREE = 3, "3"
    FOUR = 4, "4"
    FIVE = 5, "5"
    SIX = 6, "6"
    SEVEN = 7, "7"
    EIGHT = 8, "8"
    NINE = 9, "9"
    TEN = 10, "10"
    JACK = 11, "J"
    QUEEN = 12, "Q"
    KING = 13, "K"
    ACE = 14, "A"
    
    def __init__(self, value, symbol):
        self._value_ = (value, symbol)
        self.symbol = symbol

class HandRank(Enum):
    """Ranking de manos de póker"""
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

class Card:
    """Representa una carta individual"""
    
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
        self.value = rank.value[0]
        self.symbol = rank.symbol
        self.suit_symbol = suit.value

    def __str__(self):
        return f"{self.symbol}{self.suit_symbol}"

    def __repr__(self):
        return f"Card({self.rank.name}, {self.suit.name})"

    def to_dict(self):
        """Devuelve la representación de la carta como diccionario"""
        return {
            'rank': self.rank.name,
            'suit': self.suit.name,
            'value': self.value,
            'symbol': self.symbol,
            'suit_symbol': self.suit_symbol
        }
        self.value = rank.value[0]  # Usamos el valor numérico del Rank
        self.symbol = rank.symbol
        self.suit_symbol = suit.value
    
    def __repr__(self):
        return f"{self.rank.symbol}{self.suit_symbol}"
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))
    
    def __str__(self):
        return f"{self.rank.symbol}{self.suit.value}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))
