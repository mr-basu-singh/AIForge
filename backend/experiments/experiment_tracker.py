import logging
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.models import Experiment, ExperimentResult, ModelMetrics
from backend.database.db import get_db_session
from backend.adapters.groq_adapter import ModelRouter
from backend.evaluators.scoring_engine import ScoringEngine, compute_model_summary
from backend.experiments.prompt_versioning import PromptVersionManager

logger = logging.getLogger(__name__)


class ExperimentTracker:

    def __init__(self):
        self.db: Session = get_db_session()
        self.router = ModelRouter()
        self.scoring_engine = ScoringEngine()
        self.prompt_manager = PromptVersionManager()

    def run_experiment(
        self,
        name: str,
        dataset_path: str,
        selected_models: list,
        prompt_version: str = "v1",
        progress_callback=None,
    ) -> int:
        """
        Full experiment pipeline.
        Returns experiment_id.
        """

        # --- Load dataset ---
        try:
            df = pd.read_csv(dataset_path)
            if "question" not in df.columns or "expected_answer" not in df.columns:
                raise ValueError("Dataset must have 'question' and 'expected_answer' columns.")
            df = df.dropna(subset=["question", "expected_answer"])
            df = df.head(50)  # Safety limit
        except Exception as e:
            logger.error(f"Dataset loading failed: {e}")
            raise

        # --- Load prompt ---
        prompt_obj = self.prompt_manager.get_by_version(prompt_version)
        prompt_content = prompt_obj.content if prompt_obj else "You are a helpful assistant."

        # --- Create experiment record ---
        experiment = Experiment(
            name=name,
            dataset_name=dataset_path.split("/")[-1].split("\\")[-1],
            models_used=selected_models,
            prompt_version=prompt_version,
            status="running",
        )
        self.db.add(experiment)
        self.db.commit()
        self.db.refresh(experiment)
        experiment_id = experiment.id
        logger.info(f"Experiment #{experiment_id} started: {name}")

        total_steps = len(selected_models) * len(df)
        current_step = 0

        try:
            for model_name in selected_models:
                logger.info(f"Running model: {model_name}")
                model_results = []

                for _, row in df.iterrows():
                    question = str(row["question"]).strip()
                    expected = str(row["expected_answer"]).strip()

                    # Generate
                    model_response = self.router.run(prompt_content, question, model_name)

                    # Evaluate
                    eval_result = self.scoring_engine.evaluate(model_response, question, expected)

                    # Save result
                    db_result = ExperimentResult(
                        experiment_id=experiment_id,
                        model_name=model_name,
                        question=question,
                        expected_answer=expected,
                        generated_answer=eval_result.generated_answer,
                        similarity_score=eval_result.similarity_score,
                        llm_judge_score=eval_result.llm_judge_score,
                        latency_seconds=eval_result.latency_seconds,
                        tokens_used=eval_result.tokens_used,
                        cost_usd=eval_result.cost_usd,
                        is_hallucination=1 if eval_result.is_hallucination else 0,
                    )
                    self.db.add(db_result)
                    model_results.append(eval_result)

                    current_step += 1
                    if progress_callback:
                        progress_callback(current_step, total_steps)

                self.db.commit()

                # Save model summary metrics
                summary = compute_model_summary(model_results)
                metrics = ModelMetrics(
                    experiment_id=experiment_id,
                    model_name=model_name,
                    avg_similarity_score=summary["avg_similarity_score"],
                    avg_llm_judge_score=summary["avg_llm_judge_score"],
                    avg_latency_seconds=summary["avg_latency_seconds"],
                    total_cost_usd=summary["total_cost_usd"],
                    total_tokens=summary["total_tokens"],
                    success_rate=summary["success_rate"],
                    hallucination_rate=summary["hallucination_rate"],
                    total_questions=summary["total_questions"],
                )
                self.db.add(metrics)
                self.db.commit()
                logger.info(f"Model {model_name} completed. Avg similarity: {summary['avg_similarity_score']}")

            # Mark experiment complete
            experiment.status = "completed"
            experiment.completed_at = datetime.utcnow()
            self.db.commit()
            logger.info(f"Experiment #{experiment_id} completed successfully.")

        except Exception as e:
            experiment.status = "failed"
            self.db.commit()
            logger.error(f"Experiment #{experiment_id} failed: {e}")
            raise

        return experiment_id

    def get_experiment(self, experiment_id: int) -> dict:
        exp = self.db.query(Experiment).filter(Experiment.id == experiment_id).first()
        if not exp:
            return {}
        return {
            "id": exp.id,
            "name": exp.name,
            "dataset_name": exp.dataset_name,
            "models_used": exp.models_used,
            "prompt_version": exp.prompt_version,
            "status": exp.status,
            "created_at": str(exp.created_at),
            "completed_at": str(exp.completed_at),
        }

    def get_all_experiments(self) -> list:
        exps = self.db.query(Experiment).order_by(Experiment.id.desc()).all()
        return [
            {
                "id": e.id,
                "name": e.name,
                "dataset_name": e.dataset_name,
                "models_used": e.models_used,
                "status": e.status,
                "created_at": str(e.created_at),
            }
            for e in exps
        ]

    def get_experiment_metrics(self, experiment_id: int) -> list:
        metrics = self.db.query(ModelMetrics).filter(
            ModelMetrics.experiment_id == experiment_id
        ).all()
        return [
            {
                "model_name": m.model_name,
                "avg_similarity_score": m.avg_similarity_score,
                "avg_llm_judge_score": m.avg_llm_judge_score,
                "avg_latency_seconds": m.avg_latency_seconds,
                "total_cost_usd": m.total_cost_usd,
                "total_tokens": m.total_tokens,
                "success_rate": m.success_rate,
                "hallucination_rate": m.hallucination_rate,
                "total_questions": m.total_questions,
            }
            for m in metrics
        ]

    def get_experiment_results(self, experiment_id: int, model_name: str = None) -> list:
        query = self.db.query(ExperimentResult).filter(
            ExperimentResult.experiment_id == experiment_id
        )
        if model_name:
            query = query.filter(ExperimentResult.model_name == model_name)
        results = query.all()
        return [
            {
                "model_name": r.model_name,
                "question": r.question,
                "expected_answer": r.expected_answer,
                "generated_answer": r.generated_answer,
                "similarity_score": r.similarity_score,
                "llm_judge_score": r.llm_judge_score,
                "latency_seconds": r.latency_seconds,
                "tokens_used": r.tokens_used,
                "cost_usd": r.cost_usd,
                "is_hallucination": bool(r.is_hallucination),
            }
            for r in results
        ]

    def get_best_model(self, experiment_id: int) -> dict:
        metrics = self.get_experiment_metrics(experiment_id)
        if not metrics:
            return {}
        return max(metrics, key=lambda x: (x["avg_similarity_score"] + x["avg_llm_judge_score"] / 10) / 2)