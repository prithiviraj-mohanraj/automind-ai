import { motion } from "framer-motion";

const jobs = [
  {
    customer: "Sarah Chen",
    car: "Toyota Camry 2021",
    status: "In Progress",
    tech: "Mike T.",
    progress: 70,
  },
  {
    customer: "James Okafor",
    car: "BMW X5",
    status: "Diagnostics",
    tech: "Priya S.",
    progress: 40,
  },
  {
    customer: "Alex Rivera",
    car: "Ford Mustang GT",
    status: "Engine Analysis",
    tech: "Carlos R.",
    progress: 85,
  },
];

export default function ServiceTracker() {
  return (
    <div className="h-full bg-[#0f1729]/70 backdrop-blur-2xl border border-white/10 rounded-3xl p-6 shadow-2xl overflow-hidden">

      <div className="flex justify-between items-center mb-6">

        <div>
          <h2 className="text-3xl font-bold text-white">
            Live Workshop
          </h2>

          <p className="text-gray-400 mt-1">
            Real-time service operations
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-green-400 font-semibold text-sm">
            LIVE
          </span>
        </div>

      </div>

      <div className="space-y-5">

        {jobs.map((job, idx) => (
          <motion.div
            key={idx}
            whileHover={{ scale: 1.02 }}
            className="bg-[#0b1120] border border-white/5 rounded-2xl p-5"
          >

            <div className="flex justify-between items-start">

              <div>
                <h3 className="text-xl font-bold text-white">
                  {job.customer}
                </h3>

                <p className="text-gray-400 mt-1">
                  {job.car}
                </p>
              </div>

              <div className="text-right">
                <p className="text-cyan-400 font-semibold">
                  {job.status}
                </p>

                <p className="text-gray-500 text-sm mt-1">
                  {job.tech}
                </p>
              </div>

            </div>

            <div className="mt-5">

              <div className="flex justify-between text-sm text-gray-400 mb-2">
                <span>Completion</span>
                <span>{job.progress}%</span>
              </div>

              <div className="w-full h-3 bg-[#1a2235] rounded-full overflow-hidden">

                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${job.progress}%` }}
                  transition={{ duration: 1 }}
                  className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"
                />

              </div>

            </div>

          </motion.div>
        ))}

      </div>
    </div>
  );
}