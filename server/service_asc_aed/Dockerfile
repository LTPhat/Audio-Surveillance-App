FROM base AS service_asc_aed

WORKDIR /app

# Activate Conda and install exclusive dependencies
RUN /opt/conda/bin/conda init bash && \
    conda create -y --name asc_aed python=3.12 && \
    echo "source activate asc_aed" >> ~/.bashrc

SHELL ["/bin/bash", "--login", "-c"]

RUN pip install --no-cache-dir -r requirements_asc_aed.txt

    # Create additional directories
RUN mkdir -p /app/user_input /app/user_output /app/model 

COPY . .

CMD ["uvicorn", "asc_aed_API:app", "--host", "0.0.0.0", "--port", "8000"]