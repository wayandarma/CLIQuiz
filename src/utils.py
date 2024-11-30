def validate_input(prompt: str, valid_options: list = None) -> str:
    """
    Validate user input against a list of valid options.
    """
    while True:
        user_input = input(prompt).strip()
        if valid_options is None or user_input in valid_options:
            return user_input
        print(f"Invalid input. Please choose from: {', '.join(valid_options)}") 

def validate_topic_input(topic: str) -> bool:
    """
    Validate the quiz topic input.
    Returns True if valid, False otherwise.
    """
    return bool(topic and topic.strip())

def validate_difficulty_input(difficulty: str) -> bool:
    """
    Validate the difficulty level input.
    Returns True if valid, False otherwise.
    """
    valid_levels = ['easy', 'medium', 'hard']
    return difficulty.lower() in valid_levels

def validate_number_input(number: str) -> bool:
    """
    Validate the number of questions input.
    Returns True if valid, False otherwise.
    """
    try:
        num = int(number)
        return 1 <= num <= 10
    except ValueError:
        return False 