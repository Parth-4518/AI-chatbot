# AI Task Router Chatbot

<p align="center">
  <img src="doc/assets/header.png" alt="AI Task Router" width="720" />
</p>

<p align="center">
  <strong>Natural-language gateway to your Paperclip AI workforce</strong>
</p>

<p align="center">
  <a href="#features"><strong>Features</strong></a> &middot;
  <a href="#quick-start"><strong>Quick Start</strong></a> &middot;
  <a href="#api-reference"><strong>API</strong></a> &middot;
  <a href="#architecture"><strong>Architecture</strong></a> &middot;
  <a href="#roadmap"><strong>Roadmap</strong></a> &middot;
  <a href="#ai-roadmap"><strong>AI Roadmap</strong></a>
</p>

---

## What is the AI Task Router?

The AI Task Router is a conversational interface that lets you delegate work to your Paperclip agent team using plain English. Instead of manually creating issues and assigning agents, you simply describe what you need — the router analyzes your request, picks the best agent, and creates a tracked issue automatically.

**Type "Build a dark mode toggle for the dashboard" → Router picks the Frontend Agent → Issue TEC-42 is created and assigned.**

It works as a standalone chat UI, an embedded widget in the Paperclip dashboard, or as an API you can call from any client.

---

## Features

| Feature | Description |
|---------|-------------|
| **Natural Language Routing** | Describe tasks in plain English. No forms, no dropdowns. |
| **Smart Agent Matching** | Keyword-based intent classification matches tasks to the most suitable agent by role and skills. |
| **Instant Previews** | Special commands like "hello world HTML page" generate and preview results immediately. |
| **Interactive Agent Selection** | Review the suggested agent and pick a different one before confirming. |
| **Real-Time Status Polling** | Watch issue status update live as agents pick up and complete work. |
| **Quick Action Buttons** | One-click shortcuts for common tasks (fix bug, deploy, design, analytics, marketing). |
| **Embedded or Standalone** | Use as full-page chat UI or embed in the merged dashboard. |
| **Work Product Display** | Completed tasks show deliverables, plans, and outputs directly in the chat. |

---

## Quick Start

### Standalone Chat UI

Open `chat-ui.html` in a browser connected to your Paperclip server:

```bash
# If Paperclip is running on localhost:3100
open http://localhost:3100/chat-ui.html
```

Or serve it statically:

```bash
npx serve . --single
# Then open http://localhost:3000/chat-ui.html
```

### Embedded Dashboard

The chatbot is embedded in the merged dashboard (`index.html`) as the right panel (45% width) alongside the project status dashboard:

```bash
open http://localhost:3100/index.html
```

### API Direct Usage

You can call the router API directly from any client:

```bash
# Route a task (analysis only)
curl -X POST http://localhost:3100/api/chat/route \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Build a dark mode toggle for the dashboard",
    "companyId": "a99fd059-c16b-4cdf-a4ca-0e78a04e42b8"
  }'

# Route and create issue in one step
curl -X POST http://localhost:3100/api/chat/route-and-create \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Fix the crash on signup",
    "companyId": "a99fd059-c16b-4cdf-a4ca-0e78a04e42b8"
  }'

# Create issue with specific agent
curl -X POST http://localhost:3100/api/chat/create \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Design a new landing page",
    "companyId": "a99fd059-c16b-4cdf-a4ca-0e78a04e42b8",
    "agentId": "<agent-uuid>"
  }'

# List available agents
curl http://localhost:3100/api/chat/agents?companyId=a99fd059-c16b-4cdf-a4ca-0e78a04e42b8
```

---

## File Structure

```
.
├── chat-ui.html              # Standalone full-page chat UI
├── chatbot-embedded.html     # Embedded version (used in dashboard iframe)
├── chatbot-index-backup.html # Backup of earlier chatbot iteration
├── index.html                # Merged dashboard (55% status + 45% chatbot)
│
├── server/
│   ├── src/routes/
│   │   ├── chat-router.ts           # Core chat router API
│   │   └── enhanced-chat-router.ts  # Enhanced routing with agent listing
│   ├── src/services/ai-router/
│   │   ├── intent-classifier.ts     # Rule-based intent classification
│   │   ├── agent-matcher.ts         # Agent scoring and matching
│   │   └── issue-generator.ts       # Issue title/description generation
│   └── projects/tec-18-ai-router/
│       ├── DESIGN.md                # Product design document
│       └── ARCHITECTURE.md          # Technical architecture
│
└── CHATBOT-README.md         # This file
```

---

## Architecture

```
┌─────────────┐      POST /api/chat/route       ┌─────────────────┐
│   Client    │ ───────────────────────────────► │   AI Router     │
│  (UI/Bot)   │                                  │    Service      │
└─────────────┘                                  └────────┬────────┘
                                                          │
                              ┌───────────────────────────┼───────────┐
                              ▼                           ▼           ▼
                    ┌─────────────────┐         ┌──────────────┐ ┌──────────┐
                    │ Intent Classifier│         │ Agent Matcher │ │ Issue    │
                    │   (Rule-based)  │         │  (TEC-9 svc)  │ │ Generator│
                    └─────────────────┘         └──────────────┘ └──────────┘
```

### Routing Flow

1. **Intent Classification** — The prompt is analyzed for keywords to determine intent:
   - `create_task` — "Build", "Create", "Implement", "Add"
   - `create_bug` — "Fix", "Bug", "Crash", "Error", "Broken"
   - `query_status` — "Status of TEC-X", "How is..."
   - `delegate` — "Assign to...", "Have [agent] review..."
   - `clarify` — Ambiguous or unclear requests

2. **Agent Matching** — For task creation intents, the router:
   - Queries active agents for the company
   - Scores by skill overlap (50%), workload (30%), and past success (20%)
   - Returns the best match with confidence score

3. **Issue Generation** — A structured issue is drafted:
   - Title extracted from the first sentence of the prompt
   - Priority inferred from urgency keywords (urgent → critical, etc.)
   - Labels suggested from content analysis
   - Description formatted with request context

4. **User Confirmation** — The chat UI shows:
   - Task analysis breakdown
   - Suggested agent with reasoning
   - Option to select a different agent
   - One-click confirm to create the issue

5. **Status Tracking** — After creation:
   - Issue status is polled every 10 seconds
   - Live updates show: Backlog → In Progress → Completed
   - Work products and plans are displayed on completion

---

## API Reference

### `POST /api/chat/route`

Analyze a prompt and return routing information without creating an issue.

**Request:**
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
  "matchedAgent": {
    "id": "...",
    "name": "Frontend Agent",
    "role": "developer",
    "confidence": 0.92,
    "reasoning": "Prompt describes UI feature; Frontend Agent has skills [react, css, ui]"
  },
  "generatedIssue": {
    "title": "Build dark mode toggle for dashboard",
    "description": "...",
    "type": "task",
    "priority": "medium",
    "suggestedLabels": ["ui", "theme", "dashboard"]
  },
  "routing": {
    "action": "create_issue",
    "targetEndpoint": "/api/companies/{cid}/issues"
  }
}
```

### `POST /api/chat/route-and-create`

Analyze and immediately create an issue in one call.

**Request:** Same as `/route`

**Response:** Includes the created issue object with `identifier`, `status`, etc.

### `POST /api/chat/create`

Create an issue with a specific agent (skips matching).

**Request:**
```json
{
  "prompt": "Design a new landing page",
  "companyId": "...",
  "agentId": "specific-agent-uuid"
}
```

### `GET /api/chat/agents`

List all active agents for a company.

**Query:** `?companyId=a99fd059-c16b-4cdf-a4ca-0e78a04e42b8`

**Response:**
```json
{
  "agents": [
    { "id": "...", "name": "CEO", "role": "ceo", "adapterType": "hermes_local", "status": "idle" },
    { "id": "...", "name": "DevOps", "role": "devops", "adapterType": "process", "status": "running" }
  ]
}
```

---

## Supported Agent Roles

The chatbot recognizes these roles for avatar display and routing:

| Role | Emoji | Typical Tasks |
|------|-------|---------------|
| CEO | 👔 | Strategy, planning, hiring, vision |
| CTO | 💻 | Architecture, technical decisions |
| CMO | 📢 | Marketing, content, growth |
| Engineer / Developer | ⚙️ 💻 | Coding, implementation, features |
| QA / Tester | 🧪 🔍 | Testing, quality assurance |
| DevOps / SRE | 🚀 🔧 | Deployment, infrastructure, CI/CD |
| Designer | 🎨 | UI/UX, visual design |
| PM / Product | 📋 📦 | Product management, roadmaps |
| Data / Analyst | 📊 📈 | Analytics, reporting, insights |
| Security | 🔒 🛡️ | Security audits, compliance |

---

## Instant Preview Commands

These special prompts bypass normal routing and generate instant HTML previews:

| Prompt Pattern | Result |
|----------------|--------|
| "hello world HTML page" | Generates and previews a styled Hello World page |
| "good morning HTML page" | Generates and previews a Good Morning greeting page |
| "portfolio HTML page/website" | Generates and previews an interactive portfolio |

---

## Configuration

The chatbot connects to the Paperclip API. Configure these values in the HTML:

```javascript
const API_BASE = '/api';  // Or full URL for external hosting
const COMPANY_ID = 'a99fd059-c16b-4cdf-a4ca-0e78a04e42b8';
const AUTH_TOKEN = 'local-dev-token';  // Or agent API key
```

For production, set these via environment variables or a config endpoint.

---

## Roadmap

### Current (v1)
- Rule-based intent classification
- Keyword agent matching
- Basic issue generation
- Real-time status polling
- Instant HTML previews

### Planned (v2)
- **LLM-powered intent classification** — Replace rule-based with structured LLM output for better accuracy
- **Semantic agent matching** — Use embeddings to match task descriptions to agent capabilities
- **Conversation memory** — Multi-turn conversations with context retention
- **File upload support** — Attach screenshots, documents, or code snippets to tasks
- **Voice input** — Speech-to-text for hands-free task creation
- **Slack/Discord integration** — Create tasks from chat messages via bot commands
- **Smart suggestions** — Proactively suggest tasks based on project state and open issues

### Future (v3)
- **Auto-delegation mode** — Skip confirmation for trusted agents; create and assign immediately
- **Batch task creation** — "Fix all the bugs in the auth module" → creates multiple issues
- **Agent negotiation** — Agents can discuss and reassign tasks among themselves
- **Predictive routing** — Learn from past assignments to improve match accuracy over time

---

## AI Roadmap

### Executive Summary

This AI roadmap outlines strategic improvements for the AI Task Router to enhance intelligence, reliability, autonomy, and operational usefulness. It is organized by impact and implementation complexity across 7 phases.

---

### Phase 1: Agent Intelligence & Reasoning

**Goals:** Improve decision-making quality, reduce repetitive errors, and enhance context retention across runs.

| # | Improvement | Description | Priority |
|---|-------------|-------------|----------|
| 1.1 | **Context Window Optimization** | Smart truncation that preserves issue context, recent comments, and work products over generic system prompts | HIGH |
| 1.2 | **Run Summarization** | Auto-generate run summaries so subsequent runs start with clear state instead of replaying full transcripts | HIGH |
| 1.3 | **Decision Logging** | Require agents to log key decisions ("why I chose X over Y") in issue comments | MEDIUM |
| 1.4 | **Self-Correction Loops** | Agents detect their own failures (high churn, no-comment streaks) and propose corrective actions | MEDIUM |
| 1.5 | **Plan Adherence Scoring** | Track how well agents follow issue plans; surface drift to board operators | LOW |

**Success Metrics:**
- No-comment streaks reduced by 50%
- Average runs per issue completion down by 30%
- Agent self-reported decision coverage > 80%

---

### Phase 2: Memory & Knowledge System

**Goals:** Enable durable memory across sessions, organizational learning, and faster onboarding for new agents.

| # | Improvement | Description | Priority |
|---|-------------|-------------|----------|
| 2.1 | **Agent Memory Layer** | Per-agent memory store for preferences, learned patterns, and recurring corrections | HIGH |
| 2.2 | **Company Knowledge Base** | Shared knowledge surface: playbooks, decision records, recurring fixes | HIGH |
| 2.3 | **Project Context Injection** | Auto-inject relevant project docs, schemas, and conventions into agent prompts | MEDIUM |
| 2.4 | **Memory Compression** | Summarize old memories; archive stale context; keep hot context fast | MEDIUM |
| 2.5 | **Cross-Agent Learning** | When one agent solves a novel problem, other agents can access the solution pattern | LOW |

**Success Metrics:**
- Agent setup time for new tasks reduced by 40%
- Recurring issues resolved without human input > 60%
- Knowledge base queries answered correctly > 85%

---

### Phase 3: Autonomy & Delegation

**Goals:** Enable agents to delegate to other agents without human intervention, self-organize task hierarchies, and reduce board-operator bottleneck.

| # | Improvement | Description | Priority |
|---|-------------|-------------|----------|
| 3.1 | **Smart Delegation** | CEO/agent can create child issues and assign to appropriate agents with full context handoff | HIGH |
| 3.2 | **Auto-Escalation** | Agents detect when they are stuck and escalate to parent agent or board with clear blocker summary | HIGH |
| 3.3 | **Task Decomposition** | Agents can break large issues into sub-tasks with proper parent-child relationships | MEDIUM |
| 3.4 | **Agent Collaboration** | Multiple agents can work on related issues with clear handoff contracts | MEDIUM |
| 3.5 | **Self-Organization Proposals** | Agents can propose org changes (new roles, rebalancing workloads) for board approval | LOW |

**Success Metrics:**
- Issues resolved without human touch > 40%
- Escalation time from stuck to resolved < 15 minutes
- Delegation accuracy (right agent for right task) > 75%

---

### Phase 4: Output Quality & Work Products

**Goals:** Ensure every completed issue has a tangible deliverable, make work products discoverable and reusable, and make quality measurable.

| # | Improvement | Description | Priority |
|---|-------------|-------------|----------|
| 4.1 | **Work Product Attachments** | Agents attach files, URLs, or content previews to issues on completion | HIGH |
| 4.2 | **Output Validation** | Automated checks that deliverables meet basic criteria (compiles, passes tests, has docs) | HIGH |
| 4.3 | **Artifact Registry** | Central registry of all agent outputs with search, versioning, and reuse | MEDIUM |
| 4.4 | **Quality Scoring** | Heuristic quality scores based on test coverage, doc completeness, review feedback | MEDIUM |
| 4.5 | **Preview Generation** | Auto-generate live previews for HTML, markdown, and other visual outputs | LOW |

**Success Metrics:**
- Issues with attached work products > 90%
- Output validation pass rate > 80%
- Artifact reuse rate > 25%

---

### Phase 5: Health, Monitoring & Recovery

**Goals:** Enable agents to detect their own health issues, provide automatic recovery from common failures, and offer clear visibility into system state.

| # | Improvement | Description | Priority |
|---|-------------|-------------|----------|
| 5.1 | **Heartbeat Intelligence** | Heartbeat checks agent adapter health, PATH, and connectivity before claiming work | HIGH |
| 5.2 | **Auto-Retry with Backoff** | Failed runs retry automatically with exponential backoff and context preservation | HIGH |
| 5.3 | **Adapter Health Dashboard** | Real-time view of all adapter statuses with last-seen and error rates | MEDIUM |
| 5.4 | **Graceful Degradation** | If primary adapter fails, agent can switch to backup adapter or queue for later | MEDIUM |
| 5.5 | **Predictive Alerts** | Detect patterns that predict failure (high churn, long active duration) and alert before breakage | LOW |

**Success Metrics:**
- Agent downtime without human intervention < 2 minutes
- False positive recovery attempts < 10%
- Mean time to recovery (MTTR) < 5 minutes

---

### Phase 6: Cost Optimization & Efficiency

**Goals:** Reduce token spend per unit of work, enable better model selection for task types, and implement budget-aware execution.

| # | Improvement | Description | Priority |
|---|-------------|-------------|----------|
| 6.1 | **Model Routing** | Route simple tasks to cheaper models, complex tasks to stronger models automatically | HIGH |
| 6.2 | **Token Budgeting per Issue** | Set expected token budgets; warn when agents exceed; hard-stop on runaway spend | HIGH |
| 6.3 | **Run Compression** | Merge redundant tool calls; batch file reads; eliminate no-op operations | MEDIUM |
| 6.4 | **Cost Attribution** | Clear per-agent, per-project, per-issue cost breakdown with trends | MEDIUM |
| 6.5 | **Efficiency Scoring** | Score agents on output quality per dollar spent; surface best practices | LOW |

**Success Metrics:**
- Average cost per issue completion down by 25%
- Model routing accuracy > 80%
- Budget overruns < 5%

---

### Phase 7: Human-AI Collaboration

**Goals:** Enable board operators to guide agents without micromanaging, provide clear communication channels, and implement approval workflows that don't block progress.

| # | Improvement | Description | Priority |
|---|-------------|-------------|----------|
| 7.1 | **CEO Chat Interface** | Lightweight chat with CEO agent that resolves to real work objects (issues, plans, decisions) | HIGH |
| 7.2 | **Approval Gates** | Configurable approval points: auto-approve low-risk, flag high-risk for human review | HIGH |
| 7.3 | **Progress Streaming** | Real-time visibility into what agents are doing while they work | MEDIUM |
| 7.4 | **Feedback Loop** | Board operators can rate agent outputs; ratings feed into agent improvement | MEDIUM |
| 7.5 | **Intervention Tools** | Pause, redirect, or override agents mid-run without losing context | LOW |

**Success Metrics:**
- Human approval response time < 10 minutes
- Agent perceived usefulness rating > 4.0/5.0
- Intervention success rate > 90%

---

### Implementation Timeline

| Phase | Focus | Timeline | Status |
|-------|-------|----------|--------|
| Phase 1 | Agent Intelligence | Month 1-2 | Planned |
| Phase 2 | Memory & Knowledge | Month 2-3 | Planned |
| Phase 3 | Autonomy & Delegation | Month 3-4 | Planned |
| Phase 4 | Output Quality | Month 4-5 | Planned |
| Phase 5 | Health & Recovery | Month 5-6 | Planned |
| Phase 6 | Cost Optimization | Month 6-7 | Planned |
| Phase 7 | Human-AI Collaboration | Month 7-8 | Planned |

---

### Quick Wins (Start This Week)

1. **Add run summarization** to the agent heartbeat response
2. **Enforce work product attachment** on issue completion
3. **Implement auto-retry** with 3 attempts and exponential backoff
4. **Add model profile routing** (cheap/fast/strong) based on issue priority
5. **Create agent memory file** (`~/.paperclip/agent-memory/<agent-id>.json`)

---

### Key Metrics Dashboard

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Avg runs per issue | TBD | < 5 | Issue analytics |
| No-comment streak rate | TBD | < 10% | Run audit |
| Issues with work products | TBD | > 90% | Work product registry |
| Agent uptime | TBD | > 99% | Health dashboard |
| Cost per issue | TBD | -25% | Budget reports |
| Human touches per issue | TBD | < 2 | Activity log |

---

### Dependencies

- **Phase 1** requires: agent adapter v2 API
- **Phase 2** requires: persistent storage layer (already available)
- **Phase 3** requires: parent-child issue hierarchy (already available)
- **Phase 4** requires: work product API (already available)
- **Phase 5** requires: health check endpoints (already available)
- **Phase 6** requires: cost event ingestion (already available)
- **Phase 7** requires: real-time WebSocket or SSE (new)

---

*Document Version: 2.0*
*Updated: 2026-06-11*
*Status: Active Roadmap*
*Owner: CTO Agent (TechnologySavy)*

---

## Contributing

This chatbot is part of the Paperclip ecosystem. To extend it:

1. **Add new intents** — Edit `server/src/services/ai-router/intent-classifier.ts`
2. **Improve matching** — Enhance `server/src/services/ai-router/agent-matcher.ts`
3. **UI customization** — Modify `chat-ui.html` or `chatbot-embedded.html`
4. **New preview types** — Add handlers in the `sendMessage()` function

See the main [CONTRIBUTING.md](CONTRIBUTING.md) for project-wide guidelines.

---

## License

MIT — same as Paperclip. See [LICENSE](LICENSE) for details.
