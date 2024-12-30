# 🚀 Coding Assistant

## 📝 Overview

The **Coding Assistant** application is a powerful tool built with Streamlit, leveraging advanced AI models to provide coding solutions, insights, and suggestions. By integrating Stack Overflow results, it offers contextual and optimized solutions, making it an indispensable tool for developers.

---

## 🌟 Features

- **💬 Natural Language Query Support**: Ask coding-related questions in plain English and receive detailed solutions.
- **🔗 Integration with Stack Overflow**: Fetch relevant Stack Overflow answers to provide additional context and optimize solutions.
- **🤖 AI-Powered Code Suggestions**: Utilizes SambaNova's **Qwen2.5-Coder-32B-Instruct** model, which outperforms Claude and GPT in various coding benchmarks.
- **📜 Conversation Context**: Maintains conversation history to enhance response relevance based on past interactions.
- **🔒 Customizable Environment**: Manages secure configurations using `.env` for API keys.
- **⚡ Responsive UI**: Built with Streamlit, offering an intuitive interface with real-time updates and advanced features.

---

## 🛠️ Installation

### Prerequisites
- 🐍 Python 3.11 or later
- 📦 Pip or pipenv for package management
- 🔑 A valid API key for OpenAI and SambaNova
- 🗂️ Environment variables stored in a `.env` file

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Ahaskar04/codex
   cd https://github.com/Ahaskar04/codex
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create and configure your `.env` file:
   ```bash
   nano .env
   ```
   Add the following:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SAMBANOVA_API_KEY=your_sambanova_api_key
   ```

4. Optional: Export API keys in your terminal session:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export SAMBANOVA_API_KEY=your_sambanova_api_key
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## 🔧 Customization for phi.utils Library

If you're working with the **phi.utils** library, follow these steps to update its code:

1. Open the required file in a terminal:
   ```bash
   nano /Users/ahaskarkashyap/.pyenv/versions/3.11.6/lib/python3.11/site-packages/phi/utils/__init__.py
   ```

2. Add the following code:
   ```python
   def identity(x):
       return x

   NO_VALUE = object()

   def state_identity(state):
       return state

   import inspect

   def get_method_sig(func):
       """
       Retrieve the signature of a function or method.
       """
       try:
           return str(inspect.signature(func))
       except ValueError:
           return "No signature available"
   ```

3. Save and exit the editor.

---

## 🏆 Why SambaNova's Qwen Model?

The **Qwen2.5-Coder-32B-Instruct** outperforms competing AI models like Claude and GPT in several coding benchmarks. Below are some highlights:

| 📊 Benchmark         | ⚡ Qwen2.5 Coder | 🤖 GPT-4.0 | 🤖 Claude 3.5 |
|--------------------|---------------|---------|------------|
| HumanEval         | **92.7**      | 92.1    | 92.1       |
| MBPP              | **90.2**      | 86.8    | 91.0       |
| CRUXEval-O (CoT)  | **83.4**      | 89.2    | 87.2       |
| Spider            | **85.1**      | 79.8    | 74.6       |
| BigCodeBench      | **38.3**      | 37.6    | 34.5       |

These benchmarks demonstrate the superior problem-solving and coding generation capabilities of SambaNova’s model.

---

## 💡 How It Works

1. **🖊️ User Input**:  
   Enter a coding-related question or code snippet.

2. **🔗 Stack Overflow Integration**:  
   Fetches relevant Stack Overflow answers for context.

3. **🤖 AI Response Generation**:  
   Processes the query, conversation history, and Stack Overflow context using SambaNova’s model.

4. **📋 Display Results**:  
   The application displays AI-generated responses alongside relevant Stack Overflow answers.

---

## 🎯 Advantages

- **🔍 Contextual Optimization**: Integrates Stack Overflow solutions to enhance code suggestions.
- **⚙️ Cutting-Edge AI**: Leverages SambaNova’s superior model for high accuracy and performance.
- **🖥️ User-Friendly Design**: Offers a seamless and intuitive user interface.

---

## 🤝 Contribution

We welcome contributions! Feel free to:
- Submit issues
- Open pull requests for bug fixes or new features

For major changes, please open an issue first to discuss your ideas.

---

Enjoy coding smarter and faster with the Coding Assistant! 🎉
