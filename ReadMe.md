# AI Editor

A local-first AI chat editor with persistent memory and multi-model switching.

Run LLMs locally, keep your data private, switch models dynamically, and resume conversations at any time.

---

## Version
Current version: 0.1.0-dev

This is an early development build. Expect frequent changes and experimental features.

---

## Overview

Most AI tools today:

- Depend on cloud APIs  
- Do not reliably persist conversations  
- Restrict users to a single model per session  

AI Editor explores an alternative approach:

A local-first AI workspace where users maintain full control over models, data, and workflow.

---

## Features

### Local AI (No Cloud Required)
Run language models locally using Ollama. All data remains on your machine.

### Persistent Conversations
- Chats are stored as JSON  
- Resume conversations at any time  
- Maintain context across sessions  

### Multi-Model Switching
- Switch models during a conversation  
- Compare outputs seamlessly  
- Experiment without restarting sessions  

### Multi-Chat Management
- Create and manage multiple chats  
- Continue previous sessions  
- Automatically generated chat titles  

### Desktop Interface
- Built with PySide6  
- Lightweight and minimal design  
- Focused, distraction-free experience  

---

## Preview

- Chat interface  
- Model switching  
- Chat history panel  

---

## Tech Stack

- Python  
- PySide6 (UI framework)  
- Ollama (local LLM runtime)  
- JSON-based storage  

---

## Current Status

**Version:** 0.1.0-dev  

This is an early development release:

- Rapid changes are expected  
- Some features are experimental  
- Feedback is highly encouraged  

---

## Roadmap

Planned improvements include:

- Retrieval-Augmented Generation (RAG) for long-term memory  
- Enhanced context handling for extended conversations  
- Improved chat organization and search  
- Code-focused workflows (editing, execution, iteration)  

---

## License
AI Editor is licensed under the GNU General Public License v3.0 (GPLv3).
See the [LICENSE](LICENSE) file for details.

