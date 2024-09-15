# AI Consumer Research Assistant

This Chainlit-based application serves as an AI consumer research assistant, leveraging OpenAI's GPT-4 model to provide interactive product recommendations and research. It includes features for user preference tracking, alert generation, and adaptive responses.

## Features

- **OpenAI GPT-4 Integration**: Utilizes OpenAI's GPT-4 model for intelligent responses and product recommendations.
- **User Record Management**: Maintains and updates a user record with preferences and alerts.
- **Adaptive Responses**: Uses conversation history and user records to provide context-aware responses.
- **Streamed Responses**: Delivers model responses in real-time as they are generated.
- **Configurable System Prompts**: Allows enabling/disabling of system prompts and class context.
- **Automatic Assessment**: Analyzes user messages to update preferences and generate alerts.

## Prerequisites

- Python 3.7+
- OpenAI API key

## Installation and Setup

1. **Clone the Repository**:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. **API Keys**: 
   - Copy the `.env.sample` file and rename it to `.env`
   - Replace the placeholder values with your actual OpenAI API key and endpoint

2. **System Prompts and Class Context**:
   - Adjust the `ENABLE_SYSTEM_PROMPT` and `ENABLE_CLASS_CONTEXT` flags in `app.py` as needed.

3. **Customize Prompts**:
   - Modify the prompt templates in the `prompts.py` file to suit your consumer research context.

## Running the Application

1. **Activate the Virtual Environment** (if not already activated):
   ```sh
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

2. **Run the Chainlit App**:
   ```sh
   chainlit run app.py -w
   ```

3. Open your browser and navigate to the URL displayed in the terminal.

## Usage

- Start a conversation with the AI consumer research assistant by typing a message.
- The application will process your input, update the user record, and provide contextual product recommendations and research.
- User records are automatically updated and stored in `user_record.md`.

## Key Components

- `app.py`: Main application file containing the Chainlit setup, message handling logic, and user assessment functionality.
- `prompts.py`: Contains prompt templates for system instructions and assessments.
- `user_record.py`: Handles reading, writing, formatting, and parsing of user records.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License.



