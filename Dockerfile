FROM python:3.10-slim

WORKDIR /app

# Debug: List contents of different directories
RUN echo "Contents of /:" && ls -la / && \
    echo "\nContents of current dir:" && ls -la

# Copy all files at once
COPY . .

# Debug: List contents after copy
RUN echo "\nContents after COPY:" && ls -la

# Install Python dependencies
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"] 