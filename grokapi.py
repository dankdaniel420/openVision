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
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    load_dotenv()
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Path to your image
    image_path = "IC.jpg"

    # Getting the base64 string
    base64_image = encode_image(image_path)
    print(base64_image)
    print(query_image(base64_image, "Give the answer to the following questions in JSON format. valid? name? ic?"))