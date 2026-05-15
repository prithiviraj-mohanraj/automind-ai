export default function BookingForm() {
  return (
    <div className="h-full bg-[#0f1729]/70 backdrop-blur-2xl border border-white/10 rounded-3xl p-6 shadow-2xl overflow-hidden">

      <h2 className="text-3xl font-bold text-white mb-2">
        AI Service Booking
      </h2>

      <p className="text-gray-400 mb-6">
        Diagnose vehicle issues using AI agents
      </p>

      <div className="grid grid-cols-2 gap-4">

        <input
          placeholder="Customer Name"
          className="bg-[#0b1120] border border-white/10 rounded-2xl p-4 text-white outline-none focus:border-cyan-400"
        />

        <input
          placeholder="Vehicle Model"
          className="bg-[#0b1120] border border-white/10 rounded-2xl p-4 text-white outline-none focus:border-cyan-400"
        />

      </div>

      <textarea
        placeholder="Describe vehicle issue..."
        rows={5}
        className="w-full mt-4 bg-[#0b1120] border border-white/10 rounded-2xl p-4 text-white outline-none focus:border-cyan-400"
      />

      <button className="w-full mt-5 bg-gradient-to-r from-cyan-500 to-blue-500 hover:scale-[1.02] transition-all duration-300 rounded-2xl p-4 font-bold text-white shadow-xl shadow-cyan-500/20">
        Run Multi-Agent Diagnosis
      </button>

    </div>
  );
}