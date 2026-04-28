import { useState, useEffect, useRef } from "react";

// ── API Call ──
async function fetchPrice(symbol) {
  const res = await fetch(`http://127.0.0.1:8007/api/v1/live_feed/?symbols=${symbol}`);
  const data = await res.json();
  return data.live_feed[symbol].ltp;
}

export default function StockWatchlist() {
  const [stocks, setStocks] = useState([]);
  const [input, setInput] = useState("");
  const [darkMode, setDarkMode] = useState(false);
  const [addHover, setAddHover] = useState(false);
  const [inputFocused, setInputFocused] = useState(false);
  const [hoveredRow, setHoveredRow] = useState(null);
  const [cardMounted, setCardMounted] = useState(false);
  const [cardHover, setCardHover] = useState(false);

  // useRef always holds the latest stocks 
  const stocksRef = useRef(stocks);
  useEffect(() => {
    stocksRef.current = stocks;
  }, [stocks]);

  useEffect(() => {
    const saved = window.localStorage.getItem("watchlist-dark-mode");
    if (saved === "true") setDarkMode(true);
  }, []);

  useEffect(() => {
    setCardMounted(true);
  }, []);

  useEffect(() => {
    window.localStorage.setItem("watchlist-dark-mode", darkMode ? "true" : "false");
  }, [darkMode]);

  // ── Refresh all prices every 2 seconds ──
  useEffect(() => {
    const interval = setInterval(() => {
      refreshPrices();
    }, 2000);
    return () => clearInterval(interval);
  }, []); 

  async function refreshPrices() {
    const current = stocksRef.current;
    if (current.length === 0) return; 

    const updated = await Promise.all(
      current.map(async (stock) => {
        const newPrice = await fetchPrice(stock.symbol);
        return { ...stock, prevPrice: stock.price, price: newPrice };
      })
    );
    setStocks(updated);
  }

  // ── Add a stock ──
  async function addStock() {
    const symbol = input.trim().toUpperCase();
    if (!symbol) return;
    if (stocksRef.current.find((s) => s.symbol === symbol)) return;

    const price = await fetchPrice(symbol);
    setStocks((prev) => [...prev, { symbol, price, prevPrice: null }]);
    setInput("");
  }

  // ── Remove a stock ──
  function removeStock(symbol) {
    setStocks((prev) => prev.filter((s) => s.symbol !== symbol));
  }

  // ── Price color based on change ──
  function priceColor(stock) {
    if (!stock.prevPrice) return darkMode ? "#e2e8f0" : "#111827";
    if (stock.price > stock.prevPrice) return "#16a34a";
    if (stock.price < stock.prevPrice) return "#dc2626";
    return darkMode ? "#e2e8f0" : "#111827";
  }

  const theme = darkMode ? darkStyles : styles;
  const cardStyle = {
    ...theme.card,
    opacity: cardMounted ? 1 : 0,
    transform: `translateY(${cardMounted ? 0 : 18}px) scale(${cardHover ? 1.01 : 1})`,
    boxShadow: cardHover ? theme.cardHoverShadow : theme.card.boxShadow,
    transition: "opacity 0.32s ease, transform 0.32s ease, box-shadow 0.32s ease",
  };

  return (
    <div style={theme.page}>
      <div
        style={cardStyle}
        onMouseEnter={() => setCardHover(true)}
        onMouseLeave={() => setCardHover(false)}
      >

        {/* Header */}
        <div style={theme.headerRow}>
          <div>
            <h1 style={theme.title}>📈 Watchlist</h1>
            <p style={theme.subtitle}>Auto-refreshes every 2 seconds</p>
          </div>
          <button style={theme.toggleBtn} onClick={() => setDarkMode((prev) => !prev)}>
            {darkMode ? "Light Mode" : "Dark Mode"}
          </button>
        </div>

        {/* Input row */}
        <div style={theme.inputRow}>
          <input
            style={{ ...theme.input, ...(inputFocused ? theme.inputFocus : {}) }}
            placeholder="Enter stock symbol (e.g. AAPL)"
            value={input}
            onChange={(e) => setInput(e.target.value.toUpperCase())}
            onFocus={() => setInputFocused(true)}
            onBlur={() => setInputFocused(false)}
            onKeyDown={(e) => e.key === "Enter" && addStock()}
            maxLength={20}
          />
          <button
            style={{ ...theme.addBtn, ...(addHover ? theme.addBtnHover : {}) }}
            onClick={addStock}
            onMouseEnter={() => setAddHover(true)}
            onMouseLeave={() => setAddHover(false)}
          >
            Add
          </button>
        </div>

        {/* Empty state */}
        {stocks.length === 0 && (
          <p style={theme.empty}>Add a stock symbol to get started.</p>
        )}

        {/* Stock rows */}
        <div style={theme.stockList}>
          {stocks.map((stock) => {
          const diff = stock.prevPrice
            ? (stock.price - stock.prevPrice).toFixed(2)
            : null;
          const up = Number(diff) > 0; // ✅ number comparison, not string

          return (
            <div
              key={stock.symbol}
              style={{ ...theme.row, ...(hoveredRow === stock.symbol ? theme.rowHover : {}) }}
              onMouseEnter={() => setHoveredRow(stock.symbol)}
              onMouseLeave={() => setHoveredRow(null)}
            >

              {/* Symbol */}
              <span style={theme.symbol}>{stock.symbol}</span>

              {/* Change badge */}
              <span style={{ flex: 1 }}>
                {diff && (
                  <span style={{
                    ...theme.badge,
                    background: up ? "#dcfce7" : "#fee2e2",
                    color: up ? "#15803d" : "#b91c1c",
                  }}>
                    {up ? "▲" : "▼"} {Math.abs(diff)}
                  </span>
                )}
              </span>

              {/* Price */}
              <span style={{ ...theme.price, color: priceColor(stock) }}>
                {stock.price != null ? `${stock.price.toFixed(2)}` : "—"}
              </span>

              {/* Remove */}
              <button style={theme.removeBtn} onClick={() => removeStock(stock.symbol)}>
                ✕
              </button>

            </div>
          );
        })}
        </div>

      </div>
    </div>
  );
}

// ── Styles ────────────────────────────────────────────────
const styles = {
  page: {
    minHeight: "100vh",
    background: "#f1f5f9",
    display: "flex",
    justifyContent: "center",
    padding: "48px 16px",
    fontFamily: "'Segoe UI', sans-serif",
  },
  card: {
    background: "#fff",
    borderRadius: 16,
    padding: 18,
    width: "100%",
    maxWidth: 700,
    boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
    height: "fit-content",
  },
  cardHoverShadow: "0 14px 46px rgba(15, 23, 42, 0.14)",
  title: { fontSize: 22, fontWeight: 700, color: "#0f172a", margin: "0 0 4px" },
  subtitle: { fontSize: 13, color: "#94a3b8", margin: "0 0 20px" },
  headerRow: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 16,
    marginBottom: 20,
  },
  toggleBtn: {
    border: "1px solid #cbd5e1",
    background: "#fff",
    color: "#0f172a",
    borderRadius: 999,
    padding: "10px 18px",
    cursor: "pointer",
    fontWeight: 700,
    transition: "background 0.2s ease, transform 0.2s ease",
  },
  inputRow: { display: "flex", gap: 8, marginBottom: 20 },
  stockList: {
    maxHeight: 420,
    overflowY: "auto",
    paddingRight: 4,
  },
  input: {
    flex: 1, height: 44, padding: "0 14px",
    fontSize: 15, fontWeight: 600,
    border: "1.5px solid #e2e8f0", borderRadius: 10, outline: "none",
    letterSpacing: "0.04em",
    transition: "box-shadow 0.25s ease, border-color 0.25s ease",
  },
  inputFocus: {
    boxShadow: "0 12px 28px rgba(37, 99, 235, 0.14)",
    borderColor: "#2563eb",
  },
  addBtn: {
    height: 44, padding: "0 30px",
    background: "#2563eb", color: "#fff",
    border: "none", borderRadius: 10,
    fontSize: 14, fontWeight: 600, cursor: "pointer",
    transition: "background 0.2s ease",
  },
  addBtnHover: {
    background: "#1d4ed8",
  },
  empty: { textAlign: "center", color: "#94a3b8", fontSize: 13, padding: "28px 0" },
  row: {
    display: "flex", alignItems: "center", gap: 12,
    padding: "13px 4px", borderBottom: "1px solid #f1f5f9",
    transition: "background 0.25s ease, transform 0.25s ease",
  },
  rowHover: {
    background: "rgba(37, 99, 235, 0.05)",
    transform: "translateX(3px)",
  },
  symbol: { fontWeight: 700, fontSize: 15, color: "#0f172a", width: 64, letterSpacing: "0.02em" },
  price: { fontWeight: 700, fontSize: 16, transition: "color 0.4s", minWidth: 80, textAlign: "right" },
  badge: { fontSize: 11, fontWeight: 700, padding: "3px 9px", borderRadius: 99 },
  removeBtn: { background: "none", border: "none", color: "#cbd5e1", cursor: "pointer", fontSize: 15, padding: "0 2px", marginLeft: 4 },
};

const darkStyles = {
  ...styles,
  page: {
    ...styles.page,
    background: "#0b1120",
  },
  card: {
    ...styles.card,
    background: "#111827",
    boxShadow: "0 4px 40px rgba(0,0,0,0.35)",
  },
  title: { ...styles.title, color: "#f8fafc" },
  subtitle: { ...styles.subtitle, color: "#cbd5e1" },
  toggleBtn: {
    ...styles.toggleBtn,
    border: "1px solid #374151",
    background: "#1f2937",
    color: "#e2e8f0",
  },
  input: {
    ...styles.input,
    background: "#1f2937",
    color: "#e2e8f0",
    border: "1.5px solid #374151",
  },
  addBtn: {
    ...styles.addBtn,
    background: "#2563eb",
  },
  addBtnHover: {
    background: "#1d4ed8",
  },
  empty: { ...styles.empty, color: "#94a3b8" },
  row: {
    ...styles.row,
    borderBottom: "1px solid #1f2937",
  },
  symbol: { ...styles.symbol, color: "#e2e8f0" },
  removeBtn: { ...styles.removeBtn, color: "#9ca3af" },
};