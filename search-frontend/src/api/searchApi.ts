import { httpClient } from "./httpClient";
import type { SearchResult } from "../types/search";
import type { NewDocumentPayload, FullDocument } from "../types/documents";
import { mockResults } from "../mock/searchMock";

const USE_MOCK = true; // ← поки чекаєш бекенд, true

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
    // фільтрація + імітація затримки, щоб побачити loading
    const filtered = mockResults.filter((doc) => {
      const q = params.query.toLowerCase().trim();
      if (!q) return true;
      return (
        doc.title.toLowerCase().includes(q) ||
        doc.snippet.toLowerCase().includes(q)
      );
    });

    return new Promise((resolve) => {
      setTimeout(() => resolve(filtered), 600);
    });
  }

  const qs = new URLSearchParams();

  if (params.query) qs.set("q", params.query);
  if (params.doc_type) qs.set("doc_type", params.doc_type);
  if (params.entity_type) qs.set("entity_type", params.entity_type);
  if (params.entity_value) qs.set("entity_value", params.entity_value);

  const queryString = qs.toString();
  const url = queryString ? `/search?${queryString}` : "/search";

  return httpClient.get<SearchResult[]>(url);
}

export async function addDocument(
  payload: NewDocumentPayload
): Promise<FullDocument> {
  return httpClient.post<FullDocument>("/admin/documents", payload);
}
