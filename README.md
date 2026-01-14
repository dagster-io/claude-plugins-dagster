# Claude Marketplace for Dagster

A collection of Claude Code plugins for working with Dagster.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add dagster-io/dagster-claude-plugins
```

Install a plugin:

```
/plugin install dg@claude-plugins-dagster
```

To update your marketplace plugins:

```
/plugin marketplace update
```

## What's included

### Commands

**dg** - Dagster CLI commands for working with runs and logs
  - `/dg:troubleshoot <run-id>` - Debug failing runs by analyzing error logs
  - `/dg:logs <run-id> [level] [limit]` - Retrieve and display logs for a run
  - `/dg:prototype <requirements>` - Build production-ready Dagster implementations with best practices, testing, and validation

### Skills

**dagster-conventions** - Comprehensive Dagster development conventions and best practices

**dagster-integrations** - Comprehensive index of 82+ Dagster integrations including cloud platforms, data warehouses, ETL tools, AI/ML, data quality, monitoring, and more

---

<div align="center">
  <img alt="dagster logo" src="https://github.com/user-attachments/assets/6fbf8876-09b7-4f4a-8778-8c0bb00c5237" width="auto" height="32px">
</div>
