---
name: dg:create-project
description: Create a new Dagster project with recommended structure. Use when user wants to initialize, scaffold, or create a new Dagster project.
---

# Create Dagster Project Skill

This skill helps users create new Dagster projects through natural language requests.

## When to Use This Skill

Auto-invoke when users say:
- "create a dagster project"
- "initialize a dagster project"
- "scaffold a new dagster project"
- "start a new dagster project"
- "make a dagster project"
- "set up a dagster project"
- "create a new dagster project"

## How It Works

When this skill is invoked:

1. **Extract the project name** from the user's request (if provided)
2. **Invoke the underlying command**: `/dg:create-project <name>`
3. **Handle missing parameters**:
   - If user specified a name: use it directly
   - If user said "here" or "in current directory": use `.`
   - If no name provided: ask the user for the project name

## Example Flows

**User provides a name:**
```
User: "Create a dagster project called my-pipeline"
→ Invoke: /dg:create-project my-pipeline
```

**User doesn't provide a name:**
```
User: "I want to create a new dagster project"
→ Ask: "What would you like to name your Dagster project?"
→ Wait for user response
→ Invoke: /dg:create-project <user-provided-name>
```

**User wants to create in current directory:**
```
User: "Create a dagster project here"
→ Invoke: /dg:create-project .
```

**User provides a path:**
```
User: "Create a dagster project at ./my-projects/pipeline"
→ Invoke: /dg:create-project ./my-projects/pipeline
```

## Implementation Notes

- This skill is a thin wrapper that delegates to the `/dg:create-project` command
- The command file at `commands/create-project.md` contains the actual execution logic
- Explicit slash command invocation still works: `/dg:create-project <name>`
- Both natural language and explicit invocation are supported

## Related Commands

After creating a project, users may want to:
- Use `/dg:prototype <requirements>` to build their first assets
- Use `dg dev` to start the Dagster UI
- Navigate to the project directory if they created it with a name
