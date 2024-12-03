import { isAxiosError } from "axios";
import { ErrorResponse } from "../types/general";
import { notifications } from '@mantine/notifications';


const handleAPIError = (error: unknown) => {
    if (isAxiosError<ErrorResponse>(error)) {
        notifications.show({
            color: "red",
            title: "Error!",
            message: error.response?.data.detail,
            autoClose: 5000,
        })
    } else {
        console.error('Unknown error:', error);
    }
}
export default handleAPIError;