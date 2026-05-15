const items = [
  { name: "Brake Pads", qty: 12 },
  { name: "Engine Oil", qty: 20 },
  { name: "Battery", qty: 4 },
  { name: "Air Filters", qty: 9 },
];

export default function InventoryPanel() {
  return (
    <div className="h-full bg-[#0f1729]/70 backdrop-blur-2xl border border-white/10 rounded-3xl p-6 shadow-2xl overflow-hidden">

      <h2 className="text-3xl font-bold text-white mb-2">
        Inventory Status
      </h2>

      <p className="text-gray-400 mb-6">
        AI-monitored stock levels
      </p>

      <div className="space-y-4">

        {items.map((item, idx) => (
          <div
            key={idx}
            className="flex justify-between items-center bg-[#0b1120] border border-white/5 rounded-2xl p-4"
          >
            <span className="text-white font-medium">
              {item.name}
            </span>

            <span className="text-green-400 font-semibold">
              {item.qty} available
            </span>
          </div>
        ))}

      </div>

    </div>
  );
}