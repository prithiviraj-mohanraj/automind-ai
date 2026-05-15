const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const api = {
  getBookings:    () => fetch(`${BASE}/api/bookings`).then(r => r.json()),
  getStats:       () => fetch(`${BASE}/api/stats`).then(r => r.json()),
  getInventory:   () => fetch(`${BASE}/api/inventory`).then(r => r.json()),
  getActivityFeed:() => fetch(`${BASE}/api/activity-feed`).then(r => r.json()),

  createBooking: (data) => fetch(`${BASE}/api/booking`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then(r => r.json()),

  sendSupport: (data) => fetch(`${BASE}/api/support`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then(r => r.json()),

  updateStatus: (booking_id, status) => fetch(`${BASE}/api/booking/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ booking_id, status }),
  }).then(r => r.json()),
};