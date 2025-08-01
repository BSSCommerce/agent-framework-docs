# Install BSS Agent

This guide will walk you through installing BSS Agent, setting up the environment, and configuring the required databases.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for source installation)
- Docker and Docker Compose (for database setup)

## Installation Methods

### From PyPI (Recommended)

The easiest way to install BSS Agent is using pip:

```bash
pip install bssagent
```

### From Source Code

For development or to get the latest features:

```bash
# Clone the repository
git clone https://github.com/bssagent/bssagent.git
cd bssagent

# Install in development mode
pip install -e .
```

### Development Installation

For contributors and developers:

```bash
git clone https://github.com/bssagent/bssagent.git
cd bssagent

# Install with development dependencies
pip install -e ".[dev]"
```

### RAG Dependencies (Optional)

For full RAG (Retrieval-Augmented Generation) capabilities:

```bash
# Install RAG-specific dependencies
pip install -r requirements-rag.txt
```

## Setup Environment Variables

Create a `.env` file in your project root with the following configuration:

```env
# LLM API Keys (choose your preferred provider)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
OLLAMA_BASE_URL=http://localhost:11434

# LangSmith Tracing (optional)
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=your_project_name

# Database Configuration
# Option 1: Use separate databases for checkpointer and store
LANGGRAPH_CHECKPOINTER_TYPE=postgres
LANGGRAPH_CHECKPOINTER_USERNAME=user
LANGGRAPH_CHECKPOINTER_PASSWORD=password
LANGGRAPH_CHECKPOINTER_HOST=localhost
LANGGRAPH_CHECKPOINTER_PORT=5432
LANGGRAPH_CHECKPOINTER_DATABASE=bssagent_checkpoint

LANGGRAPH_STORE_TYPE=postgres
LANGGRAPH_STORE_USERNAME=user
LANGGRAPH_STORE_PASSWORD=password
LANGGRAPH_STORE_HOST=localhost
LANGGRAPH_STORE_PORT=5432
LANGGRAPH_STORE_DATABASE=bssagent_store

# Option 2: Use single database for all purposes
ONE_DB=1
DB_TYPE=postgres
DB_USERNAME=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bssagent

```

## Setup Database with Docker

BSS Agent supports multiple database backends. The easiest way to get started is using Docker Compose.

### Quick Database Setup

Use the provided Docker Compose file:

```bash
# Navigate to the examples directory
cd examples/dockerdbfile

# Start the databases
docker compose up -d

# Verify containers are running
docker ps
```

This will start:
- **PostgreSQL** on port 5432
- **MySQL** on port 3306  
- **Redis** on port 6379

### Manual Docker Setup

If you prefer to set up databases manually, create a `docker-compose.yml` file:

```yaml
services:
  postgres_db:
    image: postgres:14.18-bookworm
    container_name: postgres_container
    restart: always
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydatabase
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mysql_db:
    image: mysql:oracle
    container_name: mysql_container
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis_db:
    image: redis:bookworm
    container_name: redis_container
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  mysql_data:
  redis_data:
```

Then run:

```bash
docker compose up -d
```

### Database Connection Verification

Test your database connections:

**PostgreSQL:**
```bash
# From host machine
psql -h localhost -U user -d mydatabase

# From Docker container
docker exec -it postgres_container psql -U user -d mydatabase
```

**MySQL:**
```bash
# From host machine
mysql -h localhost -u user -p mydatabase

# From Docker container
docker exec -it mysql_container mysql -u user -p mydatabase
```

**Redis:**
```bash
# From host machine
redis-cli -h localhost -p 6379

# From Docker container
docker exec -it redis_container redis-cli
```

## Supported Database Types

BSS Agent supports the following database backends:

| Database | Type | Use Case |
|----------|------|----------|
| PostgreSQL | `postgres` | Checkpointer and Store |
| MySQL | `mysql` | Checkpointer and Store |
| MongoDB | `mongodb` | Checkpointer only |
| Redis | `redis` | Checkpointer and Store |
| SQLite | `sqlite` | Checkpointer and Store |

## Next Steps

After installation, you can:

1. **Run the Quick Start Example:**
   ```python
   from bssagent.core import BSSAgent
   from bssagent.environment import EnvironmentManager
   
   # Initialize environment
   env_manager = EnvironmentManager()
   env_manager.load_config()
   
   # Create agent
   agent = BSSAgent(
       name="business_agent",
       description="Business support agent",
       tools=["file_io", "api_integration", "database"]
   )
   
   # Run agent
   response = agent.run("Analyze the current business metrics")
   print(response)
   ```

2. **Explore Examples:** Check the `examples/` directory for usage examples
3. **Run Tests:** Execute `pytest` to verify your installation
4. **Read Documentation:** Visit the documentation for detailed guides

## Troubleshooting

### Common Issues

1. **Database Connection Errors:**
   - Verify Docker containers are running: `docker ps`
   - Check environment variables match Docker configuration
   - Ensure ports are not blocked by firewall

2. **API Key Errors:**
   - Verify API keys are correctly set in `.env` file
   - Check API key permissions and quotas

3. **Import Errors:**
   - Ensure you're using Python 3.8+
   - Reinstall dependencies: `pip install -r requirements.txt`

### Getting Help

- Check the [main documentation](../README.md)
- Review [examples](../examples/) for usage patterns
- Open an issue on GitHub for bugs or feature requests

