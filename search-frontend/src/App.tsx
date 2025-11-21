import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import AdminPage from "./pages/AdminPage";
import ThemeSwitch from "./components/ThemeSwitch";

function App() {
  return (
    <BrowserRouter>
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          backgroundColor: "var(--bg)",
          color: "var(--text)",
        }}
      >
        <header
          style={{
            padding: "0.9rem 2rem",
            borderBottom: "1px solid var(--border)",
            backgroundColor: "var(--card-bg)",
            boxShadow: "0 2px 10px rgba(15, 23, 42, 0.12)",
            position: "sticky",
            top: 0,
            zIndex: 10,
          }}
        >
          <nav
            style={{
              display: "flex",
              gap: "1rem",
              alignItems: "center",
            }}
          >
            {/* "Лого" */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "0.4rem",
                fontWeight: 600,
                fontSize: "1rem",
              }}
            >
              <div
                style={{
                  width: 26,
                  height: 26,
                  borderRadius: "0.8rem",
                  background: "linear-gradient(135deg, #2563eb, #22c55e)",
                }}
              />
              <span>DataSearch</span>
            </div>

            {/* Лінки */}
            <NavLink
              to="/"
              className={({ isActive }) =>
                "nav-link" + (isActive ? " active" : "")
              }
            >
              Пошук
            </NavLink>

            <NavLink
              to="/admin"
              className={({ isActive }) =>
                "nav-link" + (isActive ? " active" : "")
              }
            >
              Адмін
            </NavLink>

            {/* Перемикач теми */}
            <div style={{ marginLeft: "auto" }}>
              <ThemeSwitch />
            </div>
          </nav>
        </header>

        <main style={{ flex: 1, padding: "2rem" }}>
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/admin" element={<AdminPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
