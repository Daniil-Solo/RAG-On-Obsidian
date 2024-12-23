from datetime import datetime
from pathlib import Path
from pydantic import BaseModel


class IndexInfoResponse(BaseModel):
    n_documents_to_update: int
    n_all_documents: int
    last_update_time: datetime | None
    in_update_process: bool


class ClusterSchema(BaseModel):
    name: str
    x: float
    y: float


class ClustersResponse(BaseModel):
    clusters: list[ClusterSchema]

    @staticmethod
    def from_list(clusters: list[dict]) -> "ClustersResponse":
        return ClustersResponse(
            clusters=[
                ClusterSchema(name=Path(cluster["name"]).stem, x=cluster["x"], y=cluster["y"])
                for cluster in clusters
            ],
        )


class StageProgressSchema(BaseModel):
    name: str
    value: int


class UpdateIndexProgressResponse(BaseModel):
    in_progress: bool
    stages: list[StageProgressSchema]
