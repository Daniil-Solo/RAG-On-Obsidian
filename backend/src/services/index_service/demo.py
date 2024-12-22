from datetime import datetime
from pathlib import Path

from src.repositories.index.interface import FileRepository
from src.services.index_service.base import BaseIndexService


class DemoIndexService(BaseIndexService):
    def __init__(
        self,
        obsidian_path: str,
        file_repository: FileRepository,
    ) -> None:
        self.obsidian_path = Path(obsidian_path)
        self.file_repository = file_repository

    async def find_files_to_update(self) -> list[str]:
        all_file_records = await self.file_repository.get_all()
        file_to_update_time = {file_record["name"]: file_record["updated_at"] for file_record in all_file_records}

        # updated files
        current_files = []
        files_to_update = []
        for path in self.obsidian_path.rglob("*.md"):
            str_path = path.as_posix()
            if str_path in file_to_update_time and datetime.utcfromtimestamp(path.stat().st_mtime) != file_to_update_time[str_path]:
                files_to_update.append(str_path)
            current_files.append(str_path)

        # created and deleted files
        indexed_files = set(file_to_update_time.keys())
        created_and_deleted_files = list(indexed_files ^ set(current_files))

        files_to_update.extend(created_and_deleted_files)

        return files_to_update

    async def get_info(self) -> dict:
        files_to_update = await self.find_files_to_update()
        n_documents_to_update = len(files_to_update)
        n_all_documents = len(list(path for path in self.obsidian_path.rglob("*.md")))
        index_info = await self.file_repository.get_index_info()
        last_update_time = None if index_info is None else index_info["last_update_time"]
        in_update_process = False  # TODO

        return {
            "n_documents_to_update": n_documents_to_update,
            "n_all_documents": n_all_documents,
            "last_update_time": last_update_time,
            "in_update_process": in_update_process,
        }

    async def get_clusters(self) -> list[dict]:
        all_file_records = await self.file_repository.get_all()

        return [{k: file_record[k] for k in ("name", "x", "y")} for file_record in all_file_records]

    async def get_last_updated_process(self) -> dict:
        # TODO
        pass

    async def remove(self) -> None:
        await self.file_repository.remove()

    async def update(self, files: list[dict]) -> None:
        await self.remove()

        for file in files:
            await self.file_repository.update(
                name=file["file_path"],
                x=file["x"],
                y=file["y"],
                size=Path(file["file_path"]).stat().st_size,
                updated_at=datetime.utcfromtimestamp(Path(file["file_path"]).stat().st_mtime),
            )
