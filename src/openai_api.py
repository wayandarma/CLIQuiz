import json
import time
import os
from typing import List, Dict
import openai
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

console = Console()

class OpenAIQuizGenerator:
    def __init__(self):
        """Initialize OpenAI client with API key from environment variables."""
        try:
            # Load environment variables
            load_dotenv()
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
                
            # Store the client instance as a class attribute
            self.client = openai.OpenAI(api_key=api_key)
            
        except Exception as e:
            console.print(f"Error initializing OpenAI client: {str(e)}", style="red")
            raise

    def _create_quiz_prompt(self, topic: str, difficulty: str, num_questions: int) -> str:
        """Create a prompt for the OpenAI API to generate quiz questions."""
        return f"""Generate {num_questions} multiple-choice questions about {topic} at a {difficulty} difficulty level.

IMPORTANT: You must respond with ONLY a JSON array. Do not include any other text, markdown, or explanations.

The response must be a valid JSON array containing objects with this exact structure:
[
    {{
        "question": "question text",
        "options": [
            "A) first option",
            "B) second option",
            "C) third option",
            "D) fourth option"
        ],
        "correct_answer": "A",
        "explanation": "explanation text"
    }}
]

Requirements:
1. Response must start with [ and end with ]
2. Each question must have exactly 4 options
3. Options must start with "A) ", "B) ", "C) ", "D) "
4. correct_answer must be exactly "A", "B", "C", or "D"
5. No additional text before or after the JSON array

Generate the questions now:"""

    def generate_quiz_questions_sync(
        self, 
        topic: str, 
        difficulty: str, 
        num_questions: int,
        max_retries: int = 3
    ) -> List[Dict]:
        """
        Generate quiz questions using OpenAI API with retry mechanism synchronously.
        """
        retry_count = 0
        base_delay = 1  # Base delay in seconds
        
        while retry_count < max_retries:
            try:
                prompt = self._create_quiz_prompt(topic, difficulty, num_questions)
                
                # Add loading animation
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Generating your quiz questions..."),
                    transient=True
                ) as progress:
                    progress.add_task("", total=None)
                    response = self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system", 
                                "content": """You are a quiz generator that MUST:
                                1. ALWAYS respond with valid JSON array
                                2. NEVER include any additional text or explanations outside the JSON
                                3. STRICTLY follow the specified format for questions
                                4. Ensure all correct_answer values are uppercase A, B, C, or D"""
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=2000,
                        n=1,
                    )

                # Updated response parsing
                content = response.choices[0].message.content
                
                # Try to clean the response if needed
                content = content.strip()
                if not content.startswith('['):
                    # Sometimes GPT might add markdown code blocks
                    if '```json' in content:
                        content = content.split('```json')[1].split('```')[0].strip()
                    elif '```' in content:
                        content = content.split('```')[1].strip()
                
                questions = json.loads(content)
                
                # Validate the response format
                self._validate_questions(questions)
                
                return questions

            except openai.RateLimitError:
                retry_count += 1
                if retry_count == max_retries:
                    console.print("Error: Rate limit exceeded. Please try again later.", style="red")
                    raise
                delay = base_delay * (2 ** (retry_count - 1))  # Exponential backoff
                console.print(f"Rate limit reached. Retrying in {delay} seconds...", style="yellow")
                time.sleep(delay)

            except openai.APIError as e:
                console.print(f"OpenAI API Error: {str(e)}", style="red")
                raise
                
            except json.JSONDecodeError as e:
                console.print(f"JSON Decode Error. Raw content: {content}", style="red")
                raise
                
            except Exception as e:
                console.print(f"Unexpected error: {str(e)}", style="red")
                raise

    def _validate_questions(self, questions: List[Dict]) -> None:
        """
        Validate the structure of generated questions.
        Raises ValueError if validation fails.
        """
        required_keys = {'question', 'options', 'correct_answer', 'explanation'}
        
        for q in questions:
            # Check if all required keys are present
            if not all(key in q for key in required_keys):
                raise ValueError("Invalid question format: missing required keys")
            
            # Validate options
            if not isinstance(q['options'], list) or len(q['options']) != 4:
                raise ValueError("Invalid options format: must be list of 4 options")
            
            # Validate correct answer
            if q['correct_answer'] not in ['A', 'B', 'C', 'D']:
                raise ValueError("Invalid correct answer: must be A, B, C, or D")