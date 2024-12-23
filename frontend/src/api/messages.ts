import axiosInstance from "./axios-config";
import {MessageResponse} from "../types/general"
import {QueryRequest, AnswerResponse, MessageHistoryResponse} from "../types/messages"


const API_MESSAGES = '/api/messages/';


const getChatMessages = async (offset = 0, limit = 10) => {
    const response = await axiosInstance.get<MessageHistoryResponse>(API_MESSAGES, {
        params: { offset, limit }
    });
    return response.data;
};


const sendChatMessage = async (data: QueryRequest) => {
    const response = await axiosInstance.post<AnswerResponse>(API_MESSAGES, data);
    return response.data;
};

const cleanChatMessages = async () => {
    const response = await axiosInstance.delete<MessageResponse>(API_MESSAGES);
    return response.data;
};



export {getChatMessages, sendChatMessage, cleanChatMessages};