from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import json
import shutil
import subprocess
from utils import create_captioning_df_information
app = FastAPI()

# Define directories
USER_INPUT_DIR = "./user_input"
USER_OUTPUT_DIR = "./user_output"
USER_FINAL_INFO_DIR = "./user_final_info"


@app.get("/")
async def root():
    return {"message": "Processing AudioCap-Deepfake service API"}


@app.post("/process_audio/")
async def process_audio(file: UploadFile = File(...)):
    try:
        # Delete previously saved input
        for directory in [USER_INPUT_DIR, USER_OUTPUT_DIR, USER_FINAL_INFO_DIR]:
            if os.path.exists(directory):
                os.system(f'rm -rf {directory}')
            # Create new directories 
            os.makedirs(directory, exist_ok=True)
        
        # Save uploaded file
        file_path = os.path.join(USER_INPUT_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        BACKEND_DIR = os.path.dirname(os.path.abspath(__file__)) #/app dir in container

        try:
            subprocess.run(["bash", "run_cap_df_tasks.sh"], check=True)
        except subprocess.CalledProcessError:
            subprocess.run(["bash", os.path.join(BACKEND_DIR, "run_cap_df_tasks.sh")], check=True)
        # Createa JSON
        create_captioning_df_information(output_dir=USER_OUTPUT_DIR, save_dir=USER_FINAL_INFO_DIR)   
        # Load processed JSON file
        json_label_path = os.path.join(USER_FINAL_INFO_DIR, file.filename[:-4], "captioning_deepfake.json")
        if not os.path.exists(json_label_path):
            raise HTTPException(status_code=500, detail="Processed JSON file not found")
                
        # Load JSON
        with open(json_label_path, "r") as json_file:
            json_data = {"cap_df": json.load(json_file)}
        
        # Delete previously saved directory after getting JSON
        for directory in [USER_INPUT_DIR, USER_OUTPUT_DIR, USER_FINAL_INFO_DIR]:
            if os.path.exists(directory):
                os.system(f'rm -rf {directory}')
        
        return json_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
