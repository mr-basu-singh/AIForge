import os
import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from backend.api.schemas import (
    RunExperimentRequest,
    CreatePromptRequest,
)
from backend.experiments.experiment_tracker import ExperimentTracker
from backend.experiments.prompt_versioning import PromptVersionManager
from backend.adapters.groq_adapter import ModelRouter
from backend.reports.pdf_generator import PDFReportGenerator
from backend.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

tracker = ExperimentTracker()
prompt_manager = PromptVersionManager()
model_router = ModelRouter()
pdf_generator = PDFReportGenerator()


# --- Health ---
@router.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


# --- Models ---
@router.get("/models")
def get_models():
    return {"models": model_router.get_available_models()}


# --- Prompts ---
@router.get("/prompts")
def get_prompts():
    return {"prompts": prompt_manager.list_versions()}


@router.post("/prompts")
def create_prompt(request: CreatePromptRequest):
    try:
        prompt = prompt_manager.create(
            version=request.version,
            name=request.name,
            content=request.content,
            description=request.description,
        )
        return {"message": "Prompt created.", "version": prompt.version}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/prompts/{version}")
def delete_prompt(version: str):
    success = prompt_manager.delete(version)
    if not success:
        raise HTTPException(status_code=404, detail="Prompt version not found.")
    return {"message": f"Prompt version '{version}' deleted."}


# --- Dataset Upload ---
@router.post("/datasets/upload")
async def upload_dataset(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files allowed.")

        os.makedirs(settings.DATASETS_DIR, exist_ok=True)
        save_path = f"{settings.DATASETS_DIR}/{file.filename}"

        contents = await file.read()
        if len(contents) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Max 5MB.")

        with open(save_path, "wb") as f:
            f.write(contents)

        return {"message": "Dataset uploaded.", "path": save_path, "filename": file.filename}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datasets")
def list_datasets():
    try:
        files = [f for f in os.listdir(settings.DATASETS_DIR) if f.endswith(".csv")]
        return {"datasets": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Experiments ---
@router.post("/experiments/run")
def run_experiment(request: RunExperimentRequest):
    try:
        # Validate models
        available = model_router.get_available_models()
        for model in request.selected_models:
            if model not in available:
                raise HTTPException(status_code=400, detail=f"Model '{model}' not available.")

        # Validate dataset
        if not os.path.exists(request.dataset_path):
            raise HTTPException(status_code=400, detail="Dataset file not found.")

        experiment_id = tracker.run_experiment(
            name=request.name,
            dataset_path=request.dataset_path,
            selected_models=request.selected_models,
            prompt_version=request.prompt_version,
        )
        return {"message": "Experiment completed.", "experiment_id": experiment_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/experiments")
def get_all_experiments():
    return {"experiments": tracker.get_all_experiments()}


@router.get("/experiments/{experiment_id}")
def get_experiment(experiment_id: int):
    exp = tracker.get_experiment(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found.")
    return exp


@router.get("/experiments/{experiment_id}/metrics")
def get_metrics(experiment_id: int):
    metrics = tracker.get_experiment_metrics(experiment_id)
    if not metrics:
        raise HTTPException(status_code=404, detail="No metrics found.")
    return {"metrics": metrics}


@router.get("/experiments/{experiment_id}/results")
def get_results(experiment_id: int, model_name: str = None):
    results = tracker.get_experiment_results(experiment_id, model_name)
    return {"results": results}


@router.get("/experiments/{experiment_id}/best-model")
def get_best_model(experiment_id: int):
    best = tracker.get_best_model(experiment_id)
    if not best:
        raise HTTPException(status_code=404, detail="No results found.")
    return {"best_model": best}


# --- Reports ---
@router.get("/experiments/{experiment_id}/report")
def download_report(experiment_id: int):
    try:
        exp = tracker.get_experiment(experiment_id)
        if not exp:
            raise HTTPException(status_code=404, detail="Experiment not found.")

        metrics = tracker.get_experiment_metrics(experiment_id)
        best = tracker.get_best_model(experiment_id)
        results = tracker.get_experiment_results(experiment_id)

        pdf_path = pdf_generator.generate(
            experiment=exp,
            metrics=metrics,
            best_model=best,
            results=results,
        )

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"AIForge_Report_Experiment_{experiment_id}.pdf"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))