import axiosInstance from "./axios-config";
import { 
    IndexInfoResponse, 
    ClustersResponse, 
    UpdateIndexProgressResponse
} from "../types/update-index";
import { MessageResponse } from "../types/general";


const API_INDEX_INFO = '/api/index/info/';
const API_INDEX_CLUSTERS = '/api/index/clusters';
const API_INDEX_UPDATE = '/api/index/';
const API_INDEX_PROGRESS = '/api/index/progress';


const getIndexInfo = async (): Promise<IndexInfoResponse> => {
    const response = await axiosInstance.get<IndexInfoResponse>(API_INDEX_INFO);
    return response.data;
};

const getClusters = async (): Promise<ClustersResponse> => {
    const response = await axiosInstance.get<ClustersResponse>(API_INDEX_CLUSTERS);
    return response.data;
};

const updateIndex = async (): Promise<MessageResponse> => {
    const response = await axiosInstance.put<MessageResponse>(API_INDEX_UPDATE);
    return response.data;
};

const getIndexProgress = async (): Promise<UpdateIndexProgressResponse> => {
    const response = await axiosInstance.get<UpdateIndexProgressResponse>(API_INDEX_PROGRESS);
    return response.data;
};

const deleteIndex = async (): Promise<MessageResponse> => {
    const response = await axiosInstance.delete<MessageResponse>(API_INDEX_UPDATE);
    return response.data;
};

export { getIndexInfo, getClusters, updateIndex, getIndexProgress, deleteIndex };