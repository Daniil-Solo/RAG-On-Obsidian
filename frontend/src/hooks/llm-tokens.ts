import { getLLMTokens } from "../api/llm-tokens";
import {useQuery} from "@tanstack/react-query";


const useLLMTokens = () => {
    return useQuery(
        {
            queryKey: ["llm_tokens"],
            queryFn: () => getLLMTokens(),
            staleTime: 1000 * 60 * 10,
        }
    )
};


export {useLLMTokens};