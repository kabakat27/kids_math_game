"""
Integration tests for Flask API
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_dir))

import pytest
from app import create_app


@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


class TestHealthEndpoint:
    """Test /health endpoint"""
    
    def test_health_check_returns_200(self, client):
        """Test that health endpoint returns 200"""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_check_returns_json(self, client):
        """Test that health endpoint returns JSON"""
        response = client.get('/health')
        assert response.content_type == 'application/json'
    
    def test_health_check_has_status(self, client):
        """Test that health response has status field"""
        response = client.get('/health')
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'healthy'


class TestStartGameEndpoint:
    """Test POST /api/v1/game/start endpoint"""
    
    def test_start_game_returns_200(self, client):
        """Test that start game returns 200"""
        response = client.post('/api/v1/game/start')
        assert response.status_code == 200
    
    def test_start_game_returns_json(self, client):
        """Test that start game returns JSON"""
        response = client.post('/api/v1/game/start')
        assert response.content_type == 'application/json'
    
    def test_start_game_response_structure(self, client):
        """Test that start game response has required fields"""
        response = client.post('/api/v1/game/start')
        data = response.get_json()
        
        required_fields = ['success', 'game_id', 'question', 'options']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
    
    def test_start_game_success_flag(self, client):
        """Test that success flag is true"""
        response = client.post('/api/v1/game/start')
        data = response.get_json()
        assert data['success'] is True
    
    def test_start_game_has_four_options(self, client):
        """Test that game has exactly 4 options"""
        response = client.post('/api/v1/game/start')
        data = response.get_json()
        assert len(data['options']) == 4
    
    def test_start_game_options_are_unique(self, client):
        """Test that all options are unique"""
        response = client.post('/api/v1/game/start')
        data = response.get_json()
        assert len(set(data['options'])) == 4
    
    def test_start_game_returns_different_games(self, client):
        """Test that consecutive calls create different games"""
        response1 = client.post('/api/v1/game/start')
        response2 = client.post('/api/v1/game/start')
        
        data1 = response1.get_json()
        data2 = response2.get_json()
        
        assert data1['game_id'] != data2['game_id']


class TestValidateEndpoint:
    """Test POST /api/v1/game/validate endpoint"""
    
    def test_validate_without_request_body(self, client):
        """Test validation without request body"""
        response = client.post('/api/v1/game/validate')
        assert response.status_code == 400
    
    def test_validate_without_game_id(self, client):
        """Test validation without game_id"""
        response = client.post('/api/v1/game/validate', json={'answer_index': 0})
        assert response.status_code == 400
    
    def test_validate_without_answer_index(self, client):
        """Test validation without answer_index"""
        response = client.post('/api/v1/game/validate', json={'game_id': '123'})
        assert response.status_code == 400
    
    def test_validate_with_invalid_game_id(self, client):
        """Test validation with non-existent game_id"""
        response = client.post('/api/v1/game/validate', json={
            'game_id': 'invalid_id',
            'answer_index': 0
        })
        assert response.status_code == 404
    
    def test_validate_with_valid_game(self, client):
        """Test validation with valid game"""
        # Start game
        start_response = client.post('/api/v1/game/start')
        game_data = start_response.get_json()
        game_id = game_data['game_id']
        
        # Validate first option
        validate_response = client.post('/api/v1/game/validate', json={
            'game_id': game_id,
            'answer_index': 0
        })
        
        assert validate_response.status_code == 200
        data = validate_response.get_json()
        assert data['success'] is True
    
    def test_validate_response_structure(self, client):
        """Test validate response has required fields"""
        # Start game
        start_response = client.post('/api/v1/game/start')
        game_data = start_response.get_json()
        game_id = game_data['game_id']
        
        # Validate
        validate_response = client.post('/api/v1/game/validate', json={
            'game_id': game_id,
            'answer_index': 0
        })
        
        data = validate_response.get_json()
        required_fields = ['success', 'is_correct', 'correct_answer', 'selected_answer']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
    
    def test_validate_correct_answer(self, client, app):
        """Test validation recognizes correct answer"""
        with app.test_request_context():
            # Start game
            start_response = client.post('/api/v1/game/start')
            game_data = start_response.get_json()
            game_id = game_data['game_id']
            
            # Get the stored game to find correct answer
            stored_game = app.active_games[game_id]
            correct_index = game_data['options'].index(stored_game['correct_answer'])
            
            # Validate correct answer
            validate_response = client.post('/api/v1/game/validate', json={
                'game_id': game_id,
                'answer_index': correct_index
            })
            
            data = validate_response.get_json()
            assert data['is_correct'] is True
    
    def test_validate_includes_hint_on_wrong_answer(self, client, app):
        """Test that hint is provided on wrong answer"""
        with app.test_request_context():
            # Start game
            start_response = client.post('/api/v1/game/start')
            game_data = start_response.get_json()
            game_id = game_data['game_id']
            
            # Get the stored game to find wrong answer
            stored_game = app.active_games[game_id]
            correct_index = game_data['options'].index(stored_game['correct_answer'])
            
            # Find a wrong answer
            for idx in range(4):
                if idx != correct_index:
                    # Validate wrong answer
                    validate_response = client.post('/api/v1/game/validate', json={
                        'game_id': game_id,
                        'answer_index': idx
                    })
                    
                    data = validate_response.get_json()
                    assert data['is_correct'] is False
                    assert 'hint' in data
                    break


class TestHintEndpoint:
    """Test GET /api/v1/game/hint endpoint"""
    
    def test_hint_without_game_id(self, client):
        """Test hint endpoint without game_id"""
        response = client.get('/api/v1/game/hint')
        assert response.status_code == 400
    
    def test_hint_with_invalid_game_id(self, client):
        """Test hint endpoint with invalid game_id"""
        response = client.get('/api/v1/game/hint?game_id=invalid')
        assert response.status_code == 404
    
    def test_hint_with_valid_game_id(self, client):
        """Test hint endpoint with valid game_id"""
        # Start game
        start_response = client.post('/api/v1/game/start')
        game_data = start_response.get_json()
        game_id = game_data['game_id']
        
        # Get hint
        hint_response = client.get(f'/api/v1/game/hint?game_id={game_id}')
        
        assert hint_response.status_code == 200
        data = hint_response.get_json()
        assert 'hint' in data
        assert len(data['hint']) > 0


class TestNotFoundEndpoint:
    """Test 404 handling"""
    
    def test_nonexistent_endpoint_returns_404(self, client):
        """Test that nonexistent endpoint returns 404"""
        response = client.get('/api/v1/nonexistent')
        assert response.status_code == 404


class TestFullGameFlow:
    """Test complete game flow"""
    
    def test_complete_game_flow(self, client, app):
        """Test start -> validate -> result flow"""
        with app.test_request_context():
            # 1. Start game
            start_response = client.post('/api/v1/game/start')
            assert start_response.status_code == 200
            game_data = start_response.get_json()
            assert game_data['success'] is True
            
            game_id = game_data['game_id']
            stored_game = app.active_games[game_id]
            correct_index = game_data['options'].index(stored_game['correct_answer'])
            
            # 2. Validate answer
            validate_response = client.post('/api/v1/game/validate', json={
                'game_id': game_id,
                'answer_index': correct_index
            })
            assert validate_response.status_code == 200
            
            result_data = validate_response.get_json()
            assert result_data['success'] is True
            assert result_data['is_correct'] is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
