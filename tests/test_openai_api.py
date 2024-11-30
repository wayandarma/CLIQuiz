import pytest
import json
from unittest.mock import patch, MagicMock
from src.openai_api import OpenAIQuizGenerator

@pytest.fixture
def quiz_generator():
    with patch('builtins.open', create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = '''
        {"openai_api_key": "test-key"}
        '''
        return OpenAIQuizGenerator()

def test_create_quiz_prompt(quiz_generator):
    prompt = quiz_generator._create_quiz_prompt("Python", "medium", 3)
    assert "Python" in prompt
    assert "medium" in prompt
    assert "3" in prompt

@pytest.mark.asyncio
async def test_generate_quiz_questions_success(quiz_generator):
    mock_response = {
        'choices': [{
            'message': {
                'content': json.dumps([{
                    "question": "Test question?",
                    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                    "correct_answer": "A",
                    "explanation": "Test explanation"
                }])
            }
        }]
    }
    
    with patch('openai.ChatCompletion.acreate', return_value=MagicMock(**mock_response)):
        questions = await quiz_generator.generate_quiz_questions("Python", "easy", 1)
        assert len(questions) == 1
        assert "question" in questions[0]
        assert "options" in questions[0]
        assert "correct_answer" in questions[0]

@pytest.mark.asyncio
async def test_generate_quiz_questions_rate_limit(quiz_generator):
    with patch('openai.ChatCompletion.acreate') as mock_create:
        mock_create.side_effect = openai.error.RateLimitError("Rate limit exceeded")
        
        with pytest.raises(openai.error.RateLimitError):
            await quiz_generator.generate_quiz_questions("Python", "easy", 1)

def test_validate_questions_valid(quiz_generator):
    valid_questions = [{
        "question": "Test question?",
        "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
        "correct_answer": "A",
        "explanation": "Test explanation"
    }]
    
    # Should not raise any exception
    quiz_generator._validate_questions(valid_questions)

def test_validate_questions_invalid(quiz_generator):
    invalid_questions = [{
        "question": "Test question?",
        "options": ["A) option1", "B) option2"],  # Invalid: not 4 options
        "correct_answer": "A",
        "explanation": "Test explanation"
    }]
    
    with pytest.raises(ValueError):
        quiz_generator._validate_questions(invalid_questions)