SEO & CITATION AGENT

An intelligent, automated agent designed to analyze, optimize, and manage SEO workflows.
This project leverages LLMs and specialized tools to provide actionable insights, keyword analysis, and content improvements.

🚀 Quick Start
To get the project up and running quickly:


Clone the repository:
Bash
git clone https://github.com/your-username/seo_agent.git
cd seo_agent-main
Run the setup script:

Windows: Double-click setup.bat or run it in CMD.
Manual: Install dependencies via pip install -r requirements.txt.

Configure environment variables:
Rename .env.example to .env and add your API keys (LLM providers, etc.).

Launch the application:
Run run_all.bat (Windows) or python run_all.py to start both the backend and frontend.

📁 Project Structure
The project is organized into several key modules to ensure scalability and ease of maintenance:

agent/: Core logic for the SEO agent, including decision-making and task execution (seo_agent.py).
backend/: FastAPI/Flask server handling API requests and data processing (main.py).
frontend/: Web interface for interacting with the agent (index.html).
tools/: Specialized SEO tools for keyword research and site auditing (seo_tools.py).
memory/: Implementation of "Hindsight Memory" to allow the agent to learn from past optimizations.
config/: Global settings and configuration management.
data/memory/: Persistent storage for analysis history, keywords, and improvement suggestions.

🛠 Features
LLM Switching: Dynamically switch between different Language Models (refer to LLM_SWITCHING_GUIDE.md).
Automated Audits: Analyze website SEO health using the integrated tools.
Learning Capability: Utilizes a memory system to track historical performance and refine future suggestions.
Cross-Platform Launchers: Pre-configured .bat and .py scripts for easy environment setup and execution.

🧪 Testing
To ensure everything is working correctly, you can run the provided test suites:
Agent Logic: python test_agent.py
LLM Integration: python test_llm_switching.py
