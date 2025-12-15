// src/pages/SearchPage.tsx
import { useState } from "react";
import { searchDocuments } from "../api/searchApi";
import type { SearchResult } from "../types/search";
import { SearchResultCard } from "../components/SearchResultCard";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [docType, setDocType] = useState("all");
  const [entityType, setEntityType] = useState("all");
  // entityValue прибрали
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const data = await searchDocuments({
        query,
        doc_type: docType,
        entity_type: entityType,
      });
      setResults(data);
    } catch (err) {
      console.error("Error fetching search results:", err);
      setError("Помилка з'єднання з сервером");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  // Пошук при натисканні Enter
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
      <div style={{ maxWidth: "900px", margin: "0 auto" }}>
        <div
            style={{
              marginBottom: "1.5rem",
              display: "flex",
              gap: "0.75rem",
              flexWrap: "wrap",
              padding: "1rem",
              backgroundColor: "var(--card-bg)",
              borderRadius: "0.75rem",
              border: "1px solid var(--border)"
            }}
        >
          <input
              type="text"
              placeholder="Пошуковий запит (напр. університет AND набір)"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              style={{ flex: 1, minWidth: "200px", padding: "0.5rem" }}
          />

          <select
              value={docType}
              onChange={(e) => setDocType(e.target.value)}
              style={{ padding: "0.5rem" }}
          >
            <option value="all">Усі типи</option>
            <option value="news">Новини (News)</option>
            <option value="publicistic">Публіцистика (Publicistic)</option> {/* Оновлено */}
            <option value="scientific">Наукові (Scientific)</option>
          </select>

          <select
              value={entityType}
              onChange={(e) => setEntityType(e.target.value)}
              style={{ padding: "0.5rem" }}
          >
            <option value="all">Усі сутності</option>
            <option value="PER">Люди (PER)</option>
            <option value="ORG">Організації (ORG)</option>
            <option value="LOC">Локації (LOC)</option>
            <option value="DATE">Дати (DATE)</option>
          </select>

          <button
              onClick={handleSearch}
              disabled={loading || !query}
              className="btn-primary" // Якщо є клас, або додай стилі
              style={{ padding: "0.5rem 1.5rem", cursor: "pointer" }}
          >
            {loading ? "..." : "Шукати"}
          </button>
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          {results.length === 0 && !loading && !error && (
              <p style={{ color: "var(--muted-text)", textAlign: "center" }}>
                Введіть запит для пошуку...
              </p>
          )}

          {results.map((doc) => (
              <SearchResultCard key={doc.id} doc={doc} />
          ))}
        </div>
      </div>
  );
}