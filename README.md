# local-llm-prompt-basic
Basic LLM Interaction Covers Single-prompt API calls, Multi-turn conversation with messages, Streaming vs non-streaming

## Setting up Local LLM
### Setting up Ollama in Local
#### Steps for Windows
1. Install ollama
```
Download the ollama_setup.exe from here https://ollama.com/download
click on ollama_setup.exe and it starts the windows installer
once installed a GUI will open. Close this GUI.
From cli, verify ollama is installed by running below command
ollama --version 
```
2. Pull a mini model like phi3 which can run on windows setup with 8GB RAM, windows 11, with no GPU.
```
ollama pull phi3
```
3. Set env vars and start the ollama server
```
set OLLAMA_HOST=http:127.0.0.1:5000
ollama serve
```

## Running Examples
Navigate to ollama/ folder and run any file using the command
```
python single_node_streaming_prompt.py
```
