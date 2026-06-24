import logging
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.models import PromptVersion
from backend.database.db import get_db_session

logger = logging.getLogger(__name__)

DEFAULT_PROMPTS = [
    {
        "version": "v1",
        "name": "Basic Assistant",
        "content": "You are a helpful AI assistant. Answer the question clearly and concisely.",
        "description": "Simple general purpose prompt.",
    },
    {
        "version": "v2",
        "name": "Detailed Assistant",
        "content": "You are an expert AI assistant. Provide detailed, accurate, and well-structured answers. Always explain your reasoning.",
        "description": "More detailed response prompt.",
    },
    {
        "version": "v3",
        "name": "Concise Assistant",
        "content": "You are a precise AI assistant. Answer in 1-2 sentences only. Be direct and factual.",
        "description": "Short concise answers prompt.",
    },
]


class PromptVersionManager:

    def __init__(self):
        self.db: Session = get_db_session()
        self._seed_defaults()

    def _seed_defaults(self):
        try:
            existing = self.db.query(PromptVersion).count()
            if existing == 0:
                for p in DEFAULT_PROMPTS:
                    prompt = PromptVersion(**p)
                    self.db.add(prompt)
                self.db.commit()
                logger.info("Default prompts seeded.")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Seeding prompts failed: {e}")

    def get_all(self) -> list:
        try:
            return self.db.query(PromptVersion).order_by(PromptVersion.id).all()
        except Exception as e:
            logger.error(f"Failed to fetch prompts: {e}")
            return []

    def get_by_version(self, version: str) -> PromptVersion:
        try:
            return self.db.query(PromptVersion).filter(
                PromptVersion.version == version
            ).first()
        except Exception as e:
            logger.error(f"Failed to fetch prompt version {version}: {e}")
            return None

    def create(self, version: str, name: str, content: str, description: str = "") -> PromptVersion:
        try:
            existing = self.get_by_version(version)
            if existing:
                raise ValueError(f"Prompt version '{version}' already exists.")

            prompt = PromptVersion(
                version=version,
                name=name,
                content=content,
                description=description,
            )
            self.db.add(prompt)
            self.db.commit()
            self.db.refresh(prompt)
            logger.info(f"Prompt version '{version}' created.")
            return prompt

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create prompt: {e}")
            raise

    def delete(self, version: str) -> bool:
        try:
            prompt = self.get_by_version(version)
            if not prompt:
                return False
            self.db.delete(prompt)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to delete prompt: {e}")
            return False

    def list_versions(self) -> list:
        prompts = self.get_all()
        return [{"version": p.version, "name": p.name, "description": p.description} for p in prompts]