# Common Debugging Patterns

This reference covers the most frequent scenarios when debugging automation conditions and how to
diagnose them.

## Pattern 1: Asset Not Materializing - Run In Progress

### Symptoms

- `numRequested: 0`
- Root condition failed
- First child of root AND is `NOT (in_progress)`

### Evaluation Tree

```
✗ [0/1] (NOT (in_progress)) AND (...) (and)
  ✗ [0/1] NOT (in_progress) (not)
    ✓ [1/1] in_progress (or)
      ✓ [1/1] run_in_progress (identity)  ← A run is active!
```

### Diagnosis

There's already a run in progress for this asset. The automation condition includes
`NOT (in_progress)` to prevent multiple simultaneous runs.

### What to Check

1. Is the run still running? Check the Dagster UI
2. Did the run fail? Check run status
3. Did the run succeed? Check if it completed recently
4. Is the run stuck? May need intervention

### Resolution

- **If run is active**: Wait for it to complete
- **If run failed**: Investigate failure, fix issue, retry
- **If run succeeded**: Check next evaluation - should materialize if conditions met
- **If run is stuck**: Cancel the run, investigate why it's stuck

### Why This Exists

The `NOT (in_progress)` check prevents launching multiple runs for the same asset simultaneously,
which could cause:

- Resource contention
- Data corruption (multiple writes)
- Wasted compute resources

## Pattern 2: Asset Not Materializing - SINCE Condition Stuck

### Symptoms

- `numRequested: 0`
- SINCE condition in evaluation tree shows `0/1`
- Trigger condition is FALSE
- Often see `missing` with high count but `newly_missing` with 0

### Evaluation Tree

```
✗ [0/1] ((newly_missing) OR (any_deps_updated)) SINCE (handled)
  ✗ [0/None] (newly_missing) OR (any_deps_updated)
    ✗ [0/None] newly_missing
      ✓ [2377/None] missing  ← Many missing, but not NEWLY missing!
    ✗ [0/None] any_deps_updated
  ✗ [0/None] handled
```

### Diagnosis

Classic SINCE deadlock: partitions have been missing for a long time, so they're no longer "newly"
missing. The SINCE operator is waiting for new changes, but none are occurring.

### What to Check

1. How many partitions are missing? (`missing` numTrue)
2. How many are newly missing? (`newly_missing` numTrue)
3. Large gap indicates historical backlog
4. Has `handled` ever been TRUE? Check historical evaluations

### Resolution

See [SINCE Conditions](since-conditions.md) for detailed resolution strategies:

1. Manual kickstart: Materialize one partition
2. Wait for upstream dependency update
3. Change automation condition if SINCE isn't appropriate

## Pattern 3: Asset Not Materializing - No Upstream Updates

### Symptoms

- `numRequested: 0`
- `any_deps_updated` is FALSE
- No `code_version_changed` or `missing`

### Evaluation Tree

```
✓ [1/1] (NOT (in_progress)) AND (...) (and)
  ✓ [1/1] NOT (in_progress) (not)
  ✗ [0/1] (code_version_changed) OR (missing) OR (any_deps_updated) (or)
    ✗ [0/1] code_version_changed
    ✗ [0/1] missing
    ✗ [0/1] any_deps_updated (or)  ← No deps updated!
```

### Diagnosis

Asset is waiting for upstream dependencies to update. Nothing is wrong - the automation condition is
working as designed.

### What to Check

1. When did upstream dependencies last materialize?
2. Do upstream dependencies have their own automation conditions?
3. Are upstream dependencies blocked?

### Resolution

- **If this is expected**: No action needed, asset will run when upstreams update
- **If upstreams should have run**: Debug the upstream assets
- **If you need to run now**: Manually materialize, or adjust automation condition

## Pattern 4: Asset Materialized - Upstream Dependency Updated

### Symptoms

- `numRequested: 1` (or more for partitioned)
- `runIds` populated
- `any_deps_updated` branch is TRUE

### Evaluation Tree

```
✓ [1/1] (NOT (in_progress)) AND (...) (and)
  ✓ [1/1] NOT (in_progress)
  ✓ [1/1] (code_version_changed) OR (missing) OR (any_deps_updated) (or)
    ✗ [0/1] code_version_changed
    ✗ [0/1] missing
    ✓ [1/1] any_deps_updated (or)
      ✓ [1/1] upstream_asset ((newly_updated_without_root) OR ...) (identity)
        ✓ [1/1] (newly_updated_without_root) OR (will_be_requested) (or)
          ✓ [1/1] newly_updated_without_root (and)
            ✓ [1/1] newly_updated (identity)  ← Upstream just updated!
```

### Diagnosis

Asset materialized because an upstream dependency was just updated. This is the standard
eager/cascade behavior.

### What to Check

1. Which upstream asset updated? Look at `entityKey` in the tree
2. When did it update? Check `timestamp` of that upstream's evaluation
3. Was this expected? Verify the dependency relationship

### Resolution

- **If expected**: No action needed, working as designed
- **If unexpected**: Check why upstream materialized, or review dependency graph

## Pattern 5: Asset Materialized - Code Version Changed

### Symptoms

- `numRequested: 1`
- `code_version_changed` is TRUE

### Evaluation Tree

```
✓ [1/1] (NOT (in_progress)) AND (...) (and)
  ✓ [1/1] NOT (in_progress)
  ✓ [1/1] (code_version_changed) OR (missing) OR (any_deps_updated) (or)
    ✓ [1/1] code_version_changed (identity)  ← Code changed!
```

### Diagnosis

Asset materialized because its code definition changed (e.g., code deployment, config change).

### What to Check

1. Was there a recent deployment?
2. Did the asset's code or config change?
3. Was this a rollback?

### Resolution

- **If expected**: No action needed
- **If unexpected**: Review recent code changes

## Pattern 6: Short-Circuit Evaluation (0/0 Pattern)

### Symptoms

- Later conditions in AND chain show `0/0`

### Evaluation Tree

```
✗ [0/1] condition_a AND condition_b (and)
  ✗ [0/1] condition_a  ← Failed
  ✗ [0/0] condition_b  ← Skipped!
```

### Diagnosis

The AND operator short-circuits: when the first condition fails, there's no need to evaluate the
second condition.

### What This Means

- `0/0` indicates the condition was skipped, not evaluated
- To understand why the asset didn't materialize, focus on the first failing condition
- The `0/0` condition might not actually have a problem

### What to Check

Focus on the first failing condition in the AND chain - that's the actual blocker.

## Pattern 7: Partitioned Asset - Partial Materialization

### Symptoms

- `numRequested: 5` (some but not all partitions)
- `numCandidates: 10` (total partitions checked)

### Evaluation Tree

```
✓ [5/10] in_latest_time_window AND (...) (and)
  ✓ [5/10] in_latest_time_window (identity)  ← Only 5 partitions in window
```

### Diagnosis

Only some partitions met the conditions. This is normal for time-partitioned assets with time
windows.

### What to Check

1. How many partitions are in the latest time window?
2. For `eager()`, only the latest partition materializes by default
3. Check `in_latest_time_window` to see partition filtering

### Resolution

- **If expected**: No action needed
- **If you want all partitions**: Use `on_missing()` or customize time window

## Pattern 8: Dependencies Missing

### Symptoms

- `NOT (any_deps_missing)` is FALSE
- `any_deps_missing` is TRUE

### Evaluation Tree

```
✗ [0/1] ... AND (NOT (any_deps_missing)) (and)
  ✗ [0/1] NOT (any_deps_missing) (not)
    ✓ [1/1] any_deps_missing (or)
      ✓ [1/1] upstream_asset (missing AND NOT will_be_requested) (identity)
```

### Diagnosis

Asset is waiting for upstream dependencies to be materialized first. The automation condition won't
trigger until dependencies are available.

### What to Check

1. Which dependencies are missing? Look at `entityKey` in failed nodes
2. Do those dependencies have automation conditions?
3. Are those dependencies blocked?

### Resolution

1. Materialize the missing dependencies first
2. Or wait for them to materialize automatically
3. Or investigate why dependencies aren't materializing

## Pattern 9: Dependencies In Progress

### Symptoms

- `NOT (any_deps_in_progress)` is FALSE
- `any_deps_in_progress` is TRUE

### Evaluation Tree

```
✗ [0/1] ... AND (NOT (any_deps_in_progress)) (and)
  ✗ [0/1] NOT (any_deps_in_progress) (not)
    ✓ [1/1] any_deps_in_progress (or)
      ✓ [1/1] upstream_asset (in_progress) (identity)
```

### Diagnosis

Asset is waiting for upstream dependencies to finish materializing. This is normal behavior to
prevent running before dependencies are ready.

### What to Check

1. Which dependencies are in progress?
2. How long have they been running?
3. Are they making progress or stuck?

### Resolution

- **If deps are running**: Wait for them to complete
- **If deps are stuck**: Investigate upstream run issues

## Debugging Workflow

### Step 1: Check numRequested

- `0` → Asset didn't materialize, investigate why
- `>0` → Asset materialized, understand what triggered it

### Step 2: Examine Root Condition

- `numTrue: 0` → Root failed, drill down
- `numTrue: >0` → Root passed, understand which branch succeeded

### Step 3: Follow Failed Conditions

- Find the first failing condition in AND chains
- Ignore `0/0` conditions (short-circuit)
- Focus on conditions with `0/1` or `0/N`

### Step 4: Identify Pattern

Match the evaluation tree to patterns above:

- Run in progress?
- SINCE stuck?
- No upstream updates?
- Dependencies missing?

### Step 5: Resolve

Apply the resolution strategy for the identified pattern.

## Quick Diagnosis Checklist

When debugging "why isn't my asset running":

- [ ] Is `numRequested: 0`? (Confirms it didn't run)
- [ ] Is root `numTrue: 0`? (Confirms root condition failed)
- [ ] Is `NOT (in_progress)` failing? → Check for active runs
- [ ] Is there a SINCE condition? → Check for SINCE deadlock
- [ ] Is `any_deps_updated` failing? → Check upstream last-update times
- [ ] Is `any_deps_missing` failing? → Materialize missing dependencies
- [ ] Is `any_deps_in_progress` failing? → Wait for upstream runs
- [ ] Are there `0/0` patterns? → Focus on earlier failures, not these

## Historical Analysis

When debugging "why DID my asset run at time X":

1. Query evaluation at that timestamp
2. Check `numRequested: >0` (confirms it ran)
3. Check `runIds` (get the actual runs)
4. Examine which branch of root condition passed
5. Common causes:
   - Upstream dependency updated (`any_deps_updated`)
   - Code version changed (`code_version_changed`)
   - Asset was missing (`missing` or `newly_missing`)
   - Cron tick fired (`in_latest_time_window` for `on_cron`)

## Tips

1. **Start with the root**: Work your way down the tree
2. **Ignore short-circuits**: `0/0` is not the problem
3. **Check SINCE first**: It's the most common source of confusion
4. **Compare evaluations**: Look at when it worked vs when it didn't
5. **Check dependencies**: Many issues are actually upstream issues
6. **Read expandedLabel**: More human-readable than structure alone
7. **Use historical queries**: Pattern over time reveals issues

For more details on specific topics:

- SINCE conditions: [SINCE Conditions](since-conditions.md)
- Evaluation structure: [Evaluation Structure](evaluation-structure.md)
- Partitioned assets: [Partitioned Assets](partitioned-assets.md)
- GraphQL queries: [GraphQL Queries](graphql-queries.md)
