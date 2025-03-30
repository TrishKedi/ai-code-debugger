from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

doc_model_name = "google/flan-t5-base"  # or use "flan-t5-small" if you're super resource-limited
doc_tokenizer = AutoTokenizer.from_pretrained(doc_model_name)
doc_model = AutoModelForSeq2SeqLM.from_pretrained(doc_model_name)

def generate_docs_from_code(code: str) -> str:
    prompt = f"Explain what the following Python function does:\n\n{code}\n\nAnswer:"
    
    inputs = doc_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = doc_model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=False,
        temperature=0.7
    )

    result = doc_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    print(f"Documentation result {result}")

    return result
