from core.game import PokerGame, GameStage

# Prueba básica del flujo de PokerGame
if __name__ == "__main__":
    num_players = 3
    nombres = ["Ana", "Luis", "Carlos"]
    game = PokerGame(num_players, nombres)

    print("\n--- Inicio de la partida ---")
    print("Etapa:", game.stage)
    print("Jugadores:", [p.name for p in game.players])

    print("\nRepartiendo cartas iniciales...")
    game.deal_hole_cards()
    for player in game.players:
        print(f"{player.name}: {[str(c) for c in player.hand]}")

    print("\nAvanzando a Flop...")
    game.next_stage()
    print("Cartas comunitarias:", [str(c) for c in game.community_cards])
    print("Etapa actual:", game.stage)

    print("\nAvanzando a Turn...")
    game.next_stage()
    print("Cartas comunitarias:", [str(c) for c in game.community_cards])
    print("Etapa actual:", game.stage)

    print("\nAvanzando a River...")
    game.next_stage()
    print("Cartas comunitarias:", [str(c) for c in game.community_cards])
    print("Etapa actual:", game.stage)

    print("\nAvanzando a Showdown...")
    game.next_stage()
    print("Etapa actual:", game.stage)

    print("\nEstado final del juego:")
    print(game.get_game_state())
