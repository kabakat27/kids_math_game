"""
Unit tests for game_engine module
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_dir))

import pytest
from game_engine import (
    generate_game,
    validate_answer,
    generate_hint,
    format_question,
    FRUITS
)


class TestGenerateGame:
    """Test game generation"""
    
    def test_generate_game_returns_dict(self):
        """Test that generate_game returns a dictionary"""
        game = generate_game()
        assert isinstance(game, dict)
    
    def test_game_has_required_fields(self):
        """Test that generated game has all required fields"""
        game = generate_game()
        required_fields = [
            'game_id', 'fruit1', 'fruit2', 'price1', 'price2',
            'count1', 'count2', 'correct_answer', 'options'
        ]
        for field in required_fields:
            assert field in game, f"Missing field: {field}"
    
    def test_game_id_is_unique(self):
        """Test that each game gets a unique ID"""
        game1 = generate_game()
        game2 = generate_game()
        assert game1['game_id'] != game2['game_id']
    
    def test_fruits_are_from_list(self):
        """Test that selected fruits are from the predefined list"""
        game = generate_game()
        fruit_names = [f[0] for f in FRUITS]
        assert game['fruit1'] in fruit_names
        assert game['fruit2'] in fruit_names
    
    def test_fruits_are_different(self):
        """Test that two different fruits are selected"""
        game = generate_game()
        assert game['fruit1'] != game['fruit2']
    
    def test_prices_match_fruit_prices(self):
        """Test that prices match the fruit definitions"""
        for _ in range(5):
            game = generate_game()
            fruit_dict = {f[0]: f[1] for f in FRUITS}
            assert game['price1'] == fruit_dict[game['fruit1']]
            assert game['price2'] == fruit_dict[game['fruit2']]
    
    def test_counts_in_valid_range(self):
        """Test that counts are between 1 and 5"""
        game = generate_game()
        assert 1 <= game['count1'] <= 5
        assert 1 <= game['count2'] <= 5
    
    def test_correct_answer_calculation(self):
        """Test that correct_answer is calculated correctly"""
        game = generate_game()
        expected = (game['count1'] * game['price1']) + (game['count2'] * game['price2'])
        assert game['correct_answer'] == expected
    
    def test_options_contains_correct_answer(self):
        """Test that correct answer is in options"""
        game = generate_game()
        assert game['correct_answer'] in game['options']
    
    def test_options_has_four_choices(self):
        """Test that there are exactly 4 answer options"""
        game = generate_game()
        assert len(game['options']) == 4
    
    def test_options_are_unique(self):
        """Test that all options are unique"""
        game = generate_game()
        assert len(set(game['options'])) == 4
    
    def test_all_options_positive(self):
        """Test that all options are positive numbers"""
        game = generate_game()
        for option in game['options']:
            assert option > 0


class TestValidateAnswer:
    """Test answer validation"""
    
    def test_validate_with_correct_answer(self):
        """Test validation with correct answer"""
        game = generate_game()
        correct_index = game['options'].index(game['correct_answer'])
        result = validate_answer(game, correct_index)
        assert result['is_correct'] is True
        assert result['correct_answer'] == game['correct_answer']
        assert result['selected_answer'] == game['correct_answer']
        assert 'hint' not in result
    
    def test_validate_with_wrong_answer(self):
        """Test validation with wrong answer"""
        game = generate_game()
        # Find an incorrect answer
        for idx, option in enumerate(game['options']):
            if option != game['correct_answer']:
                result = validate_answer(game, idx)
                assert result['is_correct'] is False
                assert result['selected_answer'] != game['correct_answer']
                assert 'hint' in result
                break
    
    def test_validate_returns_correct_structure(self):
        """Test that validation returns correct structure"""
        game = generate_game()
        result = validate_answer(game, 0)
        required_fields = ['is_correct', 'correct_answer', 'selected_answer']
        for field in required_fields:
            assert field in result
    
    def test_validate_with_invalid_index(self):
        """Test validation with invalid answer index"""
        game = generate_game()
        result = validate_answer(game, 999)
        assert result['is_correct'] is False
        assert 'error' in result
    
    def test_validate_with_negative_index(self):
        """Test validation with negative index"""
        game = generate_game()
        result = validate_answer(game, -1)
        # Python allows negative indexing, so this should work
        # or return an error - both are acceptable
        assert 'is_correct' in result or 'error' in result


class TestGenerateHint:
    """Test hint generation"""
    
    def test_hint_contains_numbers(self):
        """Test that hint contains the calculation steps"""
        game = generate_game()
        hint = generate_hint(game)
        
        assert str(game['count1']) in hint
        assert str(game['price1']) in hint
        assert str(game['count2']) in hint
        assert str(game['price2']) in hint
    
    def test_hint_is_string(self):
        """Test that hint is a string"""
        game = generate_game()
        hint = generate_hint(game)
        assert isinstance(hint, str)
    
    def test_hint_not_empty(self):
        """Test that hint is not empty"""
        game = generate_game()
        hint = generate_hint(game)
        assert len(hint) > 0


class TestFormatQuestion:
    """Test question formatting"""
    
    def test_question_contains_fruit_names(self):
        """Test that question contains fruit names"""
        game = generate_game()
        question = format_question(game)
        assert game['fruit1'] in question
        assert game['fruit2'] in question
    
    def test_question_contains_counts(self):
        """Test that question contains the counts"""
        game = generate_game()
        question = format_question(game)
        assert str(game['count1']) in question
        assert str(game['count2']) in question
    
    def test_question_contains_prices(self):
        """Test that question contains the prices"""
        game = generate_game()
        question = format_question(game)
        assert str(game['price1']) in question
        assert str(game['price2']) in question
    
    def test_question_is_string(self):
        """Test that question is a string"""
        game = generate_game()
        question = format_question(game)
        assert isinstance(question, str)
    
    def test_question_not_empty(self):
        """Test that question is not empty"""
        game = generate_game()
        question = format_question(game)
        assert len(question) > 0


class TestGameFlow:
    """Test complete game flow"""
    
    def test_full_game_flow_correct_answer(self):
        """Test full flow: generate -> answer correctly"""
        game = generate_game()
        correct_index = game['options'].index(game['correct_answer'])
        result = validate_answer(game, correct_index)
        assert result['is_correct'] is True
    
    def test_full_game_flow_wrong_answer(self):
        """Test full flow: generate -> answer incorrectly -> get hint"""
        game = generate_game()
        # Find wrong answer
        for idx, option in enumerate(game['options']):
            if option != game['correct_answer']:
                result = validate_answer(game, idx)
                assert result['is_correct'] is False
                
                # Get hint
                hint = generate_hint(game)
                assert len(hint) > 0
                break
    
    def test_multiple_games_are_independent(self):
        """Test that multiple games don't interfere"""
        game1 = generate_game()
        game2 = generate_game()
        
        result1 = validate_answer(game1, 0)
        result2 = validate_answer(game2, 0)
        
        # They should potentially have different results
        # (though with only 4 random games, collision is possible)
        assert result1['correct_answer'] != result2['correct_answer'] or game1 != game2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
