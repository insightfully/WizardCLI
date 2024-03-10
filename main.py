import argparse
from openai import OpenAI

# Point to the local server (LM Studio HTTP server)
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

explain_prompt = "Explain the linux/bash/shell/terminal command. Keep your response short yet helpful and provide the appropriate amount of short examples. get straight to the point do not repeat the question."
default_prompt = "Keep your response short yet helpful and provide the appropriate amount of examples"


def query(sysPrompt,query):
    completion = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": sysPrompt},
        {"role": "user", "content": query}
    ],
    temperature=0.7,
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