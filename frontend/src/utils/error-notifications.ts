import { isAxiosError } from "axios";
import { MessageResponse } from "../types/general";
import { notifications } from '@mantine/notifications';


const handleAPIError = (error: unknown) => {
    if (isAxiosError<MessageResponse>(error)) {
        notifications.show({
            color: "red",
            title: "Error!",
            message: error.response?.data.message,
            autoClose: 3000,
        })
    } else {
        console.error('Unknown error:', error);
    }
}
export default handleAPIError;