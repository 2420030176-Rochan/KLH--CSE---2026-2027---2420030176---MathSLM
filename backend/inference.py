import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


# ============================================================
# CONFIG
# ============================================================

BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER = "./math_tutor_qwen"


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    BASE_MODEL
)

print("Loading base model...")

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float32
)

print("Loading trained LoRA adapter...")

model = PeftModel.from_pretrained(
    model,
    ADAPTER
)

model.eval()

print("\nMath Tutor ready!\n")


# ============================================================
# SOLVE
# ============================================================

def solve_problem(problem):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful mathematics tutor. "
                "Solve mathematical problems accurately. "
                "Explain the solution clearly and step by step. "
                "Always give the final answer."
            )
        },
        {
            "role": "user",
            "content": problem
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=8192
    )

    with torch.no_grad():

        output = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=False
        )

    # Remove the original prompt from the output
    generated_tokens = output[
        0
    ][
        inputs["input_ids"].shape[1]:
    ]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return answer


# ============================================================
# CHAT LOOP
# ============================================================

while True:

    problem = input("Problem: ")

    if problem.lower() == "quit":
        break

    print("\nTutor:")
    print(solve_problem(problem))
    print()