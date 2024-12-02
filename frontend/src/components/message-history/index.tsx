import {Stack} from '@mantine/core';
import {MessageSchema} from "../../types/messages"
import Message from "./../message"


export interface MessageHistoryProps  {
  messages: Array<MessageSchema>
}

const MessageHistory = (props: MessageHistoryProps) => {

  return (
    <Stack h="100%" >
        {
          props.messages.map(message => (
            <Message key={message.id} message={message}/>
          ))
        }
    </Stack>
    );
}
export default MessageHistory;