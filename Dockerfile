# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Install uv for fast dependency management
RUN pip install uv

# Set the working directory
WORKDIR /app

# Copy dependency files first to leverage Docker cache
COPY pyproject.toml requirements.txt* ./

# Install dependencies using uv
RUN uv pip install --system -r pyproject.toml

# Copy the rest of the application code
COPY . .

# Expose Gradio's default port
EXPOSE 7860

# Specify how to run the application
# We use uv run directly as specified in the README
CMD ["uv", "run", "python", "main.py"]
