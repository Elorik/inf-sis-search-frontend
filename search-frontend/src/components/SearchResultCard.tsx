import type { SearchResult } from "../types/search";

type Props = {
  doc: SearchResult;
};

export function SearchResultCard({ doc }: Props) {
  return (
    <article
      style={{
        padding: "0.75rem 1rem",
        borderRadius: "0.75rem",
        backgroundColor: "var(--card-bg)",
        border: "1px solid var(--border)",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          gap: "0.5rem",
          marginBottom: "0.25rem",
        }}
      >
        <h3 style={{ fontSize: "1rem", fontWeight: 600 }}>{doc.title}</h3>
        <span
          style={{
            fontSize: "0.75rem",
            padding: "0.15rem 0.5rem",
            borderRadius: "999px",
            backgroundColor: "#eff6ff",
            color: "#1d4ed8",
            textTransform: "uppercase",
          }}
        >
          {doc.doc_type}
        </span>
      </div>

      <p
        style={{
          fontSize: "0.9rem",
          color: "var(--muted-text)",
          marginBottom: "0.5rem",
        }}
      >
        {doc.snippet}
      </p>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: "0.75rem",
        }}
      >
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.35rem" }}>
          {(["PER", "ORG", "LOC", "DATE"] as const).flatMap((type) =>
            doc.entities[type].map((value) => (
              <span
                key={type + value}
                style={{
                  fontSize: "0.7rem",
                  padding: "0.15rem 0.4rem",
                  borderRadius: "999px",
                  backgroundColor: "#f3f4f6",
                  color: "#374151",
                }}
              >
                {type}: {value}
              </span>
            ))
          )}
        </div>

        <span style={{ fontSize: "0.75rem", color: "var(--muted-text)" }}>
          score: {doc.score.toFixed(3)}
        </span>
      </div>
    </article>
  );
}
