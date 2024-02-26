ARG PYTHON_VERSION=3.10.9
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

# Create a directory for the model.
RUN mkdir -p /app/models

# Set the working directory in the container
WORKDIR /app

# Copy the Streamlit app, src directory, and requirements.txt into the container.
COPY Capstone/streamlit-app/main_app.py ./
COPY Capstone/src/ ./src/
COPY Capstone/requirements.txt .

# List files in /app to verify copying (optional)
RUN ls -l

# Install dependencies from requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt


# Expose the port that the application listens on.
EXPOSE 8501

# Run the Streamlit application.
CMD ["streamlit", "run", "main_app.py"]





