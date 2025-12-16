import { useState } from "react";
import type { FormEvent } from "react";
import { searchDocuments, type SearchParams } from "../api/searchApi";
import type { SearchResult } from "../types/search";
import { SearchResultCard } from "../components/SearchResultCard";

const DOC_TYPE_OPTIONS = [
  { value: "all", label: "Усі типи" },
  { value: "news", label: "Новини" },
  { value: "opinion", label: "Публіцистика" },
  { value: "scientific", label: "Наукові" },
];

const ENTITY_TYPE_OPTIONS = [
  { value: "all", label: "Усі сутності" },
  { value: "PER", label: "PER (персони)" },
  { value: "ORG", label: "ORG (організації)" },
  { value: "LOC", label: "LOC (локації)" },
  { value: "DATE", label: "DATE (дати)" },
];

function SearchPage() {
  const [query, setQuery] = useState("");
  const [docType, setDocType] = useState("all");
  const [entityType, setEntityType] = useState("all");

  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const params: SearchParams = { query };

    if (docType !== "all") params.doc_type = docType;
    if (entityType !== "all") params.entity_type = entityType;

    try {
      const data = await searchDocuments(params);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Помилка запиту");
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 960, margin: "0 auto" }}>
      <h1 style={{ fontSize: "1.75rem", marginBottom: "1.5rem" }}>
        Пошук документів
      </h1>

      <form
        onSubmit={handleSubmit}
        style={{
          display: "grid",
          gap: "1rem",
          padding: "1.25rem",
          borderRadius: "0.75rem",
          backgroundColor: "var(--card-bg)",
          border: "1px solid var(--border)",
          marginBottom: "1.5rem",
        }}
      >
        <div>
          <label
            style={{
              display: "block",
              marginBottom: "0.25rem",
              fontWeight: 500,
            }}
          >
            Пошуковий запит
          </label>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Введіть текст запиту…"
            style={{
              width: "100%",
              padding: "0.5rem 0.75rem",
              borderRadius: "0.5rem",
              border: "1px solid var(--border)",
              fontSize: "0.95rem",
              backgroundColor: "var(--bg)",
              color: "var(--text)",
            }}
          />
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
            gap: "0.75rem",
          }}
        >
          <div>
            <label
              style={{
                display: "block",
                marginBottom: "0.25rem",
                fontWeight: 500,
              }}
            >
              Тип документа
            </label>
            <select
              value={docType}
              onChange={(e) => setDocType(e.target.value)}
              style={{
                width: "100%",
                padding: "0.5rem 0.75rem",
                borderRadius: "0.5rem",
                border: "1px solid var(--border)",
                fontSize: "0.95rem",
                backgroundColor: "var(--bg)",
                color: "var(--text)",
              }}
            >
              {DOC_TYPE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label
              style={{
                display: "block",
                marginBottom: "0.25rem",
                fontWeight: 500,
              }}
            >
              Тип сутності
            </label>
            <select
              value={entityType}
              onChange={(e) => setEntityType(e.target.value)}
              style={{
                width: "100%",
                padding: "0.5rem 0.75rem",
                borderRadius: "0.5rem",
                border: "1px solid var(--border)",
                fontSize: "0.95rem",
                backgroundColor: "var(--bg)",
                color: "var(--text)",
              }}
            >
              {ENTITY_TYPE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "flex-start",
            gap: "0.75rem",
          }}
        >
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="btn btn-primary"
          >
            {loading && <span className="spinner" />}
            <span>{loading ? "Пошук…" : "Шукати"}</span>
          </button>
        </div>
      </form>

      {error && (
        <div
          style={{
            marginBottom: "1rem",
            padding: "0.75rem 1rem",
            borderRadius: "0.5rem",
            backgroundColor: "var(--danger-bg)",
            color: "var(--danger-text)",
            fontSize: "0.9rem",
          }}
        >
          {error}
        </div>
      )}

      <section>
        <h2 style={{ fontSize: "1.25rem", marginBottom: "0.75rem" }}>
          Результати {results.length > 0 && `(${results.length})`}
        </h2>

        {loading && <p>Завантаження…</p>}

        {!loading && results.length === 0 && !error && (
          <p style={{ color: "var(--muted-text)", fontSize: "0.95rem" }}>
            Немає результатів.
          </p>
        )}

        <div style={{ display: "grid", gap: "0.75rem", marginTop: "0.5rem" }}>
          {results.map((doc) => (
            <SearchResultCard key={doc.id} doc={doc} />
          ))}
        </div>
      </section>
    </div>
  );
}

export default SearchPage;
