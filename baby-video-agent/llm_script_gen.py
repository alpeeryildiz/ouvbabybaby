import os
import json
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

template = PromptTemplate.from_template("""
You are a children's scriptwriter for a baby video series.

Characters:
{characters}
Context: {character_traits}

Generate a script for the topic "{topic}".
Structure it into short scenes with narration.
Use this format:
Scene 1: ...
Narration: ...
""")

def load_character_memory(characters):
    memory = {}
    with open("memory.json", "r") as f:
        all_mem = json.load(f)
    for c in characters.split(" and "):
        info = all_mem.get(c.strip(), {})
        memory[c.strip()] = info
    return memory

def format_traits(memory_dict):
    traits = []
    for char, mem in memory_dict.items():
        t = ', '.join(mem.get("traits", []))
        traits.append(f"{char} is {t}")
    return ". ".join(traits)

def generate_script(topic: str, characters: str) -> str:
    mem = load_character_memory(characters)
    traits_str = format_traits(mem)
    full_prompt = template | llm
    return full_prompt.invoke({
        "topic": topic,
        "characters": characters,
        "character_traits": traits_str
    }).content
