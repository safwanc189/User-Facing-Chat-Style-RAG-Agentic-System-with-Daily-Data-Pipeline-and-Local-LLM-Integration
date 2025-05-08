This project implements an advanced User-Facing Chat-Style Retrieval-Augmented Generation (RAG) Agentic system, leveraging a local Large Language Model (LLM) for real-time query resolution. The system features a fully automated data pipeline that updates a MySQL database daily with the most current information, ensuring that users interact with the latest data available.

Key Components:

Data Pipeline: A robust and efficient pipeline that automates the process of retrieving, cleaning, and storing data from an external API. The system ensures daily updates, maintaining the freshness and relevance of the data.

Local LLM Integration: The core functionality is powered by a locally hosted LLM (Qwen 2.5), which processes user queries, executes predefined tool calls, and generates accurate, contextually relevant responses.

Asynchronous Architecture: Designed with asynchronous programming principles to ensure non-blocking operations, the system maintains optimal performance and scalability.

API & WebSocket Interface: A streamlined API or WebSocket communication layer facilitates seamless interaction between the user interface and the LLM, allowing for real-time query and response handling.

Minimalistic User Interface: A straightforward, functional UI provides users with a simple interface to interact with the system, focusing on usability rather than aesthetics
