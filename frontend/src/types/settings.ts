interface LLMSettings {
    vendor: string | null,
    model: string | null,
    token: string,
    maxTokens: number
}

interface LLMSettingsRequest {
    model_type: string;
    token: string;
    model_name: string;
    max_length: number;
  }
  

interface LLMSettingsResponse {
    model_type: string;
    token: string;
    model_name: string;
    max_length: number;
}

interface LLMAvailabilityResponse {
    is_available: boolean;
}

export type {LLMSettings, LLMSettingsRequest, LLMSettingsResponse, LLMAvailabilityResponse};