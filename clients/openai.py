import openai
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class OpenAIClient:

    # If need to accept user chat, implement this
    def sanitize_text(self, text: str) -> str:
        raise NotImplementedError
        # if '{' in text:
        #     text = text.replace('{', '{{')
        # if '}' in text:
        #     text = text.replace('}', '}}')
        # return text

    async def send_message(
        self,
        system_prompt: str,
        ai_prompt: str,
        user_prompt: str,
        model_name: str,
        frequency_penalty: int = 0,
        temperature: float = 0.9,
    ):
        """
        Send message to LLM.
        Returns the LLM's reply.
        """
        openai.api_key = OPENAI_API_KEY
        openai_prompt = []

        # Add initial prompt
        openai_prompt.append({"role": "system", "content": system_prompt})
        openai_prompt.append({"role": "assistant", "content": ai_prompt})
        openai_prompt.append({"role": "user", "content": user_prompt})

        completion = await openai.ChatCompletion.acreate(
            model=model_name,
            frequency_penalty=frequency_penalty,
            temperature=temperature,
            messages=openai_prompt,
        )

        reply = completion.choices[0].message.content 

        return {"reply": reply}


