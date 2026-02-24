# Smart Monitoring Agent & Log Analyzer

A robust Python-based monitoring system designed to scrape, parse, and validate data with an intelligent AI-ready reporting layer. This project focuses on **high-signal logging**, **dynamic health analytics**, and **automated error deduplication**, ensuring that monitoring stays efficient and costs (AI tokens) are kept to a minimum.

## 🛠 Tech Stack

- **Language:** Python 3.11+
- **Logging:** Advanced `logging` module with custom `Filters` and `RotatingFileHandler`.
- **Containerization:** Docker, Docker Compose.
- **Analysis:** Integrated AI-Adapter for LLM-based diagnostics.

## 🚀 Key Features

- **Dynamic Data Generation:** Features a "Chaos Generator" that simulates real-world API variability, producing a mix of successful records and various error types (Parser/Validator) for robust monitoring testing.
- **System Health Analytics:** Real-time calculation of **Health Score** and **Error Rate** based on infrastructure-level log density.
- **Intelligent Log Filtering:** Custom architecture that filters out repetitive noise while preserving critical process information and errors.
- **Error Hashing & Deduplication:** State-aware analyzer that hashes error sets. Reports are triggered only when a _new_ error signature is detected, preventing redundant alerts.
- **AI-Ready Payloads:** Automatically generates focused prompts in `to_analyze.txt`, providing AI with context, statistics, and raw error data for instant root-cause analysis.
- **Dockerized Architecture:** Fully containerized environment using Docker Compose, featuring shared volumes for seamless integration with external tools like n8n.

## 📊 Monitoring & Analytics Logic

The system implements a **proactive observability** model. Instead of just reporting _that_ an error occurred, it provides context on the system's overall stability during each session.

### The Mathematical Formula

The engine evaluates the "noise" and stability of the entire process by analyzing the log stream from the `NEW SESSION STARTED` marker to the end of the cycle.

1. **Total Events ($N_{total}$):** Every recorded event (Info, Debug, Warning, Error) in the current session.
2. **Error Events ($N_{errors}$):** Critical failures captured by the Parser or Validator.

$$Error\ Rate = \left( \frac{N_{errors}}{N_{total}} \right) \times 100$$
$$Health\ Score = 100\% - Error\ Rate$$

### Why this approach?

This methodology follows **SRE (Site Reliability Engineering)** principles. By monitoring the ratio of errors to total system chatter, the agent can detect "degraded states" before a total system failure occurs. A drop in the **Health Score** provides a high-signal trigger for AI intervention.

## 📂 Project Structure

- `app/scraper.py` - Dynamic data acquisition & chaos generation.
- `app/parser.py` - Data transformation with robust error handling.
- `app/validator.py` - Data integrity verification.
- `app/logger.py` - Custom filtering & formatting engine.
- `app/ai_analyzer.py` - Statistical engine, error hashing & session management.
- `app/ai_adapter.py` - Prompt engineering & AI payload formatting.
- `main.py` - Main orchestration loop.

## 🔧 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/shopatomek/Projekt4.git](https://github.com/shopatomek/Projekt4.git)
   cd Projekt4
   ```
2. **Run with Docker:**

   ```bash
   docker-compose up --build
   ```

3. **Monitor Output:**

   Real-time logs: ./logs/internal.log

   AI Reports: ./shared_data/to_analyze.txt
