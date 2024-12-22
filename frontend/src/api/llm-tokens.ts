import axiosInstance from "./axios-config";
import {LLMTokensResponse} from "../types/llm-tokens";


const API_LLM_TOKENS = '/api/llm_tokens/';


const getLLMTokens = async () => {
    const response = await axiosInstance.get<LLMTokensResponse>(API_LLM_TOKENS);
    return response.data;
};


export {getLLMTokens};