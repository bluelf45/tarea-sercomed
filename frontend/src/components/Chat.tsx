import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from 'react'
import { sendChat, type ChatMessage } from '../api'
import Message from './Message'

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const endRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function submit() {
    const text = input.trim()
    if (!text || loading) return

    const next: ChatMessage[] = [...messages, { role: 'user', content: text }]
    setMessages(next)
    setInput('')
    setError(null)
    setLoading(true)
    try {
      const reply = await sendChat(next)
      setMessages([...next, { role: 'assistant', content: reply }])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error inesperado.')
      // Quita el mensaje fallido y lo devuelve al input para reintentar.
      setMessages(messages)
      setInput(text)
    } finally {
      setLoading(false)
    }
  }

  function onSubmit(e: FormEvent) {
    e.preventDefault()
    void submit()
  }

  function onKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      void submit()
    }
  }

  function reset() {
    setMessages([])
    setError(null)
    setInput('')
  }

  return (
    <div className="chat">
      <header className="chat__header">
        <h1>Asistente virtual</h1>
        <button type="button" onClick={reset} disabled={loading || messages.length === 0}>
          Nueva conversación
        </button>
      </header>

      <div className="chat__messages">
        {messages.length === 0 && (
          <p className="chat__empty">¡Hola! ¿En qué te puedo ayudar?</p>
        )}
        {messages.map((m, i) => (
          <Message key={i} role={m.role} content={m.content} />
        ))}
        {loading && (
          <div className="message message--assistant">
            <div className="bubble bubble--typing">Escribiendo…</div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      {error && <div className="chat__error">{error}</div>}

      <form className="chat__form" onSubmit={onSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Escribe tu mensaje…"
          rows={1}
          disabled={loading}
          autoFocus
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Enviar
        </button>
      </form>
    </div>
  )
}
