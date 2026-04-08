const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

async function request(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

export async function fetchFilterOptions() {
  return request("/api/filters");
}

export async function fetchDashboardData({ months = [], categories = [], fields = [] }) {
  const params = new URLSearchParams();

  months.forEach((m) => params.append("months", m));
  categories.forEach((c) => params.append("categories", c));
  fields.forEach((f) => params.append("fields", f));

  const query = params.toString();
  const path = query ? `/api/dashboard?${query}` : "/api/dashboard";
  return request(path);
}
