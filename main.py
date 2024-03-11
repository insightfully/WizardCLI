import argparse
import configparser
from openai import OpenAI

# Read Config file
config = configparser.ConfigParser()  
config.read('config.ini')

# Assign config values to variables
explain_prompt = config.get('prompts', 'explain_prompt')
default_prompt = config.get('prompts', 'default_prompt')
base_url = config.get('server', 'base_url')
api_key = config.get('server', 'api_key')
model_temperature = config.get('model','temperature')

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
    print(query(explain_prompt,args.explain))
else:
    print(query(default_prompt,args.general))