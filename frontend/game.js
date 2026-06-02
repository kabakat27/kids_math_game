// Configuration
const API_BASE_URL = 'http://localhost:5000/api/v1';

// Game state
let currentGame = null;
let questionCount = 0;
let attemptCount = 0;
const MAX_ATTEMPTS = 2;

// Initialize game on page load
document.addEventListener('DOMContentLoaded', () => {
    startNewGame();
});

/**
 * Start a new game
 */
async function startNewGame() {
    try {
        resetUI();
        
        const response = await fetch(`${API_BASE_URL}/game/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (!data.success) {
            showError(`Failed to start game: ${data.error}`);
            return;
        }

        currentGame = data;
        questionCount++;
        attemptCount = 0;

        displayGame(data);
    } catch (error) {
        showError(`Connection error: ${error.message}`);
    }
}

/**
 * Display the game question and options
 */
function displayGame(game) {
    // Update score badge
    document.getElementById('scoreBadge').textContent = `Question ${questionCount}`;

    // Display question
    document.getElementById('questionText').textContent = game.question;

    // Display options
    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.innerHTML = '';

    game.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.className = 'option-btn';
        button.textContent = `${index + 1}) ${option} dollars`;
        button.onclick = () => selectAnswer(index);
        optionsContainer.appendChild(button);
    });

    // Show question card
    document.getElementById('questionCard').classList.remove('hidden');
    document.getElementById('resultCard').classList.add('hidden');
    document.getElementById('errorCard').classList.add('hidden');
    document.getElementById('hintSection').style.display = 'none';
}

/**
 * Handle answer selection
 */
async function selectAnswer(answerIndex) {
    try {
        attemptCount++;

        const response = await fetch(`${API_BASE_URL}/game/validate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                game_id: currentGame.game_id,
                answer_index: answerIndex
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        if (!result.success) {
            showError(`Validation error: ${result.error}`);
            return;
        }

        // Highlight selected option
        const buttons = document.querySelectorAll('.option-btn');
        buttons.forEach((btn, idx) => {
            if (idx === answerIndex) {
                btn.classList.add('selected');
            }
            btn.disabled = true;
        });

        // Show result
        if (result.is_correct) {
            showCorrectResult(result);
        } else if (attemptCount < MAX_ATTEMPTS) {
            showIncorrectResult(result);
        } else {
            showFinalResult(result);
        }
    } catch (error) {
        showError(`Error validating answer: ${error.message}`);
    }
}

/**
 * Display correct answer feedback
 */
function showCorrectResult(result) {
    document.getElementById('questionCard').classList.add('hidden');
    const resultCard = document.getElementById('resultCard');
    resultCard.classList.remove('hidden', 'incorrect');
    resultCard.classList.add('correct');

    document.getElementById('resultText').textContent = 'Correct! Good Job! 🎉';
    document.getElementById('resultDetails').innerHTML = `
        <strong>Your Answer:</strong> ${result.selected_answer} dollars<br>
        <strong>Correct Answer:</strong> ${result.correct_answer} dollars<br>
        <p style="margin-top: 15px; font-weight: bold; color: #10b981;">✅ You got it right!</p>
    `;
}

/**
 * Display incorrect answer with hint option
 */
function showIncorrectResult(result) {
    document.getElementById('questionCard').classList.add('hidden');
    const resultCard = document.getElementById('resultCard');
    resultCard.classList.remove('hidden', 'correct');
    resultCard.classList.add('incorrect');

    document.getElementById('resultText').textContent = `Not quite right... Try again! (Attempt ${attemptCount}/${MAX_ATTEMPTS})`;
    document.getElementById('resultDetails').innerHTML = `
        <strong>Your Answer:</strong> ${result.selected_answer} dollars<br>
        <strong>Correct Answer:</strong> ${result.correct_answer} dollars
    `;

    // Show hint section
    const hintSection = document.getElementById('hintSection');
    hintSection.style.display = 'block';
    const hintBtn = document.getElementById('hintBtn');
    hintBtn.disabled = false;
    hintBtn.textContent = '💡 Get Hint';

    // Add retry button
    const retryBtn = document.createElement('button');
    retryBtn.className = 'btn btn-primary';
    retryBtn.style.marginTop = '10px';
    retryBtn.textContent = 'Try Another Question';
    retryBtn.onclick = startNewGame;

    // Clear previous result details and add retry button
    const resultDetails = document.getElementById('resultDetails');
    resultDetails.appendChild(document.createElement('br'));
    resultDetails.appendChild(retryBtn);

    // Display hint if available
    if (result.hint) {
        displayHint(result.hint);
    }
}

/**
 * Display final result when all attempts are used
 */
function showFinalResult(result) {
    document.getElementById('questionCard').classList.add('hidden');
    const resultCard = document.getElementById('resultCard');
    resultCard.classList.remove('hidden', 'correct');
    resultCard.classList.add('incorrect');

    document.getElementById('resultText').textContent = 'Game Over!';
    document.getElementById('resultDetails').innerHTML = `
        <strong>Your Final Answer:</strong> ${result.selected_answer} dollars<br>
        <strong>Correct Answer:</strong> ${result.correct_answer} dollars<br>
        <p style="margin-top: 15px; font-style: italic; color: #ef4444;">You've used all your attempts. Better luck next time!</p>
    `;

    // Change button text
    document.querySelector('.btn-primary').textContent = 'Try Another Question';
}

/**
 * Get hint for current question
 */
async function getHint() {
    try {
        const response = await fetch(`${API_BASE_URL}/game/hint?game_id=${currentGame.game_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (!data.success) {
            showError(`Failed to get hint: ${data.error}`);
            return;
        }

        displayHint(data.hint);
        document.getElementById('hintBtn').disabled = true;
    } catch (error) {
        showError(`Error getting hint: ${error.message}`);
    }
}

/**
 * Display hint text
 */
function displayHint(hint) {
    const hintText = document.getElementById('hintText');
    hintText.textContent = hint;
}

/**
 * Show error message
 */
function showError(message) {
    document.getElementById('questionCard').classList.add('hidden');
    document.getElementById('resultCard').classList.add('hidden');

    const errorCard = document.getElementById('errorCard');
    errorCard.classList.remove('hidden');
    document.getElementById('errorText').textContent = message;
}

/**
 * Reset UI for new game
 */
function resetUI() {
    document.getElementById('questionCard').classList.add('hidden');
    document.getElementById('resultCard').classList.add('hidden');
    document.getElementById('errorCard').classList.add('hidden');
    document.getElementById('loadingSpinner').classList.remove('hidden');

    // Simulate loading time
    setTimeout(() => {
        document.getElementById('loadingSpinner').classList.add('hidden');
    }, 500);
}
