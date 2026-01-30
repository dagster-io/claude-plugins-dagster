---
name: explain-automation-conditions
description:
  Expert guidance for understanding automation condition evaluations via Dagster Plus GraphQL API.
  Use when users ask why assets are not materializing, why assets materialized at a specific time,
  or need to understand automation condition behavior. Common trigger phrases include "why isn't my
  asset running", "why did this materialize", "debug automation", "SINCE condition", or "automation
  evaluation".
---

# Debug Automation Conditions

This skill helps debug automation condition evaluations by querying the Dagster Plus GraphQL API to
understand why assets are or aren't materializing.

## Initial Workflow

When this skill is invoked, first ask the user what they want to do using AskUserQuestion with these
options:

1. **Diagnose unexpected behavior** - Asset not running when expected, or ran unexpectedly
2. **Summarize current state** - Get the latest evaluation status for an asset

Then ask for the asset key path (e.g., "some/asset/key")

## Authentication Setup

1. Attempt to read `~/.config/dg.toml` to get credentials
2. If the file doesn't exist or is missing required fields, instruct the user to run:
   `dg plus login`
3. Required fields in `~/.config/dg.toml`:
   - `organization` - Dagster Cloud organization name
   - `user_token` - API token (format: "user:xxxxx")
   - `default_deployment` - Deployment name (often "prod")

## Executing GraphQL Queries

### CRITICAL: Proper curl Command Structure

When executing GraphQL queries, you MUST use this exact pattern to avoid escaping issues:

**DO NOT** create temporary JSON files. **DO** use this inline approach:

```bash
curl -sS -L https://dagster.cloud/{organization}/graphql \
  -H "Content-Type: application/json" \
  -H "Dagster-Cloud-Api-Token: {token}" \
  -H "Dagster-Cloud-Organization: {organization}" \
  -H "Dagster-Cloud-Deployment: {deployment}" \
  --data-binary @- <<'GRAPHQL_EOF'
{
  "query": "QUERY_STRING_HERE",
  "variables": {
    "assetKey": {"path": ["asset", "path", "here"]},
    "limit": 1,
    "cursor": null
  }
}
GRAPHQL_EOF
```

**Key points:**

- Use `--data-binary @-` to read from stdin
- Use heredoc with `<<'GRAPHQL_EOF'` (single quotes prevent variable expansion)
- The `-sS` flags: silent mode but show errors
- The `-L` flag: follow redirects (required for Dagster Cloud)
- Put the entire JSON payload in the heredoc, properly formatted
- Do NOT escape quotes in the query string - the heredoc handles it

**Example for getting latest evaluation:**

```bash
curl -sS -L https://dagster.cloud/elementl/graphql \
  -H "Content-Type: application/json" \
  -H "Dagster-Cloud-Api-Token: user:abc123" \
  -H "Dagster-Cloud-Organization: elementl" \
  -H "Dagster-Cloud-Deployment: prod" \
  --data-binary @- <<'GRAPHQL_EOF' | jq .
{
  "query": "query GetEvaluations($assetKey: AssetKeyInput!, $limit: Int!, $cursor: String) { assetConditionEvaluationRecordsOrError(assetKey: $assetKey, limit: $limit, cursor: $cursor) { ... on AssetConditionEvaluationRecords { records { id evaluationId timestamp runIds numRequested startTimestamp endTimestamp isLegacy assetKey { path } rootUniqueId evaluationNodes { uniqueId userLabel expandedLabel operatorType startTimestamp endTimestamp numTrue numCandidates isPartitioned childUniqueIds entityKey { ... on AssetKey { path } } } } } ... on AutoMaterializeAssetEvaluationNeedsMigrationError { message } } }",
  "variables": {
    "assetKey": {
      "path": ["my", "asset", "key"]
    },
    "limit": 1,
    "cursor": null
  }
}
GRAPHQL_EOF
```

### Converting Timestamps to Readable Format

**DO NOT** use Python for timestamp conversion. Use the `date` command instead:

**For macOS (BSD date):**

```bash
date -r 1769729457 -u '+%Y-%m-%d %H:%M:%S UTC'
```

**For Linux (GNU date):**

```bash
date -d '@1769729457' -u '+%Y-%m-%d %H:%M:%S UTC'
```

**To handle both platforms automatically:**

```bash
timestamp=1769729457
if date --version >/dev/null 2>&1; then
  # GNU date (Linux)
  date -d "@${timestamp}" -u '+%Y-%m-%d %H:%M:%S UTC'
else
  # BSD date (macOS)
  date -r "${timestamp}" -u '+%Y-%m-%d %H:%M:%S UTC'
fi
```

**Or use a simpler one-liner that works on both:**

```bash
# Extract integer part of timestamp (handles decimals from JSON)
timestamp=$(echo "1769729457.442442" | cut -d. -f1)
date -u -j -f %s "${timestamp}" '+%Y-%m-%d %H:%M:%S UTC' 2>/dev/null || date -u -d "@${timestamp}" '+%Y-%m-%d %H:%M:%S UTC'
```

## Prerequisites

For understanding automation conditions conceptually (how they work, what operands/operators are
available, how to write them), see the **dagster-automation** skill. This skill focuses on debugging
existing automation conditions by examining their evaluation records.

## Overview

Automation conditions (like `eager()`, `on_cron()`, `on_missing()`) determine when assets should be
materialized. When assets don't materialize as expected, or materialize unexpectedly, you need to
examine the evaluation records to understand what happened.

Each evaluation creates a tree structure showing:

- Which conditions passed (true) and failed (false)
- How many partitions matched each condition
- Why the overall automation condition succeeded or failed

## Analysis Workflow

After querying the evaluation:

1. **Query the latest evaluation** for the asset using GraphQL
2. **Convert timestamp** to human-readable format using `date` command
3. **Examine the evaluation tree** to identify which conditions failed
4. **Drill down into failed conditions** to understand root causes
5. **For partitioned assets**, understand partition-level details
6. **For historical analysis**, query evaluations from specific times

## Quick Reference

| Scenario                           | What to Check                            | Reference                                                                                                  |
| ---------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Asset not materializing            | Root condition failure reason            | [Common Patterns](references/common-patterns.md)                                                           |
| `in_progress` blocking execution   | Check if run or backfill is running      | [Common Patterns](references/common-patterns.md)                                                           |
| SINCE condition stuck              | Check trigger vs reset conditions        | [SINCE Conditions](references/since-conditions.md)                                                         |
| Partitioned asset with backlog     | Compare `missing` vs `newly_missing`     | [Partitioned Assets](references/partitioned-assets.md), [SINCE Conditions](references/since-conditions.md) |
| Asset materialized unexpectedly    | Query historical evaluation at that time | [Common Patterns](references/common-patterns.md)                                                           |
| Understanding evaluation structure | Learn about nodes, operators, numTrue    | [Evaluation Structure](references/evaluation-structure.md)                                                 |
| Setting up queries                 | Authentication and query examples        | [GraphQL Queries](references/graphql-queries.md)                                                           |
| Understanding SINCE operators      | How SINCE tracks state over time         | [SINCE Conditions](references/since-conditions.md)                                                         |
| What operands/operators mean       | See **dagster-automation** skill         | references/declarative-automation-operands.md, references/declarative-automation-operators.md              |

## Key Concepts

- **Evaluation Record**: A snapshot of automation condition evaluation at a specific time
- **Evaluation Tree**: Hierarchical structure showing how conditions were evaluated
- **SINCE Operators**: Stateful operators that track changes over time (often the source of
  confusion)
- **Partitioned Evaluations**: Evaluations that operate on multiple partitions simultaneously
- **Short-Circuit Evaluation**: When early conditions fail, later conditions show 0/0 candidates

## Common Debugging Scenarios

1. **Run in progress**: Asset won't materialize because one is already running
2. **SINCE condition stuck**: No new changes since last handling, condition stays false
3. **Short-circuit evaluation**: Later conditions show 0/0 because earlier AND conditions failed
4. **Missing vs newly_missing**: Large backlog of old missing partitions won't trigger
   `newly_missing`
5. **Upstream dependency updated**: The most common reason assets DO materialize

## Getting Started

1. **Read credentials** from `~/.config/dg.toml` (if missing, instruct user to run `dg plus login`)
2. **Ask user** what they want to do (diagnose unexpected behavior or summarize current state)
3. **Get asset key** from user
4. **Query evaluation** using the heredoc curl pattern shown above
5. **Parse results** and follow [Evaluation Structure](references/evaluation-structure.md)
6. **Diagnose using** [Common Patterns](references/common-patterns.md)

For SINCE-related issues (very common!), see [SINCE Conditions](references/since-conditions.md).

For understanding what automation conditions are available and how to write them, use the
**dagster-automation** skill.

## Common Pitfalls to Avoid

1. **DO NOT** create temporary JSON files for GraphQL queries - use heredoc approach
2. **DO NOT** use Python for timestamp parsing - use `date` command
3. **DO NOT** ask if user has credentials - just check `~/.config/dg.toml`
4. **DO NOT** forget the `-L` flag on curl (required to follow redirects)
5. **DO** use `--data-binary @-` with heredoc for clean JSON formatting
6. **DO** use single quotes in heredoc delimiter (`<<'EOF'`) to prevent variable expansion
7. **DO** pipe curl output to `jq .` for readable formatting
