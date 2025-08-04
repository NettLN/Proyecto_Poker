from flask import Flask, render_template, request, jsonify
from core.game import PokerGame
from utils.assistant import PokerAssistant
from core.card import Card, Rank, Suit

app = Flask(__name__)

game = None
assistant = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    try:
        global game, assistant
        num_players = request.json.get('num_players', 2)
        player_names = request.json.get('player_names', None)
        if not 2 <= num_players <= 6:
            return jsonify({'error': 'Número de jugadores debe estar entre 2 y 6'}), 400
        game = PokerGame(num_players, player_names)
        game.start_new_hand()
        assistant = PokerAssistant(game)
        state = game.get_game_state()
        print('[DEBUG new_game] state:', state)
        return jsonify({
            'game_id': '1',
            'game_state': state,
            'message': 'Nuevo juego creado'
        })
    except ValueError as e:
        print("ValueError:", e)
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        import traceback
        print("Exception:", e)
        traceback.print_exc()  # <--- Esto imprime el traceback real
        return jsonify({'error': 'Error al crear el juego: ' + str(e)}), 500

@app.route('/deal_cards', methods=['POST'])
def deal_cards():
    try:
        global game, assistant
        if not game:
            return jsonify({'error': 'No hay juego activo'}), 400
        # Usar el Enum GameStage para avanzar etapas
        if game.stage == game.stage.PRE_FLOP:
            game.deal_flop()
        elif game.stage == game.stage.FLOP:
            game.deal_turn()
        elif game.stage == game.stage.TURN:
            game.deal_river()
        else:
            return jsonify({'error': 'No se pueden hacer más movimientos'}), 400
        new_state = game.get_game_state()
        print('[DEBUG deal_cards] new_state:', new_state)
        return jsonify({
            'game_state': new_state,
            'message': 'Cartas repartidas'
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al repartir cartas: ' + str(e)}), 500

@app.route('/analyze_hand', methods=['POST'])
def analyze_hand():
    try:
        global game, assistant
        if not game:
            return jsonify({'error': 'No hay juego activo'}), 400
            
        player_idx = request.json.get('player_idx', 0)
        if player_idx >= game.num_players:
            return jsonify({'error': 'Índice de jugador inválido'}), 400
            
        analysis = assistant.suggest_best_action()
        print('[DEBUG analyze_hand] analysis:', analysis)
        game_state = game.get_game_state()
        print('[DEBUG analyze_hand] game_state:', game_state)
        
        if not game_state or not isinstance(game_state, dict):
            return jsonify({'error': 'Estado del juego inválido'}), 500
            
        return jsonify({
            'analysis': analysis,
            'game_state': game_state
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/advanced_analysis', methods=['POST'])
def advanced_analysis():
    try:
        global game, assistant
        if not game:
            return jsonify({'error': 'No hay juego activo'}), 400
            
        player_idx = request.json.get('player_idx', 0)
        if player_idx >= game.num_players:
            return jsonify({'error': 'Índice de jugador inválido'}), 400
            
        analysis = assistant.predict_winning_probability()
        print('[DEBUG advanced_analysis] analysis:', analysis)
        game_state = game.get_game_state()
        print('[DEBUG advanced_analysis] game_state:', game_state)
        
        if not game_state or not isinstance(game_state, dict):
            return jsonify({'error': 'Estado del juego inválido'}), 500
            
        return jsonify({
            'analysis': analysis,
            'game_state': game_state
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/reset_game/<int:game_id>', methods=['POST'])
def reset_game(game_id):
    try:
        global game, assistant
        if not game:
            return jsonify({'error': 'No hay juego activo'}), 400
        game.start_new_hand()
        game_state = game.get_game_state()
        
        if not game_state or not isinstance(game_state, dict):
            return jsonify({'error': 'Estado del juego inválido'}), 500
            
        return jsonify({
            'game_state': game_state,
            'message': 'Juego reiniciado'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/set_custom_hand', methods=['POST'])
def set_custom_hand():
    try:
        global game, assistant
        if not game:
            return jsonify({'error': 'No hay juego activo'}), 400
            
        cards = request.json.get('cards')
        if not cards or len(cards) != 2:
            return jsonify({'error': 'Las dos cartas son requeridas'}), 400
        card1, card2 = cards

        # Validar que las cartas sean válidas
        try:
            card1_obj = Card(Rank[card1['rank']], Suit[card1['suit']])
            card2_obj = Card(Rank[card2['rank']], Suit[card2['suit']])
        except (KeyError, TypeError):
            return jsonify({'error': 'Formato de cartas inválido'}), 400

        # Actualizar la mano del jugador
        game.players[0].hand = [card1_obj, card2_obj]

        game_state = game.get_game_state()

        if not game_state or not isinstance(game_state, dict):
            return jsonify({'error': 'Estado del juego inválido'}), 500
            
        return jsonify({
            'game_state': game_state,
            'message': 'Mano personalizada establecida'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
