# AI Chatbot

<p align="center">
  <strong>AI-powered task router chatbot with automated agent classification and project management</strong>
</p>

<p align="center">
  <a href="#-vision"><strong>Vision</strong></a> &middot;
  <a href="#-features"><strong>Features</strong></a> &middot;
  <a href="#-getting-started"><strong>Getting Started</strong></a> &middot;
  <a href="#-architecture"><strong>Architecture</strong></a> &middot;
  <a href="#-api-reference"><strong>API Reference</strong></a> &middot;
  <a href="#-deployment"><strong>Deployment</strong></a> &middot;
  <a href="#-troubleshooting"><strong>Troubleshooting</strong></a> &middot;
  <a href="#-roadmap"><strong>Roadmap</strong></a>
</p>

---

## Vision

AI Chatbot eliminates the friction between "I need this done" and "someone is working on it." Instead of manually filing tickets, picking assignees, and writing specs, you describe what you need in plain English. The chatbot analyzes your request, classifies intent, matches the best agent, and creates a tracked issue automatically.

**Example:** Type *"Build a dark mode toggle for the dashboard"* → router picks the Frontend Agent → issue `TEC-42` is created and assigned → you watch progress live in chat.

### Who is this for?

| User | Use Case |
|------|----------|
| **Founders / PMs** | Delegate tasks to an AI agent team without context switching |
| **Engineering Leads** | Route bugs, features, and infra work to the right agent instantly |
| **Ops Teams** | Automate recurring requests via chat or embedded widget |
| **Integrators** | Build custom workflows on top of the routing API |

### Why it matters

- **Speed:** No forms, no dropdowns, no manual triage — just type and go.
- **Accuracy:** Intent classification + skill-based agent matching reduces mis-assignment.
- **Visibility:** Real-time status polling shows exactly what is happening.
- **Flexibility:** Works standalone, embedded, or headless via API.

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

## Getting Started

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Node.js | >= 18 | LTS recommended |
| pnpm | >= 8 | Faster than npm; `corepack enable` to auto-install |
| Paperclip server | latest | [paperclip.ing](https://paperclip.ing/) or self-hosted |

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Parth-4518/AI-chatbot.git
cd AI-chatbot

# 2. Install dependencies
pnpm install

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your Paperclip credentials (see table below)

# 4. Start the development server
pnpm dev
```

The chatbot UI will be available at `http://localhost:3000`.

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PAPERCLIP_API_URL` | Yes | — | Paperclip server base URL (e.g. `http://localhost:3100/api`) |
| `PAPERCLIP_COMPANY_ID` | Yes | — | Your company UUID in Paperclip |
| `PAPERCLIP_API_KEY` | No | — | API key if Paperclip requires authentication |
| `PORT` | No | `3000` | Port for the chatbot UI/API server |
| `NODE_ENV` | No | `development` | Set to `production` for optimized builds |

### Quick Start Example

```bash
# Route a task via API
curl -X POST http://localhost:3000/api/chat/route-and-create \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Build a dark mode toggle for the dashboard",
    "companyId": "a99fd059-c16b-4cdf-a4ca-0e78a04e42b8"
  }'
```

Response:

```json
{
  "issueId": "<uuid>",
  "identifier": "TEC-42",
  "title": "Build a dark mode toggle for the dashboard",
  "status": "backlog",
  "assigneeAgentId": "<agent-uuid>"
}
```

---

## Architecture

### High-Level Flow

```
User Input
    |
    v
+---------------+     +------------------+     +----------------+
| Intent        | --> | Agent Matcher    | --> | Issue Generator|
| Classifier    |     | (skills, load)   |     | (Paperclip API)|
+---------------+     +------------------+     +----------------+
    |                           |                       |
    v                           v                       v
 intent label              ranked agents            tracked issue
 confidence                confidence score         with assignee
```

### Component Overview

| Component | Responsibility |
|-----------|----------------|
| **Intent Classifier** | Parses natural language into structured intent (`create_task`, `query_status`, `preview`, etc.). Uses keyword + pattern matching today; LLM-based classification planned. |
| **Agent Matcher** | Queries available agents from Paperclip, scores each by skill overlap, current workload, and historical success rate. Returns top-3 ranked candidates. |
| **Issue Generator** | Creates the issue via Paperclip REST API, assigns the matched agent, and returns the issue identifier. |
| **Status Poller** | Polls Paperclip for issue status updates and streams them back to the chat UI. |
| **Chat UI** | React-based interface for standalone or embedded use. Handles message history, agent cards, and live status. |

### Data Flow

1. User types a message in the chat UI.
2. Frontend POSTs to `/api/chat/route` (analysis) or `/api/chat/route-and-create` (action).
3. Server runs intent classification → agent matching → issue creation.
4. Server returns the issue details to the UI.
5. UI begins polling `/api/issues/:id` for status updates.
6. When the agent completes the task, the UI displays the deliverable.

---

## API Reference

### `POST /api/chat/route`

Analyze a prompt and return routing information **without** creating an issue.

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

Create an issue using a **specific** agent.

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

**Response:**

```json
[
  {
    "id": "<agent-uuid>",
    "name": "Frontend Agent",
    "role": "frontend",
    "skills": ["react", "css", "ui-design"]
  }
]
```

---

## Deployment

### Standalone Server

```bash
# Build for production
pnpm build

# Start production server
pnpm start
```

### Docker

```dockerfile
# Dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build
EXPOSE 3000
CMD ["pnpm", "start"]
```

Build and run:

```bash
docker build -t ai-chatbot .
docker run -p 3000:3000 --env-file .env ai-chatbot
```

### Embedded Widget

To embed the chatbot inside another dashboard, include the widget script:

```html
<div id="ai-chatbot-widget"></div>
<script src="http://localhost:3000/widget.js" data-company="a99fd059-c16b-4cdf-a4ca-0e78a04e42b8"></script>
```

---

## Troubleshooting

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ECONNREFUSED` on startup | Paperclip server not running | Start Paperclip first (`pnpm dev` in Paperclip repo) |
| `404` on `/api/chat/*` | Wrong `PAPERCLIP_API_URL` | Ensure URL ends with `/api`, not `/api/` |
| Agents list is empty | `PAPERCLIP_COMPANY_ID` mismatch | Verify the company ID in your Paperclip dashboard |
| CORS errors in browser | Missing origin whitelist | Add `http://localhost:3000` to Paperclip CORS config |
| Widget not rendering | Missing `data-company` attribute | Add `data-company="<company-id>"` to the script tag |

### FAQ

**Q: Can I use this without Paperclip?**
> A: Not today. The chatbot relies on Paperclip for agent orchestration, issue tracking, and status polling. A mock server mode is on the roadmap.

**Q: How do I add a new agent skill?**
> A: Skills are defined in Paperclip's agent configuration. Update the agent card in Paperclip; the chatbot will pick up the new skills automatically on the next request.

**Q: Can I customize the intent classifier?**
> A: The classifier is modular. Replace `src/services/intent-classifier.ts` with your own implementation (e.g. OpenAI function calling) and restart the server.

**Q: Is there a rate limit?**
> A: The chatbot itself does not rate-limit, but Paperclip may enforce limits depending on your plan. Check your Paperclip dashboard for quotas.

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full strategic plan including:

- **Phase 1: Foundation** — Core routing, chat UI, status polling ✅
- **Phase 2: Intelligence** — LLM-based classification, semantic matching, context awareness
- **Phase 3: Integrations** — Slack, Discord, Teams, email, mobile
- **Phase 4: Enterprise Features** — RBAC, audit logs, SSO, analytics
- **Phase 5: Autonomy** — Self-improving routing, predictive issues, smart escalation

---

## Development

### Run tests

```bash
pnpm test
```

### Project Structure

```
AI-chatbot/
├── README.md                 # This file
├── ROADMAP.md                # Future direction and phases
├── package.json              # Dependencies and scripts
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

## Contributing

Contributions are welcome. Please open an issue or pull request on GitHub.

---

## License

[MIT](LICENSE)
