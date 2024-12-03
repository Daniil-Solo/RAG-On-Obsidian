import {Stack} from '@mantine/core';
import {MessageSchema} from "../../types/messages"
import Message from "./../message"


export interface MessageHistoryProps  {
  messages: Array<MessageSchema>,
  isAssistantThinking: boolean
}

const assistantThinkingMessage: MessageSchema = {
  id: 'thinking',
  role: 'assistant',
  content: 'In thinking...',
  datetime: ''
}

const MessageHistory = (props: MessageHistoryProps) => {

  return (
    <Stack h="100%" >
        {
          props.messages.map(message => (
            <Message key={message.id} message={message}/>
          ))
        }
        {
          props.isAssistantThinking && <Message message={assistantThinkingMessage}/>
        }
    </Stack>
    );
}
export default MessageHistory;