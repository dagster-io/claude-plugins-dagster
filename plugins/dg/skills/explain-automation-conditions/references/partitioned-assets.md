# Partitioned Assets and Automation Conditions

This reference covers special considerations when debugging automation conditions for partitioned
assets.

## Key Differences from Unpartitioned Assets

### Evaluation Granularity

**Unpartitioned:**

- Evaluated as a single entity
- `numTrue`: 0 or 1
- `numCandidates`: 0, 1, or null

**Partitioned:**

- Evaluated per-partition
- `numTrue`: count of partitions matching condition
- `numCandidates`: count of partitions evaluated (or null if all)

### Example Comparison

**Unpartitioned Asset:**

```json
{
  "numTrue": 1, // Asset matches
  "numCandidates": 1, // 1 asset checked
  "isPartitioned": false
}
```

**Partitioned Asset:**

```json
{
  "numTrue": 5, // 5 partitions match
  "numCandidates": 10, // 10 partitions checked
  "isPartitioned": true
}
```

## Understanding Partition Counts

### numCandidates: null

When `numCandidates` is `null`, all partitions in the partitions definition were considered:

```json
{
  "numTrue": 2377,
  "numCandidates": null, // All partitions checked
  "isPartitioned": true
}
```

This commonly appears for:

- `missing` checks (checks all defined partitions)
- Root-level conditions before filtering

### numCandidates: N

When `numCandidates` is a number, only those partitions were evaluated:

```json
{
  "numTrue": 1,
  "numCandidates": 1, // Only 1 partition checked
  "isPartitioned": true
}
```

This commonly appears for:

- `in_latest_time_window` (filters to recent partitions)
- After partition filtering by time or other criteria

### numTrue vs numCandidates

```
numTrue / numCandidates
```

- `5/10`: 5 out of 10 partitions matched
- `0/1`: 0 out of 1 partition matched (condition failed)
- `2377/null`: 2377 out of all partitions matched
- `0/null`: 0 out of all partitions matched
- `0/0`: Condition was skipped (short-circuit)

## Time-Windowed Partitions

Many partitioned assets use time-based partitions (daily, hourly, etc.) with time window filtering.

### Example: in_latest_time_window

```json
{
  "uniqueId": "89e42...",
  "expandedLabel": ["in_latest_time_window"],
  "operatorType": "identity",
  "numTrue": 1, // Only 1 partition in window
  "numCandidates": null, // Checked all, filtered to 1
  "isPartitioned": true
}
```

This filters partitions to only those in the "latest" time window, which varies by partition
definition and automation condition.

### eager() Behavior with Time Partitions

The `eager()` condition, by default, only materializes the **latest partition** for time-partitioned
assets:

```
eager() includes in_latest_time_window, which for time partitions is typically:
- Daily: Today's partition
- Hourly: Current hour's partition
```

If you want to materialize older partitions, use `on_missing()` or customize `eager()`.

## Common Pattern: Large Missing Counts

### Scenario

```json
{
  "uniqueId": "60c14...",
  "expandedLabel": ["missing"],
  "numTrue": 2377, // 2377 partitions missing!
  "numCandidates": null,
  "isPartitioned": true
}
```

### What This Means

2377 partitions exist in the partition definition but don't have materializations.

### Common Causes

1. **Historical backlog**: Partition definition goes back years, but asset was recently created
2. **Data retention**: Old partition data was deleted but definition remains
3. **Never backfilled**: Asset was created but historical partitions never materialized
4. **Partition definition expanded**: Added more partitions than originally existed

### Why Asset Isn't Materializing

Even with 2377 missing partitions, the asset might not materialize if:

```json
{
  "uniqueId": "d8c6...",
  "expandedLabel": ["NEWLY_TRUE", "(missing)"],
  "numTrue": 0,  // 0 NEWLY missing (even though 2377 are missing!)
  "numCandidates": null,
  "childUniqueIds": ["60c14..."]
}
{
  "uniqueId": "60c14...",
  "expandedLabel": ["missing"],
  "numTrue": 2377,  // But 2377 ARE missing
  "numCandidates": null
}
```

**Why:** `newly_missing` is 0 because these partitions have been missing for a long time. They're
not **newly** missing, they're **historically** missing.

See [SINCE Conditions](since-conditions.md) for details on why this happens and how to fix it.

## Querying Specific Partitions

### Get True Partitions for a Node

Use the `truePartitionsForAutomationConditionEvaluationNode` query to get partition keys:

```graphql
query GetTruePartitions($assetKey: AssetKeyInput!, $evaluationId: ID!, $nodeUniqueId: String!) {
  truePartitionsForAutomationConditionEvaluationNode(
    assetKey: $assetKey
    evaluationId: $evaluationId
    nodeUniqueId: $nodeUniqueId
  )
}
```

**Returns:**

```json
["2024-01-29", "2024-01-28", "2024-01-27"]
```

**Usage:** Drill into specific nodes to see which partitions matched.

### Example Workflow

1. Query latest evaluation for partitioned asset
2. Find node with unexpected partition count (e.g., `numTrue: 5`)
3. Use `truePartitionsForAutomationConditionEvaluationNode` with that node's `uniqueId`
4. Get list of specific partitions: `["2024-01-29", "2024-01-28", ...]`
5. Investigate why those specific partitions matched

## Per-Partition Evaluation Details

For detailed analysis of a single partition, use `assetConditionEvaluationForPartition`:

```graphql
query GetPartitionEvaluation($assetKey: AssetKeyInput!, $partition: String!, $evaluationId: ID!) {
    assetConditionEvaluationForPartition(
        assetKey: $assetKey,
        partition: $partition,
        evaluationId: $evaluationId
    ) {
        rootUniqueId
        evaluationNodes {
            ... on SpecificPartitionAssetConditionEvaluationNode {
                description
                status  // "TRUE", "FALSE", or "SKIPPED"
                uniqueId
                childUniqueIds
            }
        }
    }
}
```

**Returns:** Evaluation tree where each node shows status for that specific partition.

**Usage:** Understand why partition "2024-01-29" didn't materialize while "2024-01-28" did.

## Partition-Level Dependency Checking

When evaluating upstream dependencies for partitioned assets, the evaluation checks partition
alignment:

```json
{
  "uniqueId": "f868...",
  "expandedLabel": ["ANY_DEPS_MATCH", "(upstream_asset ...)"],
  "numTrue": 1,  // 1 partition has updated upstream
  "numCandidates": 1,
  "childUniqueIds": ["50a1..."]
}
{
  "uniqueId": "50a1...",
  "expandedLabel": ["upstream_asset", "((newly_updated_without_root) OR ...)"],
  "entityKey": {"path": ["upstream", "asset"]},  // Checking upstream
  "numTrue": 1,
  "numCandidates": 1
}
```

The evaluation checks if the **corresponding partition** in the upstream asset has updated. For a
daily-partitioned downstream:

- Partition "2024-01-29" checks if upstream partition "2024-01-29" updated
- Partition "2024-01-28" checks if upstream partition "2024-01-28" updated

## Partial Materialization

It's common for only some partitions to materialize:

```json
{
  "evaluationId": "14790330529",
  "numRequested": 3, // Only 3 partitions requested
  "runIds": ["abc123..."],
  "rootUniqueId": "677e...",
  "evaluationNodes": [
    {
      "uniqueId": "677e...",
      "numTrue": 3, // Root condition true for 3 partitions
      "numCandidates": 10 // Out of 10 candidates
    }
  ]
}
```

**Interpretation:**

- 10 partitions were evaluated
- 3 partitions met all conditions
- 1 run was launched for those 3 partitions
- 7 partitions didn't meet conditions (still waiting)

## Debugging Partitioned Assets: Checklist

When partitioned asset isn't materializing:

- [ ] Check `numRequested` - how many partitions were requested?
- [ ] Check `in_latest_time_window` - is it filtering to 0 partitions?
- [ ] Check `missing` vs `newly_missing` - large gap indicates SINCE deadlock
- [ ] Check `any_deps_updated` partition counts - do upstream partitions exist?
- [ ] Use `truePartitionsForAutomationConditionEvaluationNode` to identify specific problematic
      partitions
- [ ] Query per-partition evaluation for specific partition to see detailed condition results

## Dynamic Partitions

For dynamically-partitioned assets, partition counts can change between evaluations:

```json
// Evaluation 1
{
  "numTrue": 5,
  "numCandidates": null  // 5 partitions defined
}

// Evaluation 2 (after new partition added)
{
  "numTrue": 6,
  "numCandidates": null  // Now 6 partitions defined
}
```

**Note:** `numCandidates: null` doesn't tell you how many partitions exist, just that all defined
partitions were considered.

## Backfilling Partitioned Assets

To materialize historical partitions:

### Option 1: Use on_missing()

```python
@dg.asset(automation_condition=dg.AutomationCondition.on_missing())
def my_asset():
    ...
```

This will materialize missing partitions when dependencies are available, but only for partitions
added **after** the condition was applied (not historical backlog).

### Option 2: Manual Backfill

For historical backlog, use manual backfill via UI or:

```bash
dagster asset materialize --partition-range 2024-01-01:2024-12-31 my_asset
```

### Option 3: Kickstart SINCE

Materialize one partition manually to reset SINCE state, then let automation handle the rest (if
dependencies allow).

## Tips for Partitioned Assets

1. **Check time windows first**: `in_latest_time_window` often limits which partitions are
   considered
2. **Understand missing vs newly_missing**: Critical for diagnosing SINCE deadlocks
3. **Use partition queries**: Drill into specific partitions to understand behavior
4. **Check upstream partition alignment**: Dependencies must have matching partitions
5. **Remember eager() only materializes latest**: Use `on_missing()` for backfills
6. **null candidates means "all"**: But doesn't tell you how many "all" is
7. **Partial success is normal**: Not all partitions need to materialize every evaluation

For more on SINCE conditions with partitioned assets: [SINCE Conditions](since-conditions.md) For
general debugging patterns: [Common Patterns](common-patterns.md)
