import React from 'react'
import ReactDOM from 'react-dom/client'
import {RouterProvider} from "react-router-dom";
import { createTheme, MantineProvider } from '@mantine/core';
import {QueryClient, QueryClientProvider} from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Notifications } from '@mantine/notifications'
import router from "./router";
import './index.css'
import './reset.css'
import '@mantine/core/styles.css';
import '@mantine/charts/styles.css';
import '@mantine/notifications/styles.css';


const theme = createTheme({
    fontFamily: 'Manrope, sans-serif',
    defaultRadius: 'md',
    primaryColor: "violet"
});

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            retry: 1
        }
    }
});

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <MantineProvider theme={theme} withGlobalClasses>
            <QueryClientProvider client={queryClient}>
                <Notifications />
                <RouterProvider router={router} />
                <ReactQueryDevtools initialIsOpen />
            </QueryClientProvider>
        </MantineProvider>
    </React.StrictMode>
);
