# Kids Math Game 🧮

A fun, interactive math learning game for kids! Start with a simple Python CLI game, now transformed into a production-ready web application with comprehensive testing and deployment infrastructure.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## Features

✨ **Interactive Math Questions** - Dynamic math problems with multiple choice answers  
🎯 **Instant Feedback** - Know immediately if you're correct or need to try again  
💡 **Smart Hints** - Get helpful hints to guide you to the right answer  
📱 **Responsive Design** - Works on desktop, tablet, and mobile devices  
🧪 **Fully Tested** - Comprehensive unit and integration tests  
🚀 **Production Ready** - Docker containerization, CI/CD pipeline, and environment management  
♻️ **Reusable API** - REST API for easy integration into other platforms  

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.11, Flask 2.3 |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Testing** | pytest, pytest-flask |
| **Deployment** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Package Manager** | pip |

## Quick Start

### Prerequisites

- Python 3.9+
- Git
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kids_math_game.git
   cd kids_math_game
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env as needed (defaults work for development)
   ```

5. **Run backend server**
   ```bash
   python -m flask --app backend.app run
   # Server will run on http://localhost:5000
   ```

6. **Serve frontend** (in another terminal)
   ```bash
   cd frontend
   python -m http.server 3000
   # Frontend will be available at http://localhost:3000
   ```

7. **Open in browser**
   Navigate to `http://localhost:3000`

### Using Docker Compose (Recommended)

```bash
docker-compose up --build
# Backend: http://localhost:5000
# Frontend: http://localhost:3000
```

## Project Structure

```
kids_math_game/
├── backend/                      # Python backend
│   ├── __init__.py
│   ├── game_engine.py           # Core game logic
│   ├── app.py                   # Flask application
│   └── config.py                # Configuration management
├── frontend/                     # Web frontend
│   ├── index.html               # Main page
│   ├── game.js                  # Game logic & API calls
│   └── styles.css               # Styling
├── tests/                        # Test suite
│   ├── test_game_engine.py      # Unit tests
│   └── test_api.py              # Integration tests
├── .github/workflows/           # CI/CD pipeline
│   └── ci-cd.yml
├── Dockerfile                    # Container setup
├── docker-compose.yml           # Multi-container setup
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Development

### Running Tests

**Run all tests:**
```bash
pytest tests/ -v
```

**Run only game engine tests:**
```bash
pytest tests/test_game_engine.py -v
```

**Run only API tests:**
```bash
pytest tests/test_api.py -v
```

**Run with coverage:**
```bash
pip install pytest-cov
pytest tests/ --cov=backend --cov-report=html
```

### Code Structure

#### Backend: `backend/game_engine.py`

Core game logic with reusable functions:

- `generate_game()` - Creates a new question
- `validate_answer(game_data, answer_index)` - Validates an answer
- `generate_hint(game_data)` - Returns helpful hint
- `format_question(game_data)` - Formats question text

#### Backend: `backend/app.py`

Flask REST API with endpoints:

- `POST /api/v1/game/start` - Start new game
- `POST /api/v1/game/validate` - Validate answer
- `GET /api/v1/game/hint` - Get hint for current game
- `GET /health` - Health check

#### Frontend: `frontend/game.js`

Main game controller with functions:

- `startNewGame()` - Load new question
- `selectAnswer(answerIndex)` - Process answer selection
- `getHint()` - Request hint from API
- `showCorrectResult()` / `showIncorrectResult()` - Display results

## Testing

### Test Coverage

- **Unit Tests**: Game engine logic, data validation
- **Integration Tests**: API endpoints, error handling, full game flow
- **Test Count**: 50+ tests covering all major functionality

### Running Tests with Details

```bash
pytest tests/ -v --tb=short
```

### Continuous Integration

Tests run automatically on:
- Push to `main` branch
- Push to `develop` branch
- Pull requests to `main` or `develop`

Tests run on Python 3.9, 3.10, and 3.11.

## Deployment

### Three Deployment Tiers

#### Development (Local)
```bash
FLASK_ENV=development python -m flask run
```

#### Staging (Testing in Production-like Environment)
```bash
FLASK_ENV=staging docker-compose up
```

#### Production
```bash
FLASK_ENV=production gunicorn --bind 0.0.0.0:5000 backend.app:app
```

### Docker Deployment

**Build image:**
```bash
docker build -t kids-math-game:latest .
```

**Run container:**
```bash
docker run -p 5000:5000 -e FLASK_ENV=production kids-math-game:latest
```

### Deployment Checklist

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] No linting errors (`flake8 backend`)
- [ ] `.env` file is configured for target environment
- [ ] Docker image builds successfully
- [ ] Health check endpoint responds: `curl http://localhost:5000/health`
- [ ] Frontend can access backend API (check CORS settings)
- [ ] SSL/HTTPS configured for production

## API Documentation

### Base URL
- Development: `http://localhost:5000/api/v1`
- Production: `https://your-domain.com/api/v1`

### Endpoints

#### 1. Start Game
**Request:**
```bash
POST /game/start
Content-Type: application/json
```

**Response:**
```json
{
  "success": true,
  "game_id": "123456",
  "question": "Adam bought 2 Apples(s) and 3 Banana(s)...",
  "options": [10, 12, 13, 15],
  "metadata": {
    "fruit1": "Apple",
    "fruit2": "Banana",
    "count1": 2,
    "count2": 3
  }
}
```

#### 2. Validate Answer
**Request:**
```bash
POST /game/validate
Content-Type: application/json

{
  "game_id": "123456",
  "answer_index": 2
}
```

**Response (Correct):**
```json
{
  "success": true,
  "is_correct": true,
  "correct_answer": 13,
  "selected_answer": 13
}
```

**Response (Incorrect):**
```json
{
  "success": true,
  "is_correct": false,
  "correct_answer": 13,
  "selected_answer": 10,
  "hint": "First calculate:\n2 × 2 = 4\nand\n3 × 3 = 9\nThen add the results together."
}
```

#### 3. Get Hint
**Request:**
```bash
GET /game/hint?game_id=123456
```

**Response:**
```json
{
  "success": true,
  "hint": "First calculate:\n2 × 2 = 4\nand\n3 × 3 = 9\nThen add the results together."
}
```

### Error Responses

**400 Bad Request:**
```json
{
  "success": false,
  "error": "game_id and answer_index required"
}
```

**404 Not Found:**
```json
{
  "success": false,
  "error": "Game not found. Start a new game first."
}
```

**500 Internal Server Error:**
```json
{
  "success": false,
  "error": "Internal server error"
}
```

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Write/update tests** for your changes
5. **Run tests** to ensure everything passes (`pytest tests/ -v`)
6. **Commit changes** (`git commit -m 'Add amazing feature'`)
7. **Push to branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines for Python
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.9+)
- Verify dependencies: `pip install -r requirements.txt`
- Check if port 5000 is available: `lsof -i :5000`

### Frontend won't load
- Verify backend is running: `curl http://localhost:5000/health`
- Check CORS configuration in `.env`
- Clear browser cache (Ctrl+Shift+Del or Cmd+Shift+Del)
- Check browser console for errors (F12)

### Tests failing
- Ensure backend Python dependencies are installed
- Run from project root directory
- Check test database isn't locked: `rm -f test.db`
- Verify Flask app is not running in another terminal

### Docker issues
- Rebuild image: `docker-compose build --no-cache`
- Remove old containers: `docker-compose down -v`
- Check Docker daemon is running

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for similar problems
- Include error messages and reproduction steps

---

**Happy Learning! 🎓✨**
