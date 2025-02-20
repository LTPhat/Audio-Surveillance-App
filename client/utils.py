import time


def generate_system_prompt(audio_data):
    metadata = audio_data['information']
    labels = audio_data['labels']

    # prompt = "You are a chatbot designed to perform information retrieval tasks based on provided information related to an audio recording." + \
    #          "\nGiven the following extracted information about an audio recording: \n"

    prompt = ""

    # Add metadata
    prompt += f"'duration': {metadata['duration']} seconds\n"
    prompt += f"'sample_rate': {metadata['sample_rate']} Khz\n"
    prompt += f"'channels': {metadata['channels']}\n"

    # Add labels
    for label, data in labels.items():
        prompt += f"'{label}':\n"
        if isinstance(data, dict):
            for time_range, value in data.items():
                prompt += f"- [{time_range}]: {repr(value)}\n"
        elif isinstance(data, list):
            prompt += f"- {repr(data)}\n"
        else:
            prompt += f"- {repr(data)}\n"
        prompt += "\n"

    return prompt

def allowed_file(filename):
    """
    Check wav input format
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['wav']

# Streamed response emulator
def response_generator(str):
    for word in str.split():
        yield word + " "
        time.sleep(0.1)
