import {Title, Stack} from '@mantine/core';
import BasicLayout from "../../layouts/basic-layout"

export const Page404 = () => {
    return (
        <BasicLayout>
            <Stack>
                <Title order={2} ta="center">404</Title>
                <Title order={3} ta="center">This page doesnt exist</Title>
            </Stack>
        </BasicLayout>
    );
}