from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt
from rich.panel import Panel

# Initialize Rich console with custom theme
custom_theme = Theme({
    'info': 'cyan',
    'warning': 'yellow',
    'error': 'red',
    'success': 'green',
    'prompt': 'blue'
})

console = Console(theme=custom_theme)

def display_welcome_message():
    """Display a welcoming message when the application starts."""
    welcome_text = """
    🎯 Welcome to the Quiz CLI! 🎯
    Test your knowledge with custom quizzes on any topic.
    """
    console.print(Panel(welcome_text, title="Quiz CLI", style="info"))

def get_quiz_topic() -> str:
    """Prompt user for quiz topic."""
    while True:
        topic = Prompt.ask("[prompt]Enter the topic for your quiz[/]")
        if topic.strip():  # Basic validation - non-empty string
            return topic.strip()
        console.print("Topic cannot be empty!", style="error")

def get_difficulty_level() -> str:
    """Prompt user for difficulty level."""
    valid_levels = ['easy', 'medium', 'hard']
    while True:
        difficulty = Prompt.ask(
            "[prompt]Choose difficulty level[/]",
            choices=valid_levels,
            default="medium"
        ).lower()
        if difficulty in valid_levels:
            return difficulty
        console.print(f"Please choose from: {', '.join(valid_levels)}", style="error")

def get_number_of_questions() -> int:
    """Prompt user for number of questions."""
    while True:
        try:
            num = int(Prompt.ask("[prompt]How many questions would you like? (1-10)[/]"))
            if 1 <= num <= 10:
                return num
            console.print("Please enter a number between 1 and 10", style="error")
        except ValueError:
            console.print("Please enter a valid number", style="error")

def show_question(question: str, options: list, question_number: int):
    """Display a question with its options."""
    console.print(f"\nQuestion {question_number}:", style="info")
    console.print(Panel(question, style="prompt"))
    
    for idx, option in enumerate(options):
        letter = chr(65 + idx)  # Convert 0,1,2,3 to A,B,C,D
        console.print(f"{letter}. {option}")

def display_correct_feedback():
    """Display feedback for correct answer."""
    console.print("✅ Correct! Well done!", style="success")

def display_incorrect_feedback(correct_answer: str):
    """Display feedback for incorrect answer."""
    console.print(f"❌ Sorry, that's incorrect. The correct answer was: {correct_answer}", style="error")

def display_quiz_summary(score: int, total_questions: int, csv_filename: str = None):
    """Display the final quiz summary."""
    if total_questions == 0:
        percentage = 0
    else:
        percentage = (score / total_questions) * 100

    # Determine performance message
    if percentage >= 90:
        message = "🌟 Excellent work!"
    elif percentage >= 70:
        message = "🎉 Great job!"
    elif percentage >= 50:
        message = "👍 Good effort!"
    else:
        message = "💪 Keep practicing!"

    summary = f"""
Quiz Complete!
Score: {score}/{total_questions}
Percentage: {percentage:.1f}%
{message}"""

    if csv_filename:
        summary += f"\n\nQuiz results saved to: {csv_filename}"

    console.print(Panel(summary, title="Quiz Summary", style="info")) 