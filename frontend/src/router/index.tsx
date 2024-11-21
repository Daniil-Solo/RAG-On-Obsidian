import {createBrowserRouter} from "react-router-dom";
import {Page404} from "../pages/404";
import {ChatPage} from "../pages/chat";
import {SettingsPage} from "../pages/settings";


const router = createBrowserRouter([
    {
        path: "/",
        element: (
            <ChatPage/>
        ),
    },
    {
        path: "/chat",
        element: (
            <ChatPage/>
        ),
    },
    {
        path: "/settings",
        element: (
            <SettingsPage/>
        ),
    },
    {
        path: "*",
        element: (
            <Page404/>
        )
    }
]);

export default router;