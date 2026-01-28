---
name: dg:prototype
description:
  Build production-ready Dagster implementations with best practices, testing, and validation. Use
  when user wants to prototype, build, implement, or create Dagster assets, pipelines, workflows, or
  data integrations.
---

# Prototype Dagster Implementation Skill

This skill helps users build production-ready Dagster implementations through natural language
requests.

## When to Use This Skill

Auto-invoke when users say:

- "prototype a dagster pipeline"
- "build a dagster workflow"
- "implement a dagster asset"
- "create a data pipeline in dagster"
- "I want to build [X] using dagster"
- "help me implement [Y] in dagster"
- "create a dagster implementation for [Z]"
- "build assets for [X]"
- "implement [X] with dagster"

## When to Use This Skill vs. Others

| If User Says...              | Use This Skill/Command                      | Why                                   |
| ---------------------------- | ------------------------------------------- | ------------------------------------- |
| "what's the best way to X"   | `/dagster-conventions`                      | Need patterns/best practices guidance |
| "which integration for X"    | `/dagster-integrations`                     | Need integration discovery            |
| "make this pythonic"         | `/dignified-python`                         | Need Python code review               |
| "prototype X pipeline"       | `/dg:prototype`                             | Need full implementation              |
| "create a new project"       | `/dg:create-project`                        | Need project initialization           |
| "create a workspace"         | `/dg:create-workspace`                      | Need workspace initialization         |
| "how do I structure my code" | `/dagster-conventions`                      | Need project structure guidance       |
| "show me dbt patterns"       | `/dagster-conventions` then `/dg:prototype` | First learn patterns, then implement  |

## How It Works

When this skill is invoked:

1. **Extract requirements** from the user's request (what they want to build)
2. **Identify any specific integrations** mentioned (e.g., Snowflake, dbt, APIs)
3. **Invoke the underlying command**: `/dg:prototype <requirements>`
4. **Handle vague requests**:
   - If requirements are too vague, ask clarifying questions
   - Extract data sources, transformations, destinations, and constraints

## Example Flows

**Clear requirements:**

```
User: "I want to build a data pipeline that loads data from Snowflake and transforms it with dbt"
→ Invoke: /dg:prototype Build a pipeline that: 1) loads data from Snowflake using dagster-snowflake, 2) transforms with dbt using dagster-dbt
```

**General request:**

```
User: "Prototype a dagster workflow for processing customer data"
→ Invoke: /dg:prototype Process customer data with appropriate transformations and validation
```

**Asset creation:**

```
User: "Create a dagster asset that fetches data from an API"
→ Invoke: /dg:prototype Create an asset that fetches data from an external API with error handling and retries
```

**Complex integration:**

```
User: "Build a pipeline that ingests from PostgreSQL, transforms with Spark, and loads to BigQuery"
→ Invoke: /dg:prototype Build a pipeline that: 1) ingests from PostgreSQL, 2) transforms with PySpark, 3) loads to BigQuery
```

**Vague request - needs clarification:**

```
User: "Help me build a data pipeline"
→ Ask: "What would you like your pipeline to do? Please describe:
  - Data source(s) (APIs, databases, files, etc.)
  - Transformations needed
  - Output destination(s)
  - Any specific integrations or constraints"
→ Wait for user response
→ Invoke: /dg:prototype <detailed-requirements>
```

## Implementation Notes

- This skill is a thin wrapper that delegates to the `/dg:prototype` command
- The command file at `commands/prototype.md` contains the actual execution logic
- The prototype command automatically leverages:
  - `dagster-conventions` skill for best practices
  - `dagster-integrations` skill for discovering appropriate integrations
- Explicit slash command invocation still works: `/dg:prototype <requirements>`
- Both natural language and explicit invocation are supported

## Integration with Other Skills

The `/dg:prototype` command works seamlessly with:

**dagster-conventions:**

- Provides best practices for asset design
- Guides testing patterns
- Ensures proper resource configuration
- Recommends project structure

**dagster-integrations:**

- Suggests appropriate integrations for use cases
- Provides integration-specific guidance
- Helps choose between similar tools (e.g., dbt vs Sling)

You don't need to manually invoke these skills - the prototype command handles it automatically.

## What Gets Built

When you invoke this skill, the prototype command will:

1. Analyze requirements and suggest appropriate patterns
2. Create production-ready assets with proper dependencies
3. Set up resources and configuration
4. Include comprehensive tests
5. Add documentation and metadata
6. Follow Dagster best practices throughout

## Related Commands

Before prototyping, users may need to:

- Use `/dg:create-project <name>` to set up a new project first
- Navigate to their existing Dagster project directory

After prototyping, users can:

- Run `dg dev` to see their implementation in the Dagster UI
- Use `pytest` to run the generated tests
- Extend the implementation with additional assets
