type RoleType = "user" | "assistant";

interface MessageSchema  {
    id: string,
    role: RoleType,
    content: string,
    datetime: string
}

interface MessageHistoryResponse {
    messages: MessageSchema[];
}

interface QueryRequest {
    content: string;
}

interface AnswerResponse {
    answer: string;
    related_documents: string[];
}
  


export type { MessageSchema, MessageHistoryResponse, QueryRequest, AnswerResponse };