interface LLMSettings {
    vendor: string | null,
    model: string | null,
    token: string,
    maxTokens: number
}

export type {LLMSettings};