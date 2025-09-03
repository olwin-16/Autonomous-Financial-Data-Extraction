# **Autonomous Financial Data Extraction** — 33rd Cohort Fellowship.AI

## **Project Overview**

This repository documents the research, benchmarking, and evaluation of autonomous web agents for real-time financial data extraction conducted by the 33rd cohort of the Fellowship.AI program.

The project journeyed through three major agent frameworks: Midscene.js, UI-TARS Desktop Agent, and finally the Proxy-lite agent. Each agent was assessed not only for accuracy and finish rates but also their resource efficiency, reliability, and practicality in complex financial scraping tasks.

The Proxy-lite agent emerged as the recommended choice due to its balance of efficiency and effectiveness.

## **Table of Contents**

- Project Overview
  
- Evaluation of Agents
  
  - Midscene.js Chrome Extension
  - UI-TARS Desktop Agent
  - Proxy-lite Agent (Final Selection)
    
- Benchmarking Results
  
- Demo Videos
  
- Setup and Usage Guide
  
- Public Repositories
  
- Confidentiality Notice
  
- Contact

## **Evaluation of Agents**

## **Midscene.js Chrome Extension**

**Repository**: [Midscene](https://github.com/web-infra-dev/midscene)

**Technical Summary**

- Midscene.js operates as a Chrome extension utilizing vision-language models (VLMs) configured with UI-TARS 7-B SFT. It automates browsing via natural language prompts to extract and structure financial data.

**Key Challenge**

- Faced a critical token limit error (422 Input Validation; inputs tokens + max_new_tokens > 32,768), severely limiting the complexity of tasks it could handle. Attempts to reduce inputs or max tokens failed to circumvent this.

**Example Failure**

- Failed to extract the BBC homepage headline due to exceeding token limits despite aggressive input shortening.

**Other Limitations**

- Manual scrolling and dynamic webpage elements were inadequately handled, resulting in incomplete outputs.

**Outcome**

- Although providing a valuable baseline and easy UI, these constraints prompted migration to UI-TARS Desktop for enhanced capability.

### Midscene.js Demo Videos

**Simple Task:** Open Google Chrome and search "Elon Musk" (Succeeded) 

<br>

![Midscene-Elon-Musk](https://github.com/user-attachments/assets/fe136709-8bc7-4b71-87ad-7dfa243b8696)

<br>

**Complex Task:** Open Chrome, go to BBC News, select top headline, extract title, save JSON (Failed due to token limits)  

<br>

![Midscene-BBC](https://github.com/user-attachments/assets/3f59499d-4791-4266-bfa3-dcf90c494e55)


## **UI-TARS Desktop Agent**

**Repository**: [UI-TARS](https://github.com/bytedance/UI-TARS)

**Technical Implementation**

- UI-TARS Desktop is a GUI-based autonomous agent powered by multimodal vision-language models (7B DPO primary, 2B SFT secondary). Hosted as a standalone Windows/Linux application with Hugging Face endpoints.

**Installation and Launch**

```bash

git clone https://github.com/bytedance/UI-TARS.git
cd UI-TARS
```

```bash
python -m venv venv
source venv/bin/activate          # Linux/macOS
venv\Scripts\activate             # Windows
```

```bash
pip install -r requirements.txt
```

```bash
# Launch service
python -m vllm.entrypoints.openai.api_server --served-model-name ui-tars --model path_to_model
```

```bash
# Local UI start
pnpm install && pnpm run dev
```

**Performance Highlights**

- Efficiently completed complex financial scraping tasks, including calculating loan EMI for HDFC Bank in ~2 minutes.
- Outperformed Midscene in reliability and multimodal input processing while demonstrating token-limit resilience.

**Limitations**

- Computationally demanding (requires GPUs, Hugging Face endpoints).
- Encountered runtime instability, including Colab crashes and occasional failures in supplemental tasks (e.g., saving screenshots).
- Benchmarked on reasoning datasets (GSM8K, ScienceQA, HellaSwag) showed modest accuracy (~10-40%) without further multimodal finetuning.
  
<br>
<div align="center">
<img width="500" alt="Comparison and Transition to UI-TARS Desktop" src="https://github.com/user-attachments/assets/17d7adc0-c11a-46f3-bc62-e77ae8169b09" />
</div>
<br>

**Team Contributions**

- Extensive testing performed by Olwin Christian, Rahul Thakur, and Iremide Oloyede, with mentor supervision.
- Runtime and scraping stability refined through collaborative iterations.

### UI-TARS Demo Videos

**Simple Task:** Search Notepad from desktop search results and open it (Succeeded)  

<br>

![Midscene-Notepad](https://github.com/user-attachments/assets/84d813ff-6bcd-48f1-9252-aee149830838)

<br>

**Complex Task:** Open Chrome, navigate to HDFC site, calculate EMI (Succeeded in calculation but failed to save the result screenshot)  

<br>

![UI-TARS-HDFC](https://github.com/user-attachments/assets/f2b18b19-ec78-486a-97c2-ab91aa7f7d65)


## **Proxy-lite Agent** (Final Selection)

**Repository**: [Proxy-Lite](https://github.com/convergence-ai/proxy-lite)

**Technical Implementation**

- Proxy-lite is a lightweight, CPU-efficient web agent performing browser-based scraping via JavaScript DOM interaction, explicitly avoiding OCR.

**Advantages**

- Does not require GPU or dedicated inference endpoints.
- High finish (87.8%) and success (95.1%) rates on the WebVoyager dataset.
- Balanced precision and recall across critical web interaction actions.

**Typical usage example** (educational snippet)

```bash

from proxy_lite import Runner, RunnerConfig
from transformers import AutoProcessor
from proxy_lite.tools import ReturnValueTool, BrowserTool
from proxy_lite.serializer import OpenAICompatibleSerializer
import asyncio

config = RunnerConfig.from_dict({
    "environment": {"name": "webbrowser", "homepage": "https://www.google.com/", "headless": True},
    "solver": {"name": "simple", "agent": {"name": "proxy_lite", "client": {"name": "convergence"}}},
    "max_steps": 50,
    "model_id": "convergence-ai/proxy-lite-3b",
    "api_base": "https://convergence-ai-demo-api.hf.space/v1",
    "action_timeout": 1800,
    "environment_timeout": 1800,
    "task_timeout": 18000,
    "logger_level": "DEBUG",
})

proxy = Runner(config=config)

message_history = [
    {"role": "system", "content": "You are Proxy Lite, a web-browsing agent..."},
    {"role": "user", "content": "What's the weather like in London today?"}
]

processor = AutoProcessor.from_pretrained("convergence-ai/proxy-lite-3b")
tools = OpenAICompatibleSerializer().serialize_tools([ReturnValueTool(), BrowserTool(session=None)])

templated_messages = processor.apply_chat_template(message_history, tokenize=False, add_generation_prompt=True, tools=tools)

async def main():
    response = await proxy.run(templated_messages)
    print(response)

asyncio.run(main())

```

## **Benchmarking Results Summary**

| Website     | Proxy-lite Finish Rate | Proxy-lite Success Rate | Previous Agent Finish Rate | Previous Agent Success Rate |
|-------------|-----------------------|------------------------|----------------------------|-----------------------------|
| Allrecipes  | 87.8%                 | 95.1%                  | 20%                        | 50%                         |
| Amazon      | 70%                   | 90%                    | N/A                        | N/A                         |
| Apple       | 82.1%                 | 89.7%                  | N/A                        | N/A                         |
| ArXiv       | 60.5%                 | 79.1%                  | N/A                        | N/A                         |

### Proxy-lite Demo Video

**Context** 

Below is an example GIF sourced from the internet to demonstrate Proxy-lite in action. This is not from our project, but illustrates typical web automation using Proxy-lite for educational/demo purposes.

<br>

<div align="center">
  
![Proxy-Lite-Example](https://github.com/user-attachments/assets/d6eaa6e2-4d09-4a9f-8058-4df60c4655c1)
  
</div>

**Note**: This GIF is a public demonstration, not a direct recording from our cohort’s experiments.

## **Public Agent Repositories**

- [UI-TARS Desktop](https://github.com/bytedance/UI-TARS)
- [Midscene.js Chrome Extension](https://github.com/web-infra-dev/midscene)
- [Proxy-lite Agent](https://github.com/convergence-ai/proxy-lite)

## **Confidentiality Notice**

This repository is curated to share non-confidential educational summaries, benchmarking insights, and public resources aligned with the Fellowship.AI agreement. Internal source code, full dataset details, and private cohort notebooks are not included.

## **Contact & Contributions**

Questions or collaboration requests are welcome via GitHub Issues. Please respect cohort data and code privacy.

## **License**

[MIT License](LICENSE)
