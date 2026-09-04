enterprise-agent
│
├── README.md
├── requirements.txt
├── .env.example
│
├── app
│   ├── main.py                 # FastAPI入口
│   │
│   ├── agent
│   │   ├── agent.py            # LangGraph Agent
│   │   └── tools.py            # RAG Tool
│   │
│   ├── models
│   │   ├── embedding.py        # BGE embedding
│   │   └── llm.py              # DeepSeek LLM
│   │
│   ├── rag
│   │   ├── loader.py           # 文档加载
│   │   ├── splitter.py         # 文档切分
│   │   └── vectorstore.py      # Chroma管理
│   │
│   └── core
│       └── config.py
│
├── frontend
│   └── streamlit_app.py
│
├── data
│   └── TEST.pdf
│
└── chroma_db