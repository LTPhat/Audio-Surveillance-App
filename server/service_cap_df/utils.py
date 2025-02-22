import json
import os



def create_captioning_df_information(output_dir, save_dir):
    """
    Create JSON file based on captioning-deepfake service (**Captioning and Deepfake Detection**)
    :param output_dir: Directory containing all JSON files of all tasks
    :param save_dir: Directory to save final JSON
    Examples:
    {
    "audio_captioning": [
        {
        "start": 0.0,
        "end": 3.48,
        "caption: "A person is speaking"
        "gender": "male"
        },
        {
        "start": 3.48,
        "end": 10.0,
        "caption: "A person is speaking"
        "gender": "male"
        }
        ]
    "deepfake_detection": ['Real']
    }
    """
   
        # Map file names to the respective task keys
    # Map file names to the respective task keys
    file_to_task_mapping = {
        "audio_captioning.json": "audio captioning",
        "deepfake.json": "deepfake detection"
    }
  
    for folder in os.listdir(output_dir):
        print("Processing folder: ", folder)
        folder_dir = os.path.join(output_dir, folder)
        if not os.path.isdir(os.path.join(output_dir, folder)):
            continue 
        task_data = {}
        # Process each JSON task file
        for task_file in os.listdir(folder_dir):
            task_file_path = os.path.join(folder_dir, task_file)
            if task_file in file_to_task_mapping and task_file.endswith(".json"):
                # Get task key
                task_key = file_to_task_mapping[task_file]
                with open(task_file_path, "r") as file:
                    task_data[task_key] = json.load(file)

        cap_df_infor = {"audio_captioning": None , "deepfake_detection": None}
        try:
            cap_df_infor['audio_captioning'] = task_data['audio captioning']
        except:
            cap_df_infor['audio_captioning'] = None

        try:
            cap_df_infor['deepfake_detection'] = task_data['deepfake detection']
        except:
            cap_df_infor['deepfake_detection'] = None


        save_path = os.path.join(save_dir, folder)
        print("SAVE path: ", save_path)
        if not os.path.exists(save_path):
            print("Create folder: ", save_path)
            os.makedirs(save_path)
        with open(os.path.join(save_path, "captioning_deepfake.json"), "w") as output:
            json.dump([cap_df_infor], output, indent=4)
        print(f"Save final information of file {folder} in {save_path}")
        
