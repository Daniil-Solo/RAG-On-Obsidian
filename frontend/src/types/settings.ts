interface LLMSettings {
    vendor: string | null,
    model: string | null,
    token: string,
    baseUrl: string,
    maxTokens: number
}

interface LLMSettingsRequest {
    vendor: string
    model: string;
    token: string;
    base_url: string;
    max_tokens: number;
  }
  

interface LLMSettingsResponse extends LLMSettingsRequest{};

interface LLMAvailabilityResponse {
    is_available: boolean;
    error_message: string;
}

export type {LLMSettings, LLMSettingsRequest, LLMSettingsResponse, LLMAvailabilityResponse};