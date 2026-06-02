"""
Kids Math Game Engine - Core game logic
"""

import random
from typing import Dict, Tuple, List


FRUITS = [
    ("Apple", 2),
    ("Banana", 3),
    ("Orange", 4),
    ("Pear", 5),
    ("Grapes", 6)
]


def generate_game() -> Dict:
    """
    Generate a new math game question.
    
    Returns:
        dict: Game data with question, options, and metadata
              {
                  'fruit1': str,
                  'fruit2': str,
                  'price1': int,
                  'price2': int,
                  'count1': int,
                  'count2': int,
                  'correct_answer': int,
                  'options': list[int],
                  'game_id': str  # for tracking
              }
    """
    # Select two random fruits
    fruit1, fruit2 = random.sample(FRUITS, 2)
    name1, price1 = fruit1
    name2, price2 = fruit2
    
    # Random counts
    count1 = random.randint(1, 5)
    count2 = random.randint(1, 5)
    
    # Calculate correct answer
    correct_answer = (count1 * price1) + (count2 * price2)
    
    # Generate wrong answers
    wrong_answers = set()
    while len(wrong_answers) < 3:
        wrong = correct_answer + random.randint(-5, 5)
        if wrong != correct_answer and wrong > 0:
            wrong_answers.add(wrong)
    
    # Compile options
    options = list(wrong_answers)
    options.append(correct_answer)
    random.shuffle(options)
    
    # Generate unique game ID
    game_id = f"{random.randint(100000, 999999)}"
    
    return {
        'game_id': game_id,
        'fruit1': name1,
        'fruit2': name2,
        'price1': price1,
        'price2': price2,
        'count1': count1,
        'count2': count2,
        'correct_answer': correct_answer,
        'options': options
    }


def validate_answer(game_data: Dict, answer_index: int) -> Dict:
    """
    Validate user's answer to a question.
    
    Args:
        game_data: The game data returned from generate_game()
        answer_index: 0-based index of the selected answer from options
    
    Returns:
        dict: Validation result
              {
                  'is_correct': bool,
                  'correct_answer': int,
                  'selected_answer': int,
                  'hint': str (if incorrect)
              }
    """
    try:
        selected_answer = game_data['options'][answer_index]
    except (IndexError, TypeError):
        return {
            'is_correct': False,
            'correct_answer': game_data['correct_answer'],
            'selected_answer': None,
            'error': 'Invalid answer index'
        }
    
    is_correct = selected_answer == game_data['correct_answer']
    
    result = {
        'is_correct': is_correct,
        'correct_answer': game_data['correct_answer'],
        'selected_answer': selected_answer
    }
    
    if not is_correct:
        result['hint'] = generate_hint(game_data)
    
    return result


def generate_hint(game_data: Dict) -> str:
    """
    Generate a helpful hint for an incorrect answer.
    
    Args:
        game_data: The game data
    
    Returns:
        str: Hint text
    """
    count1 = game_data['count1']
    price1 = game_data['price1']
    count2 = game_data['count2']
    price2 = game_data['price2']
    
    return (
        f"First calculate:\n"
        f"{count1} × {price1} = {count1 * price1}\n"
        f"and\n"
        f"{count2} × {price2} = {count2 * price2}\n"
        f"Then add the results together."
    )


def format_question(game_data: Dict) -> str:
    """
    Format game data into a readable question text.
    
    Args:
        game_data: The game data
    
    Returns:
        str: Formatted question
    """
    return (
        f"Adam bought {game_data['count1']} {game_data['fruit1']}(s) "
        f"and {game_data['count2']} {game_data['fruit2']}(s).\n\n"
        f"Price of one {game_data['fruit1']} = {game_data['price1']} dollars.\n"
        f"Price of one {game_data['fruit2']} = {game_data['price2']} dollars.\n\n"
        f"How much did Adam pay?"
    )
