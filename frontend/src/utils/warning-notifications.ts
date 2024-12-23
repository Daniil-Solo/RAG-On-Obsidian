import { notifications } from '@mantine/notifications';


const notifyWarning = (text: string, title: string = "Warning") => {
    notifications.show({
        color: "orange",
        title: title,
        message: text,
        autoClose: 3000,
    })
}
export default notifyWarning;