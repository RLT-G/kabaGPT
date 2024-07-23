import openai


async def fetch_chatgpt_response(model: str, prompt: str, instructions: str, max_tokens: int = 150) -> str:
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
        return f"Ошибка при получении ответа от OpenAI {e}"
