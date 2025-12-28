# KUX - MultiDevice Automation System

## Documentation Hub

**Project Status:** Production-Ready
**Last Updated:** December 2024

---

## Quick Navigation

| Section | Description | Files |
|---------|-------------|-------|
| [concept/](concept/) | Vision, master plan, roadmap | 3 |
| [architecture/](architecture/) | System design, data model, security | 5 |
| [integrations/](integrations/) | Notion & Gemini integration | 8 |
| [agents/](agents/) | Agent specifications | 6 |
| [behavior/](behavior/) | Human behavior simulation | 6 |
| [devices/](devices/) | Device pool management | 4 |
| [frontend/](frontend/) | React/Vite architecture | 4 |
| [backend/](backend/) | FastAPI architecture | 3 |
| [operations/](operations/) | Deployment & troubleshooting | 2 |
| [libraries/](libraries/) | AlignUI, Animations, MCP | 3 |
| [meta/](meta/) | Migration notes, completion summary | 3 |

---

## Quick Start

```bash
# 1. Setup
./scripts/setup.sh

# 2. Start
./scripts/start.sh

# 3. Open dashboard
open http://localhost:5173

# 4. API docs
open http://localhost:8000/docs
```

---

## Documentation Structure

### Core Documentation (41 files)

```
docs/
├── concept/                     # Project Vision (01-03)
│   ├── 01_MASTER_CONCEPT_PART_1.md
│   ├── 02_MASTER_CONCEPT_PART_2.md
│   └── 03_MASTER_CONCEPT_PART_3.md
│
├── architecture/                # System Architecture (10-14)
│   ├── 10_SYSTEM_ARCHITECTURE.md
│   ├── 11_TECH_STACK.md
│   ├── 12_DATA_MODEL.md
│   ├── 13_DEVICE_TOPOLOGY_LOCAL.md
│   └── 14_SECURITY_AND_COMPLIANCE.md
│
├── integrations/                # External Services
│   ├── notion/                  # Notion CRM (20-23)
│   │   ├── 20_NOTION_CRM_SYNC.md
│   │   ├── 21_NOTION_API_INTEGRATION.md
│   │   ├── 22_NOTION_WEBHOOK_HANDLER.md
│   │   └── 23_NOTION_ERROR_HANDLING.md
│   └── gemini/                  # Google Gemini (30-33)
│       ├── 30_GEMINI_INTEGRATION.md
│       ├── 31_GEMINI_CONTEXT_PACK.md
│       ├── 32_GEMINI_PROMPT_CONTRACT.md
│       └── 33_GEMINI_ERROR_RECOVERY.md
│
├── agents/                      # Agent Specifications (40-45)
│   ├── 40_AGENT_ARCHITECTURE.md
│   ├── 41_MAX_AGENT_SPEC.md
│   ├── 42_SMS_AGENT_SPEC.md
│   ├── 43_WHATSAPP_AGENT_SPEC.md
│   ├── 44_GEMINI_VISION_FALLBACK.md
│   └── 45_AGENT_ERROR_RECOVERY.md
│
├── behavior/                    # Human Behavior Simulation (50-55)
│   ├── 50_HUMAN_BEHAVIOR_OVERVIEW.md
│   ├── 51_HUMAN_TYPING_REALISTIC.md
│   ├── 52_HUMAN_TIMING.md
│   ├── 53_WARMUP_SCENARIOS.md
│   ├── 54_HUMAN_GESTURES.md
│   └── 55_ANTI_DETECTION_PATTERNS.md
│
├── devices/                     # Device Management (60-63)
│   ├── 60_DEVICE_POOL_MANAGER_LOCAL.md
│   ├── 61_USB_ADB_PERSISTENT_CONNECTION.md
│   ├── 62_USB_HUB_SETUP.md
│   └── 63_SCRCPY_LOCAL_CONTROL.md
│
├── frontend/                    # Frontend Architecture (70-73)
│   ├── 70_FRONTEND_ARCHITECTURE.md
│   ├── 71_VISUAL_WORKFLOW_BUILDER.md
│   ├── 72_DASHBOARD_REALTIME.md
│   └── 73_ALIGNUI_INTEGRATION.md
│
├── backend/                     # Backend Architecture (80-82)
│   ├── 80_BACKEND_ARCHITECTURE.md
│   ├── 81_EXECUTION_ENGINE.md
│   └── 82_QUEUE_AND_SCHEDULER.md
│
├── operations/                  # Operations (90-91)
│   ├── 90_DEPLOYMENT_GUIDE.md
│   └── 91_TROUBLESHOOTING_RUNBOOK.md
│
├── libraries/                   # Library Documentation
│   ├── alignui.md               # AlignUI Design System
│   ├── animations.md            # Anime.js Integration
│   └── mcp.md                   # MCP Service Connectors
│
├── meta/                        # Meta Documentation
│   ├── QUICK_LINKS.md
│   ├── COMPLETION_SUMMARY.md
│   └── MIGRATION_NOTES.md
│
├── index.json                   # Machine-readable index
└── README.md                    # This file
```

---

## Reading by Role

### Architect
1. `concept/01_MASTER_CONCEPT_PART_1.md`
2. `architecture/10_SYSTEM_ARCHITECTURE.md`
3. `architecture/12_DATA_MODEL.md`
4. `backend/80_BACKEND_ARCHITECTURE.md`
5. `frontend/70_FRONTEND_ARCHITECTURE.md`

### Backend Developer
1. `backend/80_BACKEND_ARCHITECTURE.md`
2. `backend/81_EXECUTION_ENGINE.md`
3. `backend/82_QUEUE_AND_SCHEDULER.md`
4. `integrations/notion/` (all files)
5. `integrations/gemini/` (all files)
6. `agents/40_AGENT_ARCHITECTURE.md`

### Frontend Developer
1. `frontend/70_FRONTEND_ARCHITECTURE.md`
2. `frontend/71_VISUAL_WORKFLOW_BUILDER.md`
3. `frontend/72_DASHBOARD_REALTIME.md`
4. `frontend/73_ALIGNUI_INTEGRATION.md`
5. `libraries/alignui.md`
6. `libraries/animations.md`

### DevOps Engineer
1. `operations/90_DEPLOYMENT_GUIDE.md`
2. `operations/91_TROUBLESHOOTING_RUNBOOK.md`
3. `devices/` (all files)
4. `architecture/13_DEVICE_TOPOLOGY_LOCAL.md`

---

## Library Documentation

Documentation for integrated libraries lives with the code:

| Library | Location | Description |
|---------|----------|-------------|
| **AlignUI** | `frontend/src/components/alignui/` | 45+ React components, design tokens |
| **Animations** | `frontend/src/lib/animations/` | Anime.js hooks and utilities |
| **MCP Kit** | `tools/mcp/` | Model Context Protocol connectors |

See `libraries/` folder for index files with direct links.

---

## Tech Stack

```
Frontend:   React 18 + Vite + Tailwind CSS + AlignUI
Backend:    FastAPI + Python 3.11 + SQLAlchemy
Database:   PostgreSQL 15 + Redis 7
Queue:      Celery 5 + APScheduler
AI:         Google Gemini API
Devices:    7x USB Android (ADB)
Deploy:     Docker + Docker Compose
```

---

## Project Index

For AI/automation tools, use `index.json` - contains:
- Complete file inventory
- Dependencies mapping
- Technology specifications
- Reading recommendations

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| USB devices not detected | `adb kill-server && adb start-server` |
| Port in use | `lsof -i :8000` then kill process |
| Docker issues | `docker-compose down && docker-compose up -d` |
| TypeScript errors | Check `frontend/tsconfig.json` excludes |

Full guide: `operations/91_TROUBLESHOOTING_RUNBOOK.md`
