const logs = [
  "[BookingAgent] Assigned technician Mike T.",
  "[InventoryAgent] Brake pads available.",
  "[DelayAgent] Delay risk medium.",
  "[SupportAgent] Customer notified.",
  "[BookingAgent] New booking processed.",
  "[InventoryAgent] Engine oil stock healthy.",
];

export default function AgentFeed() {
  return (
    <div className="h-full bg-[#0f1729]/70 backdrop-blur-2xl border border-white/10 rounded-3xl p-6 shadow-2xl overflow-hidden flex flex-col">

      <div className="flex justify-between items-center mb-6">

        <div>
          <h2 className="text-3xl font-bold text-white">
            AI Agent Feed
          </h2>

          <p className="text-gray-400 mt-1">
            Autonomous operational decisions
          </p>
        </div>

        <div className="w-3 h-3 bg-cyan-400 rounded-full animate-pulse"></div>

      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pr-2">

        {logs.map((log, idx) => (
          <div
            key={idx}
            className="bg-[#0b1120] border border-white/5 rounded-2xl p-4 text-sm text-gray-300"
          >
            {log}
          </div>
        ))}

      </div>

    </div>
  );
}