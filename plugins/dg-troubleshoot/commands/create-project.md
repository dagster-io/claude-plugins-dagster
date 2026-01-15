# Create a new Dagster project

Scaffold a new Dagster project with the recommended structure including assets, components, and tests.

**Usage:** `/dg:create-project <name>`

Parameters:
- `$1` (required): Project name or path. Use `.` to create in the current directory.

## Execution

Run the `uvx create-dagster project` command with the provided path:

    uvx create-dagster project $1

The command will:
- Create a new directory (unless using `.`)
- Generate project structure with src/, tests/, and configuration files
- Prompt to run `uv sync` to install dependencies

## Display

After successful execution, inform the user about:

1. **Project Structure Created**:
   - `src/<project_name>/` - Main source code with definitions.py
   - `src/<project_name>/defs/` - Directory for assets, resources, schedules
   - `src/<project_name>/components/` - Custom component types
   - `tests/` - Test directory
   - `pyproject.toml` - Project configuration

2. **Next Steps**:
   - Navigate to the project directory (if not using `.`)
   - Run `uv sync` to install dependencies (if not already done)
   - Start building assets with `dg scaffold defs dagster.asset defs/<name>.py`
   - Use `/dg:prototype` command for guided implementation
   - Launch the Dagster UI with `dg dev`

3. **Common Commands**:
   ```bash
   cd <project_name>    # Navigate to project
   uv sync              # Install dependencies
   dg list defs         # List all definitions
   dg dev               # Start Dagster UI
   ```

## Error Handling

If the directory already exists, `create-dagster` will show an error. Inform the user to:
- Choose a different project name
- Remove the existing directory if intentional
- Use `.` if they want to scaffold into an existing empty directory

If the command fails, check:
- Current directory permissions
- Valid project name (avoid special characters)
- Sufficient disk space
