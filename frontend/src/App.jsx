import TechnicianChart from "./components/TechnicianChart";
import { useEffect, useMemo, useState } from "react";
import BookingResultCard from "./components/BookingResultCard";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const API = import.meta.env.VITE_API_URL;

export default function App() {

  const [bookings, setBookings] = useState([]);
  const [feed, setFeed] = useState([]);
  const [inventory, setInventory] = useState([]);

  const [customer, setCustomer] = useState("");
  const [vehicleNumber, setVehicleNumber] = useState("");
  const [carModel, setCarModel] = useState("");
  const [description, setDescription] = useState("");

  const [query, setQuery] = useState("");
  const [queryAnswer, setQueryAnswer] = useState("");

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  const workflowStages = [

    "Booked",

    "Diagnosing",

    "Awaiting Parts",

    "Repair In Progress",

    "QA Inspection",

    "Ready Delivery",

    "Delivered"
  ];

  // LOAD DATA

  async function loadData() {

    try {

      const bookingsRes = await fetch(`${API}/api/bookings`);
      const bookingsData = await bookingsRes.json();
      setBookings(bookingsData);

      const feedRes = await fetch(`${API}/api/activity-feed`);
      const feedData = await feedRes.json();
      setFeed(feedData);

      const invRes = await fetch(`${API}/api/inventory`);
      const invData = await invRes.json();
      setInventory(invData);

    } catch (err) {

      console.log(err);

    }
  }

  useEffect(() => {

    loadData();

    const interval = setInterval(loadData, 3000);

    return () => clearInterval(interval);

  }, []);

  // CREATE BOOKING

  async function createBooking() {

    if (!customer.trim()) {
      alert("Enter customer");
      return;
    }

    if (!vehicleNumber.trim()) {
      alert("Enter vehicle number");
      return;
    }

    if (!carModel.trim()) {
      alert("Enter vehicle model");
      return;
    }

    if (!description.trim()) {
      alert("Describe issue");
      return;
    }

    try {

      setLoading(true);

      const res = await fetch(`${API}/api/booking`, {

        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({

          customer,
          vehicle_number: vehicleNumber,
          car_model: carModel,
          description

        })

      });

      const data = await res.json();

      setResult(data);

      setCustomer("");
      setVehicleNumber("");
      setCarModel("");
      setDescription("");

      loadData();

    } catch (err) {

      console.log(err);

      alert("Backend request failed");

    } finally {

      setLoading(false);

    }
  }

  // QUERY

  async function askQuery() {

    if (!query.trim()) {
      alert("Ask workshop query");
      return;
    }

    try {

      setQueryAnswer("Analyzing workshop intelligence...");

      const res = await fetch(`${API}/api/query`, {

        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          question: query
        })

      });

      const data = await res.json();

      setQueryAnswer(data.answer);

    } catch (err) {

      console.log(err);

      setQueryAnswer("AI analysis failed.");

    }
  }

  // ISSUE ANALYTICS

  const issueData = useMemo(() => {

    const issueMap = {

      Engine: 0,
      Brake: 0,
      Electrical: 0,
      AC: 0,
      Accident: 0,
      Service: 0
    };

    bookings.forEach((b) => {

      const issue = (b.issue || "").toLowerCase();

      if (issue.includes("engine"))
        issueMap.Engine++;

      else if (issue.includes("brake"))
        issueMap.Brake++;

      else if (
        issue.includes("battery") ||
        issue.includes("wiring")
      )
        issueMap.Electrical++;

      else if (issue.includes("ac"))
        issueMap.AC++;

      else if (
        issue.includes("dent") ||
        issue.includes("bumper")
      )
        issueMap.Accident++;

      else
        issueMap.Service++;

    });

    return Object.entries(issueMap).map(([name, value]) => ({
      name,
      value
    }));

  }, [bookings]);

  const revenue = bookings.reduce(
    (sum, b) => sum + (b.estimated_cost || 0),
    0
  );

  function stageColor(stage) {

    if (stage === "Booked")
      return "border-cyan-500/30";

    if (stage === "Diagnosing")
      return "border-purple-500/30";

    if (stage === "Awaiting Parts")
      return "border-orange-500/30";

    if (stage === "Repair In Progress")
      return "border-yellow-500/30";

    if (stage === "QA Inspection")
      return "border-pink-500/30";

    if (stage === "Ready Delivery")
      return "border-green-500/30";

    return "border-zinc-500/30";
  }

  return (

    <div className="min-h-screen bg-[#040814] text-white overflow-hidden">

      {/* BACKGROUND */}

      <div className="fixed inset-0 pointer-events-none">

        <div className="absolute top-0 left-0 w-[700px] h-[700px] bg-cyan-500/10 blur-[160px]" />

        <div className="absolute bottom-0 right-0 w-[700px] h-[700px] bg-purple-500/10 blur-[160px]" />

      </div>

      {/* HEADER */}

      <div className="sticky top-0 z-50 bg-[#050816]/80 border-b border-white/5 backdrop-blur-2xl">

        <div className="max-w-[1900px] mx-auto px-8 py-6 flex justify-between items-center">

          <div>

            <h1 className="text-6xl font-black bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent">
              AutoMind AI
            </h1>

            <p className="text-zinc-400 mt-2 text-lg">
              Enterprise Automotive Intelligence Platform
            </p>

          </div>

          <div className="flex gap-4">

            <div className="px-5 py-3 rounded-2xl bg-green-500/10 border border-green-500/30 text-green-400 font-bold animate-pulse">
              AI AGENTS ACTIVE
            </div>

          </div>

        </div>

      </div>

      {/* MAIN */}

      <div className="max-w-[1900px] mx-auto p-8 relative z-10">

        {/* KPI */}

        <div className="grid md:grid-cols-4 gap-6 mb-8">

          <StatCard
            title="Vehicles"
            value={bookings.length}
            color="text-cyan-400"
          />

          <StatCard
            title="AI Decisions"
            value={feed.length}
            color="text-purple-400"
          />

          <StatCard
            title="Inventory"
            value={inventory.length}
            color="text-green-400"
          />

          <StatCard
            title="Revenue"
            value={`₹${revenue.toLocaleString()}`}
            color="text-orange-400"
          />

        </div>

        {/* ANALYTICS */}

        <div className="grid xl:grid-cols-3 gap-8 mb-10">

          {/* NEW TECHNICIAN CHART */}

          <TechnicianChart bookings={bookings} />

          {/* ISSUE PIE */}

          <AnalyticsCard title="Issue Distribution">

            <ResponsiveContainer width="100%" height={350}>

              <PieChart>

                <Pie
                  data={issueData}
                  dataKey="value"
                  outerRadius={110}
                >

                  <Cell fill="#22d3ee" />
                  <Cell fill="#8b5cf6" />
                  <Cell fill="#f97316" />
                  <Cell fill="#10b981" />
                  <Cell fill="#ec4899" />
                  <Cell fill="#eab308" />

                </Pie>

                <Tooltip />

              </PieChart>

            </ResponsiveContainer>

          </AnalyticsCard>

          {/* QUERY */}

          <AnalyticsCard title="AI Workshop Intelligence">

            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              rows={5}
              placeholder="Which technician handled most brake issues?"
              className="w-full bg-[#040814] border border-white/10 rounded-2xl p-4 outline-none focus:border-cyan-400"
            />

            <button
              onClick={askQuery}
              className="w-full mt-4 bg-gradient-to-r from-purple-500 to-pink-500 py-4 rounded-2xl font-bold"
            >
              Analyze Operations
            </button>

            {queryAnswer && (

              <div className="mt-5 bg-[#040814] border border-white/5 rounded-2xl p-5">

                <div className="text-cyan-400 font-bold mb-3">
                  AI Analysis
                </div>

                <div className="leading-8 whitespace-pre-wrap">
                  {queryAnswer}
                </div>

              </div>

            )}

          </AnalyticsCard>

        </div>

        {/* FORM */}

        <div className="bg-[#0a1020]/80 border border-white/5 rounded-[30px] p-8 backdrop-blur-xl mb-8">

          <h2 className="text-4xl font-black mb-6">
            AI Vehicle Diagnosis
          </h2>

          <div className="grid md:grid-cols-3 gap-5 mb-5">

            <input
              value={customer}
              onChange={(e) => setCustomer(e.target.value)}
              placeholder="Customer Name"
              className="bg-[#040814] border border-white/10 rounded-2xl px-5 py-4"
            />

            <input
              value={vehicleNumber}
              onChange={(e) => setVehicleNumber(e.target.value)}
              placeholder="Vehicle Number"
              className="bg-[#040814] border border-white/10 rounded-2xl px-5 py-4"
            />

            <input
              value={carModel}
              onChange={(e) => setCarModel(e.target.value)}
              placeholder="Vehicle Model"
              className="bg-[#040814] border border-white/10 rounded-2xl px-5 py-4"
            />

          </div>

          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={5}
            placeholder="Describe issue..."
            className="w-full bg-[#040814] border border-white/10 rounded-2xl p-4"
          />

          <button
            onClick={createBooking}
            className="w-full mt-6 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 py-5 rounded-2xl text-xl font-black"
          >
            {
              loading
                ? "Running AI Agents..."
                : "Run Multi-Agent Diagnosis"
            }
          </button>

        </div>

        {/* RESULT */}

        <BookingResultCard result={result} />

        {/* LIVE WORKSHOP */}

        <div className="mt-10 overflow-x-auto pb-6">

          <div className="flex gap-6 min-w-[1900px]">

            {workflowStages.map((stage) => (

              <div
                key={stage}
                className={`w-[360px] rounded-[28px] bg-[#0a1020]/80 border ${stageColor(stage)} p-5 backdrop-blur-xl`}
              >

                <div className="flex items-center justify-between mb-5">

                  <div>

                    <h3 className="text-2xl font-black">
                      {stage}
                    </h3>

                    <div className="text-zinc-500 mt-1">
                      {
                        bookings.filter(
                          (b) =>
                            b.workflow_stage === stage
                        ).length
                      } Vehicles
                    </div>

                  </div>

                </div>

                <div className="space-y-4 max-h-[850px] overflow-auto pr-2">

                  {bookings
                    .filter(
                      (b) =>
                        b.workflow_stage === stage
                    )
                    .map((b) => (

                      <div
                        key={b.id}
                        className="bg-[#040814] border border-white/5 rounded-3xl p-5 hover:border-cyan-400/40 transition-all duration-300"
                      >

                        <div className="flex justify-between">

                          <div>

                            <div className="text-xl font-bold">
                              {b.customer}
                            </div>

                            <div className="text-zinc-400 mt-1">
                              {b.vehicle_number}
                            </div>

                            <div className="text-zinc-500 text-sm mt-1">
                              {b.car_model}
                            </div>

                          </div>

                          <div className="text-orange-400 font-bold">
                            {b.priority}
                          </div>

                        </div>

                        <div className="mt-5 text-cyan-300 leading-7">
                          {b.issue}
                        </div>

                        <div className="flex justify-between mt-5">

                          <div className="text-zinc-400">
                            {b.technician}
                          </div>

                          <div className="text-green-400">
                            ₹ {b.estimated_cost}
                          </div>

                        </div>

                      </div>

                    ))}

                </div>

              </div>

            ))}

          </div>

        </div>

      </div>

    </div>
  );
}

function StatCard({ title, value, color }) {

  return (

    <div className="bg-[#0a1020]/80 border border-white/5 rounded-[30px] p-6 backdrop-blur-xl">

      <div className="text-zinc-400">
        {title}
      </div>

      <div className={`text-5xl font-black mt-4 ${color}`}>
        {value}
      </div>

    </div>
  );
}

function AnalyticsCard({ title, children }) {

  return (

    <div className="bg-[#0a1020]/80 border border-white/5 rounded-[30px] p-6 backdrop-blur-xl">

      <div className="text-2xl font-black mb-6">
        {title}
      </div>

      {children}

    </div>
  );
}
