from ui import (
    display_welcome_message,
    get_quiz_topic,
    get_difficulty_level,
    get_number_of_questions,
    show_question,
    display_correct_feedback,
    display_incorrect_feedback,
    display_quiz_summary
)
import ui
from quiz_manager import QuizManager
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from openai_api import OpenAIQuizGenerator

console = Console()

def run_quiz():
    """Main function to run the quiz application."""
    ui.display_welcome_message()
    
    # Get quiz parameters from user
    topic = ui.get_quiz_topic()
    difficulty = ui.get_difficulty_level()
    num_questions = ui.get_number_of_questions()
    
    # Initialize quiz
    quiz_manager = QuizManager()
    quiz_manager.start_quiz(topic, difficulty, num_questions)
    
    current_question_num = 1
    while True:
        question = quiz_manager.get_next_question()
        if not question:
            break
            
        ui.show_question(
            question['question'],
            question['options'],
            current_question_num
        )
        
        # Get user's answer
        user_answer = ui.Prompt.ask(
            "[prompt]Your answer (A/B/C/D)[/]",
            choices=['A', 'B', 'C', 'D'],
            show_choices=False
        )
        
        # Check answer and provide feedback
        if quiz_manager.check_answer(question, user_answer):
            ui.display_correct_feedback()
        else:
            ui.display_incorrect_feedback(question['correct_answer'])
        
        current_question_num += 1
    
    # Save results to CSV and get the filename
    csv_filename = quiz_manager.save_quiz_results_to_csv()
    
    # Get and display final score
    final_score = quiz_manager.get_final_score()
    ui.display_quiz_summary(
        final_score['score'],
        final_score['total'],
        csv_filename
    )

if __name__ == "__main__":
    run_quiz() 