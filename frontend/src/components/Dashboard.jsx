import { motion } from "framer-motion";
import BookingForm from "./BookingForm";
import AgentFeed from "./AgentFeed";
import ServiceTracker from "./ServiceTracker";
import InventoryPanel from "./InventoryPanel";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-[#050816] text-white overflow-hidden">

      {/* Background Effects */}
      <div className="absolute top-[-200px] left-[-200px] w-[500px] h-[500px] bg-cyan-500/20 rounded-full blur-[140px]" />
      <div className="absolute bottom-[-200px] right-[-200px] w-[500px] h-[500px] bg-blue-500/20 rounded-full blur-[140px]" />

      <div className="relative z-10 h-screen flex flex-col p-6 gap-6">

        {/* TOP BAR */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          className="h-[90px] bg-[#0f1729]/70 backdrop-blur-2xl border border-white/10 rounded-3xl flex items-center justify-between px-8 shadow-2xl"
        >
          <div>
            <h1 className="text-4xl font-black bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              AutoMind AI
            </h1>

            <p className="text-gray-400 text-sm mt-1">
              Autonomous Workshop Intelligence Platform
            </p>
          </div>

          <div className="flex gap-4">

            <div className="bg-[#111827] px-5 py-3 rounded-2xl border border-white/5">
              <p className="text-xs text-gray-400">
                Active Jobs
              </p>

              <h2 className="text-2xl font-bold text-cyan-400">
                12
              </h2>
            </div>

            <div className="bg-[#111827] px-5 py-3 rounded-2xl border border-white/5">
              <p className="text-xs text-gray-400">
                AI Decisions
              </p>

              <h2 className="text-2xl font-bold text-amber-400">
                84
              </h2>
            </div>

            <div className="bg-[#111827] px-5 py-3 rounded-2xl border border-white/5">
              <p className="text-xs text-gray-400">
                System
              </p>

              <h2 className="text-lg font-bold text-green-400">
                ● LIVE
              </h2>
            </div>

          </div>
        </motion.div>

        {/* MAIN DASHBOARD */}
        <div className="flex-1 grid grid-cols-12 gap-6 overflow-hidden">

          {/* LEFT SIDE */}
          <div className="col-span-8 flex flex-col gap-6">

            {/* DIGITAL TWIN */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex-1"
            >
              <ServiceTracker />
            </motion.div>

            {/* BOOKING */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              className="h-[320px]"
            >
              <BookingForm />
            </motion.div>

          </div>

          {/* RIGHT SIDE */}
          <div className="col-span-4 flex flex-col gap-6">

            {/* AGENT FEED */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex-1"
            >
              <AgentFeed />
            </motion.div>

            {/* INVENTORY */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="h-[280px]"
            >
              <InventoryPanel />
            </motion.div>

          </div>

        </div>

      </div>
    </div>
  );
}