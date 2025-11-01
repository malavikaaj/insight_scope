# InsightScope Deployment Guide

This guide covers different deployment options for the InsightScope application.

## Quick Start (Docker)

The easiest way to deploy InsightScope is using Docker:

```bash
# Clone the repository
git clone <your-repo-url>
cd insight_scope

# Run the deployment script
./deploy.sh
```

The application will be available at `http://localhost:8501`

## Manual Docker Deployment

### Prerequisites

- Docker (version 20.0 or higher)
- Docker Compose (version 2.0 or higher)

### Steps

1. **Configure Environment**
   ```bash
   cp .env.production .env
   # Edit .env with your configuration
   ```

2. **Build and Run**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Verify Deployment**
   ```bash
   curl http://localhost:8501/_stcore/health
   ```

## Configuration Options

### LLM Providers

#### GPT4All (Default - No API Key Required)
```env
LLM_PROVIDER=gpt4all
GPT4ALL_MODEL=orca-mini-3b-gguf2-q4_0.gguf
GPT4ALL_MODEL_PATH=/app/models/
```

#### OpenAI
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
```

#### Ollama
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### Other Configuration
```env
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DB_PATH=/app/vector_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Production Deployment

### Cloud Platforms

#### AWS ECS
1. Push Docker image to ECR
2. Create ECS task definition
3. Deploy to ECS service

#### Google Cloud Run
```bash
# Build and push to GCR
docker build -t gcr.io/PROJECT_ID/insight-scope .
docker push gcr.io/PROJECT_ID/insight-scope

# Deploy to Cloud Run
gcloud run deploy insight-scope \
  --image gcr.io/PROJECT_ID/insight-scope \
  --platform managed \
  --port 8501
```

#### Azure Container Instances
```bash
# Build and push to ACR
docker build -t myregistry.azurecr.io/insight-scope .
docker push myregistry.azurecr.io/insight-scope

# Deploy to ACI
az container create \
  --resource-group myResourceGroup \
  --name insight-scope \
  --image myregistry.azurecr.io/insight-scope \
  --ports 8501
```

### Kubernetes Deployment

Create `k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: insight-scope
spec:
  replicas: 2
  selector:
    matchLabels:
      app: insight-scope
  template:
    metadata:
      labels:
        app: insight-scope
    spec:
      containers:
      - name: insight-scope
        image: insight-scope:latest
        ports:
        - containerPort: 8501
        env:
        - name: LLM_PROVIDER
          value: "gpt4all"
---
apiVersion: v1
kind: Service
metadata:
  name: insight-scope-service
spec:
  selector:
    app: insight-scope
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
```

## Monitoring and Maintenance

### Health Checks
- Health endpoint: `http://localhost:8501/_stcore/health`
- Docker health check included in Dockerfile

### Logs
```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f insight-scope
```

### Updates
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose build
docker-compose up -d
```

### Backup
Important directories to backup:
- `vector_db/` - Vector database
- `data/` - Uploaded documents
- `.env` - Configuration

## Troubleshooting

### Common Issues

1. **Port 8501 already in use**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8502:8501"
   ```

2. **GPT4All model download fails**
   - Check internet connection
   - Verify model name in `.env`
   - Check disk space

3. **Memory issues**
   - Reduce model size
   - Increase Docker memory limits
   - Use lighter embedding models

### Performance Optimization

1. **Use GPU acceleration** (if available)
   ```yaml
   # In docker-compose.yml
   deploy:
     resources:
       reservations:
         devices:
           - driver: nvidia
             count: 1
             capabilities: [gpu]
   ```

2. **Optimize model selection**
   - Smaller models for faster inference
   - Larger models for better quality

3. **Scale horizontally**
   - Use load balancer
   - Deploy multiple instances
   - Implement session affinity

## Security Considerations

1. **Environment Variables**
   - Never commit `.env` files
   - Use secrets management in production

2. **Network Security**
   - Use HTTPS in production
   - Implement authentication if needed
   - Restrict network access

3. **Container Security**
   - Use non-root user in container
   - Scan images for vulnerabilities
   - Keep base images updated

## Support

For issues and questions:
1. Check the logs first
2. Review this documentation
3. Check GitHub issues
4. Create a new issue with logs and configuration