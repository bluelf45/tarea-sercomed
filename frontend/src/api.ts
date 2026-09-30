export type Role = 'user' | 'assistant'

export interface ChatMessage {
  role: Role
  content: string
}

export async function sendChat(messages: ChatMessage[]): Promise<string> {
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages }),
  })
  if (!res.ok) {
    const data = await res.json().catch(() => null)
    const detail = typeof data?.detail === 'string' ? data.detail : null
    throw new Error(detail ?? `Error ${res.status} al contactar el servidor.`)
  }
  const data: { reply: string } = await res.json()
  return data.reply
}
