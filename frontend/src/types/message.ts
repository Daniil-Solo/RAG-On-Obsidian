type RoleType = "user" | "assistant";

interface IMessage {
    role: RoleType,
    content: string,
    datetime: string /* 01:26 21-11-2024 */
}

export type { IMessage };