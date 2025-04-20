from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
import os

# Output will be parsed into structured JSON
parser = JsonOutputParser()


llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",  # 👈 ADD THIS
    huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    temperature=0.7,
    max_new_tokens=512,
)

# PromptTemplate (with escaped curly braces in example)
prompt_template = PromptTemplate.from_template(
    """
You are a script writer for a baby educational video assistant.
Create a list of scenes, each a JSON object with:
- "narration": what the narrator says
- "scene": a short visual description (less than 1 line)

Output must be a valid JSON list like:
[
  {{"narration": "Hi! I'm Max the Dog. Today we'll learn colors!", "scene": "Max the Dog jumping in red puddle."}},
  {{"narration": "This is RED! Can you say red?", "scene": "Red circle filling the screen with sparkle animation."}}
]

Topic: {topic}
Characters: {characters}
Only return the JSON array. No commentary.
"""
)

# Combine prompt -> LLM -> parser
full_prompt = prompt_template | llm | parser

def generate_script(topic, characters):
    print(f"🧠 Generating script for: {topic} with {', '.join(characters)}")
    return full_prompt.invoke({"topic": topic, "characters": ", ".join(characters)})

