import { useState } from "react";
import type { FormEvent } from "react";
import { addDocument } from "../api/searchApi";
import type { FullDocument } from "../types/documents";

function AdminPage() {
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [source, setSource] = useState("");
  const [date, setDate] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [createdDoc, setCreatedDoc] = useState<FullDocument | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setCreatedDoc(null);

    try {
      const doc = await addDocument({
        title: title.trim(),
        body: body.trim(),
        source: source.trim(),
        date: date.trim(),
      });

      setCreatedDoc(doc);
      setTitle("");
      setBody("");
      setSource("");
      setDate("");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Помилка додавання документа"
      );
    } finally {
      setLoading(false);
    }
  }

  const isDisabled =
    loading || !title.trim() || !body.trim() || !source.trim() || !date.trim();

  return (
    <div style={{ maxWidth: 800, margin: "0 auto" }}>
      <h1 style={{ fontSize: "1.75rem", marginBottom: "1.5rem" }}>
        Адмін: додавання документа
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
            Заголовок
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
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

        <div>
          <label
            style={{
              display: "block",
              marginBottom: "0.25rem",
              fontWeight: 500,
            }}
          >
            Текст документа
          </label>
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            rows={8}
            style={{
              width: "100%",
              padding: "0.5rem 0.75rem",
              borderRadius: "0.5rem",
              border: "1px solid var(--border)",
              fontSize: "0.95rem",
              resize: "vertical",
              backgroundColor: "var(--bg)",
              color: "var(--text)",
            }}
          />
        </div>

        <div>
          <label
            style={{
              display: "block",
              marginBottom: "0.25rem",
              fontWeight: 500,
            }}
          >
            Джерело
          </label>
          <input
            type="text"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="Напр. https://..., або назва видання"
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

        <div>
          <label
            style={{
              display: "block",
              marginBottom: "0.25rem",
              fontWeight: 500,
            }}
          >
            Дата
          </label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
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

        <div>
          <button
            type="submit"
            disabled={isDisabled}
            className="btn btn-success"
          >
            {loading && <span className="spinner" />}
            <span>{loading ? "Збереження…" : "Додати документ"}</span>
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

      {createdDoc && (
        <section
          style={{
            padding: "1rem",
            borderRadius: "0.75rem",
            backgroundColor: "var(--success-bg)",
            border: "1px solid var(--success-border)",
          }}
        >
          <h2 style={{ fontSize: "1.1rem", marginBottom: "0.5rem" }}>
            Документ успішно додано
          </h2>
          <p style={{ fontSize: "0.9rem", marginBottom: "0.25rem" }}>
            <strong>ID:</strong> {createdDoc.id}
          </p>
          <p style={{ fontSize: "0.9rem", marginBottom: "0.25rem" }}>
            <strong>Заголовок:</strong> {createdDoc.title}
          </p>
          <p style={{ fontSize: "0.9rem", marginBottom: "0.25rem" }}>
            <strong>Тип:</strong> {createdDoc.doc_type}
          </p>
          <p
            style={{
              fontSize: "0.9rem",
              marginTop: "0.5rem",
              color: "var(--muted-text)",
            }}
          >
            NLP-аналіз (сутності, токени, класифікація) вже виконаний на
            бекенді.
          </p>
        </section>
      )}
    </div>
  );
}

export default AdminPage;
