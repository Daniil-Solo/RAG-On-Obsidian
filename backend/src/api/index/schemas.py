from datetime import datetime

from pydantic import BaseModel, Field


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
            clusters=[ClusterSchema(**cluster) for cluster in clusters],
        )


class IndexProgressResponse(BaseModel):
    name: str
    value: int
