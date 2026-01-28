---
name: dg:create-workspace
description:
  Create a new Dagster workspace for managing multiple projects. Use when user wants to initialize a
  workspace, manage multiple Dagster projects together, or set up a multi-project environment.
---

# Create Dagster Workspace Skill

This skill helps users create Dagster workspaces through natural language requests.

## When to Use This Skill

Auto-invoke when users say:

- "create a dagster workspace"
- "initialize a dagster workspace"
- "set up a multi-project dagster environment"
- "create a workspace for multiple dagster projects"
- "make a dagster workspace"
- "start a new dagster workspace"
- "scaffold a dagster workspace"

## When to Use This Skill vs. Others

| If User Says...            | Use This Skill/Command  | Why                             |
| -------------------------- | ----------------------- | ------------------------------- |
| "create a workspace"       | `/dg:create-workspace`  | Multi-project workspace needed  |
| "create a project"         | `/dg:create-project`    | Single project initialization   |
| "implement X pipeline"     | `/dg:prototype`         | Add to existing project         |
| "manage multiple projects" | `/dg:create-workspace`  | Workspace for multiple projects |
| "best practices"           | `/dagster-conventions`  | Learn patterns first            |
| "which integration"        | `/dagster-integrations` | Integration discovery           |

## How It Works

When this skill is invoked:

1. **Extract the workspace name** from the user's request (if provided)
2. **Invoke the underlying command**: `/dg:create-workspace <name>`
3. **Handle missing parameters**:
   - If user specified a name: use it directly
   - If user said "here" or "in current directory": use `.`
   - If no name provided: ask the user for the workspace name

## Example Flows

**User provides a name:**

```
User: "Create a dagster workspace called my-org"
→ Invoke: /dg:create-workspace my-org
```

**User doesn't provide a name:**

```
User: "I want to set up a workspace for multiple dagster projects"
→ Ask: "What would you like to name your Dagster workspace?"
→ Wait for user response
→ Invoke: /dg:create-workspace <user-provided-name>
```

**User wants to create in current directory:**

```
User: "Create a dagster workspace here"
→ Invoke: /dg:create-workspace .
```

**User provides a path:**

```
User: "Create a dagster workspace at ./workspaces/analytics"
→ Invoke: /dg:create-workspace ./workspaces/analytics
```

## Implementation Notes

- This skill is a thin wrapper that delegates to the `/dg:create-workspace` command
- The command file at `commands/create-workspace.md` contains the actual execution logic
- Explicit slash command invocation still works: `/dg:create-workspace <name>`
- Both natural language and explicit invocation are supported

## Related Commands

After creating a workspace, users may want to:

- Use `/dg:create-project <name>` to add projects to the workspace
- Use `dg dev` to start the Dagster UI for the workspace
- Navigate to the workspace directory if they created it with a name
