import { ConversationRequest } from "./models";


export async function callConversationApi(options: ConversationRequest, abortSignal: AbortSignal): Promise<Response> {

    let bodyContent = JSON.stringify({
        messages: options.messages,
        conversation_id: options.id
    })

    console.log(bodyContent)

    const response = await fetch("/api/conversation", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: bodyContent,
        signal: abortSignal
    });

    return response;
}
