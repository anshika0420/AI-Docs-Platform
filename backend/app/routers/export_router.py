from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import get_current_user
from .. import models
from ..generator import assemble_docx, assemble_pptx

router = APIRouter(prefix="/api/export", tags=["export"])

@router.get("/{project_id}")
def export_project(
    project_id: int,
    format: str = "auto",  # 'docx', 'pptx', or 'auto'
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

    sections = project.sections

    doc_type = project.doc_type
    if format in ("docx", "pptx"):
        doc_type = format

    if doc_type == "pptx":
        bio = assemble_pptx(project, sections)
        filename = f"project_{project.id}.pptx"
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    else:
        bio = assemble_docx(project, sections)
        filename = f"project_{project.id}.docx"
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    return StreamingResponse(bio, media_type=media_type, headers=headers)
