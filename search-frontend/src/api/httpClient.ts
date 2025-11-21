const BASE_URL = "http://localhost:8000"; // замінити на реальний бек

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(BASE_URL + path, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP error ${res.status}`);
  }

  return res.json() as Promise<T>;
}

export const httpClient = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body: unknown) =>
    request<T>(path, {
      method: "POST",
      body: JSON.stringify(body),
    }),
};
