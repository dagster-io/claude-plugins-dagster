# Understanding Evaluation Structure

This reference explains how automation condition evaluations are structured and how to read
evaluation trees.

## Evaluation Record

An evaluation record is a snapshot of an automation condition evaluation at a specific point in
time.

### Top-Level Fields

```json
{
  "id": "38b9447f-648b-4460-be06-5800e4568c99",  // UUID for this record
  "evaluationId": "14790330529",  // Evaluation tick ID (shared across assets)
  "timestamp": 1769709949.144791,  // Unix timestamp of evaluation
  "runIds": ["5af4ef35-647e-4e87-ba25-dc10af6a9787"],  // Runs launched
  "numRequested": 1,  // Number of partitions/assets requested
  "startTimestamp": 1769709948.45114,  // Evaluation start time
  "endTimestamp": 1769709948.5402973,  // Evaluation end time
  "isLegacy": false,  // True if using old rule-based system
  "assetKey": {"path": ["my", "asset"]},  // Asset being evaluated
  "rootUniqueId": "677e243ed57cb83fbaed10095ea96a69",  // Root node ID
  "evaluationNodes": [...]  // Flattened tree of all nodes
}
```

### Key Indicators

**Did the asset materialize?**

- `numRequested > 0`: Yes, asset was requested
- `numRequested == 0`: No, asset was not requested
- Check `runIds` for the run IDs that were launched

**When did it happen?**

- `timestamp`: When the evaluation occurred
- Convert to datetime for human-readable format

## Evaluation Tree

The evaluation tree is a hierarchical structure showing how the automation condition was evaluated.
It's returned as a flattened array in `evaluationNodes`.

### Node Structure

```json
{
  "uniqueId": "677e243ed57cb83fbaed10095ea96a69",
  "userLabel": "eager", // Custom label via .with_label()
  "expandedLabel": [
    // Human-readable description
    "(in_latest_time_window)",
    "AND",
    "(((newly_missing) OR (any_deps_updated)) SINCE (handled))"
  ],
  "operatorType": "and", // "and", "or", "not", "identity"
  "startTimestamp": 1769709948.45114,
  "endTimestamp": 1769709948.5402973,
  "numTrue": 1, // Partitions/assets that matched
  "numCandidates": 1, // Partitions/assets evaluated
  "isPartitioned": false, // Whether asset is partitioned
  "childUniqueIds": [
    // IDs of child nodes
    "2de4e7aadfa772d02135a5fab75b19bb",
    "ed746bd28c6b01d83859298678a7e111"
  ],
  "entityKey": { "path": ["my", "asset"] } // Which asset this node evaluates
}
```

### Operator Types

- **`"and"`**: All children must be true
- **`"or"`**: At least one child must be true
- **`"not"`**: Negates the child condition
- **`"identity"`**: Pass-through node (no logical operation)

### Reading numTrue and numCandidates

#### Unpartitioned Assets

```
numTrue: 0 or 1
numCandidates: 0, 1, or null
```

- `numTrue: 1, numCandidates: 1` → Condition is TRUE
- `numTrue: 0, numCandidates: 1` → Condition is FALSE
- `numTrue: 0, numCandidates: 0` → Condition was SKIPPED (short-circuit)

#### Partitioned Assets

```
numTrue: count of matching partitions
numCandidates: count of evaluated partitions (or null)
```

- `numTrue: 5, numCandidates: 10` → 5 out of 10 partitions matched
- `numTrue: 0, numCandidates: null` → 0 out of all partitions matched
- `numTrue: 2377, numCandidates: null` → 2377 partitions matched

### Short-Circuit Evaluation

When an AND condition fails early, later conditions show `0/0`:

```
✗ [0/1] (NOT (in_progress)) AND (any_deps_updated) (and)
  ✗ [0/1] NOT (in_progress) (not)
    ✓ [1/1] in_progress (identity)
  ✗ [0/0] any_deps_updated (or)  ← SKIPPED due to first failure
```

The `any_deps_updated` condition shows `0/0` because:

1. The AND requires both conditions to be true
2. The first condition `NOT (in_progress)` failed
3. No need to evaluate `any_deps_updated`, so it was skipped

## Traversing the Evaluation Tree

### Method 1: Find Root Node

```python
root_node = next(
    node for node in evaluation_nodes
    if node["uniqueId"] == root_unique_id
)
```

### Method 2: Find Child Nodes

```python
def get_children(node, all_nodes):
    return [
        n for n in all_nodes
        if n["uniqueId"] in node["childUniqueIds"]
    ]
```

### Method 3: Recursive Traversal

```python
def print_tree(node, all_nodes, indent=0):
    prefix = "  " * indent
    label = " ".join(node["expandedLabel"])
    status = "✓" if node["numTrue"] > 0 else "✗"
    print(f"{prefix}{status} [{node['numTrue']}/{node['numCandidates']}] {label}")

    for child_id in node["childUniqueIds"]:
        child = next(n for n in all_nodes if n["uniqueId"] == child_id)
        print_tree(child, all_nodes, indent + 1)
```

## Example: Reading an Evaluation

### Scenario: Asset Not Materializing

```json
{
  "evaluationId": "14791707384",
  "numRequested": 0,  ← Asset was NOT requested
  "rootUniqueId": "677e243ed57cb83fbaed10095ea96a69",
  "evaluationNodes": [
    {
      "uniqueId": "677e243ed57cb83fbaed10095ea96a69",
      "expandedLabel": ["(NOT (in_progress))", "AND", "..."],
      "operatorType": "and",
      "numTrue": 0,  ← Root condition FAILED
      "numCandidates": 1,
      "childUniqueIds": ["2de4...", "ed746..."]
    },
    {
      "uniqueId": "2de4...",
      "expandedLabel": ["NOT", "(in_progress)"],
      "operatorType": "not",
      "numTrue": 0,  ← This child FAILED
      "numCandidates": 1,
      "childUniqueIds": ["5395..."]
    },
    {
      "uniqueId": "5395...",
      "expandedLabel": ["(run_in_progress)", "OR", "(backfill_in_progress)"],
      "operatorType": "or",
      "numTrue": 1,  ← A run IS in progress!
      "numCandidates": 1,
      "childUniqueIds": ["4383...", "2eaf..."]
    }
  ]
}
```

**Analysis:**

1. Root AND condition failed (`numTrue: 0`)
2. First child `NOT (in_progress)` failed
3. Because `in_progress` is TRUE (a run is in progress)
4. This blocked the asset from materializing

### Scenario: Asset Materialized Due to Upstream Update

```json
{
  "evaluationId": "14790330529",
  "numRequested": 1,  ← Asset WAS requested
  "rootUniqueId": "677e...",
  "evaluationNodes": [
    {
      "uniqueId": "677e...",
      "operatorType": "and",
      "numTrue": 1,  ← Root condition PASSED
      "childUniqueIds": ["2de4...", "ed746..."]
    },
    {
      "uniqueId": "ed746...",
      "expandedLabel": ["(code_version_changed)", "OR", "(missing)", "OR", "(any_deps_updated)"],
      "operatorType": "or",
      "numTrue": 1,  ← This branch PASSED
      "childUniqueIds": ["3b52...", "1339...", "f868..."]
    },
    {
      "uniqueId": "f868...",
      "expandedLabel": ["ANY_DEPS_MATCH", "(purina/core/dim_compass_users ...)"],
      "operatorType": "or",
      "numTrue": 1,  ← any_deps_updated PASSED
      "childUniqueIds": ["50a1..."]
    },
    {
      "uniqueId": "50a1...",
      "expandedLabel": ["purina/core/dim_compass_users", "((newly_updated_without_root) OR ...)"],
      "numTrue": 1,  ← Upstream asset matched
      "childUniqueIds": ["3a13..."]
    },
    {
      "uniqueId": "3a13...",
      "expandedLabel": ["(newly_updated_without_root)", "OR", "(will_be_requested)"],
      "operatorType": "or",
      "numTrue": 1,
      "childUniqueIds": ["cc55...", "f9df..."]
    },
    {
      "uniqueId": "cc55...",
      "expandedLabel": ["(newly_updated)", "AND", "(NOT (executed_with_root_target))"],
      "operatorType": "and",
      "numTrue": 1,  ← newly_updated_without_root PASSED
      "childUniqueIds": ["a6bf...", "b23a..."]
    },
    {
      "uniqueId": "a6bf...",
      "expandedLabel": ["newly_updated"],
      "operatorType": "identity",
      "numTrue": 1,  ← Upstream was NEWLY UPDATED!
      "childUniqueIds": []
    }
  ]
}
```

**Analysis:**

1. Root condition passed (`numTrue: 1`)
2. The `any_deps_updated` branch passed
3. Upstream asset `purina/core/dim_compass_users` was `newly_updated`
4. This triggered the downstream asset to materialize

## Entity Keys in Evaluation Nodes

Note that `entityKey` can point to different assets when evaluating dependencies:

```json
{
  "uniqueId": "50a1...",
  "expandedLabel": ["purina/core/dim_compass_users", "..."],
  "entityKey": {"path": ["dwh_reporting", "product", "compass_users"]},
  // Still evaluating the root asset
  "childUniqueIds": ["3a13..."]
}
{
  "uniqueId": "3a13...",
  "expandedLabel": ["(newly_updated_without_root)", "OR", "..."],
  "entityKey": {"path": ["purina", "core", "dim_compass_users"]},
  // Now evaluating the upstream asset
  "childUniqueIds": ["cc55...", "f9df..."]
}
```

When traversing dependency checks, the `entityKey` switches to the upstream asset being evaluated.

## Tips for Reading Evaluations

1. **Start with numRequested**: Tells you if asset materialized
2. **Find the root node**: Use `rootUniqueId` to locate it
3. **Check root numTrue**: If 0, condition failed; if >0, condition passed
4. **Follow failures down the tree**: Find which child caused the failure
5. **Watch for 0/0 patterns**: Indicates short-circuit evaluation
6. **Check entityKey switches**: Shows when evaluating dependencies
7. **Use expandedLabel**: More readable than trying to interpret structure
8. **Look for SINCE nodes**: Often the source of confusion (see SINCE Conditions reference)
