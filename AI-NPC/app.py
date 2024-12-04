import gradio as gr
import requests

# Backend storage for character data
character_data = {}

# SambaNova API Configurations
API_URL = "https://api.sambanova.ai/v1/chat/completions"  # Replace with the correct endpoint
API_KEY = "d2f70592-b2a1-451b-813c-6454d7e09c4f"  # Replace with your actual API key

# Function to save identity information
def save_identity(name, pronouns, role, stage_of_life, hobbies):
    character_data["Identity"] = {
        "Name": name,
        "Pronouns": pronouns,
        "Role": role,
        "Stage of Life": stage_of_life,
        "Hobbies and Interests": hobbies,
    }
    return "Identity saved."

# Function to save description information
def save_description(core_desc, flaws, motivations):
    character_data["Description"] = {
        "Core Description": core_desc,
        "Flaws": flaws,
        "Motivations": motivations,
    }
    return "Description saved."

# Function to save scene information
def save_scene(scene_name, scene_desc, scene_trigger):
    character_data["Scene"] = {
        "Scene Name": scene_name,
        "Description": scene_desc,
        "Trigger": scene_trigger,
    }
    return "Scene saved."

# Function to save mood and personality information
def save_mood_personality(sadness, joy, anger, fear, disgust, trust, 
                          negative, positive, aggressive, peaceful, cautious, open_trait):
    character_data["Mood & Personality"] = {
        "Mood": {
            "Sadness": sadness,
            "Joy": joy,
            "Anger": anger,
            "Fear": fear,
            "Disgust": disgust,
            "Trust": trust,
        },
        "Personality": {
            "Negative": negative,
            "Positive": positive,
            "Aggressive": aggressive,
            "Peaceful": peaceful,
            "Cautious": cautious,
            "Open": open_trait,
        },
    }
    return "Mood & Personality saved."
# Function to send character data to SambaNova and ask a question
def analyze_character_and_chat(question):
    # Check if all character data is filled
    if not all([character_data.get("Identity"), character_data.get("Description"), character_data.get("Scene"), character_data.get("Mood & Personality")]):
        return "Please complete all sections (Identity, Description, Scene, Mood & Personality) before asking a question."
    
    # Headers for API authentication
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Determine the length of the question and create the appropriate prompt
    question_length = len(question.split())

    # Constructing the prompt based on question length
    npc_prompt = (
        f"Character Details:\n"
        f"Identity: {character_data.get('Identity', {})}\n"
        f"Description: {character_data.get('Description', {})}\n"
        f"Scene: {character_data.get('Scene', {})}\n"
        f"Mood & Personality: {character_data.get('Mood & Personality', {})}\n\n"
        f"Consider this information as the character's context and respond as the character.\n\n"
    )

    # Adjust the level of detail in the response based on question length
    if question_length <= 5:  # Short question
        npc_prompt += f"Provide a concise response to the following question: {question}"
    else:  # Long question
        npc_prompt += f"Provide a detailed response to the following question: {question}"

    # API payload
    payload = {
        "model": "Meta-Llama-3.1-8B-Instruct",  # Update to the correct model if needed
        "messages": [{"role": "user", "content": npc_prompt}],
    }

    try:
        # Send the POST request to SambaNova API
        response = requests.post(API_URL, headers=headers, json=payload)

        # Process and return the response
        if response.status_code == 200:
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Gradio UI
with gr.Blocks(css=".gradio-container {background-color: #f0f4f8;}") as demo:
    gr.Markdown("<h1 style='text-align: center; color: #3c91e6;'>NPC Character Creator & Chat</h1>")

    # Tabs for different sections
    with gr.Tab("Character Creation"):
        # Identity Section
        with gr.Row():
            name = gr.Textbox(label="Name", placeholder="Enter the character's name")
            pronouns = gr.Dropdown(["she/her/hers", "he/him/his", "they/them/theirs"], label="Pronouns", value="she/her/hers")
            role = gr.Textbox(label="Role", placeholder="Enter the character's role")
            stage_of_life = gr.Dropdown(["Childhood", "Adulthood", "Elderhood"], label="Stage of Life", value="Adulthood")
            hobbies = gr.CheckboxGroup(["Exploring", "Trying new foods", "Telling jokes", "Spreading joy"], label="Hobbies and Interests")
        save_identity_button = gr.Button("Save Identity")
        save_identity_button.click(
            save_identity,
            inputs=[name, pronouns, role, stage_of_life, hobbies],
            outputs=[]
        )

        # Description Section
        core_desc = gr.Textbox(label="Core Description", placeholder="Enter the core description of your character")
        flaws = gr.Textbox(label="Flaws", placeholder="Enter any flaws of the character")
        motivations = gr.Textbox(label="Motivations", placeholder="Describe the character's motivations")
        save_description_button = gr.Button("Save Description")
        save_description_button.click(
            save_description,
            inputs=[core_desc, flaws, motivations],
            outputs=[]
        )

        # Scene Section
        scene_name = gr.Textbox(label="Scene Name", placeholder="Enter the name of the scene")
        scene_desc = gr.Textbox(label="Scene Description", placeholder="Describe the scene")
        scene_trigger = gr.Textbox(label="Scene Trigger", placeholder="Enter trigger for the scene")
        save_scene_button = gr.Button("Save Scene")
        save_scene_button.click(
            save_scene,
            inputs=[scene_name, scene_desc, scene_trigger],
            outputs=[]
        )

        # Mood & Personality Section
        sadness = gr.Slider(0, 10, label="Sadness", value=0)
        joy = gr.Slider(0, 10, label="Joy", value=0)
        anger = gr.Slider(0, 10, label="Anger", value=0)
        fear = gr.Slider(0, 10, label="Fear", value=0)
        disgust = gr.Slider(0, 10, label="Disgust", value=0)
        trust = gr.Slider(0, 10, label="Trust", value=0)
        negative = gr.Slider(0, 10, label="Negative", value=0)
        positive = gr.Slider(0, 10, label="Positive", value=0)
        aggressive = gr.Slider(0, 10, label="Aggressive", value=0)
        peaceful = gr.Slider(0, 10, label="Peaceful", value=0)
        cautious = gr.Slider(0, 10, label="Cautious", value=0)
        open_trait = gr.Slider(0, 10, label="Open", value=0)
        save_mood_personality_button = gr.Button("Save Mood & Personality")
        save_mood_personality_button.click(
            save_mood_personality,
            inputs=[sadness, joy, anger, fear, disgust, trust, negative, positive, aggressive, peaceful, cautious, open_trait],
            outputs=[]
        )

    with gr.Tab("Chat with NPC"):
        question = gr.Textbox(label="Ask the NPC a question", placeholder="Type a question for the NPC...")
        ask_button = gr.Button("Ask")
        npc_response = gr.Textbox(label="NPC Response", interactive=False)
        ask_button.click(
            analyze_character_and_chat,
            inputs=[question],
            outputs=[npc_response]
        )

demo.launch()
