compose = """services:
  officeqa_agent:
    image: ghcr.io/n8vember/officeqa-purple:latest
    command: ["--host", "0.0.0.0", "--port", "9009", "--card-url", "http://officeqa_agent:9009"]
    ports:
      - "9019:9009"
    environment:
      - PYTHONUNBUFFERED=1
      - LLM_PROVIDER=${LLM_PROVIDER:-openai}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=${OPENAI_MODEL:-gpt-4o-mini}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - ANTHROPIC_MODEL=${ANTHROPIC_MODEL:-claude-opus-4-1}
      - ENABLE_WEB_SEARCH=${ENABLE_WEB_SEARCH:-false}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9009/.well-known/agent-card.json"]
      interval: 5s
      timeout: 3s
      retries: 10
      start_period: 20s
    networks:
      - agentnet

  judge:
    image: ghcr.io/arnavsinghvi11/officeqa-judge:latest
    command: ["--host", "0.0.0.0", "--port", "9009", "--card-url", "http://judge:9009"]
    ports:
      - "9009:9009"
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=INFO
    depends_on:
      officeqa_agent:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9009/.well-known/agent-card.json"]
      interval: 5s
      timeout: 3s
      retries: 10
      start_period: 20s
    networks:
      - agentnet

networks:
  agentnet:
    driver: bridge
"""

with open("docker-compose.yml", "w") as f:
    f.write(compose)

print("Generated docker-compose.yml")
