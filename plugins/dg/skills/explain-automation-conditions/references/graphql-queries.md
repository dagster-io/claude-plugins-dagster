# GraphQL Queries for Automation Evaluation Debugging

This reference covers how to query the Dagster Plus GraphQL API to retrieve automation condition
evaluation records.

## Authentication Setup

### Config File Location

Dagster Plus credentials are stored in `~/.config/dg.toml`:

```toml
[cli.plus]
organization = "your-org"
user_token = "user:xxxxx"
default_deployment = "prod"  # optional
```

### Creating API Tokens

Generate API tokens at: `https://dagster.cloud/[your-org]/settings/tokens`

### Headers Required

GraphQL requests to Dagster Plus require these headers:

```
Dagster-Cloud-Api-Token: user:xxxxx
Dagster-Cloud-Organization: your-org
Dagster-Cloud-Deployment: prod  # optional
```

### API Endpoint

```
https://dagster.cloud/{organization}/graphql
```

## Core Queries

### 1. Get Latest Evaluations for an Asset

Query recent evaluation records for a specific asset.

**Query:**

```graphql
query GetEvaluations($assetKey: AssetKeyInput!, $limit: Int!, $cursor: String) {
  assetConditionEvaluationRecordsOrError(assetKey: $assetKey, limit: $limit, cursor: $cursor) {
    ... on AssetConditionEvaluationRecords {
      records {
        id
        evaluationId
        timestamp
        runIds
        numRequested
        startTimestamp
        endTimestamp
        isLegacy
        assetKey {
          path
        }
        rootUniqueId
        evaluationNodes {
          uniqueId
          userLabel
          expandedLabel
          operatorType
          startTimestamp
          endTimestamp
          numTrue
          numCandidates
          isPartitioned
          childUniqueIds
          entityKey {
            ... on AssetKey {
              path
            }
          }
        }
      }
    }
    ... on AutoMaterializeAssetEvaluationNeedsMigrationError {
      message
    }
  }
}
```

**Variables:**

```json
{
  "assetKey": {
    "path": ["my_asset"] // or ["namespace", "asset_name"]
  },
  "limit": 10, // number of evaluations to fetch
  "cursor": null // for pagination, use previous evaluationId
}
```

**Usage:**

- Set `limit: 1` to get only the latest evaluation
- Set `limit: 50` to see historical pattern
- Use `cursor` for pagination (pass previous evaluationId as string)

### 2. Get All Evaluations for a Specific Evaluation ID

Query all asset evaluations that happened during a specific evaluation tick (across multiple
assets).

**Query:**

```graphql
query GetEvaluationsForEvaluationId($evaluationId: ID!) {
  assetConditionEvaluationsForEvaluationId(evaluationId: $evaluationId) {
    ... on AssetConditionEvaluationRecords {
      records {
        id
        evaluationId
        timestamp
        runIds
        numRequested
        assetKey {
          path
        }
        rootUniqueId
        evaluationNodes {
          uniqueId
          userLabel
          expandedLabel
          operatorType
          numTrue
          numCandidates
          isPartitioned
          childUniqueIds
        }
      }
    }
  }
}
```

**Variables:**

```json
{
  "evaluationId": "14790330529" // string representation of evaluation ID
}
```

**Usage:**

- Useful for understanding what happened across all assets during a specific tick
- Helps identify if an evaluation affected multiple assets

### 3. Get True Partitions for a Specific Node

For partitioned assets, get the specific partition keys that were true for a condition node.

**Query:**

```graphql
query GetTruePartitions($assetKey: AssetKeyInput!, $evaluationId: ID!, $nodeUniqueId: String!) {
  truePartitionsForAutomationConditionEvaluationNode(
    assetKey: $assetKey
    evaluationId: $evaluationId
    nodeUniqueId: $nodeUniqueId
  )
}
```

**Variables:**

```json
{
  "assetKey": {
    "path": ["my_partitioned_asset"]
  },
  "evaluationId": "14790330529",
  "nodeUniqueId": "a6bf3e155627fef7c542fd37c7741b7a" // from evaluation tree
}
```

**Returns:** Array of partition keys (strings) that were true for that node.

**Usage:**

- Drill into specific nodes to see which partitions matched
- Useful for understanding partition-level behavior in complex conditions

### 4. Get Evaluation for a Specific Partition (Legacy)

Get the evaluation tree for a single partition.

**Query:**

```graphql
query GetPartitionEvaluation($assetKey: AssetKeyInput!, $partition: String!, $evaluationId: ID!) {
  assetConditionEvaluationForPartition(
    assetKey: $assetKey
    partition: $partition
    evaluationId: $evaluationId
  ) {
    rootUniqueId
    evaluationNodes {
      ... on SpecificPartitionAssetConditionEvaluationNode {
        description
        status
        uniqueId
        childUniqueIds
        entityKey {
          ... on AssetKey {
            path
          }
        }
      }
    }
  }
}
```

**Variables:**

```json
{
  "assetKey": {
    "path": ["my_partitioned_asset"]
  },
  "partition": "2024-01-29",
  "evaluationId": "14790330529"
}
```

**Usage:**

- Understand why a specific partition did or didn't materialize
- Status values: "TRUE", "FALSE", "SKIPPED"

## Response Structure

### Key Fields in Evaluation Records

- **`evaluationId`**: Unique identifier for the evaluation tick (integer as string)
- **`timestamp`**: Unix timestamp when evaluation occurred
- **`numRequested`**: Number of partitions/assets requested (0 = not materialized)
- **`runIds`**: Array of run IDs launched by this evaluation
- **`rootUniqueId`**: ID of the root node in the evaluation tree
- **`evaluationNodes`**: Array of all nodes in the evaluation tree (flattened)

### Key Fields in Evaluation Nodes

- **`uniqueId`**: Unique identifier for this condition node
- **`userLabel`**: Custom label if set via `.with_label()`
- **`expandedLabel`**: Array of strings showing the full condition description
- **`operatorType`**: `"and"`, `"or"`, `"not"`, or `"identity"`
- **`numTrue`**: Count of partitions/assets that matched this condition
- **`numCandidates`**: Count of partitions/assets evaluated (null for non-partitioned, or when all
  partitions considered)
- **`isPartitioned`**: Boolean indicating if this is a partitioned asset
- **`childUniqueIds`**: Array of child node IDs (use to traverse tree)

### Understanding numTrue and numCandidates

- **Unpartitioned assets**:
  - `numTrue`: 0 or 1
  - `numCandidates`: 0 or 1 (or null)

- **Partitioned assets**:
  - `numTrue`: Count of partitions that matched
  - `numCandidates`: Count of partitions evaluated (null if all partitions)

- **Short-circuit evaluation**:
  - When AND condition fails early: `numTrue: 0, numCandidates: 0`
  - Indicates the condition was skipped due to earlier failure

## Common Query Patterns

### Pattern 1: Check Latest Status

```
1. Query with limit=1 to get latest evaluation
2. Check numRequested (0 = didn't run, >0 = requested)
3. Examine root condition to see pass/fail
```

### Pattern 2: Historical Investigation

```
1. Query with limit=50 to see pattern over time
2. Identify evaluation where behavior changed
3. Compare passing vs failing evaluations
```

### Pattern 3: Partition-Level Debugging

```
1. Query latest evaluation for partitioned asset
2. Identify node showing unexpected numTrue count
3. Use truePartitionsForAutomationConditionEvaluationNode to get specific partitions
4. Analyze which partitions matched and why
```

## Error Handling

### Migration Error

If you receive `AutoMaterializeAssetEvaluationNeedsMigrationError`:

- Instance schedule storage doesn't support evaluations
- Run `dagster instance migrate` to enable
- Or schedule storage is not configured

### No Records

If `records` array is empty:

- Asset may not have automation condition set
- Automation condition sensor may not be enabled
- Asset may never have been evaluated yet

## Tips

- Always check `isLegacy` field - legacy evaluations use old rule-based format
- Use `cursor` for pagination through large evaluation histories
- `expandedLabel` is more readable than `userLabel` for debugging
- Convert `timestamp` to human-readable format for easier analysis
- Store `evaluationId` when you find interesting cases for later reference
