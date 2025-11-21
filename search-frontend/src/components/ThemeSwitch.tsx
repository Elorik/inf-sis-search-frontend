import { useEffect, useState } from "react";

function getInitialTheme(): boolean {
  if (typeof window === "undefined") return false;

  const saved = localStorage.getItem("theme");
  if (saved === "theme-dark") return true;
  if (saved === "theme-light") return false;

  return false; // за замовчуванням світла
}

export default function ThemeSwitch() {
  const [dark, setDark] = useState<boolean>(getInitialTheme);

  useEffect(() => {
    const root = document.documentElement;

    root.classList.remove("theme-dark", "theme-light");
    root.classList.add(dark ? "theme-dark" : "theme-light");

    localStorage.setItem("theme", dark ? "theme-dark" : "theme-light");
  }, [dark]);

  return (
    <label className="switch">
      <input
        type="checkbox"
        checked={dark}
        onChange={() => setDark((prev) => !prev)}
      />
      <span className="slider round"></span>
    </label>
  );
}
