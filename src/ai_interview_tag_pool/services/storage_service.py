"""
Storage Service - Handles persistence of tagged data (JSON, CSV)

Saves tagged subtitle/segment results to disk for later use or review.
"""
from typing import Any, Dict, List, Optional
from .base_service import BaseService
import os
import json
import csv

class StorageService(BaseService):
    """
    StorageService saves tagged results to JSON and/or CSV format.
    """
    def __init__(self, config):
        super().__init__(config)
        self.save_dir = getattr(config, "SAVE_DIR", "output")
        os.makedirs(self.save_dir, exist_ok=True)

    def execute(self, data: Dict[str, Any], prefix: str = "result") -> Dict[str, Any]:
        try:
            basepath = os.path.join(self.save_dir, f"{prefix}")
            json_path = basepath + ".json"
            csv_path = basepath + ".csv"
            self._save_json(data, json_path)
            self._save_csv(data, csv_path)
            return self.success_result({
                "json_path": json_path,
                "csv_path": csv_path
            }, message="Data saved to disk")
        except Exception as e:
            self.log_error("Failed to save results", e)
            return self.error_result("Persistence failed", e)

    def _save_json(self, data: Dict[str, Any], path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _save_csv(self, data: Dict[str, Any], path: str) -> None:
        segments = data.get("segments") or data.get("subtitles") or []
        if not segments:
            return
        keys = list(segments[0].keys())
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(segments)
