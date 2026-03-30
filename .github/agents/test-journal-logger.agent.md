---
name: test-journal-logger
description: This agent logs every interaction with Copilot into a `JOURNAL.md` file in reverse-chronological order. Each entry includes the prompt, response, and timestamp. The agent ensures that all interactions are documented for future reference and learning.
argument-hint: "After each interaction with Copilot, log the prompt, response, and timestamp in `JOURNAL.md`."
tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo'] # specify the tools this agent can use. If not set, all enabled tools are allowed.
---
Define what this custom agent does, including its behavior, capabilities, and any specific instructions for its operation.