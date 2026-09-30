import type { ChatMessage } from '../api'

export default function Message({ role, content }: ChatMessage) {
  return (
    <div className={`message message--${role}`}>
      <div className="bubble">{content}</div>
    </div>
  )
}
