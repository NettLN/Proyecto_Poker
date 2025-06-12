from typing import List, Dict
from collections import defaultdict
import random
from core.game import PokerGame
from core.card import Card, Rank, Suit, HandRank
from core.hand_evaluator import HandEvaluator

class PokerAssistant:
    """Asistente inteligente para póker que ayuda con análisis y predicciones"""
    
    def __init__(self, game: PokerGame, player_idx: int = 0):
        self.game = game
        self.player_idx = player_idx
        self.known_cards = set()
        self.update_known_cards()
    
    def update_known_cards(self):
        """Actualiza las cartas conocidas (mano del jugador + cartas comunitarias)"""
        self.known_cards = set()
        if self.player_idx < len(self.game.players):
            self.known_cards.update(self.game.players[self.player_idx].hand)
        self.known_cards.update(self.game.community_cards)
    
    def get_remaining_deck(self) -> List[Card]:
        """Obtiene las cartas que quedan en el mazo (excluyendo las conocidas)"""
        all_cards = [Card(rank, suit) for rank in Rank for suit in Suit]
        return [card for card in all_cards if card not in self.known_cards]
    
    def calculate_hand_strength(self) -> Dict[str, any]:
        """Calcula la fuerza actual de la mano del jugador"""
        if len(self.game.community_cards) < 3:
            return {"error": "Necesita al menos el flop para calcular fuerza"}
        
        self.update_known_cards()
        all_cards = self.game.players[self.player_idx].hand + self.game.community_cards
        current_rank, values = HandEvaluator.evaluate_hand(all_cards)
        print('[DEBUG calculate_hand_strength] current_rank:', current_rank, 'values:', values)
        
        return {
            "current_hand": current_rank.name,
            "hand_values": values,
            "strength_percentile": self._calculate_percentile(current_rank, values),
            "cards_in_hand": all_cards
        }
    
    def calculate_outs(self) -> Dict[str, any]:
        """Calcula las cartas que pueden mejorar tu mano (outs)"""
        if len(self.game.community_cards) >= 5:
            return {
                "message": "Juego terminado, no hay más cartas por salir",
                "total_outs": 0,
                "out_cards": [],
                "improvements": {},
                "probability": 0.0
            }
        
        self.update_known_cards()
        current_hand = self.game.players[self.player_idx].hand + self.game.community_cards
        current_rank, current_values = HandEvaluator.evaluate_hand(current_hand)
        print('[DEBUG calculate_outs] current_rank:', current_rank, 'current_values:', current_values)
        
        remaining_cards = self.get_remaining_deck()
        outs = []
        improvement_chances = defaultdict(list)
        
        # Probar cada carta restante
        for card in remaining_cards:
            test_hand = current_hand + [card]
            test_rank, test_values = HandEvaluator.evaluate_hand(test_hand)
            print('[DEBUG calculate_outs] test_card:', card, 'test_rank:', test_rank, 'test_values:', test_values)
            
            # Si mejora la mano
            if (test_rank.value > current_rank.value or 
                (test_rank.value == current_rank.value and self._compare_values(test_values, current_values) > 0)):
                
                print('[DEBUG calculate_outs] OUT found:', card)
                outs.append(card)
                improvement_chances[test_rank.name].append(card)
        
        print('[DEBUG calculate_outs] outs:', outs)
        return {
            "total_outs": len(outs),
            "out_cards": outs,
            "improvements": dict(improvement_chances),
            "probability": self._calculate_probability(len(outs), 5 - len(self.game.community_cards))
        }
    
    def predict_winning_probability(self, num_opponents: int = 1) -> Dict[str, float]:
        """Predice la probabilidad de ganar contra N oponentes"""
        if len(self.game.community_cards) < 3:
            return {"error": "Necesita al menos el flop para predicciones precisas"}
        
        self.update_known_cards()
        remaining_cards = self.get_remaining_deck()
        player_hand = self.game.players[self.player_idx].hand + self.game.community_cards
        
        # Simulación Monte Carlo
        wins = 0
        simulations = 1000
        cards_to_deal = 5 - len(self.game.community_cards)
        
        for _ in range(simulations):
            # Crear una baraja temporal
            temp_deck = remaining_cards.copy()
            random.shuffle(temp_deck)
            
            # Completar las cartas comunitarias
            if cards_to_deal > 0:
                additional_community = temp_deck[:cards_to_deal]
                complete_community = self.game.community_cards + additional_community
                temp_deck = temp_deck[cards_to_deal:]
            else:
                complete_community = self.game.community_cards
            
            # Mano completa del jugador
            player_complete = self.game.players[self.player_idx].hand + complete_community
            player_rank, player_values = HandEvaluator.evaluate_hand(player_complete)
            print('[DEBUG predict_winning_probability] player_rank:', player_rank, 'player_values:', player_values)
            
            # Simular manos de oponentes
            player_wins = True
            cards_used = cards_to_deal
            
            for opponent in range(num_opponents):
                if len(temp_deck) < 2:
                    break
                
                opponent_hole = temp_deck[cards_used:cards_used + 2]
                opponent_complete = opponent_hole + complete_community
                opponent_rank, opponent_values = HandEvaluator.evaluate_hand(opponent_complete)
                print('[DEBUG predict_winning_probability] opponent_rank:', opponent_rank, 'opponent_values:', opponent_values)
                
                # Comparar manos
                if (opponent_rank.value > player_rank.value or 
                    (opponent_rank.value == player_rank.value and 
                    self._compare_values(opponent_values, player_values) > 0)):
                    player_wins = False
                    break
                
                cards_used += 2
            
            if player_wins:
                wins += 1
        
        print('[DEBUG predict_winning_probability] wins:', wins, 'simulations:', simulations)
        win_probability = wins / simulations
        
        return {
            "win_probability": win_probability,
            "win_percentage": win_probability * 100,
            "simulations_run": simulations,
            "opponents": num_opponents,
            "opponent_analysis": {
                "board_texture": "N/A (análisis de textura pendiente)",
                "percentages": {} 
            },
            "bluff_analysis": {
                "bluff_recommended": False, 
                "reasoning": "N/A (análisis de farol pendiente)" 
            }
        }
    
    def suggest_best_action(self, pot_odds: float = 0.0) -> Dict[str, any]:
        """Sugiere la mejor acción basada en el análisis de la mano"""
        try:
            hand_strength_data = self.calculate_hand_strength()
            print(f"[DEBUG suggest_best_action] hand_strength_data: {hand_strength_data}")
            outs_info = self.calculate_outs()
            print(f"[DEBUG suggest_best_action] outs_info: {outs_info}")
            win_prob = self.predict_winning_probability()
            print(f"[DEBUG suggest_best_action] win_prob: {win_prob}")
        
            if "error" in hand_strength_data or "error" in win_prob:
                print('[DEBUG suggest_best_action] error:', hand_strength_data.get("error"), win_prob.get("error"))
                suggestion = {
                    "action": "NO_ACTION",
                    "reason": "Insuficiente información para sugerir acción",
                    "confidence": 0,
                    "additional_info": {
                        "total_outs": 0,
                        "out_cards": [],
                        "improvement_probability": 0.0,
                        "current_hand": "N/A",
                        "strength_percentile": 0.0,
                        "win_percentage": 0.0
                    },
                    "hand_values": []
                }
                print('[DEBUG suggest_best_action] suggestion:', suggestion)
                return suggestion
        
            win_percentage = win_prob["win_percentage"]
            suggestion = {
                "action": "",
                "reason": "",
                "confidence": 0,
                "additional_info": {
                    "total_outs": outs_info.get("total_outs", 0),
                    "out_cards": [card.to_dict() for card in outs_info.get("out_cards", [])],
                    "improvement_probability": outs_info.get("probability", 0.0) * 100,
                    "current_hand": hand_strength_data.get("current_hand", "N/A"),
                    "strength_percentile": hand_strength_data.get("strength_percentile", 0.0) * 100,
                    "win_percentage": win_prob.get("win_percentage", 0.0)
                },
                "hand_values": hand_strength_data.get("values", [])
            }
            print(f"[DEBUG suggest_best_action] Pre-decision suggestion: {suggestion}")
            # Lógica de decisión simplificada
            if win_percentage > 70:
                suggestion["action"] = "BET/RAISE (Apostar/Subir)"
                suggestion["reason"] = f"Mano muy fuerte ({win_percentage:.1f}% probabilidad de ganar)"
                suggestion["confidence"] = 9
        
            elif win_percentage > 50:
                if outs_info.get("total_outs", 0) > 8:
                    suggestion["action"] = "CALL/BET (Igualar/Apostar)"
                    suggestion["reason"] = f"Mano decente con {outs_info['total_outs']} outs"
                    suggestion["confidence"] = 7
                else:
                    suggestion["action"] = "CALL (Igualar)"
                    suggestion["reason"] = f"Mano marginal ({win_percentage:.1f}% probabilidad)"
                    suggestion["confidence"] = 5
        
            elif win_percentage > 30:
                if outs_info.get("total_outs", 0) > 6:
                    suggestion["action"] = "CALL si las odds son favorables"
                    suggestion["reason"] = f"{outs_info['total_outs']} outs disponibles"
                    suggestion["confidence"] = 4
                else:
                    suggestion["action"] = "CHECK/FOLD (Pasar/Retirarse)"
                    suggestion["reason"] = f"Mano débil ({win_percentage:.1f}% probabilidad)"
                    suggestion["confidence"] = 3
        
            else:
                suggestion["action"] = "FOLD (Retirarse)"
                suggestion["reason"] = f"Mano muy débil ({win_percentage:.1f}% probabilidad)"
                suggestion["confidence"] = 8
        
            print(f"[DEBUG suggest_best_action] Final suggestion: {suggestion}")
            return suggestion
        except Exception as e:
            print(f"[ERROR suggest_best_action] Exception type: {type(e).__name__}, message: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"error": "Error interno al sugerir acción"}

    
    def _calculate_percentile(self, rank: HandRank, values: List[int]) -> float:
        """Calcula el percentil de fuerza de la mano"""
        rank_value = rank.value * 1000000 + sum(v * (100 ** i) for i, v in enumerate(reversed(values)))
        return rank_value / (HandRank.ROYAL_FLUSH.value * 1000000 + 14 * 10000 + 14 * 100 + 14)
    
    def _compare_values(self, values1: List[int], values2: List[int]) -> int:
        """Compara dos listas de valores para desempate"""
        for v1, v2 in zip(values1, values2):
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0
    
    def _calculate_probability(self, outs: int, cards_to_come: int) -> float:
        """Calcula la probabilidad de mejorar la mano"""
        if cards_to_come == 1:
            return outs / 47
        elif cards_to_come == 2:
            return 1 - ((47 - outs) / 47) * ((46 - outs) / 46)
        return 0
