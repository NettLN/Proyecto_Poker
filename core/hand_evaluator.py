from typing import List, Tuple
from core.card import Card, HandRank, Rank

class HandEvaluator:
    """
    Clase responsable de evaluar la fuerza de una mano de póker Texas Hold'em.
    Cumple con SOLID y POO: separación de responsabilidades, métodos estáticos, y fácil extensión.
    """

    @staticmethod
    def evaluate_hand(cards: List[Card]) -> Tuple[HandRank, List[int]]:
        import traceback
        print("[DEBUG evaluate_hand] input:", cards)
        print("[DEBUG evaluate_hand] types:", [type(c) for c in cards])
        try:
            if len(cards) < 5:
                raise ValueError("Se requieren al menos 5 cartas para evaluar una mano")
            cards = sorted(cards, key=lambda c: c.rank.value[0], reverse=True)
            print('[DEBUG evaluate_hand] sorted cards:', cards)
            if HandEvaluator._is_royal_flush(cards):
                print('[DEBUG evaluate_hand] hand: ROYAL_FLUSH')
                return (HandRank.ROYAL_FLUSH, HandEvaluator._get_high_cards(cards, 5))
            if HandEvaluator._is_straight_flush(cards):
                print('[DEBUG evaluate_hand] hand: STRAIGHT_FLUSH')
                return (HandRank.STRAIGHT_FLUSH, HandEvaluator._get_straight_high(cards))
            if HandEvaluator._is_four_of_a_kind(cards):
                print('[DEBUG evaluate_hand] hand: FOUR_OF_A_KIND')
                return (HandRank.FOUR_OF_A_KIND, HandEvaluator._get_multiples(cards, 4))
            if HandEvaluator._is_full_house(cards):
                print('[DEBUG evaluate_hand] hand: FULL_HOUSE')
                return (HandRank.FULL_HOUSE, HandEvaluator._get_full_house(cards))
            if HandEvaluator._is_flush(cards):
                print('[DEBUG evaluate_hand] hand: FLUSH')
                return (HandRank.FLUSH, HandEvaluator._get_high_cards(cards, 5))
            if HandEvaluator._is_straight(cards):
                print('[DEBUG evaluate_hand] hand: STRAIGHT')
                return (HandRank.STRAIGHT, HandEvaluator._get_straight_high(cards))
            if HandEvaluator._is_three_of_a_kind(cards):
                print('[DEBUG evaluate_hand] hand: THREE_OF_A_KIND')
                return (HandRank.THREE_OF_A_KIND, HandEvaluator._get_multiples(cards, 3))
            if HandEvaluator._is_two_pair(cards):
                print('[DEBUG evaluate_hand] hand: TWO_PAIR')
                return (HandRank.TWO_PAIR, HandEvaluator._get_two_pair(cards))
            if HandEvaluator._is_one_pair(cards):
                print('[DEBUG evaluate_hand] hand: ONE_PAIR')
                return (HandRank.ONE_PAIR, HandEvaluator._get_multiples(cards, 2))
            print('[DEBUG evaluate_hand] hand: HIGH_CARD')
            return (HandRank.HIGH_CARD, HandEvaluator._get_high_cards(cards, 5))
        except Exception as e:
            print("[ERROR evaluate_hand]", str(e))
            traceback.print_exc()
            raise

    # Métodos auxiliares para detección de manos
    @staticmethod
    def _is_flush(cards: List[Card]) -> bool:
        suits = [c.suit for c in cards]
        for suit in set(suits):
            if suits.count(suit) >= 5:
                return True
        return False

    @staticmethod
    def _is_straight(cards: List[Card]) -> bool:
        print("[DEBUG _is_straight] input:", cards)
        print("[DEBUG _is_straight] types:", [type(c) for c in cards])
        ranks = sorted(set([c.rank.value[0] for c in cards]), reverse=True)
        count = 0
        last = None
        for r in ranks:
            if last is not None and last - r == 1:
                count += 1
            elif last is not None and last - r > 1:
                count = 0
            else:
                count = 0
            last = r
            if count >= 4:
                return True
        if set([14, 2, 3, 4, 5]).issubset(ranks):
            return True
        return False

    @staticmethod
    def _is_straight_flush(cards: List[Card]) -> bool:
        print("[DEBUG _is_straight_flush] input:", cards)
        print("[DEBUG _is_straight_flush] types:", [type(c) for c in cards])
        for suit in set(c.suit for c in cards):
            suited = [c for c in cards if c.suit == suit]
            if len(suited) >= 5:
                from itertools import combinations
                for comb in combinations(suited, 5):
                    print("[DEBUG _is_straight_flush] comb:", comb)
                    if HandEvaluator._is_straight(list(comb)):
                        return True
        return False

    @staticmethod
    def _is_royal_flush(cards: List[Card]) -> bool:
        for suit in set(c.suit for c in cards):
            suited = [c for c in cards if c.suit == suit]
            if len(suited) >= 5:
                ranks = set(c.rank.value for c in suited)
                if set([10,11,12,13,14]).issubset(ranks):
                    # Verifica que sea escalera real (no solo las cartas)
                    from itertools import combinations
                    for comb in combinations(suited, 5):
                        comb_ranks = set(c.rank.value for c in comb)
                        if comb_ranks == set([10,11,12,13,14]):
                            return True
        return False

    @staticmethod
    def _is_four_of_a_kind(cards: List[Card]) -> bool:
        return HandEvaluator._has_n_of_a_kind(cards, 4)

    @staticmethod
    def _is_full_house(cards: List[Card]) -> bool:
        return HandEvaluator._has_n_of_a_kind(cards, 3) and HandEvaluator._has_n_of_a_kind(cards, 2)

    @staticmethod
    def _is_three_of_a_kind(cards: List[Card]) -> bool:
        return HandEvaluator._has_n_of_a_kind(cards, 3)

    @staticmethod
    def _is_two_pair(cards: List[Card]) -> bool:
        ranks = [c.rank.value[0] for c in cards]
        return len([r for r in set(ranks) if ranks.count(r) >= 2]) >= 2

    @staticmethod
    def _is_one_pair(cards: List[Card]) -> bool:
        return HandEvaluator._has_n_of_a_kind(cards, 2)

    @staticmethod
    def _has_n_of_a_kind(cards: List[Card], n: int) -> bool:
        ranks = [c.rank.value[0] for c in cards]
        return any(ranks.count(r) >= n for r in set(ranks))

    # Métodos auxiliares para obtener valores de desempate
    @staticmethod
    def _get_high_cards(cards: List[Card], n: int) -> List[int]:
        return [c.rank.value[0] for c in sorted(cards, key=lambda c: c.rank.value[0], reverse=True)[:n]]

    @staticmethod
    def _get_straight_high(cards: List[Card]) -> List[int]:
        print("[DEBUG _get_straight_high] input:", cards)
        print("[DEBUG _get_straight_high] types:", [type(c) for c in cards])
        ranks = sorted(set([c.rank.value[0] for c in cards]), reverse=True)
        count = 0
        last = None
        for i, r in enumerate(ranks):
            if last is not None and last - r == 1:
                count += 1
            elif last is not None and last - r > 1:
                count = 0
            else:
                count = 0
            last = r
            if count >= 4:
                res = [ranks[i-4]]
                print("[DEBUG _get_straight_high] return:", res, type(res))
                return res  # Mayor de la escalera
        if set([14, 2, 3, 4, 5]).issubset(ranks):
            print("[DEBUG _get_straight_high] return:", [5], type([5]))
            return [5]
        print("[DEBUG _get_straight_high] return:", [max(ranks)], type([max(ranks)]))
        return [max(ranks)]

    @staticmethod
    def _get_multiples(cards: List[Card], n: int) -> List[int]:
        try:
            ranks = [c.rank.value[0] for c in cards]
            multiples = [r for r in set(ranks) if ranks.count(r) == n]
            kickers = [r for r in ranks if r not in multiples]
            res = sorted(multiples, reverse=True) + sorted(kickers, reverse=True)[:5-len(multiples)]
            print("[DEBUG _get_multiples] return:", res, type(res))
            return res
        except Exception as e:
            print("[ERROR _get_multiples]", str(e))
            raise

    @staticmethod
    def _get_full_house(cards: List[Card]) -> List[int]:
        ranks = [c.rank.value[0] for c in cards]
        triple = [r for r in set(ranks) if ranks.count(r) >= 3]
        pair = [r for r in set(ranks) if ranks.count(r) >= 2 and r not in triple]
        if triple:
            if pair:
                res = [max(triple), max(pair)]
                print("[DEBUG _get_full_house] return:", res, type(res))
                return res
            else:
                res = [max(triple), 0]
                print("[DEBUG _get_full_house] return:", res, type(res))
                return res
        res = [max(ranks), 0]
        print("[DEBUG _get_full_house] return:", res, type(res))
        return res

    @staticmethod
    def _get_two_pair(cards: List[Card]) -> List[int]:
        ranks = [c.rank.value[0] for c in cards]
        pairs = sorted([r for r in set(ranks) if ranks.count(r) == 2], reverse=True)
        kicker = max([r for r in ranks if r not in pairs], default=0)
        res = pairs[:2] + [kicker]
        print("[DEBUG _get_two_pair] return:", res, type(res))
        return res
