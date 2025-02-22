FROM base AS service_cap_df

WORKDIR /app

# Activate Conda and install exclusive dependencies
RUN /opt/conda/bin/conda init bash && \
    conda create -y --name asc_aed python=3.9 && \
    echo "source activate cap_df" >> ~/.bashrc

SHELL ["/bin/bash", "--login", "-c"]

RUN pip install --no-cache-dir -r requirements_captioning_df.txt

    # Create additional directories
RUN mkdir -p /app/user_input /app/user_output /app/model /app/user_final_info

COPY . .

CMD ["uvicorn", "cap_df_API:app", "--host", "0.0.0.0", "--port", "8002"]