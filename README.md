# MathSLM — AI-Powered Mathematics Tutor

An AI-powered mathematics tutoring system built using a fine-tuned Large Language Model (LLM) that solves mathematical problems and generates step-by-step explanations.

## Overview

MathSLM explores how a pretrained language model can be adapted for mathematics-focused tasks through parameter-efficient fine-tuning. The system uses **Qwen2.5-1.5B-Instruct**, fine-tuned using **LoRA (Low-Rank Adaptation)** on arithmetic examples and mathematical word problems.

Users can enter mathematical questions through a conversational web interface and receive generated solutions designed to make problem-solving easier to understand.

## Features

- **Fine-Tuned Language Model:** Adapts a pretrained instruction-following model for mathematics-focused tasks.
- **Step-by-Step Solutions:** Generates explanations that break mathematical problems into understandable steps.
- **Word Problem Solving:** Handles natural-language mathematics questions.
- **Custom Arithmetic Dataset:** Incorporates approximately 100,000 sampled arithmetic examples.
- **Parameter-Efficient Fine-Tuning:** Uses LoRA to adapt the model without updating all its parameters.
- **Interactive Web Interface:** Provides a conversational interface for submitting questions and viewing answers.
- **Local Inference:** Supports running the model locally without requiring a paid LLM API.

## Technology Stack

| Component | Technology |
|---|---|
| Base Model | Qwen2.5-1.5B-Instruct |
| Fine-Tuning | LoRA |
| Model Training | PyTorch |
| Model Integration | Hugging Face Transformers, PEFT |
| Backend | Python, FastAPI |
| Frontend | Next.js, React, Tailwind CSS |
| Mathematical Data | GSM8K, custom arithmetic dataset |
| Local Acceleration | PyTorch MPS on supported Apple devices |

## System Architecture

```text
          User
            |
            v
     Next.js Frontend
            |
            v
       FastAPI Backend
            |
            v
    Qwen2.5-1.5B-Instruct
       + LoRA Adapter
            |
            v
   Generated Math Solution
            |
            v
     Step-by-Step Response
            |
            v
          User
```

## Model Training

The project starts with a pretrained instruction-following language model and specializes it for mathematics using supervised fine-tuning.

### Training Pipeline

1. **Dataset Preparation:** Prepare arithmetic expressions and mathematical word problems for training.
2. **Data Balancing:** Sample arithmetic examples across operation categories to reduce imbalance between source files.
3. **Parameter-Efficient Fine-Tuning:** Apply LoRA to adapt the pretrained model.
4. **Model Integration:** Load the trained adapter alongside the original base model for inference.
5. **Evaluation:** Compare the base and fine-tuned models on mathematical accuracy, explanation quality, and response time.

### Datasets

- **GSM8K:** Grade-school mathematical word problems with worked solutions.
- **Custom Arithmetic Dataset:** Arithmetic expressions covering addition, subtraction, multiplication, division, exponents, and other numerical tasks.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- Git
- Sufficient memory to load the model and its adapter

### 1. Clone the Repository

```bash
git clone https://github.com/2420030176-Rochan/KLH--CSE---2026-2027---2420030176---MathSLM.git

cd KLH--CSE---2026-2027---2420030176---MathSLM
```

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install torch transformers peft fastapi uvicorn
```

Ensure the fine-tuned model adapter is available at the path configured in `app.py`. The base model is downloaded through Hugging Face when needed.

Start the backend:

```bash
uvicorn app:app --reload
```

The API should be available at `http://127.0.0.1:8000`.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### 3. Set Up the Frontend

Open a second terminal from the repository root:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

> **Note:** These instructions assume the project uses the `backend/` and `frontend/` directory structure described above. Adjust the commands if your repository differs.

## Evaluation

The system can be evaluated using a common test set containing arithmetic questions and mathematical word problems.

| Metric | Purpose |
|---|---|
| Mathematical Accuracy | Measures the proportion of questions answered correctly |
| Word Problem Accuracy | Evaluates solutions to natural-language math problems |
| Explanation Quality | Assesses clarity, correctness, and step-by-step reasoning |
| Response Latency | Measures the time required to generate a response |

Comparing the pretrained base model with the fine-tuned model helps assess the effect of domain-specific training. Quantitative results should be reported after evaluation on a held-out test set.

## Project Objective

To investigate how parameter-efficient fine-tuning can transform a compact, pretrained language model into a specialized AI mathematics tutor capable of solving mathematical problems and generating understandable explanations.

## Future Improvements

- Improve mathematical reasoning and explanation consistency.
- Expand the training dataset to cover more mathematical topics.
- Optimize inference latency and memory usage.
- Conduct systematic evaluation against the base model.
- Improve mathematical notation rendering in generated responses.
