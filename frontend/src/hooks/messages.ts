import { getChatMessages, sendChatMessage, cleanChatMessages } from "../api/messages";
import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import { QueryRequest } from "../types/messages";
import handleAPIError from "../utils/error-notifications";


const useChatMessages = () => {
    return useQuery(
        {
            queryKey: ["chat_messages"],
            queryFn: () => getChatMessages(),
            staleTime: 1000 * 60 * 10,
        }
    )
};

const useSendChatMessage = () => {
    const queryClient = useQueryClient();
    return useMutation(
        {
            mutationKey: ["send_chat_messages"],
            mutationFn: (data: QueryRequest) => sendChatMessage(data),
            onError: handleAPIError,
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["chat_messages"] });
            },
        }
    )
};

const useCleanChatMessage = () => {
    const queryClient = useQueryClient();
    return useMutation(
        {
            mutationKey: ["clean_chat_messages"],
            mutationFn: () => cleanChatMessages(),
            onError: handleAPIError,
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["chat_messages"] });
            },
        }
    )
};

export {useChatMessages, useSendChatMessage, useCleanChatMessage};