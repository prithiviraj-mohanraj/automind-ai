export default function BookingResultCard({ result }) {

  if (!result) return null;

  const booking = result.booking || {};
  const inventory = result.inventory || {};
  const delay = result.delay || {};
  const billing = result.billing || {};

  const severityColor = {
    LOW: "text-green-400 border-green-500/30 bg-green-500/10",
    MEDIUM: "text-yellow-400 border-yellow-500/30 bg-yellow-500/10",
    HIGH: "text-orange-400 border-orange-500/30 bg-orange-500/10",
    CRITICAL: "text-red-400 border-red-500/30 bg-red-500/10",
  };

  return (

    <div className="space-y-6">

      {/* TOP ALERT */}

      <div className={`border rounded-3xl p-6 ${severityColor[booking.severity]}`}>

        <div className="flex items-center justify-between">

          <div>

            <div className="text-sm uppercase tracking-widest opacity-70">
              AI Vehicle Inspection
            </div>

            <div className="text-3xl font-black mt-2">
              {booking.severity} SEVERITY
            </div>

          </div>

          <div className={`px-5 py-3 rounded-2xl font-black text-lg ${
            booking.safe_to_drive
              ? "bg-green-500/20 text-green-300"
              : "bg-red-500/20 text-red-300"
          }`}>

            {booking.safe_to_drive
              ? "SAFE TO DRIVE"
              : "NOT SAFE TO DRIVE"}

          </div>

        </div>

      </div>

      {/* MAIN GRID */}

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

        {/* LEFT */}

        <div className="space-y-6">

          {/* DIAGNOSIS */}

          <div className="bg-[#0f172a] border border-white/5 rounded-3xl p-6">

            <h2 className="text-2xl font-black mb-5">
              Triage Inspection Agent
            </h2>

            <div className="space-y-4">

              <div>
                <div className="text-zinc-500 text-sm">
                  Detected Issues
                </div>

                <div className="text-xl font-bold text-cyan-400 mt-1">
                  {booking.likely_issue}
                </div>
              </div>

              <div>
                <div className="text-zinc-500 text-sm">
                  Assigned Specialist
                </div>

                <div className="text-lg font-semibold mt-1">
                  {booking.technician}
                </div>
              </div>

              <div>
                <div className="text-zinc-500 text-sm">
                  Inspection Level
                </div>

                <div className="text-lg mt-1">
                  {booking.inspection_levels?.join(", ")}
                </div>
              </div>

              <div>
                <div className="text-zinc-500 text-sm">
                  Estimated Workshop Time
                </div>

                <div className="text-orange-400 font-bold mt-1">
                  {booking.eta_minutes} minutes
                </div>
              </div>

            </div>

          </div>

          {/* CHECKLIST */}

          <div className="bg-[#0f172a] border border-white/5 rounded-3xl p-6">

            <h2 className="text-2xl font-black mb-5">
              Inspection Checklist
            </h2>

            <div className="space-y-3">

              {booking.systems_to_check?.map((item, idx) => (

                <div
                  key={idx}
                  className="flex items-center gap-3 bg-[#050816] border border-white/5 rounded-2xl p-4"
                >

                  <div className="w-3 h-3 rounded-full bg-cyan-400 animate-pulse" />

                  <div className="font-medium">
                    {item}
                  </div>

                </div>

              ))}

            </div>

          </div>

        </div>

        {/* RIGHT */}

        <div className="space-y-6">

          {/* INVENTORY */}

          <div className="bg-[#0f172a] border border-white/5 rounded-3xl p-6">

            <h2 className="text-2xl font-black mb-5">
              Inventory Intelligence Agent
            </h2>

            <div className={`p-4 rounded-2xl border ${
              inventory.all_available
                ? "bg-green-500/10 border-green-500/20 text-green-300"
                : "bg-red-500/10 border-red-500/20 text-red-300"
            }`}>

              {inventory.message}

            </div>

            <div className="mt-5">

              <div className="text-zinc-500 text-sm mb-3">
                Required Parts
              </div>

              <div className="flex flex-wrap gap-3">

                {booking.parts_needed?.map((part, idx) => (

                  <div
                    key={idx}
                    className="bg-[#050816] border border-white/10 rounded-2xl px-4 py-2"
                  >
                    {part}
                  </div>

                ))}

              </div>

            </div>

          </div>

          {/* BILLING */}

          <div className="bg-[#0f172a] border border-white/5 rounded-3xl p-6">

            <h2 className="text-2xl font-black mb-5">
              Billing & Insurance Agent
            </h2>

            <div className="space-y-4">

              <div className="flex justify-between">
                <span className="text-zinc-400">Parts Cost</span>
                <span>₹{billing.parts_cost}</span>
              </div>

              <div className="flex justify-between">
                <span className="text-zinc-400">Labor Cost</span>
                <span>₹{billing.labor_cost}</span>
              </div>

              <div className="flex justify-between">
                <span className="text-zinc-400">GST</span>
                <span>₹{billing.gst}</span>
              </div>

              <div className="flex justify-between">
                <span className="text-zinc-400">
                  Insurance Coverage
                </span>

                <span className={
                  billing.insurance_applicable
                    ? "text-green-400"
                    : "text-red-400"
                }>

                  {billing.insurance_applicable
                    ? "Covered"
                    : "Not Covered"}

                </span>

              </div>

              <div className="flex justify-between">
                <span className="text-zinc-400">
                  Insurance Pays
                </span>

                <span className="text-green-400">
                  ₹{billing.insurance_covered_amount}
                </span>

              </div>

              <div className="border-t border-white/10 pt-4 flex justify-between text-xl font-black">

                <span>Customer Pays</span>

                <span className="text-cyan-400">
                  ₹{billing.customer_payable}
                </span>

              </div>

            </div>

          </div>

          {/* DELAY */}

          <div className="bg-[#0f172a] border border-white/5 rounded-3xl p-6">

            <h2 className="text-2xl font-black mb-5">
              Delay Prediction Agent
            </h2>

            <div className="w-full bg-[#050816] rounded-full h-5 overflow-hidden">

              <div
                className={`h-full ${
                  delay.delay_risk > 70
                    ? "bg-red-500"
                    : delay.delay_risk > 40
                    ? "bg-yellow-500"
                    : "bg-green-500"
                }`}
                style={{
                  width: `${delay.delay_risk}%`
                }}
              />

            </div>

            <div className="mt-4 flex justify-between items-center">

              <div className="text-zinc-400">
                Workshop Congestion
              </div>

              <div className="text-2xl font-black">
                {delay.delay_risk}%
              </div>

            </div>

            <div className="mt-3 text-zinc-300">
              {delay.message}
            </div>

          </div>

        </div>

      </div>

      {/* AI SUMMARY */}

      <div className="bg-gradient-to-r from-cyan-500/10 to-purple-500/10 border border-cyan-500/20 rounded-3xl p-6">

        <div className="text-cyan-400 font-black text-xl mb-4">
          AI Inspection Summary
        </div>

        <div className="text-zinc-200 leading-8 whitespace-pre-wrap">
          {booking.inspection_summary}
        </div>

      </div>

    </div>

  );
}