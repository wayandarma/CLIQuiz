from typing import Dict, List
import csv
from datetime import datetime
from pathlib import Path
from openai_api import OpenAIQuizGenerator

class QuizManager:
    def __init__(self):
        self.current_score = 0
        self.total_questions = 0
        self.questions = []
        self.quiz_generator = OpenAIQuizGenerator()
        self.question_history = []  # List to store question history
        self.topic = ""  # Store the quiz topic
        self.difficulty = ""  # Store the difficulty level

    def start_quiz(self, topic: str, difficulty: str, num_questions: int) -> None:
        """Initialize and start the quiz by fetching questions."""
        self.total_questions = num_questions
        self.topic = topic
        self.difficulty = difficulty
        try:
            # Fetch questions synchronously
            self.questions = self.quiz_generator.generate_quiz_questions_sync(
                topic, difficulty, num_questions
            )
            self.current_score = 0
            self.question_history = []  # Reset question history
        except Exception as e:
            print(f"Failed to start quiz: {e}")
            self.questions = []

    def get_next_question(self) -> Dict:
        """Get the next question from the quiz."""
        if self.questions:
            return self.questions.pop(0)
        return None

    def check_answer(self, question: Dict, user_answer: str) -> bool:
        """Check if the user's answer is correct and store the result."""
        is_correct = user_answer.upper() == question['correct_answer'].upper()
        if is_correct:
            self.current_score += 1
            
        # Store question and answer in history
        self.question_history.append({
            'question': question['question'],
            'user_answer': user_answer,
            'correct_answer': question['correct_answer'],
            'is_correct': is_correct
        })
        
        return is_correct

    def get_final_score(self) -> Dict:
        """Get the final score and statistics."""
        if self.total_questions == 0:
            percentage = 0
        else:
            percentage = (self.current_score / self.total_questions) * 100
        return {
            'score': self.current_score,
            'total': self.total_questions,
            'percentage': percentage
        } 

    def save_quiz_results_to_csv(self) -> str:
        """Save quiz results to a CSV file and return the filename."""
        # Create results directory if it doesn't exist
        results_dir = Path("quiz_results")
        results_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = results_dir / f"quiz_results_{timestamp}.csv"
        
        # Write results to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['topic', 'difficulty', 'question', 'user_answer', 
                         'correct_answer', 'is_correct']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for entry in self.question_history:
                writer.writerow({
                    'topic': self.topic,
                    'difficulty': self.difficulty,
                    'question': entry['question'],
                    'user_answer': entry['user_answer'],
                    'correct_answer': entry['correct_answer'],
                    'is_correct': entry['is_correct']
                })
        
        return str(filename)