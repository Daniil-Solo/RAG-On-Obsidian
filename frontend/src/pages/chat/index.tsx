import BasicLayout from "../../layouts/basic-layout"
import MessageHistory from "../../components/message-history"
import  {ScrollArea, Textarea , ActionIcon, Flex, Button, List, ThemeIcon, Text, Accordion } from '@mantine/core';
import { IconArrowRight, IconInfoHexagonFilled, IconBookmarksFilled, IconSettingsFilled } from '@tabler/icons-react';
import { useEffect, useRef, useState } from "react";
import { useChatMessages, useSendChatMessage, useCleanChatMessage } from "../../hooks/messages";
import {useLLMSettings} from "../../hooks/settings";
import {useLLMTokens} from "../../hooks/llm-tokens";
import { MessageSchema } from "../../types/messages";




export const ChatPage = () => {
    const viewport = useRef<HTMLDivElement | null>(null);
    const [messages, setMessages] = useState<Array<MessageSchema>>([]);
    const [userCurrentMessage, setUserCurrentMessage] = useState("");
    const [relatedDocuments, setRelatedDocuments] = useState<Array<string>>([]);
    const {data, isSuccess} = useChatMessages();
    const {data: llmTokens, isSuccess: isLLMTokensSuccess} = useLLMTokens();
    const {data: llmSettings, isSuccess: isLLMSettingsSuccess} = useLLMSettings();
    const {mutateAsync: sendMessage, isPending: isSendMessagePending} = useSendChatMessage();
    const {mutateAsync: cleanMessages, isPending: isCleanMessagesPending} = useCleanChatMessage();

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
                setRelatedDocuments(() => data.related_documents)
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

    const cleanMessagesWrapper = () => {
        setRelatedDocuments([]);
        cleanMessages();
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
                            <ActionIcon loaderProps={{type: "oval"}} loading={isSendMessagePending} size={28} radius="xl" color={"violet"} variant="filled" onClick={sendMessageWrapper}>
                                <IconArrowRight style={{ width: 18, height: 18 }} stroke={1.5} />
                            </ActionIcon>
                        }
                    />
                </Flex>
                <Accordion ps={12} multiple={true}  w={"30%"} defaultValue={["General"]} variant="separated">
                    <Accordion.Item value={"General"}>
                        <Accordion.Control icon={<IconInfoHexagonFilled color="var(--violet)"/>}>
                            General
                        </Accordion.Control>
                        <Accordion.Panel>
                            <Text>
                                In-Tokens: {isLLMTokensSuccess? llmTokens.input_tokens: "no data"} <br/>
                                Out-Tokens: {isLLMTokensSuccess? llmTokens.output_tokens: "no data"} <br/>
                                Model: {isLLMSettingsSuccess && llmSettings.model !== ''? llmSettings.model: "not selected"}
                            </Text>
                        </Accordion.Panel>
                    </Accordion.Item>
                    <Accordion.Item value={"Related"}>
                        <Accordion.Control icon={<IconBookmarksFilled color="var(--violet)"/>}>
                            Related documents
                        </Accordion.Control>
                        <Accordion.Panel>
                            {
                                relatedDocuments.length == 0
                                ? (
                                    <Text>
                                        No documents
                                    </Text>
                                ): null
                            }
                            <ScrollArea scrollbars="y" style={{flexGrow: 1}}>
                                <List
                                    spacing="xs"
                                    size="sm"
                                    center
                                    icon={<ThemeIcon color="violet" size={8} radius="xl"/>}
                                >
                                    {relatedDocuments.map(doc => (
                                        <List.Item>
                                            <Text fw={500}>
                                                {doc}
                                            </Text>
                                        </List.Item>
                                    ))}
                                </List>
                         </ScrollArea>
                        </Accordion.Panel>
                    </Accordion.Item>
                    <Accordion.Item value={"Management"}>
                        <Accordion.Control icon={<IconSettingsFilled color="var(--violet)"/>}>
                            Management
                        </Accordion.Control>
                        <Accordion.Panel>
                            <Button loaderProps={{type: "dots"}} loading={isCleanMessagesPending} onClick={cleanMessagesWrapper}>
                                Clear history
                            </Button>
                        </Accordion.Panel>
                    </Accordion.Item>
                </Accordion>
            </Flex>
        </BasicLayout>
    );
}