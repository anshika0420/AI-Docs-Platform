# AI-Assisted Document Authoring and Generation Platform

This is a full-stack implementation of the assignment:

> AI-Assisted Document Authoring and Generation Platform

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, JWT auth, python-docx, python-pptx
- **Frontend:** React (Create React App style), react-router-dom, axios
- **DB:** SQLite (file-based, easy to run)
- **LLM Integration:** Real APIs via environment variables
  - Supports `OPENAI` or `GEMINI` via `.env`

## Folder Structure

```
ai-docs-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── deps.py
│   │   ├── llm_client.py
│   │   ├── generator.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── auth_router.py
│   │       ├── projects_router.py
│   │       └── export_router.py
│   ├── requirements.txt
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.js
│       ├── App.js
│       ├── api.js
│       ├── components/
│       │   └── Navbar.js
│       └── pages/
│           ├── Login.js
│           ├── Dashboard.js
│           ├── ConfigureProject.js
│           └── Editor.js
└── .env.example
```

## 1. Backend Setup

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in `backend/` based on `.env.example` from the project root:

```bash
cp ../.env.example .env
```

Edit `.env`:

- `SECRET_KEY` → any long random string
- `DATABASE_URL` → leave default for SQLite
- `LLM_PROVIDER` → `openai` or `gemini` or `mock`
- For OpenAI:
  - `OPENAI_API_KEY=<your key>`
- For Gemini:
  - `GEMINI_API_KEY=<your key>`

Then run the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

API docs: open http://localhost:8000/docs in your browser.

## 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

The app will run at http://localhost:3000

## 3. Basic Flow

1. Register a user (from Login page: click "Register" toggle).
2. Login → token is stored in browser localStorage.
3. Create a new project:
   - Choose document type: `.docx` or `.pptx`
   - Set title and topic
   - Add section titles (for `.docx`) or slide titles (for `.pptx`)
4. Click "Generate with AI" to generate section/slide content via LLM.
5. Open a project in Editor:
   - View each section
   - Refine using instruction textbox per section
   - Like/Dislike
   - Add comments
6. Click "Export DOCX" or "Export PPTX" to download the assembled file.

## 4. Notes

- All data (users, projects, sections) is stored in SQLite (`app.db` by default).
- LLM calls are abstracted in `llm_client.py` — you can swap providers by env var.
- If you don't want to spend API, set `LLM_PROVIDER=mock` and it will generate placeholder text.
