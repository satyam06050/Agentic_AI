"""
Agentic AI Course — Setup Verification Script
Dr. Kanthi Kiran Sirra | March-April 2026

Run: python verify_setup.py
All GREEN = You're ready for Day 1!
"""

import sys
import os

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
WARN = "\033[93m[WARN]\033[0m"
INFO = "\033[94m[INFO]\033[0m"

results = {"pass": 0, "fail": 0, "warn": 0}

def check(label, condition, fail_msg="", is_warning=False):
    if condition:
        print(f"  {PASS} {label}")
        results["pass"] += 1
        return True
    else:
        if is_warning:
            print(f"  {WARN} {label} — {fail_msg}")
            results["warn"] += 1
        else:
            print(f"  {FAIL} {label} — {fail_msg}")
            results["fail"] += 1
        return False


print()
print("=" * 60)
print("  AGENTIC AI COURSE — SETUP VERIFICATION")
print("  Dr. Kanthi Kiran Sirra | Sr. AI Engineer")
print("=" * 60)
print()

# --------------------------------------------------
# 1. PYTHON VERSION
# --------------------------------------------------
print("1. Python Environment")
print("-" * 40)
v = sys.version_info
check(f"Python version: {v.major}.{v.minor}.{v.micro}",
      v.major == 3 and v.minor >= 10,
      f"Need Python 3.10+, you have {v.major}.{v.minor}. Download from python.org")

in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
check("Virtual environment active",
      in_venv,
      "Not in a virtual environment. Run: python -m venv venv && source venv/bin/activate (Mac/Linux) or venv\\Scripts\\activate (Windows)",
      is_warning=True)
print()

# --------------------------------------------------
# 2. CORE PACKAGES
# --------------------------------------------------
print("2. Core Packages")
print("-" * 40)

packages = {
    "langchain": "langchain",
    "langchain_groq": "langchain-groq",
    "langchain_google_genai": "langchain-google-genai",
    "langgraph": "langgraph",
    "smolagents": "smolagents",
    "crewai": "crewai",
    "chromadb": "chromadb",
    "faiss": "faiss-cpu (import as faiss)",
    "sentence_transformers": "sentence-transformers",
    "pypdf": "pypdf",
    "rank_bm25": "rank-bm25",
    "streamlit": "streamlit",
    "fastapi": "fastapi",
    "dotenv": "python-dotenv",
    "duckduckgo_search": "duckduckgo-search",
    "requests": "requests",
    "bs4": "beautifulsoup4",
    "pydantic": "pydantic",
}

for module, pip_name in packages.items():
    try:
        __import__(module)
        check(f"{pip_name}", True)
    except ImportError:
        check(f"{pip_name}", False, f"pip install {pip_name}")

# Check RAGAS separately (can have import issues)
try:
    import ragas
    check("ragas", True)
except Exception:
    check("ragas", False, "pip install ragas", is_warning=True)

print()

# --------------------------------------------------
# 3. EMBEDDING MODEL
# --------------------------------------------------
print("3. Embedding Model (one-time download, ~90MB)")
print("-" * 40)
try:
    from sentence_transformers import SentenceTransformer
    print(f"  {INFO} Loading all-MiniLM-L6-v2 (first time downloads ~90MB)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    test_embedding = model.encode(["Hello world"])
    check(f"all-MiniLM-L6-v2 loaded, embedding dim: {test_embedding.shape[1]}", True)
except Exception as e:
    check("Embedding model", False, str(e))
print()

# --------------------------------------------------
# 4. API KEYS (.env file)
# --------------------------------------------------
print("4. API Keys (.env file)")
print("-" * 40)

env_exists = os.path.exists(".env")
check(".env file exists", env_exists,
      "Create a .env file in project root. See setup guide for template.")

if env_exists:
    from dotenv import load_dotenv
    load_dotenv()

groq_key = os.getenv("GROQ_API_KEY", "")
check("GROQ_API_KEY set",
      len(groq_key) > 10,
      "Get free key at console.groq.com")

gemini_key = os.getenv("GOOGLE_API_KEY", "")
check("GOOGLE_API_KEY set",
      len(gemini_key) > 10,
      "Get free key at aistudio.google.com (backup LLM)",
      is_warning=True)

hf_token = os.getenv("HF_TOKEN", "")
check("HF_TOKEN set",
      len(hf_token) > 10,
      "Get free token at huggingface.co/settings/tokens",
      is_warning=True)
print()

# --------------------------------------------------
# 5. LLM API TEST (Groq)
# --------------------------------------------------
print("5. LLM API Test")
print("-" * 40)

if len(groq_key) > 10:
    try:
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=50,
            api_key=groq_key
        )
        response = llm.invoke("Say 'Setup successful!' in exactly 2 words.")
        check(f"Groq API call successful: {response.content.strip()[:50]}", True)
    except Exception as e:
        error_msg = str(e)[:80]
        check("Groq API call", False, f"Error: {error_msg}")
else:
    check("Groq API call", False, "Skipped — GROQ_API_KEY not set")
print()

# --------------------------------------------------
# 6. VECTOR DB TEST
# --------------------------------------------------
print("6. Vector Database Test")
print("-" * 40)
try:
    import chromadb
    client = chromadb.Client()
    collection = client.create_collection("test_verify")
    collection.add(
        documents=["This is a test document for verification"],
        ids=["test1"]
    )
    query_result = collection.query(query_texts=["test"], n_results=1)
    check(f"ChromaDB working — queried and got {len(query_result['ids'][0])} result(s)", True)
    client.delete_collection("test_verify")
except Exception as e:
    check("ChromaDB", False, str(e))
print()

# --------------------------------------------------
# 7. STREAMLIT CHECK
# --------------------------------------------------
print("7. Deployment Tools")
print("-" * 40)
try:
    import streamlit
    check(f"Streamlit v{streamlit.__version__} installed", True)
except ImportError:
    check("Streamlit", False, "pip install streamlit")

try:
    import fastapi
    check(f"FastAPI v{fastapi.__version__} installed", True)
except ImportError:
    check("FastAPI", False, "pip install fastapi", is_warning=True)
print()

# --------------------------------------------------
# FINAL REPORT
# --------------------------------------------------
print("=" * 60)
total = results["pass"] + results["fail"] + results["warn"]
print(f"  RESULTS: {results['pass']}/{total} passed", end="")
if results["warn"]:
    print(f", {results['warn']} warnings", end="")
if results["fail"]:
    print(f", {results['fail']} failed", end="")
print()

if results["fail"] == 0:
    print(f"\n  {PASS} ALL SET! You're ready for Day 1!")
    print("  See you in class on March 18th!")
elif results["fail"] <= 2:
    print(f"\n  {WARN} ALMOST THERE! Fix the {results['fail']} failed item(s) above.")
    print("  Most issues are fixed with: pip install -r requirements.txt")
else:
    print(f"\n  {FAIL} NEEDS ATTENTION: {results['fail']} items failed.")
    print("  Run: pip install -r requirements.txt")
    print("  Then create .env file with API keys (see setup guide).")
    print("  If stuck, bring your laptop to class — we'll help!")

print()
print("  Questions? Post in the class WhatsApp group.")
print("  Backup: Google Colab will work if local setup fails.")
print("=" * 60)
print()
