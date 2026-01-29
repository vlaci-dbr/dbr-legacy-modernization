# Conversational AI Template Framework

## Overview

This is a Claude-driven framework for creating ElevenLabs Conversational AI voice agent projects. The framework provides templates, schemas, and utilities for generating, validating, and deploying voice agents.

**Core Principle:** Claude reads templates and guides, then generates project-specific files based on user input.

## Directory Structure

```
conversational-ai-template/
├── .claude/
│   ├── commands/           # Slash commands
│   │   ├── init-project.md     # Project initialization wizard
│   │   ├── create-project.md   # Create project from template
│   │   ├── generate-agent.md   # Agent generation
│   │   ├── generate-workflow.md
│   │   ├── generate-kb.md
│   │   ├── validate.md
│   │   ├── deploy.md
│   │   ├── preview.md          # Local preview
│   │   └── sync-elevenlabs.md  # ElevenLabs sync
│   ├── guides/             # Generation guides
│   │   ├── project-setup-guide.md
│   │   ├── agent-generation-guide.md
│   │   ├── workflow-generation-guide.md
│   │   └── kb-generation-guide.md
│   └── settings.json
├── framework/
│   ├── schemas/            # JSON Schema definitions
│   │   ├── project.schema.json
│   │   ├── agent.schema.json
│   │   ├── workflow.schema.json
│   │   ├── knowledge-base.schema.json
│   │   ├── deployment.schema.json
│   │   └── widget.schema.json
│   ├── templates/          # Template documents
│   │   ├── agents/         # Agent prompt templates
│   │   │   ├── orchestrator.md
│   │   │   ├── specialist.md
│   │   │   ├── finalizer.md
│   │   │   └── snippets/
│   │   ├── workflows/      # Workflow JSON templates
│   │   ├── knowledge-bases/ # KB templates
│   │   └── projects/       # Project templates
│   └── defaults/           # Default settings
│       ├── llm-settings.json
│       ├── audio-settings.json
│       └── voices.json
├── lib/                    # Python library
│   ├── elevenlabs_client.py
│   ├── config_loader.py
│   ├── schema_validator.py
│   └── md_to_json.py
├── projects/               # Generated projects
│   └── <project-name>/
│       ├── config/
│       ├── agents/
│       ├── knowledge-bases/
│       └── deployment/
└── web/                    # Web components
```

## Main Commands

| Command | Description |
|---------|-------------|
| `/init-project` | Interactive wizard for new project |
| `/create-project` | Create project from template |
| `/generate-agent` | Generate custom agent prompt |
| `/generate-workflow` | Generate ElevenLabs workflow |
| `/generate-kb` | Generate knowledge base content |
| `/validate` | Validate project configuration |
| `/deploy` | Deploy to ElevenLabs |
| `/preview` | Local widget preview |
| `/sync-elevenlabs` | Sync with ElevenLabs platform |

## Generation Flow

```
1. User: /init-project
       ↓
2. Claude reads: .claude/guides/project-setup-guide.md
       ↓
3. Claude interactively gathers data from user
       ↓
4. Claude reads appropriate templates:
   - framework/templates/projects/<template>.json
   - framework/templates/agents/*.md
   - framework/templates/workflows/*.json
   - framework/templates/knowledge-bases/*.md
       ↓
5. Claude generates project files:
   - projects/<project>/config/project.json
   - projects/<project>/config/workflow.json
   - projects/<project>/agents/*.md
   - projects/<project>/knowledge-bases/*.md
       ↓
6. Claude validates outputs against schemas
       ↓
7. /deploy → Python utility uploads to ElevenLabs
```

## Agent Types

| Type | Role | Template |
|------|------|----------|
| orchestrator | Entry point, routing, greeting | orchestrator.md |
| specialist | Domain-specific data collection | specialist.md |
| finalizer | Summary, closing | finalizer.md |

## Workflow Types

| Type | Use Case | Agent Count |
|------|----------|-------------|
| linear | Simple chain | 2-3 |
| branching | Orchestrator → N specialists → Finalizer | 3+ |
| hub-and-spoke | Return to orchestrator | 3+ |
| transfer-tool | Two-agent transfer | 2 |

## KB Types

| Type | Content |
|------|---------|
| faq | Frequently asked questions |
| product-catalog | Products and services |
| company-info | Company information |
| procedures | Process documentation |
| domain-knowledge | Domain-specific terminology |

## Project Templates

| Template | Description |
|----------|-------------|
| customer-service | Customer service with specialists |
| appointment-booking | Appointment booking system |
| info-hotline | FAQ-based information line |
| event-guide | Event information assistant |
| insurance-call-center | Insurance claim reporting |

## Important Files

### Schemas (for validation)
- `framework/schemas/project.schema.json` - Project config schema
- `framework/schemas/workflow.schema.json` - ElevenLabs native workflow schema
- `framework/schemas/agent.schema.json` - Agent config schema
- `framework/schemas/knowledge-base.schema.json` - KB schema
- `framework/schemas/deployment.schema.json` - Deployment config schema
- `framework/schemas/widget.schema.json` - Widget config schema

### Templates
- `framework/templates/agents/*.md` - 6-pillar agent prompt structure
- `framework/templates/workflows/*.json` - ElevenLabs native format
- `framework/templates/projects/*.json` - Project template manifests

### Defaults
- `framework/defaults/voices.json` - Hungarian and English voices
- `framework/defaults/llm-settings.json` - LLM settings by role
- `framework/defaults/audio-settings.json` - TTS/STT settings

## Conventions

### Naming
- Agent ID: kebab-case (e.g., `health-specialist`)
- KB ID: `kb-` prefix (e.g., `kb-company-faq`)
- Node ID: `node_` prefix (e.g., `node_receptionist`)
- Edge ID: `edge_` prefix (e.g., `edge_to_health`)

### Language
- Prompt content: Project language (hu/en)
- Config/code: English
- Variable names: English

### 6-pillar Prompt Structure
Every agent prompt contains:
1. **PERSONALITY** - Who the agent is
2. **ENVIRONMENT** - Context and background
3. **TONE** - Communication style
4. **GOAL** - Main goal and tasks
5. **GUARDRAILS** - Restrictions and rules
6. **TOOLS** - Available tools

## ElevenLabs Specific Rules

### Workflow Node Types
- `start` - Start node (exactly one)
- `override_agent` - Agent node

### Workflow Condition Types
- `unconditional` - Always executes
- `llm` - LLM evaluates (natural language condition)

### Transfer Mechanism
- Edges with `forward_condition`
- LLM condition: natural language description
- `edge_order` order matters (first match wins)

## Typical Usage

```bash
# 1. Create new project
/init-project
# → Choose: event-guide
# → Enter: event name, date, venue, agent name

# 2. Fill in knowledge bases
# Edit: projects/<project>/knowledge-bases/*.md

# 3. Validate project
/validate

# 4. Local preview
/preview

# 5. Deploy to ElevenLabs
/deploy

# 6. Test
# → Web interface or phone
```

## Troubleshooting

### Common Errors
- **"KB reference not found"** - Check KB ID in project.json
- **"Workflow node doesn't exist"** - Check agent IDs
- **"Schema validation error"** - Check schema requirements

### Debug
```bash
# Verbose deploy
cd lib && python -c "from elevenlabs_client import ElevenLabsClient; ..."

# Validate only
/validate
```
