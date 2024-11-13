import {Stack} from '@mantine/core';
import {IMessage} from "./../../types/message"
import Message from "./../message"


export interface MessageHistoryProps  {
  messages: Array<IMessage>
}

const MessageHistory = (props: MessageHistoryProps) => {

  return (
    <Stack h="100%" >
        {
          props.messages.map(message => (
            <Message message={message}/>
          ))
        }
    </Stack>
    );
}
export default MessageHistory;