# Content Governance Suite: Agents Documentation & Code Review

## Overview

The suite uses an **agent-based architecture** for content generation, review, and governance. Each agent is responsible for a specific aspect of the pipeline, promoting modularity and extensibility. Below is a summary and review of each major agent.

---

## 1. ContentGeneratorAgent
**Location:** `agents/generator/content_generator.py`

- **Purpose:** Generates AI-driven content using a language model (Perplexity) with RAG knowledge base for grounding.
- **Key Methods:**
  - `process(content_request)`: Generates content based on topic, type, style guide, and audience.
  - `_setup_knowledge_base()`: Initializes FAISS vector store using best practices docs.
  - `_calculate_quality_score(content)`: Heuristic for basic content quality.
- **Review:** See previous documentation for details. Overall, modular and testable.

---

## 2. FactualityAgent
**Location:** `agents/factcheck/factuality_agent.py` *(not fully included in previous context, but referenced in tests and workflow)*

- **Purpose:** Evaluates the factual accuracy and compliance of generated content.
- **Key Functions:**
  - `process(content)`: Checks for verifiable claims, compliance with guidelines, and flags inaccuracies.
- **How Used:** Invoked first in the review workflow (`review_workflow.execute`) to ensure only accurate content proceeds.
- **Review:**  
  - **Strengths:** Modular placement ensures critical checks are prioritized.
  - **Suggestions:** Add external fact-checking sources and more robust claim extraction. Improve error handling for ambiguous or uncheckable content.

---

## 3. StyleAnalyzerAgent
**Location:** `agents/sentiment/style_analyzer.py`

- **Purpose:** Analyzes writing style, tone, and sentiment to ensure alignment with intended audience and guidelines.
- **Key Functions:**
  - `process(content)`: Assesses tone, length, readability, and sentiment.
- **How Used:** Second in the review workflow after factuality.
- **Review:**  
  - **Strengths:** Enforces style consistency, can be expanded to check for inclusivity or bias.
  - **Suggestions:** Integrate with NLP libraries for advanced readability (e.g., Flesch-Kincaid), and support for multilingual content.

---

## 4. MultimodalReviewerAgent
**Location:** `agents/multimodal/multimodal_reviewer.py`

- **Purpose:** Reviews non-textual content (audio, video, images) and ensures multimodal content meets quality and compliance standards.
- **Key Functions:**
  - `process(content)`: Dispatches to `_review_audio`, `_review_video`, etc., based on content type.
- **How Used:** Third in review pipeline if content includes multimodal elements.
- **Review:**  
  - **Strengths:** Supports extensibility for future content types.
  - **Suggestions:** Placeholder implementations for audio/video; add integration with specialized libraries (e.g., speech-to-text, image moderation) for deeper analysis.

---

## 5. ConsensusAgent
**Location:** `agents/consensus/consensus_agent.py`

- **Purpose:** Aggregates results from all review agents to make a final decision (approve/revise/reject), calculate final score, and provide summary.
- **Key Functions:**
  - `process(review_results)`: Weighs outputs, calculates consensus, generates summary points.
- **How Used:** Final step in pipeline, invoked after review workflow.
- **Review:**  
  - **Strengths:** Centralizes governance logic, supports explainability.
  - **Suggestions:** Make weighting configurable, add support for user overrides or appeals, expand summary generation with clear rationales.

---

## 6. Other Notable Services

### AnalyticsService
**Location:** `services/analytics_service.py`
- **Purpose:** Provides dashboards and trend analysis for content generation and review activity.
- **Review:** Good for monitoring, can add more advanced metrics (engagement, retention, etc.).

### ExportService
**Location:** `services/export_service.py`
- **Purpose:** Exports content and review results to PDF, Word, CSV.
- **Review:** Well-structured; ensure proper error handling for large datasets and support for additional formats.

### ABTestingService
**Location:** `services/ab_testing_service.py`
- **Purpose:** Manages A/B tests for generation and review parameters (e.g., temperature, strictness).
- **Review:** Useful for model optimization; consider expanding analytics/reporting.

---

## 7. Review Workflow

**Location:** `workflows/review_workflow.py`

- **Executes:** FactualityAgent → StyleAnalyzerAgent → MultimodalReviewerAgent (if applicable) → ConsensusAgent.
- **Early Exit:** If factuality fails, content is halted.
- **Review:** Logical, modular, and extensible.

---

## 8. General Recommendations

- **Docstrings:** Add/expand function-level docstrings for all agents.
- **Testing:** Test agents with edge cases and multimodal content.
- **Extensibility:** Maintain modularity; allow easy addition of new agent types.
- **Security:** For agents processing user content, add input validation and sanitization.
- **Explainability:** Consensus and review agents should surface clear rationales for decisions.

---

**For deeper or per-agent API docs, request specific agent details.**


.venv/scripts/activate
cd content-governance-suite
uvicorn api.main:app --reload

cd content-governance-suite/frontend
npm run dev
@coderabbitai can you create a redme file that documents all my code