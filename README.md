# AI Chatbot

<p align="center">
  <strong>AI-powered task router chatbot with automated agent classification and project management</strong>
</p>

<p align="center">
  <a href="#features"><strong>Features</strong></a> &middot;
  <a href="#installation"><strong>Installation</strong></a> &middot;
  <a href="#usage"><strong>Usage</strong></a> &middot;
  <a href="#api-reference"><strong>API Reference</strong></a> &middot;
  <a href="#project-structure"><strong>Project Structure</strong></a>
</p>

---

## Overview

AI Chatbot is a conversational interface that lets you delegate work to your AI agent team using plain English. Instead of manually creating tasks and assigning agents, you describe what you need — the chatbot analyzes your request, classifies the intent, picks the best agent, and creates a tracked issue automatically.

**Example:** Type *"Build a dark mode toggle for the dashboard"* → the router picks the Frontend Agent → issue `TEC-42` is created and assigned.

The chatbot is designed to work as a:

- Standalone chat UI
- Embedded widget inside a project dashboard
- Programmable API for custom integrations

---

## Features

| Feature | Description |
|---------|-------------|
| **Natural Language Routing** | Describe tasks in plain English. No forms or dropdowns required. |
| **Automated Agent Classification** | Intent-based classification matches requests to the most suitable agent by role and skills. |
| **Smart Agent Matching** | Scores agents by skill overlap, current workload, and past success. |
| **Instant Previews** | Special commands generate and preview results immediately. |
| **Interactive Agent Selection** | Review the suggested agent and choose a different one before confirming. |
| **Real-Time Status Polling** | Watch issue status update live as agents pick up and complete work. |
| **Quick Action Buttons** | One-click shortcuts for common tasks like bug fixes, deployments, design, analytics, and marketing. |
| **Work Product Display** | Completed tasks show deliverables, plans, and outputs directly in the chat. |

---

## Installation

### Prerequisites

- [Node.js](https://nodejs.org/) 18 or higher
- [pnpm](https://pnpm.io/) (recommended) or npm
- A running [Paperclip](https://paperclip.ing/) server instance (for agent orchestration)

### Clone the repository

```bash
git clone https://github.com/Parth-4518/AI-chatbot.git
cd AI-chatbot
```

### Install dependencies

```bash
pnpm install
```

### Configure environment variables

Create a `.env` file in the project root:

```env
# Paperclip server URL
PAPERCLIP_API_URL=http://localhost:3100/api

# Your company ID in Paperclip
PAPERCLIP_COMPANY_ID=a99fd059-c16b-4cdf-a4ca-0e78a04e42b8

# Optional: API key if your Paperclip instance requires authentication
PAPERCLIP_API_KEY=your_api_key_here

# Server port for the chatbot UI/API
PORT=3000
```

### Start the development server

```bash
pnpm dev
```

The chatbot UI will be available at `http://localhost:3000`.

---

## Usage

### Standalone Chat UI

Open the chat UI in your browser:

```bash
open http://localhost:3000
```

Type a request such as:

- `"Create a login page for the dashboard"`
- `"Fix the crash on the signup form"`
- `"Show me the status of TEC-42"`
- `"Assign the landing page redesign to the Design Agent"`

### Embedded Widget

To embed the chatbot inside another dashboard, include the widget script:

```html
<div id="ai-chatbot-widget"></div>
<script src="http://localhost:3000/widget.js" data-company="a99fd059-c16b-4cdf-a4ca-0e78a04e42b8"></script>
```

### API Direct Usage

You can call the router API directly from any client:

#### Route a task (analysis only)

```bash
curl -X POST http://localhost:3000/api/chat/route \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Build a dark mode toggle for the dashboard",
    "companyId": "a99fd059-c16b-4cdf-a4ca-0e78a04e42b8"
  }'
```

#### Route and create an issue in one step

```bash
curl -X POST http://localhost:3000/api/chat/route-and-create \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Fix the crash on signup",
    "companyId": "a99fd059-c16b-4cdf-a4ca-0e78a04e42b8"
  }'
```

#### Create an issue with a specific agent

```bash
curl -X POST http://localhost:3000/api/chat/create \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Design a new landing page",
    "companyId": "a99fd059-c16b-4cdf-a4ca-0e78a04e42b8",
    "agentId": "<agent-uuid>"
  }'
```

#### List available agents

```bash
curl "http://localhost:3000/api/chat/agents?companyId=a99fd059-c16b-4cdf-a4ca-0e78a04e42b8"
```

---

## API Reference

### `POST /api/chat/route`

Analyze a prompt and return routing information without creating an issue.

**Request body:**

```json
{
  "prompt": "Build a dark mode toggle for the dashboard",
  "companyId": "a99fd059-c16b-4cdf-a4ca-0e78a04e42b8",
  "context": {
    "projectId": "optional-project-uuid",
    "priority": "high"
  }
}
```

**Response:**

```json
{
  "intent": "create_task",
  "title": "Build a dark mode toggle for the dashboard",
  "description": "Add a dark mode toggle to the project dashboard UI.",
  "priority": "high",
  "suggestedAgent": {
    "id": "<agent-uuid>",
    "name": "Frontend Agent",
    "confidence": 0.92
  }
}
```

### `POST /api/chat/route-and-create`

Analyze a prompt and immediately create a tracked issue.

**Request body:**

```json
{
  "prompt": "Fix the crash on signup",
  "companyId": "a99fd059-c16b-4cdf-a4ca-0e78a04e42b8"
}
```

**Response:**

```json
{
  "issueId": "<issue-uuid>",
  "identifier": "TEC-42",
  "title": "Fix the crash on signup",
  "status": "backlog",
  "assigneeAgentId": "<agent-uuid>"
}
```

### `POST /api/chat/create`

Create an issue using a specific agent.

**Request body:**

```json
{
  "prompt": "Design a new landing page",
  "companyId": "a99fd059-c16b-4cdf-a4ca-0e78a04e42b8",
  "agentId": "<agent-uuid>"
}
```

### `GET /api/chat/agents`

List agents available for a company.

**Query parameters:**

- `companyId` (required): The company UUID.

---

## Project Structure

```
AI-chatbot/
├── README.md                 # This file
├── package.json              # Project dependencies and scripts
├── .env.example              # Example environment variables
├── src/
│   ├── server.ts             # Express server entry point
│   ├── routes/
│   │   └── chat.ts           # Chat API routes
│   ├── services/
│   │   ├── intent-classifier.ts
│   │   ├── agent-matcher.ts
│   │   └── issue-generator.ts
│   └── types/
│       └── index.ts
├── ui/
│   ├── index.html            # Standalone chat UI
│   └── widget.js             # Embeddable widget script
└── tests/
    └── chat.router.test.ts
```

---

## Development

### Run tests

```bash
pnpm test
```

### Build for production

```bash
pnpm build
```

### Start production server

```bash
pnpm start
```

---

## Roadmap

- [ ] Multi-turn conversation context
- [ ] LLM-based intent classification
- [ ] Voice and Slack integrations
- [ ] Agent performance analytics
- [ ] Mobile app companion

---

## Contributing

Contributions are welcome. Please open an issue or pull request on GitHub.

---

## License

[MIT](LICENSE)
