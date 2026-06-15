# AI Task Router Chatbot

<p align="center">
  <img src="doc/assets/header.png" alt="AI Task Router - Intelligent Agent Orchestration" width="720" />
</p>

<p align="center">
  <a href="#quickstart"><strong>Quickstart</strong></a> &middot;
  <a href="#architecture"><strong>Architecture</strong></a> &middot;
  <a href="#features"><strong>Features</strong></a> &middot;
  <a href="#deployment"><strong>Deployment</strong></a> &middot;
  <a href="#roadmap"><strong>Roadmap</strong></a>
</p>

<p align="center">
  <a href="https://github.com/Parth-4518/AI-chatbot/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License" /></a>
  <a href="https://github.com/Parth-4518/AI-chatbot/stargazers"><img src="https://img.shields.io/github/stars/Parth-4518/AI-chatbot?style=flat" alt="Stars" /></a>
</p>

---

## What is AI Task Router?

**AI Task Router** is an intelligent chatbot system that routes natural language requests to the right AI agents using intent classification and skill matching. Built on the Paperclip framework, it automates software development workflows by understanding what you need and delegating to specialized AI employees.

### The Vision

Imagine telling a chatbot "Build me a login page with OAuth" and it automatically:
1. Understands your intent (frontend authentication feature)
2. Matches the task to agents with the right skills (React engineer + security reviewer)
3. Creates tracked issues and assigns them
4. Monitors progress and reports back

**You describe. It delegates. Work gets done.**

### Target Users

- **Solo developers** who want an AI team without the overhead
- **Startup founders** who need to scale development without hiring
- **Product managers** who want to delegate tasks through natural language
- **AI researchers** exploring multi-agent orchestration

---

## Quickstart

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Node.js | 20+ | LTS recommended |
| pnpm | 9.15+ | Package manager |
| Git | 2.30+ | For workspace management |

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/Parth-4518/AI-chatbot.git
cd AI-chatbot

# 2. Install dependencies
pnpm install

# 3. Set up environment (optional - uses embedded DB by default)
cp .env.example .env
# Edit .env with your settings (see Environment Variables below)

# 4. Start the development server
pnpm dev
```

The API server starts at `http://localhost:3100` with an embedded PostgreSQL database.

### Quick Verification

```bash
# Check health
curl http://localhost:3100/api/health

# List companies
curl http://localhost:3100/api/companies
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Chat UI     │  │ Chrome Page │  │ Dashboard               │  │
│  │ (chat-ui)   │  │ (chrome)    │  │ (Agent Cards + Status)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  INTENT CLASSIFICATION ENGINE                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐ │
│  │ Natural Language│  │ Rule-Based      │  │ Confidence     │ │
│  │ Input Parser    │  │ Intent Matcher  │  │ Scoring        │ │
│  └─────────────────┘  └─────────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT MATCHING SYSTEM                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐ │
│  │ Skill Database  │  │ Workload        │  │ Priority       │ │
│  │ (Agent Skills)  │  │ Balancer        │  │ Router         │ │
│  └─────────────────┘  └─────────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PAPERCLIP ORCHESTRATION                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│
│  │ Issue       │  │ Heartbeat     │  │ Budget & Cost           ││
│  │ Generation  │  │ Scheduler     │  │ Tracking                ││
│  └─────────────┘  └─────────────┘  └─────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AI AGENT POOL                               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ CEO     │ │ CTO     │ │ Engineer│ │ Designer│ │ Marketer│   │
│  │ (Claude)│ │ (Claude)│ │ (Codex) │ │ (Claude)│ │ (Claude)│   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### How It Works

1. **Intent Classification**: User input is parsed to identify the type of request (coding, design, research, etc.)
2. **Agent Matching**: The system matches the intent against agent skills, workload, and availability
3. **Issue Generation**: A tracked issue is created with proper assignment and context
4. **Execution**: The assigned agent receives a heartbeat and begins work
5. **Monitoring**: Progress is tracked through the dashboard with real-time status updates

---

## Features

### Core Chatbot Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Natural Language Routing** | Describe tasks in plain English, get them routed to the right agent | ✅ Live |
| **Intent Classification** | Rule-based matching with extensible classification system | ✅ Live |
| **Agent Skill Matching** | Match tasks to agents based on skills, workload, and priority | ✅ Live |
| **Multi-Agent Chat UI** | Interactive chat interface with agent cards and status | ✅ Live |
| **Issue Auto-Generation** | Creates tracked issues with proper assignment and context | ✅ Live |
| **Standalone & Embedded** | Run as standalone page or embed in other applications | ✅ Live |

### Paperclip Framework Features

| Feature | Description |
|---------|-------------|
| **Org Chart Management** | Hierarchical agent organization with roles and reporting |
| **Heartbeat Scheduling** | Automated agent wake-up and task execution |
| **Budget Control** | Token and cost tracking with hard-stop limits |
| **Governance & Approvals** | Board-level oversight with approval gates |
| **Multi-Company Support** | Run multiple AI companies from one instance |
| **Plugin System** | Extend with custom adapters and integrations |

---

## Deployment Guide

### Local Development

```bash
pnpm dev              # Full dev mode (API + UI, watch mode)
pnpm dev:once         # Full dev without file watching
pnpm dev:server       # Server only
```

### Production Build

```bash
pnpm build            # Build all packages
pnpm typecheck        # Type checking
pnpm test             # Run test suite
```

### Docker Deployment

```bash
# Build the Docker image
docker build -t ai-task-router .

# Run with environment variables
docker run -p 3100:3100 \
  -e DATABASE_URL=postgresql://... \
  -e GH_TOKEN=your_token \
  ai-task-router
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | No | embedded PGlite | PostgreSQL connection string |
| `GH_TOKEN` | Yes | - | GitHub token for repo access |
| `GITHUB_TOKEN` | Yes | - | Alias for GH_TOKEN |
| `PAPERCLIP_TELEMETRY_DISABLED` | No | 0 | Set to 1 to disable telemetry |
| `PORT` | No | 3100 | Server port |

---

## Troubleshooting

### Common Issues

**Issue**: Server won't start
```bash
# Solution: Kill existing processes and restart
pkill -f "paperclip"
pkill -f "tsx.*index.ts"
pnpm dev
```

**Issue**: Build hangs on Windows/WSL
```bash
# Solution: Use direct node path instead of npx
node node_modules/vite/bin/vite.js build
```

**Issue**: Vite cache issues
```bash
# Solution: Clear both dist and cache
rm -rf ui/dist ui/node_modules/.vite
pnpm dev
```

**Issue**: Port 3100 already in use
```bash
# Solution: The server auto-detects and uses 3101+
# Or manually kill the process using port 3100
lsof -ti:3100 | xargs kill -9
```

**Issue**: Database connection errors
```bash
# Solution: Reset local dev DB
rm -rf data/pglite
pnpm dev
```

### FAQ

**Q: Can I use my own AI models?**
A: Yes! Configure adapters in the board UI. Supports Claude, Codex, Cursor, Gemini, and custom HTTP adapters.

**Q: How do I add new agents?**
A: Go to Board → Agents → Hire Agent. Choose an adapter and configure skills.

**Q: Is this a fork of Paperclip?**
A: Yes, this is a specialized fork focused on chatbot-based task routing with natural language intent classification.

**Q: Can I run this without Paperclip?**
A: The chat UI works standalone, but the full orchestration requires the Paperclip server.

---

## Development

```bash
pnpm dev              # Full dev (API + UI, watch mode)
pnpm dev:once         # Full dev without file watching
pnpm dev:server       # Server only
pnpm build            # Build all
pnpm typecheck        # Type checking
pnpm test             # Cheap default test run (Vitest only)
pnpm test:watch       # Vitest watch mode
pnpm test:e2e         # Playwright browser suite
pnpm db:generate      # Generate DB migration
pnpm db:migrate       # Apply migrations
```

See [doc/DEVELOPING.md](doc/DEVELOPING.md) for the full development guide.

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full AI Task Router roadmap covering:
- Phase 1: Foundation (Current)
- Phase 2: Intelligence (LLM-based classification)
- Phase 3: Integrations (Slack, Discord, Teams)
- Phase 4: Enterprise Features (RBAC, audit logs)
- Phase 5: Autonomy (Self-improving routing)

---

## Contributing

We welcome contributions! See the [contributing guide](CONTRIBUTING.md) for details.

---

## License

MIT &copy; 2026 AI Task Router

---

<p align="center">
  <sub>Built with Paperclip. Powered by AI agents. Made for builders.</sub>
</p>
