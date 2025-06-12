# Lógica principal del juego de póker Texas Hold'em
from enum import Enum, auto
from typing import List, Optional
from core.deck import Deck
from core.player import Player
from core.card import Card

class GameStage(Enum):
    PRE_FLOP = auto()
    FLOP = auto()
    TURN = auto()
    RIVER = auto()
    SHOWDOWN = auto()

class PokerGame:
    """
    Clase principal que gestiona el flujo del juego de póker, siguiendo principios SOLID y POO.
    """
    def __init__(self, num_players: int, player_names: Optional[List[str]] = None):
        if not 2 <= num_players <= 10:
            raise ValueError("El número de jugadores debe estar entre 2 y 10")
        self.deck = Deck()
        self.players: List[Player] = []
        self.community_cards: List[Card] = []
        self.stage = GameStage.PRE_FLOP
        self.current_player_idx = 0
        self.num_players = num_players
        self._init_players(player_names)

    def _init_players(self, player_names: Optional[List[str]]):
        self.players = []
        for i in range(self.num_players):
            name = player_names[i] if player_names and i < len(player_names) else f"Jugador {i+1}"
            self.players.append(Player(name))

    def start_new_hand(self):
        self.deck.reset()
        self.community_cards = []
        self.stage = GameStage.PRE_FLOP
        for player in self.players:
            player.reset_hand()
        self.deal_hole_cards()

    def deal_hole_cards(self):
        for player in self.players:
            player.hand = self.deck.deal_cards(2)

    def deal_flop(self):
        if self.stage != GameStage.PRE_FLOP:
            raise Exception("No se puede repartir el flop en esta etapa")
        self.community_cards = self.deck.deal_cards(3)
        self.stage = GameStage.FLOP

    def deal_turn(self):
        if self.stage != GameStage.FLOP:
            raise Exception("No se puede repartir el turn en esta etapa")
        self.community_cards.append(self.deck.deal_card())
        self.stage = GameStage.TURN

    def deal_river(self):
        if self.stage != GameStage.TURN:
            raise Exception("No se puede repartir el river en esta etapa")
        self.community_cards.append(self.deck.deal_card())
        self.stage = GameStage.RIVER

    def next_stage(self):
        if self.stage == GameStage.PRE_FLOP:
            self.deal_flop()
        elif self.stage == GameStage.FLOP:
            self.deal_turn()
        elif self.stage == GameStage.TURN:
            self.deal_river()
        elif self.stage == GameStage.RIVER:
            self.stage = GameStage.SHOWDOWN
        else:
            raise Exception("El juego ya está en showdown.")

    def get_game_state(self) -> dict:
        return {
            "stage": self.stage.name,
            "community_cards": [card.to_dict() for card in self.community_cards],
            "players": [
                {
                    "name": player.name,
                    "hand": [card.to_dict() for card in player.hand],
                } for player in self.players
            ]
        }
