# Agent Benchmarking & Finetuning

## Repository Structure

### 1. **Benchmarking and Comparison of Agents**
- Contains setup for our internal benchmarking framework, and includes detailed Benchmarking Reports.

### 2. **Presentation**
- Weekly presentation slides from **Week 1 through Week 8**.
- Covers progress updates, demo sessions, and key findings.

### 3. **Notebooks**
This folder features extensive research and experiments:
- **LLM Benchmarking**: Evaluations on datasets such as:
  - HellaSwag
  - GSM8K
  - SQuAD
  - CNN/DailyMail
- **VLM Benchmarking**: Tasks include:
  - Image Captioning
  - Visual Question Answering (VQA)
  - ScienceQA
- **Web Agents**: Iterations and experiments with:
  - **Proxy Lite**
  - **UI TARS**
- **Prompt Engineering & Finetuning**:
  - Experiments using [`dspy`](https://github.com/stanfordnlp/dspy)
  - DSL-style pipeline development for agent tuning and instruction-following

---

## 🔗 External Resources

### Tools & Libraries
- **Proxy Lite Hugging Face Model**:  
  [`convergence-ai/proxy-lite-3b`](https://huggingface.co/convergence-ai/proxy-lite-3b)

- **Proxy Lite GitHub Repository**:  
  [GitHub - Proxy Lite](https://github.com/convergence-ai/proxy-lite/tree/main)

- **Stanford DSPy Framework**:  
  - [GitHub](https://github.com/stanfordnlp/dspy)  
  - [Documentation](https://dspy.ai/)  
  - [Awesome DSPy Projects](https://github.com/ganarajpr/awesome-dspy)

### VLM Finetuning
- [MLX-VLM: Finetuning VLMs](https://github.com/Blaizzy/mlx-vlm/tree/main)

### Finance LLMs & Finetuning

- **FinGPT**:
  - [GitHub](https://github.com/AI4Finance-Foundation/FinGPT)
  - Finetuned using LLaMA-2-7B-Chat + LoRA on DOW30 market data.
  - Utilizes Hugging Face datasets:
    - `Dahoas/rm-static`
    - `Dahoas/full-hh-rlhf`
    - `Dahoas/synthetic-instruct-gptj-pairwise`
    - `yitingxie/rlhf-reward-datasets`
    - `openai/webgpt_comparisons`
    - `stanfordnlp/SHP`

- **Awesome FinLLMs**:  
  [Collection of Finetuned Finance LLMs](https://github.com/IDEA-FinAI/Awesome-FinLLMs)

- **Finance Specialist AI**:  
  [GitHub](https://github.com/MarinaComotti/Finance_Specialist_AI)

---
