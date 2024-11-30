# Quiz CLI Application

An interactive command-line quiz application that generates questions using OpenAI's API.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.\.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `data/config.json.example` to `data/config.json` and add your OpenAI API key

## Usage

Run the application:

```bash
python src/main.py
```

## Testing

Run tests using pytest:

```bash
pytest tests/
```
