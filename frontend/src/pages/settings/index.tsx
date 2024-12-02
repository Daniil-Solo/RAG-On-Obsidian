import BasicLayout from "../../layouts/basic-layout"
import {Tabs, Flex, Stack, TextInput, NumberInput, Select, Group, Button, useComputedColorScheme, useMantineColorScheme, MantineColorScheme } from '@mantine/core';
import { useState, useEffect } from "react";
import { VENDORS } from "./settings_config";
import { LLMSettings } from "../../types/settings";
import { useLLMSettings } from "../../hooks/settings";


const initialLLMSettings: LLMSettings = {
    vendor: null,
    model: null,
    token: "",
    maxTokens: 512
}

export const SettingsPage = () => {
    const [llmSettings, setLLMSettings] = useState<LLMSettings>(initialLLMSettings);
    const { setColorScheme } = useMantineColorScheme();
    const computedColorScheme = useComputedColorScheme('light', { getInitialValueInEffect: true });

    const {data, isSuccess} = useLLMSettings()
    useEffect(() => {
        if (data){
            setLLMSettings({vendor: data.model_type, model: data.model_name, token: data.token, maxTokens: data.max_length})
        }
    }, [isSuccess, data]);


    return (
        <BasicLayout>
            <Flex align="center" justify="center" pt={24}>
                <Tabs defaultValue="preferences" orientation="vertical" h={400} w={600} my="auto" variant="pills">
                    <Tabs.List>
                        <Tabs.Tab value="preferences">Preferences</Tabs.Tab>
                        <Tabs.Tab value="llm">LLM</Tabs.Tab>
                        <Tabs.Tab disabled value="retriever">Retriever</Tabs.Tab>
                    </Tabs.List>

                    <Tabs.Panel value="llm">
                        <Stack ps={48}>
                            <Select 
                                variant="filled"
                                size="sm"
                                w={300}
                                label="Type"
                                placeholder="Not selected"
                                data={VENDORS.map(vendor => vendor.name)}
                                value={llmSettings.vendor} 
                                onChange={value => setLLMSettings({...llmSettings, vendor: value, model: null})}
                            />
                            <Select
                                variant="filled"
                                size="sm"
                                w={300}
                                label="Model"
                                placeholder={llmSettings.vendor? "Not selected": "Сhoose a vendor first"}
                                data={llmSettings.vendor? VENDORS.filter(vendor => vendor.name == llmSettings.vendor)[0].models: []}
                                value={llmSettings.model} 
                                onChange={value => setLLMSettings({...llmSettings, model: value})}
                            />
                            <TextInput 
                                variant="filled"
                                size="sm"
                                w={300}
                                label="API Token"
                                placeholder="Input here"
                                value={llmSettings.token}
                                onChange={e => setLLMSettings({...llmSettings, token: e.target.value})}
                            />
                            <NumberInput 
                                variant="filled"
                                size="sm"
                                w={300}
                                label="Maximum of tokens for answer"
                                placeholder="Not selected"
                                thousandSeparator=" "
                                min={1}
                                max={130000}
                                value={llmSettings.maxTokens}
                                onChange={value => setLLMSettings({...llmSettings, maxTokens: +value})}
                            />
                            <Group>
                                <Button size="sm" variant="outline">
                                    Check
                                </Button>
                                <Button size="sm" variant="filled">
                                    Save
                                </Button>
                            </Group>
                        </Stack>
                    </Tabs.Panel>
                    <Tabs.Panel value="retriever">
                        Comming soon...
                    </Tabs.Panel>
                    <Tabs.Panel value="preferences">
                        <Stack ps={48}>
                            <Select
                                variant="filled"
                                size="sm"
                                w={300}
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