from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_KEY)
async def debug_code(code:str):
    promt = f""" You are an experinece developer

    debug this code and 
    1) Share the clean code
    2) Share documentation

    {code}

"""
    
    response = await client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "messages": promt}],
        temperature=0.5
    )

    result = response.choices[0].message.content
    
    return {
       "llm_output": result
    }
    