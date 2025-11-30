from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from .. import schemas, models, llm_client
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("/", response_model=List[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db), user=Depends(get_current_user)):
    projects = db.query(models.Project).filter(models.Project.owner_id == user.id).all()
    return projects

@router.post("/", response_model=schemas.ProjectOut)
def create_project(p: schemas.ProjectCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if p.doc_type not in ("docx", "pptx"):
        raise HTTPException(status_code=400, detail="doc_type must be 'docx' or 'pptx'")
    project = models.Project(
        title=p.title,
        topic=p.topic,
        doc_type=p.doc_type,
        owner_id=user.id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    for s in p.outline:
        sec = models.Section(
            project_id=project.id,
            title=s.title,
            order=s.order,
            content="",
        )
        db.add(sec)
    db.commit()
    db.refresh(project)
    return project

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.owner_id == user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/{project_id}/generate")
def generate_content(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.owner_id == user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    sections = project.sections
    for s in sections:
        base_topic = project.topic or project.title
        prompt = (
            f"Generate content for a {'slide' if project.doc_type=='pptx' else 'document section'} titled '{s.title}'.\n"
            f"Main topic: {base_topic}.\n"
            "Write clear, structured, business-style content. Use bullet points for PPT, paragraphs for DOCX. "
            "Make it concise but informative."
        )
        s.content = llm_client.call_llm(prompt)
        db.add(s)
    db.commit()
    return {"status": "ok", "message": "Content generated."}

@router.post("/{project_id}/sections/{section_id}/refine")
def refine_section(
    project_id: int,
    section_id: int,
    body: schemas.RefineRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.owner_id == user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    section = (
        db.query(models.Section)
        .filter(models.Section.id == section_id, models.Section.project_id == project.id)
        .first()
    )
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    prompt = (
        f"Original content:\n{section.content}\n\n"
        f"Instruction: {body.instruction}\n"
        "Return ONLY the improved content, without any explanation."
    )
    new_content = llm_client.call_llm(prompt)

    try:
        history = json.loads(section.refinement_history) if section.refinement_history else []
    except Exception:
        history = []
    history.append({"instruction": body.instruction, "result": new_content})
    section.refinement_history = json.dumps(history)
    section.content = new_content
    db.add(section)
    db.commit()
    db.refresh(section)
    return {"status": "ok", "content": section.content}

@router.post("/{project_id}/sections/{section_id}/feedback")
def feedback_section(
    project_id: int,
    section_id: int,
    body: schemas.FeedbackRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.owner_id == user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    section = (
        db.query(models.Section)
        .filter(models.Section.id == section_id, models.Section.project_id == project.id)
        .first()
    )
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    if body.action == "like":
        section.likes = (section.likes or 0) + 1
    elif body.action == "dislike":
        section.dislikes = (section.dislikes or 0) + 1

    if body.comment:
        try:
            comments = json.loads(section.comments) if section.comments else []
        except Exception:
            comments = []
        comments.append({"comment": body.comment})
        section.comments = json.dumps(comments)

    db.add(section)
    db.commit()
    return {"status": "ok"}

@router.post("/{project_id}/ai-template")
def ai_template(project_id: int, body: schemas.TemplateRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.owner_id == user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    prompt = (
        f"Generate an outline for a business document on topic: {body.topic}. "
        f"Type: {'PowerPoint slides' if body.doc_type=='pptx' else 'Word document'}. "
        "Return 6-8 clear section or slide titles as a JSON array of strings."
    )
    raw = llm_client.call_llm(prompt)
    try:
        titles = json.loads(raw)
        if not isinstance(titles, list):
            raise ValueError
    except Exception:
        # fallback: simple line split
        titles = [line.strip("- •").strip() for line in raw.splitlines() if line.strip()][:8]

    return {"outline": titles}
