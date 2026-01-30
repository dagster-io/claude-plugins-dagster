# Compute Integrations

Cloud platforms, container orchestration, and distributed processing frameworks for scalable
computation.

---

## Cloud Computing Services

### AWS

**Package:** `dagster-aws` | **Support:** Dagster-supported

Amazon Web Services integration covering compute services including Glue, EMR, Lambda, ECS, and
more.

**Use cases:**

- Run serverless functions with Lambda
- Execute Spark jobs on EMR clusters
- Run ETL jobs with AWS Glue
- Deploy containers on ECS
- Manage secrets with AWS Secrets Manager
- Store data in S3 (see Storage category)

**Quick start:**

```python
from dagster_aws.s3 import S3Resource

# Note: S3 storage functionality covered in Storage category
# This example shows compute-related AWS usage

@dg.asset
def aws_lambda_job():
    # Trigger AWS Lambda function
    # Integration with AWS compute services
    pass
```

**Docs:** https://docs.dagster.io/integrations/libraries/aws

---

### Azure

**Package:** `dagster-azure` | **Support:** Dagster-supported

Microsoft Azure integration focusing on compute services like Databricks and Synapse.

**Use cases:**

- Run Databricks jobs on Azure infrastructure
- Execute queries on Azure Synapse Analytics
- Deploy containerized workloads
- Integrate with Azure compute services
- Store data in Azure Blob Storage (see Storage category)

**Docs:** https://docs.dagster.io/integrations/libraries/azure

---

### GCP (Google Cloud Platform)

**Package:** `dagster-gcp` | **Support:** Dagster-supported

Google Cloud Platform services including Dataproc for Spark and Cloud Run for containers.

**Use cases:**

- Run Spark jobs on Dataproc clusters
- Deploy serverless containers on Cloud Run
- Execute cloud functions
- Manage cloud compute resources
- Store data in GCS (see Storage category)

**Docs:** https://docs.dagster.io/integrations/libraries/gcp

---

### Databricks

**Package:** `dagster-databricks` | **Support:** Dagster-supported

Unified analytics platform integration using PipesDatabricksClient to run Python code on Databricks
clusters.

**Use cases:**

- Execute notebooks on Databricks clusters
- Run Spark jobs for large-scale data processing
- Integrate ML workloads with Databricks ML
- Use Delta Lake for reliable data storage

**Quick start:**

```python
from dagster_databricks import PipesDatabricksClient

databricks = PipesDatabricksClient(
    host=dg.EnvVar("DATABRICKS_HOST"),
    token=dg.EnvVar("DATABRICKS_TOKEN")
)

@dg.asset
def databricks_job(
    context: dg.AssetExecutionContext,
    databricks: PipesDatabricksClient
):
    return databricks.run(
        context=context,
        task_key="my-task",
        cluster={"cluster_id": "1234-567890-abc123"},
        python_file="dbfs:/scripts/process.py"
    ).get_results()
```

**Docs:** https://docs.dagster.io/integrations/libraries/databricks

---

## Distributed Processing

### Spark

**Package:** `dagster-spark` | **Support:** Dagster-supported

Apache Spark integration for distributed data processing across clusters (lower-level than PySpark).

**Use cases:**

- Manage Spark jobs and sessions
- Submit Spark applications
- Configure Spark clusters
- Low-level Spark control

**Quick start:**

```python
from dagster_spark import spark_resource

spark = spark_resource.configured({
    "spark_conf": {
        "spark.executor.memory": "2g"
    }
})

@dg.op(required_resource_keys={"spark"})
def spark_job(context):
    spark_session = context.resources.spark.spark_session
    df = spark_session.read.csv("data.csv")
    return df.count()
```

**Docs:** https://docs.dagster.io/integrations/libraries/spark

---

### Dask

**Package:** `dagster-dask` | **Support:** Dagster-supported

Parallel computing library with pandas-like API for larger-than-memory datasets.

**Use cases:**

- Scale pandas code to larger datasets
- Parallel computation on single machine or cluster
- Out-of-core processing
- Alternative to Spark for Python users

**Quick start:**

```python
from dagster_dask import dask_resource
import dask.dataframe as dd

dask = dask_resource.configured({
    "cluster": {"local": {"n_workers": 4}}
})

@dg.op(required_resource_keys={"dask"})
def dask_computation(context):
    # Read larger-than-memory CSV
    df = dd.read_csv("large-file-*.csv")
    result = df.groupby("category").amount.sum().compute()
    return result
```

**Docs:** https://docs.dagster.io/integrations/libraries/dask

---

### Ray

**Package:** `dagster-ray` | **Support:** Community-supported

Distributed computing framework for scaling Python workloads and ML training.

**Use cases:**

- Distributed ML training
- Parallel hyperparameter tuning
- Scale Python functions across clusters
- Ray Serve for model serving

**Quick start:**

```python
from dagster_ray import ray_resource
import ray

ray_config = ray_resource.configured({
    "address": "auto"  # or specific Ray cluster address
})

@dg.op(required_resource_keys={"ray"})
def distributed_training(context):
    ray.init(address=context.resources.ray.address)

    @ray.remote
    def train_model(data):
        # Training logic
        return model

    results = ray.get([train_model.remote(d) for d in datasets])
    return results
```

**Docs:** https://docs.dagster.io/integrations/libraries/ray

---

## Container Orchestration

### Docker

**Package:** `dagster-docker` | **Support:** Dagster-supported

Execute code in Docker containers using Dagster Pipes for isolated and reproducible environments.

**Use cases:**

- Run Python code in isolated environments
- Use different package versions per asset
- Execute non-Python code (R, Julia, etc.)
- Reproducible computation environments

**Quick start:**

```python
from dagster_docker import PipesDockerClient

docker = PipesDockerClient()

@dg.asset
def docker_computation(
    context: dg.AssetExecutionContext,
    docker: PipesDockerClient
):
    return docker.run(
        context=context,
        image="python:3.11",
        command=["python", "script.py"]
    ).get_results()
```

**Docs:** https://docs.dagster.io/integrations/libraries/docker

---

### Kubernetes

**Package:** `dagster-k8s` | **Support:** Dagster-supported

Execute code on Kubernetes pods using Pipes for scalable cloud-native execution.

**Use cases:**

- Run jobs on Kubernetes clusters
- Scale computation horizontally
- Use spot/preemptible instances
- Cloud-native data processing

**Quick start:**

```python
from dagster_k8s import PipesK8sClient

k8s = PipesK8sClient()

@dg.asset
def k8s_job(
    context: dg.AssetExecutionContext,
    k8s: PipesK8sClient
):
    return k8s.run(
        context=context,
        image="my-image:latest",
        command=["python", "process.py"],
        namespace="data-pipelines"
    ).get_results()
```

**Docs:** https://docs.dagster.io/integrations/libraries/k8s

---

### Celery

**Package:** `dagster-celery` | **Support:** Dagster-supported

Distributed task queue for executing Dagster ops across multiple workers.

**Use cases:**

- Distribute ops across worker nodes
- Queue-based job execution
- Scale computation horizontally
- Existing Celery infrastructure

**Quick start:**

```python
from dagster_celery import celery_executor

defs = dg.Definitions(
    assets=[...],
    jobs=[
        dg.define_asset_job(
            name="celery_job",
            executor_def=celery_executor
        )
    ]
)
```

**Docs:** https://docs.dagster.io/integrations/libraries/celery

---

## Compute Platform Selection

| Platform       | Best For              | Scale        | Deployment        | Cost Model     |
| -------------- | --------------------- | ------------ | ----------------- | -------------- |
| **AWS**        | AWS ecosystem         | Large        | Cloud             | Pay-per-use    |
| **Azure**      | Microsoft ecosystem   | Large        | Cloud             | Pay-per-use    |
| **GCP**        | Google ecosystem      | Large        | Cloud             | Pay-per-use    |
| **Databricks** | Unified analytics     | Large        | Cloud             | Cluster-based  |
| **Spark**      | Big data processing   | Very Large   | Self-hosted/Cloud | Infrastructure |
| **Dask**       | Python-native scaling | Medium-Large | Self-hosted/Cloud | Infrastructure |
| **Ray**        | ML/Python workloads   | Large        | Self-hosted/Cloud | Infrastructure |
| **Docker**     | Isolated execution    | Any          | Any               | Infrastructure |
| **K8s**        | Cloud-native          | Large        | Cloud/Self-hosted | Infrastructure |
| **Celery**     | Distributed tasks     | Medium       | Self-hosted       | Infrastructure |

## Common Patterns

### Cloud Cluster Compute

```python
# Databricks, EMR, Dataproc
@dg.asset
def distributed_processing(
    context: dg.AssetExecutionContext,
    pipes_client: PipesClient
):
    return pipes_client.run(
        context=context,
        script="process_large_dataset.py",
        cluster_config={
            "num_workers": 10,
            "instance_type": "m5.xlarge"
        }
    ).get_results()
```

### Containerized Processing

```python
# Docker/K8s
@dg.asset
def containerized_job(
    context: dg.AssetExecutionContext,
    pipes_client: PipesClient
):
    return pipes_client.run(
        context=context,
        image="my-processor:v1",
        command=["python", "process.py"],
        env={"DATA_PATH": "/mnt/data"}
    ).get_results()
```

### Distributed Framework

```python
# Spark/Dask/Ray
@dg.asset
def parallel_processing(compute_resource: ComputeResource):
    # Initialize distributed framework
    client = compute_resource.get_client()

    # Distribute work across cluster
    results = client.map(process_partition, data_partitions)

    return client.gather(results)
```

## Tips

- **Cost optimization**: Use spot/preemptible instances for non-critical workloads
- **Right-sizing**: Start small and scale up based on actual resource needs
- **Monitoring**: Track compute resource utilization and costs
- **Isolation**: Use Docker/K8s for dependency isolation and reproducibility
- **Cloud choice**: Choose cloud provider based on existing infrastructure and team expertise
- **Spark vs Dask**: Dask is more Pythonic, Spark better for very large scale (>1TB)
- **Ray for ML**: Ray excels at distributing ML training and inference workloads
- **Local dev**: Test with smaller Docker containers locally before scaling to K8s/cloud
- **Caching**: Enable caching in Spark/Dask for reused DataFrames
- **Credentials**: Use environment variables or secret managers, never hardcode
