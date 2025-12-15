import { useState } from "react";
import { SearchResultCard } from "../components/SearchResultCard";
import type { SearchResult } from "../types/search";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [docType, setDocType] = useState("all");
  const [entityType, setEntityType] = useState("all");
  const [entityValue, setEntityValue] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);

  const handleSearch = async () => {
    try {
      const url = new URL("http://127.0.0.1:8000/search");
      url.searchParams.append("q", query);
      url.searchParams.append("doc_type", docType);
      url.searchParams.append("entity_type", entityType);
      url.searchParams.append("entity_value", entityValue);

      const res = await fetch(url.toString(), { method: "GET" });
      if (!res.ok) {
        console.error("Error fetching search results", res.status);
        return;
      }

      const data: SearchResult[] = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: "1rem", display: "flex", gap: "0.5rem" }}>
        <input
          type="text"
          placeholder="Пошуковий запит"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <select value={docType} onChange={(e) => setDocType(e.target.value)}>
          <option value="all">Усі типи</option>
          <option value="news">news</option>
          <option value="opinion">opinion</option>
          <option value="publicistic">publicistic</option>
          <option value="scientific">scientific</option>
        </select>
        <select
          value={entityType}
          onChange={(e) => setEntityType(e.target.value)}
        >
          <option value="all">Усі сутності</option>
          <option value="PER">PER</option>
          <option value="ORG">ORG</option>
          <option value="LOC">LOC</option>
          <option value="DATE">DATE</option>
        </select>
        <input
          type="text"
          placeholder="Значення сутності"
          value={entityValue}
          onChange={(e) => setEntityValue(e.target.value)}
        />
        <button onClick={handleSearch}>Шукати</button>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        {results.length === 0 && <p>Немає результатів.</p>}
        {results.map((doc) => (
          <SearchResultCard key={doc.id} doc={doc} />
        ))}
      </div>
    </div>
  );
}
