import {Title, Stack, Progress, Group, Button, Text, Paper, Box, LoadingOverlay } from '@mantine/core';
import { useState, useEffect } from 'react';
import { ScatterChart } from '@mantine/charts';
import { useClusters, useIndexInfo, useDeleteIndex, useUpdateIndex, useIndexProgress } from "../../hooks/update-index";
import { ClusterSchema } from '../../types/update-index';
import { getRandomColorAndNumber } from "../../utils/random-color"
import { formatDatetime } from "../../utils/format-datetime"
import BasicLayout from "../../layouts/basic-layout"




const toScatterChartSeries = (clusters: Array<ClusterSchema>) => {
    return clusters.map(cluster => {
        return {
            color: getRandomColorAndNumber(),
            name: cluster.name,
            data: [
                {x: cluster.x, y: cluster.y}
            ]
        }
    })
}


const ChartTooltip = (props: {payload: {name: string, x: number, y: number}}) => {
    if (!props.payload) return null;
    if (!props.payload["name"]) return null;
    return (
      <Paper px="md" py="sm" withBorder shadow="md" radius="md">
          <Text fz="xs">
            {props.payload.name}
          </Text>
      </Paper>
    );
  }
  


export const IndexPage = () => {
    const [shouldFetch, setShouldFetch] = useState(false);

    const {data: clusterData, isSuccess: isClusterSuccess,  isLoading: isClusterLoading} = useClusters();
    const {data: indexInfo, isSuccess: isIndexInfoSuccess, isLoading: isIndexInfoLoading, refetch: refetchIndexInfo} = useIndexInfo();
    const {mutateAsync: deleteIndex, isPending: isDeletePending} = useDeleteIndex();
    const {mutateAsync: startUpdateIndex, isPending: isUpdatePending} = useUpdateIndex();
    const {data: indexProgress, isSuccess: isProgressSuccess} = useIndexProgress(shouldFetch);

    useEffect(() => {
        if (isProgressSuccess && indexProgress && !indexProgress.in_progress) {
            setShouldFetch(false);
        }
      }, [indexProgress]);

    
    const updateIndex = () => {
        startUpdateIndex();
        setShouldFetch(true);
    }
    
    return (
        <BasicLayout>
            <Stack>
                <Box pos="relative">
                    <LoadingOverlay visible={isClusterLoading} zIndex={1000} loaderProps={{ color: 'violet', type: 'bars' }} overlayProps={{ radius: "sm", blur: 1 }} />
                    <ScatterChart
                        h={400}
                        data={isClusterSuccess? toScatterChartSeries(clusterData.clusters): []}
                        dataKey={{ x: 'x', y: 'y' }}
                        xAxisLabel=""
                        yAxisLabel=""
                        withYAxis={false}
                        withXAxis={false}
                        gridAxis="xy"
                        tooltipProps={{offset:0, content: ({payload}) => payload && payload.length && <ChartTooltip payload={payload[0].payload} />}}
                    />
                </Box>
                <Group>
                    <Button onClick={() => refetchIndexInfo()} disabled={isIndexInfoLoading} loading={isIndexInfoLoading} loaderProps={{type: "dots"}}>
                        Refresh info
                    </Button>
                    <Button onClick={updateIndex} disabled={isDeletePending || isUpdatePending} loading={isUpdatePending} loaderProps={{type: "dots"}}>
                        Update Index
                    </Button>
                    <Button onClick={() => deleteIndex()} disabled={isDeletePending || isUpdatePending} loading={isDeletePending} loaderProps={{type: "dots"}}>
                        Remove Index
                    </Button>
                </Group>
                <div>
                    <Title order={4} ta="left">
                        General information
                    </Title>
                    <Text >
                        The index was last updated on {isIndexInfoLoading? "loading": isIndexInfoSuccess && indexInfo.last_update_time? formatDatetime(indexInfo.last_update_time): "not found"}
                    </Text>
                    <Text >
                        The number of all documents is {isIndexInfoLoading? "loading": isIndexInfoSuccess? indexInfo.n_all_documents: "not found"}
                    </Text>
                    <Text >
                        The number of all documents to update is {isIndexInfoLoading? "loading": isIndexInfoSuccess? indexInfo.n_documents_to_update: "not found"}
                    </Text>
                </div>
                {
                    isProgressSuccess && indexProgress.in_progress && (
                        <Title order={4} ta="left">
                            The progress of updating index
                        </Title>
                    )
                }
                {
                    isProgressSuccess && indexProgress.in_progress && indexProgress.stages.map(
                        stage => (
                            <Group>
                                <Title w={150} order={4} ta="left">
                                    {stage.name}
                                </Title>
                                <Progress w={400} color="violet" value={stage.value} animated />
                            </Group>
                        )
                    )
                }
            </Stack>
        </BasicLayout>
    );
}