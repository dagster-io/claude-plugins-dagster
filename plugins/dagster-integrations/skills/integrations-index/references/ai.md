# AI Integrations

AI integrations for machine learning platforms, LLM APIs, and experiment tracking tools.

---

### OpenAI
**Package:** `dagster-openai` | **Support:** Dagster-supported

Integrate OpenAI's GPT models, embeddings, and other AI capabilities into data pipelines.

**Use cases:**
- Generate text with GPT models
- Create embeddings for semantic search
- Build LLM-powered data processing
- Content generation and summarization

**Quick start:**
```python
from dagster_openai import OpenAIResource

openai = OpenAIResource(
    api_key=dg.EnvVar("OPENAI_API_KEY")
)

@dg.asset
def generate_summary(openai: OpenAIResource):
    client = openai.get_client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Summarize this data..."}
        ]
    )
    return response.choices[0].message.content
```

**Docs:** https://docs.dagster.io/integrations/libraries/openai

---

### Anthropic
**Package:** `dagster-anthropic` | **Support:** Community-supported

Integrate Claude AI models for advanced language understanding and generation.

**Use cases:**
- Use Claude models for text processing
- Long-context document analysis
- AI-powered data transformation
- Content analysis and generation

**Quick start:**
```python
from dagster_anthropic import AnthropicResource

anthropic = AnthropicResource(
    api_key=dg.EnvVar("ANTHROPIC_API_KEY")
)

@dg.asset
def claude_analysis(anthropic: AnthropicResource):
    client = anthropic.get_client()
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Analyze this dataset..."}
        ]
    )
    return message.content
```

**Docs:** https://docs.dagster.io/integrations/libraries/anthropic

---

### Gemini
**Package:** `dagster-gemini` | **Support:** Community-supported

Google's multimodal AI model for text, image, and video understanding.

**Use cases:**
- Multimodal content analysis
- Image and video processing
- Document understanding
- AI-powered insights

**Quick start:**
```python
from dagster_gemini import GeminiResource

gemini = GeminiResource(
    api_key=dg.EnvVar("GOOGLE_API_KEY")
)

@dg.asset
def gemini_analysis(gemini: GeminiResource):
    client = gemini.get_client()
    response = client.generate_content(
        "Analyze this image and data..."
    )
    return response.text
```

**Docs:** https://docs.dagster.io/integrations/libraries/gemini

---

### MLflow
**Package:** `dagster-mlflow` | **Support:** Dagster-supported

Experiment tracking, model registry, and ML lifecycle management platform.

**Use cases:**
- Track ML experiments and metrics
- Version and deploy models
- Compare model performance
- Manage ML model lifecycle

**Quick start:**
```python
from dagster_mlflow import mlflow_tracking

mlflow = mlflow_tracking.configured({
    "experiment_name": "my_experiment",
    "mlflow_tracking_uri": "http://localhost:5000"
})

@dg.op(required_resource_keys={"mlflow"})
def train_model(context):
    import mlflow

    with mlflow.start_run():
        # Training code
        mlflow.log_param("learning_rate", 0.01)
        mlflow.log_metric("accuracy", 0.95)
        mlflow.sklearn.log_model(model, "model")
```

**Docs:** https://docs.dagster.io/integrations/libraries/mlflow

---

### Weights & Biases (W&B)
**Package:** `dagster-wandb` | **Support:** Community-supported

ML experiment tracking and visualization platform with advanced collaboration features.

**Use cases:**
- Track ML experiments with rich visualizations
- Compare hyperparameter configurations
- Monitor training runs in real-time
- Collaborate on ML projects

**Quick start:**
```python
from dagster_wandb import wandb_resource
import wandb

wandb_config = wandb_resource.configured({
    "api_key": {"env": "WANDB_API_KEY"},
    "project": "my-project"
})

@dg.op(required_resource_keys={"wandb"})
def train_with_wandb(context):
    run = wandb.init(project="my-project")

    # Log metrics during training
    wandb.log({"loss": 0.5, "accuracy": 0.9})

    # Save model
    wandb.save("model.pkl")
    run.finish()
```

**Docs:** https://docs.dagster.io/integrations/libraries/wandb

---

### NotDiamond
**Package:** `dagster-notdiamond` | **Support:** Community-supported

LLM routing and optimization platform for selecting the best model for each query.

**Use cases:**
- Optimize LLM selection for cost/quality
- Route queries to appropriate models
- A/B test different LLMs
- Reduce LLM costs

**Quick start:**
```python
from dagster_notdiamond import NotDiamondResource

notdiamond = NotDiamondResource(
    api_key=dg.EnvVar("NOTDIAMOND_API_KEY")
)

@dg.asset
def optimized_llm_call(notdiamond: NotDiamondResource):
    client = notdiamond.get_client()
    # NotDiamond selects the best model
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Query..."}],
        model=["gpt-4", "claude-3", "gemini-pro"]
    )
    return response.content
```

**Docs:** https://docs.dagster.io/integrations/libraries/notdiamond

---

## AI/ML Integration Selection

| Integration | Best For | Type | Cost Model |
|-------------|----------|------|------------|
| **OpenAI** | General LLM tasks | LLM API | Pay per token |
| **Anthropic** | Long-context, reasoning | LLM API | Pay per token |
| **Gemini** | Multimodal AI | LLM API | Pay per token |
| **MLflow** | Experiment tracking | Platform | Open-source |
| **W&B** | Advanced ML tracking | Platform | Freemium |
| **NotDiamond** | LLM optimization | Routing | Pay per call |

## Common Patterns

### LLM Processing Pipeline
```python
@dg.asset
def raw_data() -> list[str]:
    return ["text1", "text2", "text3"]

@dg.asset
def llm_processed_data(
    raw_data: list[str],
    openai: OpenAIResource
) -> list[str]:
    client = openai.get_client()
    results = []

    for text in raw_data:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Process: {text}"}]
        )
        results.append(response.choices[0].message.content)

    return results
```

### ML Experiment Tracking
```python
@dg.asset
def train_model(mlflow: MLflowResource):
    import mlflow

    with mlflow.start_run():
        # Log parameters
        mlflow.log_params({
            "learning_rate": 0.01,
            "batch_size": 32
        })

        # Training code
        for epoch in range(10):
            loss = train_epoch()
            mlflow.log_metric("loss", loss, step=epoch)

        # Log model
        mlflow.sklearn.log_model(model, "model")
```

### Embeddings Generation
```python
@dg.asset
def generate_embeddings(
    documents: list[str],
    openai: OpenAIResource
) -> list[list[float]]:
    client = openai.get_client()

    embeddings = []
    for doc in documents:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=doc
        )
        embeddings.append(response.data[0].embedding)

    return embeddings
```

## Tips

- **Costs**: LLM APIs can be expensive - track token usage and set budgets
- **Caching**: Cache LLM responses to avoid redundant API calls
- **Batch processing**: Process multiple items together when possible
- **Error handling**: LLM APIs can fail - implement retries and fallbacks
- **Prompts**: Version control prompts alongside code
- **Experiments**: Use MLflow/W&B to track prompt engineering iterations
- **Testing**: Use cheaper models (gpt-3.5) for development, upgrade for production
