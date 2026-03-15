# Project Infrastructure: Davis Iron AI

## 1. Operating Environment
- **OS:** Windows 10/11
- **Python Version:** 3.10+
- **Terminal:** PowerShell 5.1+

## 2. Tech Stack
- **AI Engine:** Google Generative AI (Gemini 1.5/2.0 Flash)
- **Telegram Framework:** python-telegram-bot or aiogram
- **Automation Tools:**
    - `pyautogui`: Screen capture, mouse/keyboard control
    - `subprocess`: OS command execution
    - `webbrowser`: Browser interactions
- **Environment Management:** `python-dotenv`

## 3. Configuration & Ports
- **Port Range:** 8900-8999 (Internal services if any)
- **Secrets:** Handled via `.env` file (API keys, Whitelist IDs)

## 4. Project Structure (Proposed)
- `src/`: Core logic
- `config/`: Configuration settings
- `logs/`: Runtime logs
- `.agent/`: Agent intelligence & workflows

## 5. Security Protocols
- **Telegram Whitelist:** Hardcoded or env-based user ID verification.
- **Function Calling:** Strictly defined tools for Gemini to prevent arbitrary code execution.
