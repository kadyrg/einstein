from openai import AsyncOpenAI
from fastapi.responses import StreamingResponse
from fastapi import UploadFile
import base64

from app.core import settings


class AskAI:
    def __init__(self, ai_key):
        self.client = AsyncOpenAI(api_key=ai_key)

    async def ask_question(self, course: str, chapter: str, question: str, image: UploadFile) -> StreamingResponse:
        image_bytes = await image.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        async def event_generator():
            stream = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"This is the: {course} course. the chapter is {chapter}\n. Focus on the red highlighted part. Respond with a short, direct answer. User asks:{question}"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": "auto"
                                },
                            },
                        ],
                    }
                ],
                stream=True,
                max_tokens=1000,
            )

            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    yield content
        return StreamingResponse(event_generator(), media_type="text/plain")

ask_ai = AskAI(settings.AI_KEY)
