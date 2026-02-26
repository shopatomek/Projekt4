# 🤖 AI-Driven SRE Monitoring & Orchestration System

A sophisticated, self-healing monitoring pipeline that bridges **Python-based data engineering** with **AI orchestration (n8n & Gemini)**. The system doesn't just find errors; it analyzes them via LLM, notifies stakeholders, and manages its own state by cleaning up processed data.

---

## 🏗 System Architecture & Workflow

The project implements a full **Observe-Analyze-Act** loop:

1. **Observability (Python Agent):** A custom agent monitors internal processes, generates health metrics, and hashes error signatures.
2. **Shared State (Docker Volume):** When a high-signal event occurs, a payload is dropped into a shared volume, acting as a bridge between the agent and the orchestrator.
3. **Intelligence (n8n & Gemini):** n8n detects new reports, sends them to **Google Gemini 1.5 Flash** for root-cause analysis, and formats a human-readable alert.
4. **Action & Cleanup (Node.js):** After sending the alert via **Telegram**, n8n executes a native JavaScript cleanup script to wipe the processed report, ensuring no duplicate alerts and a clean system state.

---

## 🛠 Tech Stack

- **Backend:** Python 3.11+ (Logging, Hashing, Analytics)
- **Orchestration:** n8n (Docker-hosted)
- **Intelligence:** Google Gemini 1.5 Flash API
- **DevOps:** Docker, Docker Compose (Root-level orchestration)
- **Communications:** Telegram Bot API

---

## 🚀 Key Features (Portfolio Highlights)

- **AI-Native Diagnostics:** Uses LLM to translate raw stack traces into actionable "Fix-it" plans.
- **Sandbox-Bypassed Orchestration:** Configured n8n with specialized Docker environments (`NODE_FUNCTION_ALLOW_BUILTIN`) to allow native filesystem interaction via JavaScript.
- **Idempotent Alerting:** The system ensures that the same error doesn't trigger multiple alerts by using state-aware hashing, saving AI tokens and developer attention.
- **Automated State Management:** Implements a "zero-leftover" policy in shared volumes using automated post-processing cleanup.

---

## 📊 Monitoring & Analytics Logic

The system moves beyond simple "error logging" into **Proactive Observability**. It treats the log stream as a data source to calculate the real-time stability of the infrastructure.

### The Signal-to-Noise Methodology

Instead of alerting on every single warning, the agent analyzes the **Log Density** within a specific execution session. This allows the system to distinguish between "transient hiccups" and "systemic degradation."

#### 1. Total Events ($N_{total}$)

This represents the sum of all system activities (INFO, DEBUG, WARNING, ERROR). It serves as the **baseline** for normal system chatter.

#### 2. Error Events ($N_{errors}$)

Specifically targeted critical failures (Parser exceptions, Validator breaches).

#### 3. Mathematical Indicators

We use two primary metrics to determine if an AI intervention is necessary:

- **Error Rate ($ER$):** The percentage of system activity that results in failure.
  $$ER = \left( \frac{N_{errors}}{N_{total}} \right) \times 100$$
- **Health Score ($HS$):** A high-level stability index. A drop below a specific threshold (e.g., 80%) triggers the n8n orchestration pipeline.
  $$HS = 100\% - ER$$

### Why this matters for the business?

1. **Token Efficiency:** By calculating these scores locally in Python, we only trigger the expensive LLM (Gemini) analysis when the `Health Score` indicates a genuine issue.
2. **Contextual Alerts:** The AI doesn't just receive an error; it receives the context (e.g., _"Error rate is 15%, suggesting a degraded state rather than a total crash"_).
3. **Noise Reduction:** Minor warnings are absorbed into the $N_{total}$ without waking up the engineer, preventing "alert fatigue."

---

## 🔧 Installation & Security

To protect sensitive data, this project uses an environment-based configuration. **Never commit your `.env` file.**

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/shopatomek/Projekt4.git](https://github.com/shopatomek/Projekt4.git)
   cd Projekt4
   ```

2. **Configure Environment:**
   Create a `.env` file based on the provided template:

   ```bash
   cp .env.example .env
   # Edit .env and add your API keys (Gemini, Telegram)
   ```

3. **Run the Stack:**

   ```bash
   docker-compose up -d --build
   ```

4. **Setup n8n:**
   - Open `http://localhost:5678`.
   - **Import Logic:** Open the Workflow Menu (top right), select **Import from File**, and choose `n8n/monitoring_workflow.json`.
   - **Credentials:** Double-click Gemini/Telegram nodes to link your API keys.
   - **Activate:** Toggle the **Active** switch to enable 24/7 monitoring.
   - **Dashboard:** Access live reports at `http://localhost:5678/webhook/dashboard`.

---

## 📂 Project Structure

- `app/` - Python Monitoring Agent (Logic, Analytics, Logging).
- `n8n/` - Exported workflow JSON (Import this into your n8n instance).
- `docker-compose.yml` - Multi-container setup (Agent + n8n + Volumes).
- `shared_data/` - Interaction layer for inter-container communication.
- `logs/` - Internal system logs.
- `.env.example` - Template for environment variables.
