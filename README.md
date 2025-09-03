# **Autonomous Financial Data Extraction Agents** — 33rd Cohort Fellowship.AI

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

**Technical Summary**:

- Midscene.js operates as a Chrome extension utilizing vision-language models (VLMs) configured with UI-TARS 7-B SFT. It automates browsing via natural language prompts to extract and structure financial data.

**Key Challenge**:

- Faced a critical token limit error (422 Input Validation; inputs tokens + max_new_tokens > 32,768), severely limiting the complexity of tasks it could handle. Attempts to reduce inputs or max tokens failed to circumvent this.

**Example Failure**:

- Failed to extract the BBC homepage headline due to exceeding token limits despite aggressive input shortening.

**Other Limitations**:

- Manual scrolling and dynamic webpage elements were inadequately handled, resulting in incomplete outputs.

**Outcome**:

- Although providing a valuable baseline and easy UI, these constraints prompted migration to UI-TARS Desktop for enhanced capability.
