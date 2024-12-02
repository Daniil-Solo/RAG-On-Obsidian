import { getLLMSettings, updateLLMSettings, checkLLMAvailability } from "../api/settings";
import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query";
import { LLMSettingsRequest, LLMAvailabilityResponse } from "../types/settings";
import handleAPIError from "../utils/error-notifications";
import notifySuccess from "../utils/success-notifications";
import notifyWarning from "../utils/warning-notifications";


const useLLMSettings = () => {
    return useQuery(
        {
            queryKey: ["settings_llm"],
            queryFn: () => getLLMSettings(),
            staleTime: 1000 * 60 * 10,
        }
    )
};

const useUpdateLLMSettings = () => {
    const queryClient = useQueryClient();
    return useMutation(
        {
            mutationKey: ["settings_llm_check"],
            mutationFn: (data: LLMSettingsRequest) => updateLLMSettings(data),
            onError: handleAPIError,
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ["settings_llm"] });
            },
        }
    )
};

const useCheckLLM = () => {
    return useMutation(
        {
            mutationKey: ["settings_llm_check"],
            mutationFn: (data: LLMSettingsRequest) => checkLLMAvailability(data),
            onError: handleAPIError,
            onSuccess: (data: LLMAvailabilityResponse) => {
                if (data.is_available){
                    notifySuccess("LLM is available")
                } else {
                    notifyWarning("LLM is not available with these credentials")
                }
            },
        }
    )
};

export {useLLMSettings, useUpdateLLMSettings, useCheckLLM};