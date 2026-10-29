import torch

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER = "./math_tutor_qwen"


print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float32
)

# model = PeftModel.from_pretrained(
#     base_model,
#     ADAPTER
# )

model.eval()

print("Model loaded!")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful mathematics tutor. "
                "Solve mathematical problems accurately. "
                "Explain the solution clearly and step by step. "
                "Always give the final answer.\n\n"
                "FORMAT RULES:\n"
                "Use Markdown for your response.\n"
                "For inline mathematics, use $...$.\n"
                "For important equations, use $$...$$.\n"
                "Never put LaTeX commands inside ordinary parentheses "
                "or square brackets.\n"
                "Example: write $144 \\div 12 = 12$, "
                "not (144 \\div 12 = 12)."
            )
        },
        {
            "role": "user",
            "content": request.message
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
            max_new_tokens=400,
            do_sample=False
        )

    generated_tokens = output[0][
        inputs["input_ids"].shape[1]:
    ]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    answer = answer.replace("\\\\(", "\\(")
    answer = answer.replace("\\\\)", "\\)")
    answer = answer.replace("\\\\[", "\\[")
    answer = answer.replace("\\\\]", "\\]")

    return ChatResponse(response=answer)