# SINCE Conditions: Understanding Stateful Evaluation

SINCE conditions are stateful operators that track whether a condition has become true since the
last time it was "handled". They're core to the `eager()` automation condition and are often the
source of confusion when debugging.

## What SINCE Does

The SINCE operator has two parts:

1. **Trigger condition**: The condition you want to detect
2. **Reset condition**: The condition that resets the state (called "handled")

Format: `<trigger> SINCE <reset>`

Example: `(newly_missing OR any_deps_updated) SINCE (handled)`

### Behavior

SINCE evaluates to TRUE when:

- The trigger condition has become true at least once
- AND it hasn't been reset since then

Once the reset condition becomes true, the SINCE state is cleared, and it waits for the trigger
condition again.

## Why SINCE Exists

SINCE prevents repeated execution of the same work. Without it:

```python
# Without SINCE
condition = AutomationCondition.missing()

# This would try to materialize EVERY MISSING PARTITION on EVERY EVALUATION
# For an asset with 1000 missing partitions, it would repeatedly request
# all 1000 partitions every 30 seconds!
```

With SINCE:

```python
# With SINCE
condition = AutomationCondition.newly_missing()  # which uses SINCE internally

# This only materializes partitions that became missing since last handling
# Once they're handled (requested/updated), it won't request them again
```

## Common SINCE Patterns

### Pattern 1: newly_missing

```
newly_missing = NEWLY_TRUE(missing)
              = missing SINCE (initial_evaluation)
```

Only triggers for partitions that transition from present → missing during evaluation period.

### Pattern 2: newly_updated

```
newly_updated = NEWLY_TRUE(updated)
              = updated SINCE (initial_evaluation)
```

Only triggers for assets that were updated in the current evaluation window.

### Pattern 3: eager() core condition

```
((newly_missing) OR (any_deps_updated)) SINCE (handled)
```

Where `handled` is:

```
(newly_requested) OR (newly_updated) OR (initial_evaluation)
```

This means: "Trigger if missing or deps updated, but only until we handle it (request or update)"

## The SINCE Deadlock Problem

### Scenario

You have an asset with 2377 missing partitions that have been missing for months.

```
✗ [0/1] ((newly_missing) OR (any_deps_updated)) SINCE (handled) (identity)
  ✗ [0/None] (newly_missing) OR (any_deps_updated) (or)
    ✗ [0/None] newly_missing (identity)
      ✓ [2377/None] missing (identity)  ← 2377 partitions ARE missing
    ✗ [0/None] any_deps_updated (or)
  ✗ [0/None] handled (or)
    ✗ [0/None] newly_requested (identity)
    ✗ [0/None] newly_updated (identity)
    ✗ [0/None] initial_evaluation (identity)
```

### Why It's Stuck

1. **`missing` is TRUE** for 2377 partitions
2. **BUT `newly_missing` is FALSE** - these partitions have been missing for a long time, they're
   not _newly_ missing
3. **`any_deps_updated` is FALSE** - no dependencies have updated recently
4. **So the trigger `(newly_missing OR any_deps_updated)` is FALSE**
5. **The SINCE condition stays FALSE** because the trigger never fired

### Why This Happens

The partitions became missing long ago:

- At that time, `newly_missing` would have been TRUE
- The SINCE would have been TRUE
- But nothing ever "handled" it (the asset was never requested or updated)
- Over time, those partitions are no longer "newly" missing
- Now the SINCE is stuck waiting for NEW changes, but there are none

## Diagnosing SINCE Issues

### Check 1: Is the Trigger Condition True?

Look at the immediate child of the SINCE node:

```
✗ [0/1] <trigger> SINCE <reset>
  ✗ [0/None] <trigger> ← Check this
```

If the trigger is FALSE:

- Check why it's false
- For `newly_missing`: Check if `missing` is TRUE but `newly_missing` is FALSE
- For `any_deps_updated`: Check if any dependencies exist and their state

### Check 2: Has It Ever Been Handled?

Look at the reset condition:

```
✗ [0/1] <trigger> SINCE <reset>
  ✗ [0/None] <trigger>
  ✗ [0/None] <reset> ← Check this (often "handled")
```

If `handled` is FALSE across all evaluations:

- Nothing has ever reset the SINCE
- Need to manually kickstart by materializing or requesting

### Check 3: Compare with `missing` vs `newly_missing`

```
✗ [0/None] newly_missing
  ✓ [2377/None] missing  ← Many missing, but not newly missing
```

This pattern indicates:

- Historical backlog of missing partitions
- SINCE deadlock: old missing partitions won't trigger `newly_missing`

## Fixing SINCE Deadlocks

### Solution 1: Manual Kickstart

Materialize one partition manually:

1. This sets `newly_updated` to TRUE
2. `handled` becomes TRUE (because `newly_updated` is part of `handled`)
3. This resets the SINCE state
4. Next evaluation, if there are still missing partitions or deps update, the condition can trigger

### Solution 2: Wait for Dependency Update

If the asset has upstream dependencies:

- Wait for an upstream asset to materialize
- This will set `any_deps_updated` to TRUE
- The trigger fires, SINCE becomes TRUE
- Asset materializes

### Solution 3: Change Automation Condition

If SINCE is causing persistent issues:

- Consider `AutomationCondition.on_missing()` for backfills
- Or customize the condition to not use SINCE for your use case
- Or use `on_cron()` if time-based execution is acceptable

## Understanding "handled"

The `handled` condition is:

```
(newly_requested) OR (newly_updated) OR (initial_evaluation)
```

- **`newly_requested`**: Asset was requested in the current evaluation
- **`newly_updated`**: Asset was materialized in the current evaluation
- **`initial_evaluation`**: This is the first evaluation ever for this asset

### Why initial_evaluation?

On the very first evaluation, there's no prior state, so SINCE would be stuck forever.
`initial_evaluation` allows the first evaluation to succeed.

## SINCE with Partitioned Assets

For partitioned assets, SINCE tracks state per-partition:

```
Partition "2024-01-01":
  - missing SINCE handled: TRUE (became missing, not yet handled)

Partition "2024-01-02":
  - missing SINCE handled: FALSE (already handled)
```

This allows fine-grained control: only request partitions that need attention, not all missing
partitions.

## Example: Reading SINCE in Evaluations

### Stuck SINCE

```json
{
  "uniqueId": "0d4629...",
  "expandedLabel": ["((newly_missing) OR (any_deps_updated))", "SINCE", "(handled)"],
  "operatorType": "identity", // SINCE is represented as identity
  "numTrue": 0,
  "numCandidates": 1,
  "childUniqueIds": ["4c3728...", "4db5d0..."]
}
```

Look at children:

```json
{
  "uniqueId": "4c3728...",
  "expandedLabel": ["(newly_missing)", "OR", "(any_deps_updated)"],
  "numTrue": 0  // ← Trigger is FALSE
},
{
  "uniqueId": "4db5d0...",
  "expandedLabel": ["(newly_requested)", "OR", "(newly_updated)", "OR", "..."],
  "numTrue": 0  // ← Reset is FALSE
}
```

Both children are FALSE → SINCE is stuck waiting for trigger to fire.

### Active SINCE

```json
{
  "uniqueId": "0d4629...",
  "expandedLabel": ["((newly_missing) OR (any_deps_updated))", "SINCE", "(handled)"],
  "operatorType": "identity",
  "numTrue": 1, // ← SINCE is TRUE!
  "numCandidates": 1,
  "childUniqueIds": ["4c3728...", "4db5d0..."]
}
```

Look at children:

```json
{
  "uniqueId": "4c3728...",
  "expandedLabel": ["(newly_missing)", "OR", "(any_deps_updated)"],
  "numTrue": 1  // ← Trigger fired!
},
{
  "uniqueId": "4db5d0...",
  "expandedLabel": ["(newly_requested)", "OR", "(newly_updated)", "OR", "..."],
  "numTrue": 0  // ← Not yet reset
}
```

Trigger is TRUE and reset hasn't happened yet → SINCE is TRUE, asset will materialize.

## SINCE Metadata

For SINCE conditions, evaluation nodes may include special metadata:

```json
{
  "uniqueId": "...",
  "expandedLabel": ["...", "SINCE", "..."],
  "sinceMetadata": {
    "triggerEvaluationId": "14790123456",
    "triggerTimestamp": 1769709000.0,
    "resetEvaluationId": "14790000000",
    "resetTimestamp": 1769708000.0
  }
}
```

This shows:

- When the trigger last fired
- When it was last reset
- Useful for understanding SINCE state history

## Key Takeaways

1. **SINCE prevents repeated work** by tracking state over time
2. **SINCE can get stuck** when historical conditions are true but not "newly" true
3. **Check both trigger and reset** conditions when debugging SINCE
4. **`missing` ≠ `newly_missing`**: Large difference indicates SINCE deadlock
5. **Manual kickstart** often fixes stuck SINCE by resetting the state
6. **SINCE is per-partition** for partitioned assets, allowing granular control

For more on how to compose and customize conditions with SINCE, see the **dagster-automation** skill
references on operators and customization.
