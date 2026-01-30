# Create a new Dagster workspace

Initialize a new Dagster workspace for managing multiple projects with shared deployments and
configuration.

**Usage:** `/dg:create-workspace <name>`

Parameters:

- `$1` (required): Workspace name or path. Use `.` to create in the current directory.

## Execution

Run the `uvx create-dagster workspace` command with the provided path:

    yes | uvx create-dagster workspace $1

The command will:

- Create a new directory (unless using `.`)
- Generate workspace structure with projects/, deployments/, and dg.toml
- Prompt to run `uv sync` to install dependencies

## Display

After successful execution, inform the user about:

1. **Workspace Structure Created**:
   - `projects/` - Directory for multiple Dagster projects
   - `deployments/local/` - Local deployment configuration
   - `deployments/local/pyproject.toml` - Dependencies for deployment
   - `dg.toml` - Workspace configuration file

2. **Next Steps**:
   - Navigate to the workspace directory (if not using `.`)
   - Create your first project with `/dg:create-project projects/<project_name>`
   - Add existing projects to the workspace by moving them to `projects/`
   - Configure deployment settings in `deployments/local/pyproject.toml`
   - Start the workspace with `dg dev` from the workspace root

3. **Workspace Benefits**:
   - **Shared deployments**: Common dependencies across projects
   - **Cross-project dependencies**: Assets can depend on assets from other projects
   - **Unified UI**: View all projects in a single Dagster UI
   - **Environment management**: Separate dev/staging/prod deployments

4. **Common Commands**:
   ```bash
   cd <workspace_name>                          # Navigate to workspace
   uvx create-dagster project projects/my-proj  # Add a new project
   dg dev                                       # Start Dagster UI for workspace
   dg list defs                                 # List all defs across projects
   ```

## Error Handling

If the directory already exists, `create-dagster` will show an error. Inform the user to:

- Choose a different workspace name
- Remove the existing directory if intentional
- Use `.` if they want to scaffold into an existing empty directory

If the command fails, check:

- Current directory permissions
- Valid workspace name (avoid special characters)
- Sufficient disk space

## When to Use Workspaces

Use a workspace when:

- Managing multiple related Dagster projects
- Sharing common dependencies across projects
- Building modular data pipelines with cross-project dependencies
- Deploying multiple projects together

Use a single project when:

- Starting with a simple implementation
- All assets belong to one logical domain
- No need for project separation
