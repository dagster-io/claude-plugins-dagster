<div align="center">
  <img width="auto" height="38px" alt="dagster-hearts-claude" src="https://github.com/user-attachments/assets/b162dddf-6a7e-459e-be06-29d34d637650" />
</div>

# Dagster Skills

[![Lint](https://github.com/dagster-io/skills/actions/workflows/lint.yml/badge.svg)](https://github.com/dagster-io/skills/actions/workflows/lint.yml)

AI assistant skills for building workflows and data pipelines using Dagster.

**Compatible with Claude Code, OpenCode, OpenAI Codex, Pi, and other Agent Skills-compatible tools.**

## Installation

### Claude Code

Install using the
[Claude plugin marketplace](https://code.claude.com/docs/en/discover-plugins#add-from-github):

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

## Skills

### `dg`

Comprehensive skill for all `dg` CLI operations. Use natural language to interact with the Dagster
command-line tool.

**What you can do:**

- Create projects and workspaces
- Scaffold components (assets, schedules, sensors, integrations)
- Launch assets with partitions and configurations
- List definitions and discover components
- View logs and troubleshoot failures

**Examples:**

```
/dg create a new project called analytics
/dg scaffold a dbt integration
/dg launch all assets with tag:priority=high
/dg show me the logs for the last run
/dg help me debug why my asset failed
```

### `dagster-best-practices`

Expert guidance for Dagster patterns and architectural decisions.

**What you can do:**

- Learn asset design patterns (dependencies, partitions, multi-assets)
- Choose automation strategies (declarative automation, schedules, sensors)
- Understand resource patterns (database connections, API clients, env vars)
- Implement testing strategies (unit tests, integration tests, asset checks)
- Apply ETL patterns (dbt, dlt, Sling integration patterns)
- Organize project structure (single project vs workspace)

**Example questions:**

```
How should I structure my assets?
When should I use schedules vs sensors?
How do I test my data pipeline?
What's the best way to integrate dbt?
```

### `dagster-integrations`

Comprehensive catalog of 82+ Dagster integrations organized by category.

**What's included:**

- **AI & ML**: OpenAI, Anthropic, Gemini, MLflow, W&B
- **ETL/ELT**: dbt, Fivetran, Airbyte, dlt, Sling, PySpark
- **Storage**: Snowflake, BigQuery, Postgres, S3, DuckDB, Weaviate
- **Compute**: AWS, Azure, GCP, Databricks, Spark, Kubernetes
- **BI**: Looker, Tableau, PowerBI, Sigma, Hex
- **Monitoring**: Datadog, Prometheus, Papertrail
- **Alerting**: Slack, PagerDuty, MS Teams, Discord, Twilio
- **Testing**: Great Expectations, Pandera
- **Other**: Pandas, Polars

**Example questions:**

```
Which tool should I use for data warehousing?
Does Dagster support dbt?
How do I compare Snowflake vs BigQuery?
What integrations are available for ML?
```

### `dignified-python`

Production-quality Python coding standards for modern Python.

Use for general Python code quality, not Dagster-specific patterns.

**What's included:**

- Modern type syntax (list[str], str | None)
- LBYL exception handling patterns
- Pathlib operations
- Python version-specific features (3.10-3.13)
- CLI patterns (Click, argparse)
- Advanced typing patterns
- Interface design (ABC, Protocol)
- API design principles

**Example questions:**

```
Is this good Python code?
How should I annotate this function?
What's the difference between LBYL and EAFP?
Should I use pathlib or os.path?
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

<div align="center">
  <img alt="dagster logo" src="https://github.com/user-attachments/assets/6fbf8876-09b7-4f4a-8778-8c0bb00c5237" width="auto" height="16px">
</div>
