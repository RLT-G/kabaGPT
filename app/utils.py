import tiktoken
import asyncio


async def count_tokens(prompt: str, instructions: str) -> int:
    """Мерзость для токенизации текста"""

    try:
        # cl100k_base - все остальное
        # o200k_base - gpt-4o
        tokenizer = tiktoken.get_encoding("cl100k_base")  

        prompt_tokens = tokenizer.encode(prompt)
        instructions_tokens = tokenizer.encode(instructions)

        total_tokens = len(prompt_tokens) + len(instructions_tokens) + 3  # Добавляем 3 для учета токенов системы и пользователя

        return total_tokens
    except Exception as e:
        return -1 


async def main():
    prompt = "Какой сегодня день?"
    instructions = "Ответь как можно лучше на этот запрос."
    token_count = await count_tokens(prompt, instructions)
    print(f"Общее количество токенов: {token_count}")

if __name__ == "__main__":
    asyncio.run(main())
