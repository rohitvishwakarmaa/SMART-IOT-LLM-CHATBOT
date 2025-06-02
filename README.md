# Smart IoT Chatbot with LLM and Microcontroller Integration

## How it works:
- Chat with natural language
- LLM parses command
- Backend sends action to ESP32/Arduino

## Run Instructions
1. Set your OpenAI key:
```bash
export OPENAI_API_KEY=your-key-here
```
2. Run Flask app:
```bash
cd backend
python app.py
```
3. Access via `http://127.0.0.1:5000`

## MCB Endpoint:
Ensure your microcontroller (ESP32) has a REST endpoint at `http://192.168.4.1/command`.
