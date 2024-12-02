import axiosInstance from "./axios-config";
import {LLMSettingsRequest, LLMSettingsResponse, LLMAvailabilityResponse} from "../types/settings";
import { MessageResponse } from "../types/general";


const API_SETTINGS_LLM = '/api/settings/llm';
const API_SETTINGS_LLM_CHECK = `${API_SETTINGS_LLM}/checking`;


const checkLlmAvailability = async (data: LLMSettingsRequest) => {
    const response = await axiosInstance.post<LLMAvailabilityResponse>(API_SETTINGS_LLM_CHECK, data);
    return response.data;
};


const updateLlmSettings = async (data: LLMSettingsRequest) => {
    const response = await axiosInstance.put<MessageResponse>(API_SETTINGS_LLM, data);
    return response.data;
};

const getLlmSettings = async () => {
    const response = await axiosInstance.get<LLMSettingsResponse>(API_SETTINGS_LLM);
    return response.data;
};


export {checkLlmAvailability, updateLlmSettings, getLlmSettings};