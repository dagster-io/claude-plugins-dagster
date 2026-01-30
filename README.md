<div align="center">
  <img width="auto" height="38px" alt="dagster-hearts-claude" src="https://github.com/user-attachments/assets/b162dddf-6a7e-459e-be06-29d34d637650" />
</div>

# Dagster Skills

[![Lint](https://github.com/dagster-io/skills/actions/workflows/lint.yml/badge.svg)](https://github.com/dagster-io/skills/actions/workflows/lint.yml)

AI assistant skills for building workflows and data pipelines using Dagster.

**Compatible with Claude Code, OpenCode, OpenAI Codex, Pi, and other Agent Skills-compatible tools.**

## What's New (v0.0.7)

**Simplified structure**: Consolidated from 9 skills to **4 simple skills** with flat organization:
- ✅ Single `/dg` skill for all CLI operations (replaces 6 separate `/dg:*` skills)
- ✅ Renamed `/dagster-conventions` → `/dagster-best-practices`
- ✅ Renamed `/integrations-index` → `/dagster-integrations`
- ✅ Kept `/dignified-python` as general Python standards skill

**Migration guide**: See [MIGRATION.md](#migration-from-v006) below.

## Installation

### Claude Code

Install using the [Claude plugin marketplace](https://code.claude.com/docs/en/discover-plugins#add-from-github):

```
/plugin marketplace add dagster-io/skills
```

### Using `npx skills`

Install using the [`npx skills`](https://skills.sh/) command-line:

```bash
npx skills add dagster-io/skills
```

### Manual Installation

<details>
<summary>See full instructions...</summary>

Clone the repository and copy skills to your tool's skills directory:

**OpenCode:**

```bash
git clone https://github.com/dagster-io/skills.git
cp -r skills/skills/* ~/.config/opencode/skill/
```

**OpenAI Codex:**

```bash
git clone https://github.com/dagster-io/skills.git
cp -r skills/skills/* ~/.codex/skills/
```

**Pi Agent:**

```bash
git clone https://github.com/dagster-io/skills.git
cp -r skills/skills/* ~/.pi/agent/skills/
```

</details>

## Skills Overview

4 focused skills for Dagster development:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **`/dg`** | Dagster CLI operations | Create projects, scaffold components, launch assets, list definitions, view logs, troubleshoot |
| **`/dagster-best-practices`** | Architectural guidance | Decide how to structure assets, choose automation, design resources, learn testing strategies |
| **`/dagster-integrations`** | Integration catalog | Discover 82+ integrations (dbt, Fivetran, Snowflake, etc.) |
| **`/dignified-python`** | Python standards | Write production-quality Python code (general, not Dagster-specific) |

## Skill Details

### `/dg` - Dagster CLI

**Single skill for all `dg` CLI operations** (replaces previous 6 separate `/dg:*` skills).

**Use when you need to:**
- Create projects: "create a new dagster project"
- Scaffold components: "scaffold an asset" / "add a dbt integration"
- Launch assets: "run my assets" / "materialize customers asset"
- List definitions: "show all my assets" / "what components exist"
- View logs: "show logs for last run"
- Troubleshoot: "debug this failed run"

**Natural language invocation**: Just say what you want with `/dg` instead of using specific subcommands.

**Examples:**
```
/dg create a new project called analytics
/dg scaffold a dbt integration
/dg launch all assets with tag:priority=high
/dg show me the logs for the last run
/dg help me debug why my asset failed
```

**What's included:**
- Project creation (single project and workspaces)
- Component scaffolding (assets, schedules, sensors, integrations)
- Asset execution (launch with partitions, configs, environments)
- Definition discovery (list defs, components, envs, projects)
- Log viewing (recent runs, specific runs, live following)
- Prototyping (production-ready implementations)
- Troubleshooting (failure analysis, debugging)

### `/dagster-best-practices` - Architectural Guidance

**Expert guidance for Dagster patterns and architectural decisions** (renamed from `/dagster-conventions`).

**Use when you need to:**
- Structure assets: "how should I design my assets"
- Choose automation: "schedules vs sensors vs automation conditions"
- Manage resources: "how to handle database connections"
- Testing strategies: "how do I test my assets"
- ETL patterns: "dbt integration patterns" / "data quality patterns"
- Project organization: "single project vs workspace"

**What's included:**
- Asset design patterns (dependencies, partitions, multi-assets)
- Automation strategies (declarative automation, schedules, sensors)
- Resource patterns (database connections, API clients, env vars)
- Testing approaches (unit tests, integration tests, asset checks)
- ETL patterns (dbt, dlt, Sling integration patterns)
- Project structure (organization, components, code locations)

**References:**
- `references/assets.md` - Asset design patterns
- `references/automation.md` - Automation strategies
- `references/resources.md` - Resource patterns
- `references/testing.md` - Testing strategies
- `references/etl-patterns.md` - ETL/ELT patterns
- `references/project-structure.md` - Project organization

### `/dagster-integrations` - Integration Catalog

**Comprehensive catalog of 82+ Dagster integrations** (renamed from `/integrations-index`).

**Use when you need to:**
- Discover integrations: "which tool for data warehousing"
- Compare options: "snowflake vs bigquery"
- Find capabilities: "does dagster support dbt"
- Choose integrations: "best ETL tool for my use case"

**What's included:**
- **AI & ML** (6): OpenAI, Anthropic, Gemini, MLflow, W&B
- **ETL/ELT** (9): dbt, Fivetran, Airbyte, dlt, Sling, PySpark
- **Storage** (35+): Snowflake, BigQuery, Postgres, S3, DuckDB, Weaviate
- **Compute** (15+): AWS, Azure, GCP, Databricks, Spark, Kubernetes
- **BI** (7): Looker, Tableau, PowerBI, Sigma, Hex
- **Monitoring** (3): Datadog, Prometheus, Papertrail
- **Alerting** (6): Slack, PagerDuty, MS Teams, Discord, Twilio
- **Testing** (2): Great Expectations, Pandera
- **Other** (2+): Pandas, Polars

**References:**
- `references/ai.md` - AI & ML platforms
- `references/etl.md` - ETL/ELT tools
- `references/storage.md` - Data storage
- `references/compute.md` - Compute platforms
- `references/bi.md` - BI & visualization
- `references/monitoring.md` - Monitoring & observability
- `references/alerting.md` - Alerting & notifications
- `references/testing.md` - Data quality & testing
- `references/other.md` - Miscellaneous

### `/dignified-python` - Python Standards

**Production-quality Python coding standards** (general Python, not Dagster-specific).

**Use when you need to:**
- Code review: "is this good python" / "make this more pythonic"
- Type hints: "how should I annotate this"
- Exception handling: "LBYL vs EAFP patterns"
- Path operations: "pathlib vs os.path"
- CLI patterns: "click usage patterns"

**What's included:**
- Modern type syntax (list[str], str | None)
- LBYL exception handling patterns
- Pathlib operations
- Python version-specific features (3.10-3.13)
- CLI patterns (Click, argparse)
- Advanced typing patterns
- Interface design (ABC, Protocol)
- API design principles

**References:**
- `references/core-standards.md` - Essential standards
- `references/cli-patterns.md` - CLI patterns
- `references/versions/python-3.10.md` - Python 3.10+ features
- `references/versions/python-3.11.md` - Python 3.11+ features
- `references/versions/python-3.12.md` - Python 3.12+ features
- `references/versions/python-3.13.md` - Python 3.13+ features
- `references/advanced/exception-handling.md` - Exception patterns
- `references/advanced/interfaces.md` - Interface design
- `references/advanced/typing-advanced.md` - Advanced typing
- `references/advanced/api-design.md` - API design

## Usage Examples

### Creating a New Project

```
User: "Create a new Dagster project for analytics"
→ /dg create a project called analytics

Follow-up:
→ /dagster-best-practices for project structure guidance
→ /dagster-integrations to discover which tools to integrate
→ /dg to scaffold integrations and assets
```

### Scaffolding Components

```
User: "Add a dbt integration to my project"
→ /dagster-integrations (discover dbt in ETL category)
→ /dg scaffold a dbt integration
→ /dagster-best-practices (learn dbt patterns in etl-patterns.md)
```

### Building Assets

```
User: "How should I structure my data pipeline?"
→ /dagster-best-practices (learn asset patterns, dependencies, organization)
→ /dg scaffold assets following those patterns
→ /dignified-python for Python code quality
```

### Launching Assets

```
User: "Run all my high-priority assets"
→ /dg launch --assets "tag:priority=high"

User: "View the logs from that run"
→ /dg logs --follow
```

### Debugging

```
User: "My asset failed, help me debug it"
→ /dg troubleshoot (analyzes failure, suggests solutions)
→ /dagster-best-practices (learn testing patterns to prevent issues)
```

## Workflow Patterns

### Discovery → Learning → Implementation

1. **Discover** integrations with `/dagster-integrations`
2. **Learn** patterns with `/dagster-best-practices`
3. **Implement** with `/dg` (scaffold, launch, troubleshoot)
4. **Polish** Python code with `/dignified-python`

### Example: Setting Up dbt

```
1. /dagster-integrations → Find dbt in ETL category
2. /dg list components --package dagster_dbt
3. /dagster-best-practices → Learn dbt patterns
4. /dg scaffold defs dagster_dbt.DbtProjectComponent my_dbt
5. /dg launch --assets my_dbt
6. /dg troubleshoot (if issues occur)
```

## Directory Structure

```
skills/
├── dg/                           # CLI operations skill
│   ├── SKILL.md
│   └── references/
│       ├── README.md
│       ├── create-project.md
│       ├── create-workspace.md
│       ├── scaffold.md
│       ├── launch.md
│       ├── list.md
│       ├── logs.md
│       ├── prototype.md
│       └── troubleshoot.md
│
├── dagster-best-practices/       # Architectural guidance skill
│   ├── SKILL.md
│   └── references/
│       ├── README.md
│       ├── assets.md
│       ├── automation.md
│       ├── resources.md
│       ├── testing.md
│       ├── etl-patterns.md
│       └── project-structure.md
│
├── dagster-integrations/         # Integration catalog skill
│   ├── SKILL.md
│   └── references/
│       ├── README.md
│       ├── ai.md
│       ├── etl.md
│       ├── storage.md
│       ├── compute.md
│       ├── bi.md
│       ├── monitoring.md
│       ├── alerting.md
│       ├── testing.md
│       └── other.md
│
└── dignified-python/             # Python standards skill
    ├── SKILL.md
    └── references/
        ├── README.md
        ├── core-standards.md
        ├── cli-patterns.md
        ├── versions/
        │   ├── python-3.10.md
        │   ├── python-3.11.md
        │   ├── python-3.12.md
        │   └── python-3.13.md
        └── advanced/
            ├── exception-handling.md
            ├── interfaces.md
            ├── typing-advanced.md
            └── api-design.md
```

## Migration from v0.0.6

**Breaking changes** in v0.0.7:

### Skill Name Changes

| Old Skill | New Skill | Migration |
|-----------|-----------|-----------|
| `/dg:create-project` | `/dg create project` | Use natural language with `/dg` |
| `/dg:create-workspace` | `/dg create workspace` | Use natural language with `/dg` |
| `/dg:scaffold` | `/dg scaffold` | Use natural language with `/dg` |
| `/dg:launch` | `/dg launch` | Use natural language with `/dg` |
| `/dg:list` | `/dg list` | Use natural language with `/dg` |
| `/dg:logs` | `/dg logs` | Use natural language with `/dg` |
| `/dg:prototype` | `/dg prototype` | Use natural language with `/dg` |
| `/dagster-conventions` | `/dagster-best-practices` | Use new name |
| `/integrations-index` | `/dagster-integrations` | Use new name |
| `/dignified-python` | `/dignified-python` | No change |

### What Changed

**Consolidated CLI skills**: The 6 separate `/dg:*` skills are now a single `/dg` skill. Instead of invoking specific subcommands, use natural language:
- Before: `/dg:scaffold`
- After: `/dg scaffold an asset` or just `/dg` with natural language

**Renamed for clarity**:
- `/dagster-conventions` → `/dagster-best-practices` (clearer purpose)
- `/integrations-index` → `/dagster-integrations` (more discoverable)

**Flattened structure**:
- Before: `plugins/*/skills/*/SKILL.md` (nested)
- After: `skills/*/SKILL.md` (flat)

### Why These Changes?

Based on team feedback:
- **Simpler**: 4 skills instead of 9 (55% reduction)
- **More intuitive**: Natural language with `/dg` instead of remembering subcommands
- **Clearer names**: "best-practices" is clearer than "conventions"
- **Less overwhelming**: Fewer choices when installing
- **Better discoverability**: Flat structure is easier to navigate

### Update Your Workflow

**Old workflow:**
```
/dg:create-project my-analytics
/dg:scaffold asset
/dg:launch
/dg:list
```

**New workflow:**
```
/dg create a project called my-analytics
/dg scaffold an asset
/dg launch my assets
/dg list all definitions
```

or just:
```
/dg create a project
# Claude understands natural language and routes to appropriate references
```

## Philosophy

**"At the end of the day it's all markdown"** - We keep it simple. Skills are lightweight markdown wrappers that guide AI assistants to the right reference documentation.

**LLM-friendly**: Dense references with decision trees help AI navigate to the right information quickly.

**Self-selecting**: Users naturally invoke the skill they need based on clear descriptions. No complex categorization required.

**Discovery-first**: Encourage discovery workflows (`dg list components`) before scaffolding.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Version History

- **v0.0.7** (2026-01-30): Simplified structure - 9 skills → 4 skills, flat organization
- **v0.0.6** (2026-01-27): Previous version with plugin-based organization

<div align="center">
  <img alt="dagster logo" src="https://github.com/user-attachments/assets/6fbf8876-09b7-4f4a-8778-8c0bb00c5237" width="auto" height="16px">
</div>
