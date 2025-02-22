FROM base AS service_whisper

WORKDIR /app

# Activate Conda and install exclusive dependencies
RUN /opt/conda/bin/conda init bash && \
    conda create -y --name whisper python=3.10 && \
    echo "source activate whisper" >> ~/.bashrc

SHELL ["/bin/bash", "--login", "-c"]

RUN pip install --no-cache-dir -r requirements_whisper.txt

    # Create additional directories
RUN mkdir -p /app/user_input /app/user_output /app/model /app/user_final_info /app/s2t_segments 

COPY . .

CMD ["uvicorn", "whisper_based_API:app", "--host", "0.0.0.0", "--port", "8001"]