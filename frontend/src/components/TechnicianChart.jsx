export default function TechnicianChart({ bookings }) {

  const technicianMap = {};

  bookings.forEach((b) => {

    if (!b.technician) return;

    if (!technicianMap[b.technician]) {
      technicianMap[b.technician] = 0;
    }

    technicianMap[b.technician] += 1;

  });

  const technicians = Object.entries(technicianMap);

  return (

    <div className="bg-[#0a1020]/80 border border-white/5 rounded-[30px] p-6 backdrop-blur-xl h-full">

      {/* HEADER */}

      <div className="flex items-center justify-between mb-5">

        <div>

          <h2 className="text-2xl font-black">
            Technician Workload
          </h2>

          <p className="text-zinc-500 mt-1 text-sm">
            Live workshop analytics
          </p>

        </div>

        <div className="w-3 h-3 rounded-full bg-cyan-400 animate-pulse" />

      </div>

      {/* TECH GRID */}

      <div className="grid grid-cols-4 gap-3">

        {technicians.map(([name, jobs]) => (

          <div
            key={name}
            className="
              bg-[#040814]
              border border-white/5
              rounded-2xl
              p-3
              hover:border-cyan-400/30
              transition-all
              duration-300
            "
          >

            <div className="text-zinc-400 text-[11px] truncate">
              {name}
            </div>

            <div className="text-3xl font-black text-cyan-400 mt-2">
              {jobs}
            </div>

            <div className="text-zinc-500 text-[10px] mt-1">
              Jobs
            </div>

          </div>

        ))}

      </div>

      {/* FOOTER */}

      <div className="mt-5 pt-4 border-t border-white/5 flex justify-between">

        <div>

          <div className="text-zinc-500 text-xs">
            Technicians
          </div>

          <div className="text-xl font-black text-white mt-1">
            {technicians.length}
          </div>

        </div>

        <div className="text-right">

          <div className="text-zinc-500 text-xs">
            Total Jobs
          </div>

          <div className="text-xl font-black text-green-400 mt-1">
            {bookings.length}
          </div>

        </div>

      </div>

    </div>

  );

}