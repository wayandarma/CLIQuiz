# Comprehensive Project Instructions for the Quiz CLI Application

This guide provides detailed instructions broken down into main tasks and subtasks to help you build the Quiz CLI application effectively.

## Table of Contents

1. Project Setup
2. Basic Application Flow
3. User Interface (CLI)
4. OpenAI API Integration
5. Quiz Management
6. Gamification Features
7. Configuration and Extensibility
8. Testing
9. Dependencies and Documentation

## 1. Project Setup

### Main Tasks:

- Create the Project Structure
- Initialize Version Control
- Set Up Virtual Environment
- Install Dependencies

### Subtasks:

#### a. Create the Project Directory

- **Create Main Directory:**
  - Create a directory named `quiz-cli-app/`.
- **Create Subdirectories:**
  - Inside `quiz-cli-app/`, create the following directories:
    - `src/`
    - `data/`
    - `tests/`
- **Create Files:**
  - In `src/`, create:
    - `main.py`
    - `ui.py`
    - `openai_api.py`
    - `quiz_manager.py`
    - `gamification.py`
    - `utils.py`
  - In `data/`, create:
    - `config.json`
  - In `tests/`, create:
    - `test_ui.py`
    - `test_openai_api.py`
    - `test_quiz_manager.py`
    - `test_gamification.py`
  - At the root level, create:
    - `requirements.txt`
    - `README.md`
    - `LICENSE`

#### b. Initialize Version Control

- **Git Initialization:**
  - Navigate to `quiz-cli-app/` directory.
  - Run `git init` to initialize a Git repository.
- **Create .gitignore:**
  - Add common Python exclusions (e.g., `__pycache__/`, `.venv/`, `*.pyc`).
  - Ensure `config.json` is added to `.gitignore` to prevent exposing API keys.

#### c. Set Up Virtual Environment

- **Create Virtual Environment:**
  - Run `python -m venv .venv` to create a virtual environment.
- **Activate Virtual Environment:**
  - On Windows: `.\.venv\Scripts\activate`
  - On macOS/Linux: `source .venv/bin/activate`

#### d. Install Dependencies

- **Create requirements.txt:**
  - Add the following initial dependencies:
    ```
    openai
    rich
    pytest
    ```
- **Install Dependencies:**
  - Run `pip install -r requirements.txt`.

## 2. Basic Application Flow

### Main Tasks:

- Design the Application Workflow
- Implement Main Entry Point

### Subtasks:

#### a. Design the Application Workflow

- **Startup Sequence:**
  - Display a colorful welcome message.
  - Prompt user for quiz topic, difficulty level, and number of questions.
- **Quiz Generation:**
  - Use `openai_api.py` to fetch quiz questions based on user input.
- **Quiz Execution:**
  - Present questions and options one at a time.
  - Collect and validate user responses.
- **Gamification:**
  - Track user performance.
  - Provide immediate feedback and a summary at the end.

#### b. Implement Main Entry Point (main.py)

- **Structure main.py:**
  - Import necessary modules.
  - Implement the main function to control the application flow.
  - Use `if __name__ == "__main__":` to run the main function.

## 3. User Interface (CLI)

### Main Tasks:

- Implement CLI Components
- Enhance User Experience with Colors
- Handle User Inputs and Errors

### Subtasks:

#### a. Implement CLI Components (ui.py)

- **Welcome Message Function:**
  - Create `display_welcome_message()` to show an engaging welcome text.
- **Prompt Functions:**
  - `get_quiz_topic()`
  - `get_difficulty_level()`
  - `get_number_of_questions()`
- **Display Question Function:**
  - `show_question(question, options)`
- **Feedback Functions:**
  - `display_correct_feedback()`
  - `display_incorrect_feedback(correct_answer)`
- **Summary Function:**
  - `display_quiz_summary(score, total_questions)`

#### b. Enhance User Experience with Colors

- **Use rich Library:**
  - Import rich components like Console and Style.
- **Apply colors to:**
  - Questions
  - Options
  - Feedback messages
- **Establish Color Scheme:**
  - Correct answers: Green
  - Incorrect answers: Red
  - Prompts and inputs: Blue

#### c. Handle User Inputs and Errors (utils.py)

- **Input Validation Functions:**
  - `validate_topic_input(topic)`
  - `validate_difficulty_input(difficulty)`
  - `validate_number_input(number)`
- **Error Handling:**
  - Use try-except blocks to catch exceptions.
  - Provide meaningful error messages.

## 4. OpenAI API Integration

### Main Tasks:

- Configure API Access
- Implement API Interaction
- Handle API Responses and Errors

### Subtasks:

#### a. Configure API Access (openai_api.py)

- **Load API Key:**
  - Read `openai_api_key` from `config.json` securely.
- **Set Up OpenAI Client:**
  - Initialize OpenAI client with the API key.

#### b. Implement API Interaction

- **Generate Quiz Questions Function:**
  - `generate_quiz_questions(topic, difficulty, num_questions)`
  - Build the prompt using user inputs.
  - Send the prompt to OpenAI’s API.
- **Optimize API Calls:**
  - Set appropriate parameters (e.g., temperature, max_tokens).

#### c. Handle API Responses and Errors

- **Parse Responses:**
  - Extract questions and options from the API’s response.
  - Ensure consistency in the data format.
- **Error Handling:**
  - Implement retries with exponential backoff.
  - Handle specific exceptions (e.g., `openai.error.RateLimitError`).
- **Logging:**
  - Log API interactions and errors for debugging.

## 5. Quiz Management

### Main Tasks:

- Control Quiz Flow
- Randomize Options
- Validate User Answers

### Subtasks:

#### a. Control Quiz Flow (quiz_manager.py)

- **Start Quiz Function:**
  - `start_quiz()`
  - Coordinate the quiz sequence.
  - Integrate UI, OpenAI API, and Gamification modules.
- **Question Loop:**
  - Iterate over the list of questions.
  - Display each question and collect answers.

#### b. Randomize Options

- **Shuffle Options:**
  - Use Python’s `random.shuffle()` to randomize answer options.
  - Update the correct answer key after shuffling.

#### c. Validate User Answers

- **Answer Validation:**
  - Accept inputs like ‘A’, ‘B’, ‘C’, ‘D’ (case-insensitive).
  - Re-prompt user on invalid input.
- **Record Responses:**
  - Keep track of user answers for scoring.

## 6. Gamification Features

### Main Tasks:

- Implement Scoring System
- Provide Feedback
- Summarize Performance

### Subtasks:

#### a. Implement Scoring System (gamification.py)

- **Initialize Score Variables:**
  - `correct_answers = 0`
  - `incorrect_answers = 0`
- **Update Scores:**
  - Increment counters based on user responses.

#### b. Provide Feedback

- **Immediate Feedback:**
  - After each question, inform the user if they were correct.
  - Use encouraging messages like “Great job!” or “Don’t give up!”
- **Use Color Coding:**
  - Display feedback messages in green or red.

#### c. Summarize Performance

- **Calculate Results:**
  - `total_questions = correct_answers + incorrect_answers`
  - `percentage = (correct_answers / total_questions) * 100`
- **Display Summary:**
  - Show total correct and incorrect answers.
  - Provide a performance message based on the percentage.
- **Performance Messages:**
  - 90-100%: “Excellent work!”
  - 70-89%: “Great job!”
  - 50-69%: “Good effort!”
  - Below 50%: “Keep practicing!”

## 7. Configuration and Extensibility

### Main Tasks:

- Implement Configurable Settings
- Design for Future Features

### Subtasks:

#### a. Implement Configurable Settings (config.json)

- **Add Settings:**
  - Default difficulty level
  - Default number of questions
  - Available difficulty levels: `["easy", "medium", "hard"]`
- **Modify utils.py:**
  - Functions to read and write configurations.
  - Allow users to save preferences.

#### b. Design for Future Features

- **Extensible Question Formats:**
  - Structure code to support different question types.
  - Use classes or data structures that can be extended.
- **Modular Codebase:**
  - Keep functions and classes modular for reusability.
  - Use design patterns where appropriate.

## 8. Testing

### Main Tasks:

- Write Unit Tests
- Mock External Services
- Ensure Code Coverage

### Subtasks:

#### a. Write Unit Tests (tests/)

- **UI Tests (test_ui.py):**
  - Test display functions without actual printing.
  - Use mocking for input/output.
- **OpenAI API Tests (test_openai_api.py):**
  - Test API interaction functions.
  - Ensure proper handling of responses and errors.
- **Quiz Manager Tests (test_quiz_manager.py):**
  - Test the quiz flow logic.
  - Validate that correct answers update scores appropriately.
- **Gamification Tests (test_gamification.py):**
  - Test scoring calculations.
  - Verify performance messages are accurate.

#### b. Mock External Services

- **Mock OpenAI API:**
  - Use `unittest.mock` to simulate API responses.
  - Create sample responses for testing purposes.
- **Mock User Inputs:**
  - Simulate user inputs for different scenarios.

#### c. Ensure Code Coverage

- **Run Tests:**
  - Use `pytest` to run all tests.
  - Generate a coverage report.
- **Aim for High Coverage:**
  - Strive for at least 80% code coverage.
  - Identify and test untested code paths.

## 9. Dependencies and Documentation

### Main Tasks:

- Manage Dependencies
- Create Comprehensive Documentation

### Subtasks:

#### a. Manage Dependencies (requirements.txt)

- **Specify Versions:**
  - Pin versions to ensure compatibility.
    ```
    openai==X.X.X
    rich==X.X.X
    pytest==X.X.X
    ```
- **Update Dependencies:**
  - Regularly check for updates and test compatibility.

#### b. Create Comprehensive Documentation (README.md)

- **Project Overview:**
  - Describe the purpose and features of the application.
- **Installation Instructions:**
  - Step-by-step guide on setting up the environment.
- **Usage Guide:**
  - How to run the application.
  - Explanation of command-line arguments (if any).
- **Testing Instructions:**
  - How to run the test suite.
- **Contributing Guidelines:**
  - Instructions for contributing to the project.

#### c. Include License (LICENSE)

- **Choose a License:**
  - Select an appropriate license (e.g., MIT, Apache 2.0).
- **Add License File:**
  - Place the license text in `LICENSE` file at the root.

## Additional Tips

- **Version Control:**
  - Commit changes frequently with meaningful messages.
  - Use branching strategies for new features.
- **Code Quality:**
  - Follow PEP 8 style guidelines.
  - Use linters like flake8 or pylint.
- **Security:**
  - Never commit API keys or sensitive information.
  - Consider using environment variables for API keys.
- **Collaboration:**
  - Use pull requests for code reviews.
  - Document code thoroughly for team understanding.

By following these detailed instructions, you’ll create a robust, user-friendly Quiz CLI application that’s easy to maintain and extend. Happy coding!
