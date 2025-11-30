Understood — here is the **complete READY-TO-COPY README.md code** exactly as you asked 👇
(No explanation — only the code.)

---

```markdown
# 🧠 AI-Assisted Document Authoring & Generation Platform

A full-stack **AI Docs Platform** that allows users to create, refine, and export **Word (.docx)** and **PowerPoint (.pptx)** documents using AI.

---

## 🚀 Features

| Category | Capability |
|---------|-------------|
| Authentication | JWT Login / Register |
| Document Types | `.docx` & `.pptx` |
| AI Content | Generates section/slide text using OpenAI or Gemini |
| Refinement | Modify text via natural-language instructions |
| Feedback | Likes, dislikes & comments per section |
| Export | Download final DOCX / PPTX |
| Storage | SQLite (file-based) |

---

## 🖼 UI Screenshots

### 🔐 Login
![Login](login.png)

### 🏠 Dashboard
![Dashboard](dashboard.png)

### ➕ Create Project
![Create Project](create_project.png)

### ✍️ Editor
![Editor](editor.png)

### 📤 Export DOCX / PPTX
![Export](export.png)

---

## 🧱 Tech Stack

```

Backend → FastAPI, SQLAlchemy, JWT, python-docx, python-pptx
Frontend → React, react-router-dom, axios
Database → SQLite
AI Models → OpenAI / Gemini / Mock mode

```

---

## 📂 Folder Structure

```

ai-docs-platform/
├── backend/
│   ├── app/
│   │   ├── **init**.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── deps.py
│   │   ├── llm_client.py
│   │   ├── generator.py
│   │   └── routers/
│   │       ├── **init**.py
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
├── login.png
├── dashboard.png
├── create_project.png
├── editor.png
├── export.png
└── .env.example

````

---

## ⚙️ Backend Setup

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
# source venv/bin/activate
pip install -r requirements.txt
````

Create a `.env` in `/backend` (based on `.env.example`):

```
SECRET_KEY=your_random_string
DATABASE_URL=sqlite:///./app.db
LLM_PROVIDER=openai   # openai | gemini | mock

# For OpenAI
OPENAI_API_KEY=your_openai_key

# For Gemini
GEMINI_API_KEY=your_gemini_key
```

Run backend:

```bash
uvicorn app.main:app --reload --port 8000
```

API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🌐 Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend starts at → [http://localhost:3000](http://localhost:3000)

---

## 🔄 Usage Flow

1️⃣ Register or Login
2️⃣ Create New Project
3️⃣ Set title, topic & document type (.docx or .pptx)
4️⃣ Add section/slide titles
5️⃣ Click **Generate with AI**
6️⃣ Open project → refine, like/dislike, comment
7️⃣ Export **DOCX/PPTX**

---

## 📝 Notes

* All user & document data stored in SQLite → `backend/app.db`
* AI provider switching is controlled via `.env`
* Development without API cost:

  ```
  LLM_PROVIDER=mock
  ```

---

## 🔮 Future Enhancements (Optional)

* AI-generated images inside PPT slides
* Collaboration (multi-user editing)
* Document themes / templates

---

## 👤 Author

Developed by **Anshika Srivastava**
⭐ If this project inspires you, please **star the repository!**

```

---

If you want, I can also add:
✔ badges (OpenAI / Gemini / FastAPI / React / License)  
✔ deployment instructions (Render / Railway / Vercel)  

Just tell me and I’ll update it. 🚀
```
