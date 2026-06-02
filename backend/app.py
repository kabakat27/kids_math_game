"""
Flask API for Kids Math Game
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from game_engine import generate_game, validate_answer, format_question
from config import get_config


def create_app(config_name: str = None) -> Flask:
    """
    Factory function to create Flask app.
    
    Args:
        config_name: Environment name ('development', 'staging', 'production', 'testing')
    
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})
    
    # Store games in memory (in production, use database)
    app.active_games = {}
    
    # ==================== ROUTES ====================
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'environment': app.config.get('ENV', 'unknown')
        }), 200
    
    
    @app.route('/api/v1/game/start', methods=['POST'])
    def start_game():
        """
        Start a new game.
        
        Returns:
            JSON: {
                'game_id': str,
                'question': str,
                'options': list[int],
                'fruit1': str,
                'fruit2': str,
                'count1': int,
                'count2': int
            }
        """
        try:
            game_data = generate_game()
            
            # Store game data (needed to validate later)
            app.active_games[game_data['game_id']] = game_data
            
            # Return question data (don't expose correct_answer to client!)
            return jsonify({
                'success': True,
                'game_id': game_data['game_id'],
                'question': format_question(game_data),
                'options': game_data['options'],
                # Optional: for debugging
                'metadata': {
                    'fruit1': game_data['fruit1'],
                    'fruit2': game_data['fruit2'],
                    'count1': game_data['count1'],
                    'count2': game_data['count2']
                }
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    
    @app.route('/api/v1/game/validate', methods=['POST'])
    def validate_game_answer():
        """
        Validate an answer to a question.
        
        Request body:
            {
                'game_id': str,
                'answer_index': int (0-based index into options array)
            }
        
        Returns:
            JSON: {
                'success': bool,
                'is_correct': bool,
                'correct_answer': int,
                'selected_answer': int,
                'hint': str (only if incorrect)
            }
        """
        try:
            data = request.get_json(force=False, silent=True)
            
            if not data:
                return jsonify({
                    'success': False,
                    'error': 'Request body required'
                }), 400
            
            game_id = data.get('game_id')
            answer_index = data.get('answer_index')
            
            if game_id is None or answer_index is None:
                return jsonify({
                    'success': False,
                    'error': 'game_id and answer_index required'
                }), 400
            
            # Get stored game
            game_data = app.active_games.get(game_id)
            if not game_data:
                return jsonify({
                    'success': False,
                    'error': 'Game not found. Start a new game first.'
                }), 404
            
            # Validate answer
            result = validate_answer(game_data, answer_index)
            
            # Clean up old games to prevent memory leak (optional)
            if result['is_correct']:
                del app.active_games[game_id]
            
            return jsonify({
                'success': True,
                **result
            }), 200
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    
    @app.route('/api/v1/game/hint', methods=['GET'])
    def get_hint():
        """
        Get hint for current game.
        
        Query params:
            game_id: str
        
        Returns:
            JSON: {'hint': str}
        """
        try:
            game_id = request.args.get('game_id')
            
            if not game_id:
                return jsonify({
                    'success': False,
                    'error': 'game_id query parameter required'
                }), 400
            
            game_data = app.active_games.get(game_id)
            if not game_data:
                return jsonify({
                    'success': False,
                    'error': 'Game not found'
                }), 404
            
            from game_engine import generate_hint
            hint = generate_hint(game_data)
            
            return jsonify({
                'success': True,
                'hint': hint
            }), 200
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors"""
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app


# Create app instance for production
if __name__ != '__main__':
    app = create_app()


if __name__ == '__main__':
    # For development: python app.py
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
