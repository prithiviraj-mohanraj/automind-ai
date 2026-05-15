import { useState } from "react";
import { api } from "../api";

export default function SupportChat({ bookings }) {
  const [selectedId, setSelectedId] = useState("");
  const [message, setMessage]       = useState("");
  const [reply, setReply]           = useState("");
  const [loading, setLoading]       = useState(false);

  const send = async () => {
    if (!message.trim()) return;
    setLoading(true);
    const res = await api.sendSupport({ message, booking_id: selectedId ? parseInt(selectedId) : null });
    setReply(res.reply);
    setLoading(false);
  };

  const inputCls = "w-full bg-[#0a0a0f] border border-[#1f1f2e] rounded px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-sky-500 transition-colors";

  return (
    <div className="bg-[#13131a] border border-[#1f1f2e] rounded-lg p-4">
      <h2 className="text-xs uppercase tracking-widest text-slate-400 mb-3">Support Chat</h2>
      <select className={`${inputCls} mb-2`} value={selectedId} onChange={e => setSelectedId(e.target.value)}>
        <option value="">— No booking selected —</option>
        {bookings.map(b => (
          <option key={b.id} value={b.id}>#{b.id} {b.customer} – {b.car_model}</option>
        ))}
      </select>
      <textarea
        className={`${inputCls} resize-none h-16 mb-2`}
        placeholder="Customer message..."
        value={message}
        onChange={e => setMessage(e.target.value)}
      />
      <button
        onClick={send}
        disabled={loading || !message.trim()}
        className="w-full bg-sky-600 hover:bg-sky-500 disabled:opacity-40 text-white font-bold py-1.5 rounded text-sm transition-colors mb-3"
      >
        {loading ? "Thinking..." : "Send"}
      </button>
      {reply && (
        <div className="bg-[#0a0a0f] border border-sky-900 rounded p-3 text-xs text-sky-200">
          <p className="text-sky-500 mb-1 text-xs">SupportAgent:</p>
          {reply}
        </div>
      )}
    </div>
  );
}