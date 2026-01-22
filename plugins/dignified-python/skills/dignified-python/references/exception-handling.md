---
description: Detailed exception handling patterns including B904 chaining, third-party API compatibility, and anti-patterns.
---

# Exception Handling Reference

**Read when**: Writing try/except blocks, wrapping third-party APIs, seeing `from e` or `from None`

---

## When Exceptions ARE Acceptable

Exceptions are ONLY acceptable at:

1. **Error boundaries** (CLI/API level)
2. **Third-party API compatibility** (when no alternative exists)
3. **Adding context before re-raising**

### 1. Error Boundaries

```python
# ACCEPTABLE: CLI command error boundary
@click.command("create")
@click.pass_obj
def create(ctx: ErkContext, name: str) -> None:
    """Create a worktree."""
    try:
        create_worktree(ctx, name)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: Git command failed: {e.stderr}", err=True)
        raise SystemExit(1)
```

### 2. Third-Party API Compatibility

```python
# ACCEPTABLE: Third-party API forces exception handling
def _get_bigquery_sample(sql_client, table_name):
    """
    BigQuery's TABLESAMPLE doesn't work on views.
    There's no reliable way to determine a priori whether
    a table supports TABLESAMPLE.
    """
    try:
        return sql_client.run_query(f"SELECT * FROM {table_name} TABLESAMPLE...")
    except Exception:
        return sql_client.run_query(f"SELECT * FROM {table_name} ORDER BY RAND()...")
```

> **The test for "no alternative exists"**: Can you validate or check the condition BEFORE calling the API? If yes (even using a different function/method), use LBYL. The exception only applies when the API provides NO way to determine success a priori—you literally must attempt the operation to know if it will work.

### What Does NOT Qualify as Third-Party API Compatibility

Standard library functions with known LBYL alternatives do NOT qualify:

```python
# WRONG: int() has LBYL alternative (str.isdigit)
try:
    port = int(user_input)
except ValueError:
    port = 80

# CORRECT: Check before calling
if user_input.lstrip('-+').isdigit():
    port = int(user_input)
else:
    port = 80

# WRONG: datetime.fromisoformat() can be validated first
try:
    dt = datetime.fromisoformat(timestamp_str)
except ValueError:
    dt = None

# CORRECT: Validate format before parsing
def _is_iso_format(s: str) -> bool:
    return len(s) >= 10 and s[4] == "-" and s[7] == "-"

if _is_iso_format(timestamp_str):
    dt = datetime.fromisoformat(timestamp_str)
else:
    dt = None
```

### 3. Adding Context Before Re-raising

```python
# ACCEPTABLE: Adding context before re-raising
try:
    process_file(config_file)
except yaml.YAMLError as e:
    raise ValueError(f"Failed to parse config file {config_file}: {e}") from e
```

---

## Exception Chaining (B904 Lint Compliance)

**Ruff rule B904** requires explicit exception chaining when raising inside an `except` block. This prevents losing the original traceback.

```python
# CORRECT: Chain to preserve context
try:
    parse_config(path)
except ValueError as e:
    click.echo(json.dumps({"success": False, "error": str(e)}))
    raise SystemExit(1) from e  # Preserves traceback

# CORRECT: Explicitly break chain when intentional
try:
    fetch_from_cache(key)
except KeyError:
    # Original exception is not relevant to caller
    raise ValueError(f"Unknown key: {key}") from None

# WRONG: Missing exception chain (B904 violation)
try:
    parse_config(path)
except ValueError:
    raise SystemExit(1)  # Lint error: missing 'from e' or 'from None'

# CORRECT: CLI error boundary with JSON output
try:
    result = some_operation()
except RuntimeError as e:
    click.echo(json.dumps({"success": False, "error": str(e)}))
    raise SystemExit(0) from None  # Exception is in JSON, traceback irrelevant to CLI user
```

**When to use each:**

- `from e` - Preserve original exception for debugging
- `from None` - Intentionally suppress original (e.g., transforming exception type, CLI JSON output)

---

## Exception Anti-Patterns

**Never swallow exceptions silently**

Even at error boundaries, you must at least log/warn so issues can be diagnosed:

```python
# WRONG: Silent exception swallowing
try:
    risky_operation()
except:
    pass

# WRONG: Silent swallowing even at error boundary
try:
    optional_feature()
except Exception:
    pass  # Silent - impossible to diagnose issues

# CORRECT: Let exceptions bubble up (default)
risky_operation()

# CORRECT: At error boundaries, log the exception
try:
    optional_feature()
except Exception as e:
    logging.warning("Optional feature failed: %s", e)  # Diagnosable
```

**Never use silent fallback behavior**

```python
# WRONG: Silent fallback masks failure
def process_text(text: str) -> dict:
    try:
        return llm_client.process(text)
    except Exception:
        return regex_parse_fallback(text)

# CORRECT: Let error bubble to boundary
def process_text(text: str) -> dict:
    return llm_client.process(text)
```
