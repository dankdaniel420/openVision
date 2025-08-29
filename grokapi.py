from groq import Groq
import os
import base64
from dotenv import load_dotenv

def query_image(base64_contentbytes: str, query: str): 
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": query,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_contentbytes}",
                        },
                    },
                ],
            }
        ],
        model="deepseek-r1-distill-llama-70b",
        temperature=0.5,
        max_completion_tokens=1024,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    return chat_completion.choices[0].message.content

def query_text(video_idea: str):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chat_completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {
                "role": "user",
                "content": f"""
Analyze the following video idea and provide a JSON output containing:
- A 'summary' of the idea rewritten in one short sentence. 
    - Keep it clear and informal. 
    - Do not add details or infer new meaning. 
    - Do not use commas.
- A boolean 'is_safe' field:
    - true if the idea is harmless, fun, and appropriate for all audiences.
    - false if the idea violates safety guidelines (violence, hate, illegal activity, explicit content, etc.).

Video Idea:
{video_idea}
"""
            }
        ],
        temperature=0.5,
        max_completion_tokens=1024,
        stream=False,
        response_format={"type": "json_object"},
        reasoning_format="hidden",
        stop=None,
    )

    return chat_completion.choices[0].message.content

def find_similar(video_idea: str, database_ideas: list[str]):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chat_completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {
                "role": "user",
                "content": f"""
Analyze the following video idea and provide a JSON output containing:
- A 'similar' field that lists the top 3 most similar ideas from the provided database of existing ideas.  
    - Do not invent new ideas.  
    - Only select from the provided list.  
    - Return up to 3 items, but fewer if fewer strong matches exist. 
    - If no ideas are similar, return an empty list.  

Video Idea:
{video_idea}

Database of existing ideas:
{database_ideas}
"""
            }
        ],
        temperature=0.5,
        max_completion_tokens=1024,
        stream=False,
        response_format={"type": "json_object"},
        reasoning_format="hidden",
        stop=None,
    )

    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    load_dotenv()
    # print(query_text("Go for a Staycation at Marina Bay Sands"))

    video_idea = "Do a dance challenge with your dog wearing costumes"

    database_ideas = [
        "Teach your dog a funny trick",
        "Dance challenge with your cat",
        "Lip sync battle with coworkers",
        "Cooking challenge with only 3 ingredients",
        "Dog fashion show in costumes"
    ]

    print(find_similar(video_idea, database_ideas))

    # Function to encode the image
    # def encode_image(image_path):
    #     with open(image_path, "rb") as image_file:
    #         return base64.b64encode(image_file.read()).decode('utf-8')

    # # Path to your image
    # image_path = "IC.jpg"

    # # Getting the base64 string
    # base64_image = encode_image(image_path)
    # print(base64_image)
    # print(query_image(base64_image, "Give the answer to the following questions in JSON format. valid? name? ic?"))