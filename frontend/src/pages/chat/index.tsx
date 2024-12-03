import BasicLayout from "../../layouts/basic-layout"
import MessageHistory from "../../components/message-history"
import {ScrollArea, Textarea , ActionIcon, Flex} from '@mantine/core';
import { IconArrowRight } from '@tabler/icons-react';
import {useEffect, useRef, useState} from "react";
import { useChatMessages, useSendChatMessage } from "../../hooks/messages";
import { MessageSchema } from "../../types/messages";




export const ChatPage = () => {
    const viewport = useRef<HTMLDivElement | null>(null);
    const [messages, setMessages] = useState<Array<MessageSchema>>([]);
    const [userCurrentMessage, setUserCurrentMessage] = useState("");
    const {data, isSuccess} = useChatMessages();
    const {mutateAsync: sendMessage, isPending: isSendMessagePending} = useSendChatMessage();

    useEffect(() => {
        if (data){
            setMessages(data.messages)
        }
    }, [isSuccess, data]);

    useEffect(() => {
        viewport.current!.scrollTo({ top: viewport.current!.scrollHeight, behavior: 'smooth' });
    }, [messages]);

    const sendMessageWrapper = () => {
        if (userCurrentMessage !== "") {
            setMessages(messages => [...messages, {role: "user", content: userCurrentMessage, datetime: "now", id: new Date().getTime().toString()}]);
            setUserCurrentMessage("");
            sendMessage({content: userCurrentMessage}).then((data) => {
                setMessages(messages => [...messages, {role: "assistant", content: data.answer, datetime: "now", id: "123"}]);
            }, (reason) => {
                console.log(reason);
            })
        }
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey){
            e.preventDefault();
            sendMessageWrapper();
        }
    }


    return (
        <BasicLayout>
            <Flex direction={"row"} h="100%" pb={8}>
                <Flex direction={"column"} h="100%" w="70%">
                    <ScrollArea p={16} style={{flexGrow: 1}} viewportRef={viewport}>
                        <MessageHistory messages={messages} isAssistantThinking={isSendMessagePending}/>
                    </ScrollArea>
                    <Textarea
                        autoFocus={true}
                        value={userCurrentMessage}
                        onChange={e => setUserCurrentMessage(e.target.value)}
                        mt={"auto"}
                        radius="md"
                        size="md"
                        autosize={true}
                        maxRows={5}
                        onKeyDown={handleKeyDown}
                        placeholder="Type your question"
                        rightSectionWidth={42}
                        rightSection={
                            <ActionIcon loading={isSendMessagePending} size={28} radius="xl" color={"violet"} variant="filled" onClick={sendMessageWrapper}>
                                <IconArrowRight style={{ width: 24, height: 24 }} stroke={1.5} />
                            </ActionIcon>
                        }
                    />
                </Flex>
                <div style={{height: "100%", width: "30%"}}>
                    {/*Related docs*/}
                </div>
            </Flex>
        </BasicLayout>
    );
}