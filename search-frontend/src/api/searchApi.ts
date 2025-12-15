import type { SearchResult } from "../types/search";
import type { NewDocumentPayload, FullDocument } from "../types/documents";
import { mockResults } from "../mock/searchMock";

const USE_MOCK = false; // ← включаємо справжній бекенд
const BASE_URL = "http://127.0.0.1:8000"; // базовий URL бекенду

export type SearchParams = {
  query: string;
  doc_type?: string;
  entity_type?: string;
  entity_value?: string;
};

export async function searchDocuments(
  params: SearchParams
): Promise<SearchResult[]> {
  if (USE_MOCK) {
    const filtered = mockResults.filter((doc) => {
      const q = params.query.toLowerCase().trim();
      if (!q) return true;
      return (
        doc.title.toLowerCase().includes(q) ||
        doc.snippet.toLowerCase().includes(q)
      );
    });
    return new Promise((resolve) => setTimeout(() => resolve(filtered), 600));
  }

  const qs = new URLSearchParams();
  if (params.query) qs.set("q", params.query);
  if (params.doc_type) qs.set("doc_type", params.doc_type);
  if (params.entity_type) qs.set("entity_type", params.entity_type);
  if (params.entity_value) qs.set("entity_value", params.entity_value);

  const url = `${BASE_URL}/search?${qs.toString()}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Search failed: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function addDocument(payload: NewDocumentPayload): Promise<FullDocument> {
  const res = await fetch(`${BASE_URL}/admin/documents`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) throw new Error(`Add document failed: ${res.status} ${res.statusText}`);
  return res.json();
}