from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import re
from textwrap import dedent
from app.services.documentation_generator import generate_docs_from_code

model_name = "Salesforce/codegen-350M-mono"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def format_prompt(code: str) -> str:
    return dedent(f"""
    # Task: Fix bugs in the code and explain what it does.

    # Original Code:
    {code}

    # Fixed Code:
    """)


def parse_output(raw_output: str) -> dict:
    # print(raw_output)
    # Extract first code block as clean_code
    code_match = re.search(r"(def\s+\w+\(.*\):[\s\S]+?)(\n{2,}|\Z)", raw_output)
    doc_match = re.search(r"(#.*?[\.\n]){1,5}", raw_output)

    clean_code = code_match.group(1).strip() if code_match else "⚠️ Could not extract clean code."
    documentation = generate_docs_from_code(clean_code)

    return {
        "llm_output": clean_code,
        "documentation": documentation
    }


def debug_code(code: str) -> dict:
    prompt = format_prompt(code)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id
    )
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # print(result)
    generated = result[len(prompt):].strip()
    return parse_output(generated)
