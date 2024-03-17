import argparse
import configparser
from openai import OpenAI
import re
from colorama import Fore, Style
from colorama import init
from llama_cpp import Llama
import json

# Read Config file
config = configparser.ConfigParser()  
config.read('config.ini')

# Assign config values to variables
explain_prompt = config.get('prompts', 'explain_prompt')
default_prompt = config.get('prompts', 'default_prompt')
base_url = config.get('server', 'base_url')
api_key = config.get('server', 'api_key')
model_temperature = config.get('model','temperature')
compact = config.get('output','compact')

def llama_cpp_query(sysPrompt,query):
    llm = Llama(
      model_path=path,)
    
    # Generate a completion
    llm.create_chat_completion(
      messages = [
          {"role": "system", "content": sysPrompt},
          {
              "role": "user",
              "content": query
          }
      ]
)
    
    print(llm)
    
# Point to the local server (LM Studio HTTP server)
client = OpenAI(base_url=base_url, api_key=api_key)

def query(sysPrompt,query):
    # Send completion request to LM Studio HTTP server
    completion = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": sysPrompt},
        {"role": "user", "content": query}
    ],
    temperature=model_temperature,
    )

    return completion.choices[0].message.content



# Remove junk styling automatically added by gemma
def clean_text(text):
    # Replace markdown styling with colorama colors
    cleaned_text = re.sub(r'\*\*(.*?)\*\*', f'{Fore.BLUE}\\1{Style.RESET_ALL}', text)
    cleaned_text = re.sub(r'`([^`]+)`', f'{Fore.GREEN}\\1{Style.RESET_ALL}', cleaned_text)

    # Remove code blocks
    cleaned_text = re.sub(r'```[^`]+```', '', cleaned_text)

    if compact == "True":
        # Remove extra newlines to make the response more compact
        cleaned_text = re.sub(r'\n{2,}', '\n', cleaned_text)

    return cleaned_text.strip()

# Create ArgumentParser object
parser = argparse.ArgumentParser(description='Query self-hosted AI without leaving your terminal')

# Create a mutually exclusive group
group = parser.add_mutually_exclusive_group(required=True)

# Add arguments to the group
group.add_argument('--explain', type=str, help='Query the model to explain a command')
group.add_argument('--general', type=str, help='General Query')

# Parse the arguments
args = parser.parse_args()

# Access parsed argument , determine correct system prompt and print result
if args.explain != None:
    print(clean_text(query(explain_prompt,args.explain)))
else:
    print(clean_text(query(default_prompt,args.general)))
