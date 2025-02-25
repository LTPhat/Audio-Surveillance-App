FROM my_base_image AS service_whisper

WORKDIR /app

# Ensure Conda is initialized and create the Conda environment
RUN /opt/conda/bin/conda init bash && \
    /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda create -y --name whisper python=3.10.15"

# Set Conda shell settings for activation
SHELL ["/bin/bash", "--login", "-c"]

COPY requirements_whisper.txt .

# Activate Conda in the same RUN command and install dependencies
RUN source /opt/conda/etc/profile.d/conda.sh && conda activate whisper && \
    conda activate whisper && \
    pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu118 --timeout 10000 && \
    pip install --no-cache-dir -r requirements_whisper.txt --timeout 1000

RUN apt update && apt install -y ffmpeg
# Create additional directories
RUN mkdir -p /app/user_input /app/user_output /app/model /app/user_final_info /app/s2t_segments 

COPY . .

# Copy the entrypoint script and make it executable - Make sure add this file to container
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

CMD ["uvicorn", "whisper_based_API:app", "--host", "0.0.0.0", "--port", "8001"]