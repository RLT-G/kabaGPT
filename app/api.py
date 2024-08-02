import openai
import asyncio
import config


openai.api_key = config.OPAENAI_TOKEN


async def fetch_chatgpt_response(model: str, prompt: str, instructions: str, max_tokens: int = 1024) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка при получении ответа от OpenAI {e if config.DEBUG else ''}"


async def fetch_dalle_response(prompt: str, num_images: int = 1) -> str:
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=num_images,
            size="1024x1024",
            response_format="url"
        )
        
        return response['data'][0]['url']
    except Exception as e:
        return f"Ошибка при получении ответа от OpenAI {e if config.DEBUG else ''}"
                                                        

if __name__ == "__main__":
    asyncio.run(
        fetch_chatgpt_response(
            model='gpt-4o-mini',
            instructions='Ответь как можно лучше на этот вопрос',
            prompt='Ты знаешь Python?'
        )
    )