interface IndexInfoResponse {
    n_documents_to_update: number;
    n_all_documents: number;
    last_update_time: string | null;
    in_update_process: boolean;
}

interface ClusterSchema {
    name: string;
    x: number;
    y: number;
}

interface ClustersResponse {
    clusters: ClusterSchema[];
}

interface StageProgressSchema {
    name: string;
    value: number;
}

interface UpdateIndexProgressResponse {
    in_progress: boolean;
    stages: StageProgressSchema[];
}

export type { IndexInfoResponse, ClusterSchema, ClustersResponse, StageProgressSchema, UpdateIndexProgressResponse }