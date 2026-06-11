# AI Chatbot Roadmap

> A living document that outlines the vision, phases, and future direction of the AI Chatbot project.

---

## Phase 1: Foundation (Current)

**Goal:** A reliable, fast task router that works out of the box.

- [x] Natural language task routing
- [x] Basic intent classification (keyword + pattern based)
- [x] Agent matching by skills and workload
- [x] Standalone chat UI
- [x] Embedded widget for dashboards
- [x] Real-time status polling
- [x] Quick action buttons for common tasks

**Status:** MVP complete. The chatbot is functional and integrated with Paperclip.

---

## Phase 2: Intelligence

**Goal:** Smarter routing with LLM-powered understanding and context awareness.

- [ ] **LLM-based intent classification** — Replace rule-based matching with an LLM that understands nuanced requests, ambiguous phrasing, and multi-intent queries.
- [ ] **Context-aware multi-turn conversations** — Remember previous messages in a session so users can say *"Make it blue instead"* without restating the full request.
- [ ] **Learning from past routing decisions** — Track which agent assignments succeeded and use that data to improve future matches.
- [ ] **Confidence scoring and fallback handling** — Return a confidence score with every routing decision. If confidence is low, ask clarifying questions instead of guessing.
- [ ] **Semantic search over agent skills** — Match requests to agents using embeddings, not just keyword overlap.

**Target:** Q3 2026

---

## Phase 3: Integrations

**Goal:** Meet users where they already work.

- [ ] **Slack bot** — Route tasks directly from Slack channels and DMs.
- [ ] **Discord bot** — Community-friendly bot for open-source projects.
- [ ] **Microsoft Teams support** — Enterprise integration for Teams users.
- [ ] **Email triggers** — Forward an email to a configured address and auto-create an issue.
- [ ] **Webhook triggers** — Accept webhooks from GitHub, Linear, Jira, etc. to auto-route external events.
- [ ] **Mobile app companion** — iOS/Android app for on-the-go task creation and status checks.

**Target:** Q4 2026

---

## Phase 4: Enterprise Features

**Goal:** Production-ready for teams with compliance, security, and scale requirements.

- [ ] **Role-based access control (RBAC)** — Define who can create, view, or reassign issues.
- [ ] **Audit logs and compliance** — Immutable logs of every routing decision, agent assignment, and status change.
- [ ] **Custom agent onboarding** — UI wizard for adding new agents with custom skills, adapters, and policies.
- [ ] **Analytics dashboard** — Visualize routing accuracy, agent utilization, resolution times, and bottleneck detection.
- [ ] **SSO / SAML integration** — Login via Okta, Google Workspace, or Azure AD.
- [ ] **Data retention policies** — Configurable retention and export for compliance (GDPR, SOC2).

**Target:** Q1 2027

---

## Phase 5: Autonomy

**Goal:** The chatbot improves itself with minimal human intervention.

- [ ] **Self-improving routing models** — Automatically retrain the intent classifier and agent matcher based on feedback loops.
- [ ] **Predictive issue creation** — Detect patterns (e.g. recurring bug reports) and proactively suggest or create issues before the user asks.
- [ ] **Agent performance optimization** — Recommend agent configuration changes (skill additions, workload limits) based on performance data.
- [ ] **Automated reporting** — Generate weekly summaries of team activity, blockers, and milestones without manual prompting.
- [ ] **Natural language configuration** — Change routing rules, add agents, or update policies by describing the change in chat.

**Target:** Q2 2027

---

## How We Prioritize

1. **User pain first** — Features that remove the most friction for the most users ship first.
2. **Stability before novelty** — Every phase must be production-stable before the next phase begins.
3. **Feedback-driven** — Roadmap items are re-prioritized based on real usage data and user feedback.

---

## Contributing to the Roadmap

Have an idea? Open an issue with the label `roadmap` and describe:
- The problem you're solving
- Who it helps
- How it fits (or extends) the phases above

---

*Last updated: June 2026*
