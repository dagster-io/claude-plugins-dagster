# Get logs for a Dagster run

Retrieve and display logs for the specified run ID.

**Usage:** `/dg:logs <run-id> [level] [limit]`

Parameters:

- `$1` (required): Run ID
- `$2` (optional): Log level filter (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `$3` (optional): Maximum number of log entries to return

## Execution

First, fetch the logs using the `dg api log get` command:

    dg api log get $1 --json

If a log level filter is provided (e.g., ERROR, WARNING), filter the logs:

    dg api log get $1 --json | jq --arg level "$2" '.logs[] | select(.level == $level)'

If a limit is specified, apply it to the results:

    dg api log get $1 --limit $3 --json

If both level and limit are provided:

    dg api log get $1 --level $2 --limit $3 --json

## Display

Parse and display the logs in a readable format showing:

1. **Timestamp** - When the log entry occurred
2. **Level** - Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
3. **Step** - Which step generated the log (if applicable)
4. **Message** - The log message content

Organize logs chronologically and highlight ERROR and CRITICAL level logs for easy identification.

If no logs are found, inform the user that the run exists but has no logs matching the criteria.
