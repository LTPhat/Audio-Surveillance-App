# Use the official Miniconda image
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy only the requirement files first (better for caching)
COPY requirements_asc_aed.txt requirements_whisper.txt requirements_captioning_df.txt ./

# Create Conda environments separately
RUN conda create -n whisper python=3.10 -y && \
    conda create -n asc_aed python=3.12 -y && \
    conda create -n captioning_deepfake python=3.9 -y 

# Install dependencies in each Conda environment
RUN conda run -n whisper pip install --no-cache-dir -r requirements_whisper.txt --timeout 1000 && \
    conda run -n asc_aed pip install --no-cache-dir -r requirements_asc_aed.txt --timeout 1000 && \
    conda run -n captioning_deepfake pip install --no-cache-dir -r requirements_captioning_df.txt --timeout 1000

# Install FAST API and uvicorn for base conv server
RUN pip install fastapi uvicorn python-multipart

# Ensure necessary directories exist
RUN mkdir -p /app/user_input /app/user_output /app/user_final_info /app/model /app/s2t_segments

# Copy model folder from local to container 
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]