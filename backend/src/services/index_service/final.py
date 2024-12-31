import logging
from datetime import datetime
from pathlib import Path

from src.repositories.index.interface import FileRepository, UpdateProgressRepository
from src.services.index_service.base import BaseIndexService


class DemoIndexService(BaseIndexService):
    def __init__(
        self,
        obsidian_path: str,
        file_repository: FileRepository,
        update_progress_repository: UpdateProgressRepository,
    ) -> None:
        self.obsidian_path = Path(obsidian_path)
        self.file_repository = file_repository
        self.update_progress_repository = update_progress_repository

    async def find_files_to_update(self) -> list[str]:
        all_file_records = await self.file_repository.get_all()
        file_to_update_time = {file_record["name"]: file_record["updated_at"] for file_record in all_file_records}

        # updated files
        current_files_set = set()
        files_to_update_set = set()
        for path in self.obsidian_path.rglob("*.md"):
            str_path = path.as_posix()
            existing_file_has_been_updated = (
                str_path in file_to_update_time and
                datetime.utcfromtimestamp(path.stat().st_mtime) != file_to_update_time[str_path]
            )
            if existing_file_has_been_updated:
                files_to_update_set.add(str_path)
            current_files_set.add(str_path)

        # created and deleted files
        indexed_files_set = set(file_to_update_time.keys())
        created_and_deleted_files = list(indexed_files_set ^ current_files_set)
        for file in created_and_deleted_files:
            files_to_update_set.add(file)

        return list(files_to_update_set)

    async def get_info(self) -> dict:
        files_to_update = await self.find_files_to_update()
        n_documents_to_update = len(files_to_update)
        n_all_documents = len(list(self.obsidian_path.rglob("*.md")))

        last_update_process = await self.update_progress_repository.get_last_update_process()
        last_update_time = None if last_update_process is None else last_update_process["finished_at"]
        in_update_process = False if last_update_process is None else last_update_process["is_actual"]

        return {
            "n_documents_to_update": n_documents_to_update,
            "n_all_documents": n_all_documents,
            "last_update_time": last_update_time,
            "in_update_process": in_update_process,
        }

    async def get_clusters(self) -> list[dict]:
        all_file_records = await self.file_repository.get_all()
        return [{k: file_record[k] for k in ("name", "x", "y")} for file_record in all_file_records]

    async def remove(self) -> None:
        await self.file_repository.remove()

    async def update(self, files: list[dict]) -> None:
        process = await self.update_progress_repository.get_update_process()
        stage_id = await self.update_progress_repository.start_progress_stage(
            name="2. Updating index", process_id=process["id"]
        )
        for idx, file in enumerate(files):
            await self.update_progress_repository.update_progress_stage(
                stage_id=stage_id,
                progress=int(idx / len(files) * 100),
            )
            if file["is_removed"]:
                await self.file_repository.remove_one(file["file_path"])
                continue
            await self.file_repository.update(
                name=file["file_path"],
                x=file["x"],
                y=file["y"],
                size=Path(file["file_path"]).stat().st_size,
                updated_at=datetime.utcfromtimestamp(Path(file["file_path"]).stat().st_mtime),
            )
        await self.update_progress_repository.finish_progress_stage(stage_id=stage_id)
