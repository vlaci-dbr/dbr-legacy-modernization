# Conversational AI Template Framework

A reusable framework for creating ElevenLabs Conversational AI voice agent projects.

## Features

- **Interactive Project Wizard**: Create new voice agent projects with guided setup
- **Multiple Project Templates**: Pre-built templates for common use cases
- **6-Pillar Prompt Structure**: Consistent agent prompt architecture
- **Schema Validation**: JSON Schema validation for all configurations
- **Multi-platform Deployment**: GitHub Pages, Vercel, Netlify, Docker support
- **Markdown-first Knowledge Base**: Easy to edit, version-controlled KB content
- **Claude Integration**: Slash commands and specialized guides

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/conversational-ai-template.git
cd conversational-ai-template
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment

```bash
cp .env.example .env
# Edit .env and add your ELEVENLABS_API_KEY
```

### 4. Create a New Project (with Claude Code)

```
/init-project
```

Follow the interactive wizard to create your voice agent project.

### 5. Deploy

```
/deploy
```

## Project Templates

| Template | Description | Agents |
|----------|-------------|--------|
| `customer-service` | Customer service with specialists | 3-5 |
| `appointment-booking` | Appointment booking system | 2-3 |
| `info-hotline` | FAQ-based information line | 1-2 |
| `event-guide` | Event information assistant | 1 |
| `insurance-call-center` | Insurance claim reporting | 3-5 |

## Directory Structure

```
conversational-ai-template/
├── .claude/                 # Claude Code configuration
│   ├── commands/            # Slash commands
│   └── guides/              # Generation guides
├── framework/               # Framework core
│   ├── schemas/             # JSON Schemas
│   ├── templates/           # Project templates
│   └── defaults/            # Default configurations
├── lib/                     # Python library
├── projects/                # Generated projects
├── web/                     # Web components
├── docker/                  # Docker support
└── docs/                    # Documentation
```

## Commands

| Command | Description |
|---------|-------------|
| `/init-project` | Interactive project creation wizard |
| `/create-project` | Create project from template |
| `/generate-agent` | Generate agent prompt |
| `/generate-workflow` | Generate workflow configuration |
| `/generate-kb` | Generate knowledge base content |
| `/validate` | Validate project configuration |
| `/deploy` | Deploy to ElevenLabs |
| `/preview` | Local preview server |
| `/sync-elevenlabs` | Sync with ElevenLabs |

## Usage Examples

### Create an Event Guide Project

```
/init-project event-guide

Event name: Tech Conference 2026
Event date: March 15-16, 2026
Venue: Budapest Congress Center
Agent name: Emma
```

### Validate a Project

```
/validate projects/tech-conference-2026
```

### Deploy to ElevenLabs

```
/deploy projects/tech-conference-2026
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ELEVENLABS_API_KEY` | ElevenLabs API key | Yes |
| `DEFAULT_VOICE_ID` | Default voice ID | No |
| `DEFAULT_LLM_MODEL` | Default LLM model | No |

### Project Configuration

Each project contains:

```
projects/<project-name>/
├── config/
│   ├── project.json       # Main configuration
│   ├── workflow.json      # Workflow definition
│   ├── deployment.json    # Deployment settings
│   └── widget.json        # Widget customization
├── agents/
│   └── *.md               # Agent prompts
├── knowledge-bases/
│   └── *.md               # Knowledge base content
├── web/
│   └── index.html         # Landing page
└── deployment/
    ├── agent-ids.json     # ElevenLabs IDs
    └── kb-ids.json        # KB IDs
```

## Agent Prompt Structure (6-Pillar)

Every agent prompt follows this structure:

1. **PERSONALITY** - Who the agent is
2. **ENVIRONMENT** - Context and background
3. **TONE** - Communication style
4. **GOAL** - Main objectives
5. **GUARDRAILS** - Restrictions and rules
6. **TOOLS** - Available tools

## Deployment Options

### GitHub Pages

Automatic deployment via GitHub Actions when pushing to main.

### Vercel

```bash
vercel --prod
```

### Netlify

```bash
netlify deploy --prod
```

### Docker

```bash
docker-compose up -d
```

## Development

### Install Dev Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Format Code

```bash
black lib/ cli/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- [Documentation](docs/)
- [Issues](https://github.com/your-org/conversational-ai-template/issues)
- [Discussions](https://github.com/your-org/conversational-ai-template/discussions)
