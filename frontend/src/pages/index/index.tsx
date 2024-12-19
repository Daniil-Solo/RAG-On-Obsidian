import {Title, Stack, Progress, Group, Button, Text, Paper, Flex, Box, LoadingOverlay } from '@mantine/core';
import { ScatterChart } from '@mantine/charts';
import BasicLayout from "../../layouts/basic-layout"


const data = [
    {
      color: 'blue.5',
      name: 'PySpark',
      data: [
        { x: 25, y: 20 },
      ],
    },
    {
        color: 'violet.9',
        name: 'Apache Spark',
        data: [
          { x: 26, y: 22 },
        ],
      },
]


const ChartTooltip = (props: {payload: {name: string, x: number, y: number}}) => {
    if (!props.payload) return null;
    if (!props.payload["name"]) return null;
    return (
      <Paper px="md" py="sm" withBorder shadow="md" radius="md">
          <Text fz="sm">
            {props.payload.name}
          </Text>
      </Paper>
    );
  }
  


export const IndexPage = () => {
    return (
        <BasicLayout>
            <Stack>
                <Flex gap={0} justify="flex-start" align="flex-start">
                <Box w={"70%"} pos="relative">
                    <LoadingOverlay visible={false} zIndex={1000} loaderProps={{ color: 'violet', type: 'bars' }} overlayProps={{ radius: "sm", blur: 1 }} />
                    <ScatterChart
                        h={350}
                        data={data}
                        dataKey={{ x: 'x', y: 'y' }}
                        xAxisLabel=""
                        yAxisLabel=""
                        withYAxis={false}
                        withXAxis={false}
                        gridAxis="xy"
                        tooltipProps={{content: ({payload}) => payload && payload.length && <ChartTooltip payload={payload[0].payload} />}}
                    />
                </Box>
                    
                    <div style={{width: "30%", paddingLeft: "16px"}}>
                        <Title w={200} order={4} ta="left">
                            General information
                        </Title>
                        <Text >
                            Last update date: 08.12.2024
                        </Text>
                        <Text >
                            All documents: 87
                        </Text>
                        <Text >
                            All symbols: 12354
                        </Text>
                        <Text >
                            Documents to update: 2
                        </Text>
                    </div>
                    
                </Flex>
                <Group>
                    <Button>
                        Update Index
                    </Button>
                    <Button>
                        Remove Index
                    </Button>
                </Group>
                <Group>
                    <Title w={150} order={4} ta="left">
                        Search files
                    </Title>
                    <Progress w={400} color="violet" value={30} animated />
                </Group>
                <Group>
                    <Title w={150} order={4} ta="left">
                        Vectorization
                    </Title>
                    <Progress w={400} color="violet" value={0} animated />
                </Group>
                <Group>
                    <Title w={150} order={4} ta="left">
                        Updating Index
                    </Title>
                    <Progress w={400} color="violet" value={0} animated />
                </Group>
            </Stack>
        </BasicLayout>
    );
}