import BasicLayout from "../../layouts/basic-layout"
import MessageHistory from "../../components/message-history"
import {ScrollArea, Textarea , ActionIcon, Flex} from '@mantine/core';
import { IconArrowRight } from '@tabler/icons-react';
import {MESSAGES} from "./../../mock_data/message";
import {useEffect, useRef, useState} from "react";





export const ChatPage = () => {
    const viewport = useRef<HTMLDivElement | null>(null);
    const [messages, setMessages] = useState(MESSAGES);
    const [userCurrentMessage, setUserCurrentMessage] = useState("");

    useEffect(() => {
        viewport.current!.scrollTo({ top: viewport.current!.scrollHeight, behavior: 'smooth' });
    }, [messages]);

    const sendMessage = () => {
        if (userCurrentMessage !== "") {
            setMessages([...messages, {role: "user", content: userCurrentMessage, datetime: "now"}]);
            setUserCurrentMessage("");
        }
    }

    const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey){
            e.preventDefault();
            sendMessage();
        }
    }


    return (
        <BasicLayout>
            <Flex direction={"row"} h="100%" pb={8}>
                <Flex direction={"column"} h="100%" w="70%">
                    <ScrollArea p={16} style={{flexGrow: 1}} viewportRef={viewport}>
                        <MessageHistory messages={messages}/>
                    </ScrollArea>
                    <Textarea
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
                            <ActionIcon size={28} radius="xl" color={"violet"} variant="filled" onClick={sendMessage}>
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