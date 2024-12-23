import { getIndexInfo, getClusters, updateIndex, getIndexProgress, deleteIndex } from "../api/update-index";
import { useMutation, useQuery, useQueryClient, keepPreviousData  } from "@tanstack/react-query";
import { MessageResponse } from "../types/general";
import handleAPIError from "../utils/error-notifications";
import notifySuccess from "../utils/success-notifications";

const useIndexInfo = () => {
    return useQuery({
        queryKey: ["index_info"],
        queryFn: getIndexInfo,
        staleTime: 1000 * 60 * 10,
    });
};

const useClusters = () => {
    return useQuery({
        queryKey: ["index_clusters"],
        queryFn: getClusters,
        staleTime: 1000 * 60 * 10,
    });
};

const useUpdateIndex = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: ["update_index"],
        mutationFn: updateIndex,
        onError: handleAPIError,
        onSuccess: (data: MessageResponse) => {
            queryClient.invalidateQueries({ queryKey: ["index_info"] });
            queryClient.invalidateQueries({ queryKey: ["index_clusters"] });
            queryClient.invalidateQueries({ queryKey: ["index_progress"] });
            notifySuccess(data.message);
        },
    });
};

const useIndexProgress = (shouldFetch: boolean) => {
    return useQuery({
        queryKey: ["index_progress"],
        queryFn: getIndexProgress,
        staleTime: 1000 * 60 * 10,
        placeholderData: keepPreviousData,
        enabled: shouldFetch,
        refetchInterval: shouldFetch ? 1000 : false
    });
};

const useDeleteIndex = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: ["delete_index"],
        mutationFn: deleteIndex,
        onError: handleAPIError,
        onSuccess: (data: MessageResponse) => {
            queryClient.invalidateQueries({ queryKey: ["index_info"] });
            queryClient.invalidateQueries({ queryKey: ["index_clusters"] });
            queryClient.invalidateQueries({ queryKey: ["index_progress"] });
            notifySuccess(data.message);
        },
    });
};

// Экспорт хуков
export { useIndexInfo, useClusters, useUpdateIndex, useIndexProgress, useDeleteIndex };