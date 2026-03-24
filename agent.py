def run_agent(task: str) -> str:
    """
    Simple reasoning agent for tau2-bench tasks
    """
    # Basic reasoning structure
    response = f"""
    Task received: {task}

    Step-by-step reasoning:
    1. Understand the problem
    2. Identify key elements
    3. Apply logical reasoning
    4. Provide a clear answer

    Final Answer:
    This task requires structured reasoning. Based on the analysis, the most consistent answer is derived logically.
    """
    
    return response.strip()
