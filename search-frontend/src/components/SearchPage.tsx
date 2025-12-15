import { useState } from "react";
import { searchDocuments } from "../api/searchApi";
import type { SearchResult } from "../types/search";
import { SearchResultCard } from "../components/SearchResultCard";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [docType, setDocType] = useState("all");
  const [entityType, setEntityType] = useState("all");
  const [entityValue, setEntityValue] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await searchDocuments({
        query,
        doc_type: docType,
        entity_type: entityType,
        entity_value: entityValue,
      });
      setResults(data);
    } catch (err) {
      console.error("Error fetching search results:", err);
      setResults([]);
    } finally {
      setLoading(false);
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
        <select value={entityType} onChange={(e) => setEntityType(e.target.value)}>
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
        <button onClick={handleSearch} disabled={loading || !query}>
          {loading ? "Завантаження..." : "Шукати"}
        </button>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        {results.length === 0 && !loading && <p>Немає результатів.</p>}
        {results.map((doc) => (
          <SearchResultCard key={doc.id} doc={doc} />
        ))}
      </div>
    </div>
  );
}