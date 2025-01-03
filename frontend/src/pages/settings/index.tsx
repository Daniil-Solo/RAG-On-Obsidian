import BasicLayout from "../../layouts/basic-layout"
import {Tabs, Flex, Stack, TextInput, NumberInput, Select, Group, Button, useComputedColorScheme, useMantineColorScheme, MantineColorScheme, Box } from '@mantine/core';
import { useState, useEffect } from "react";
import { VENDORS } from "./settings_config";
import { LLMSettings } from "../../types/settings";
import { useCheckLLM, useLLMSettings, useUpdateLLMSettings } from "../../hooks/settings";


const initialLLMSettings: LLMSettings = {
    vendor: "Mistral AI",
    model: null,
    token: "",
    baseUrl: "",
    maxTokens: 512
}

export const SettingsPage = () => {
    const [llmSettings, setLLMSettings] = useState<LLMSettings>(initialLLMSettings);
    const { setColorScheme } = useMantineColorScheme();
    const computedColorScheme = useComputedColorScheme('light', { getInitialValueInEffect: true });
    const {mutateAsync: updateLLMSettings} = useUpdateLLMSettings();
    const {mutateAsync: checkLLM, isPending: isCheckPending} = useCheckLLM()
    const {data, isSuccess} = useLLMSettings();
    useEffect(() => {
        if (data){
            setLLMSettings({vendor: data.vendor, model: data.model, token: data.token, maxTokens: data.max_tokens, baseUrl: data.base_url})
        }
    }, [isSuccess, data]);


    return (
        <BasicLayout>
            <Flex align="center" justify="center" pt={24}>
                <Tabs defaultValue="preferences" orientation="vertical" h={400} w={500} my="auto" variant="pills">
                    <Tabs.List>
                        <Tabs.Tab value="preferences">Preferences</Tabs.Tab>
                        <Tabs.Tab value="mistralai">Mistral AI</Tabs.Tab>
                    </Tabs.List>

                    <Tabs.Panel value="mistralai">
                        <Stack ps={24}>
                            <Box pos="relative">
                                <Select
                                    variant="filled"
                                    size="sm"
                                    w="100%"
                                    label="Model"
                                    placeholder={llmSettings.vendor? "Not selected": "Сhoose a vendor first"}
                                    data={llmSettings.vendor? VENDORS.filter(vendor => vendor.name == llmSettings.vendor)[0].models: []}
                                    value={llmSettings.model} 
                                    onChange={value => setLLMSettings({...llmSettings, model: value})}
                                />
                                <TextInput 
                                    variant="filled"
                                    size="sm"
                                    w="100%"
                                    label={"API Token"}
                                    placeholder="Input here"
                                    value={llmSettings.token}
                                    onChange={e => setLLMSettings({...llmSettings, token: e.target.value})}
                                />
                                <NumberInput 
                                    variant="filled"
                                    size="sm"
                                    w="100%"
                                    label="Maximum of tokens for answer"
                                    placeholder="Not selected"
                                    thousandSeparator=" "
                                    min={1}
                                    max={130000}
                                    value={llmSettings.maxTokens}
                                    onChange={value => setLLMSettings({...llmSettings, maxTokens: +value})}
                                />
                            </Box>
                            <Group>
                                <Button size="sm" variant="outline" loading={isCheckPending} loaderProps={{type: "dots"}} disabled={isCheckPending} onClick={() => checkLLM({
                                    vendor: llmSettings.vendor || "",
                                    token: llmSettings.token,
                                    model: llmSettings.model || "",
                                    max_tokens: llmSettings.maxTokens,
                                    base_url: llmSettings.baseUrl
                                })}>
                                    Check
                                </Button>
                                <Button size="sm" variant="filled" onClick={() => updateLLMSettings({
                                    vendor: llmSettings.vendor || "",
                                    token: llmSettings.token,
                                    model: llmSettings.model || "",
                                    max_tokens: llmSettings.maxTokens,
                                    base_url: llmSettings.baseUrl
                                })}>
                                    Save
                                </Button>
                            </Group>
                        </Stack>
                    </Tabs.Panel>
                    <Tabs.Panel value="preferences">
                        <Stack ps={24}>
                            <Select
                                variant="filled"
                                size="sm"
                                w="100%"
                                label="Theme"
                                data={[{label: "Dark", value: "dark"}, {label: "Light", value: "light"}]}
                                value={computedColorScheme} 
                                onChange={value => value && setColorScheme(value as MantineColorScheme)}
                            />
                        </Stack>
                    </Tabs.Panel>
                </Tabs>
            </Flex>
        </BasicLayout>
    );
}