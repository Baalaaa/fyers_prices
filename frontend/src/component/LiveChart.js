import { useEffect, useRef, useState } from "react";
import { createChart, CrosshairMode } from "lightweight-charts";

export default function LiveCandles() {

  const [selectedSymbol, setSelectedSymbol] = useState("NIFTY50-INDEX");

  // Symbol 
  const symbols = ["NSE:NIFTY50-INDEX", 'NSE:ADANIENT-EQ', 'NSE:ADANIPORTS-EQ', 'NSE:APOLLOHOSP-EQ', 'NSE:ASIANPAINT-EQ', 'NSE:AXISBANK-EQ',
                    'NSE:BAJFINANCE-EQ', 'NSE:BAJAJFINSV-EQ', 'NSE:BEL-EQ', 'NSE:BHARTIARTL-EQ', 'NSE:BPCL-EQ',
                    'NSE:BRITANNIA-EQ', 'NSE:CIPLA-EQ', 'NSE:COALINDIA-EQ', 'NSE:DIVISLAB-EQ', 'NSE:DRREDDY-EQ',
                    'NSE:EICHERMOT-EQ', 'NSE:GRASIM-EQ', 'NSE:HCLTECH-EQ', 'NSE:HDFCBANK-EQ', 'NSE:HDFCLIFE-EQ',
                    'NSE:HEROMOTOCO-EQ', 'NSE:HINDALCO-EQ', 'NSE:HINDUNILVR-EQ', 'NSE:ICICIBANK-EQ', 'NSE:INDUSINDBK-EQ',
                    'NSE:INFY-EQ', 'NSE:ITC-EQ', 'NSE:JSWSTEEL-EQ', 'NSE:KOTAKBANK-EQ', 'NSE:LT-EQ','NSE:M&M-EQ',
                    'NSE:MARUTI-EQ', 'NSE:NESTLEIND-EQ', 'NSE:NTPC-EQ', 'NSE:ONGC-EQ','NSE:POWERGRID-EQ',
                    'NSE:RELIANCE-EQ', 'NSE:SBILIFE-EQ', 'NSE:SBIN-EQ', 'NSE:SHRIRAMFIN-EQ', 'NSE:SIEMENS-EQ',
                    'NSE:SUNPHARMA-EQ', 'NSE:TATACONSUM-EQ', 'NSE:TATASTEEL-EQ', 'NSE:TCS-EQ',
                    'NSE:TECHM-EQ', 'NSE:TITAN-EQ', 'NSE:ULTRACEMCO-EQ', 'NSE:WIPRO-EQ']

  const chartContainerRef = useRef();

  useEffect(() => {

    // ---- Create Chart ----
    const chart = createChart(chartContainerRef.current, {

      width: chartContainerRef.current.clientWidth,
      height: 500,

      layout: {
        background: { color: "#0f172a" },
        textColor: "#cbd5e1",
      },

      grid: {
        vertLines: { color: "#1e293b" },
        horzLines: { color: "#1e293b" },
      },

      crosshair: {
        mode: CrosshairMode.Normal,
      },

      rightPriceScale: {
        borderColor: "#334155",
      },

      localization: {
        locale: "en-IN",
      },

      timeScale: {

        borderColor: "#334155",

        timeVisible: true,
        secondsVisible: false,

        tickMarkFormatter: (time) => {

          const date = new Date(time * 1000);

          return date.toLocaleTimeString("en-IN", {
            hour: "2-digit",
            minute: "2-digit",
            hour12: true,
          });
        },
      },
    });

    // ---- Candlestick Series ----
    const candleSeries = chart.addCandlestickSeries({

      upColor: "#22c55e",
      downColor: "#ef4444",

      borderVisible: false,

      wickUpColor: "#22c55e",
      wickDownColor: "#ef4444",
    });

    // ---- WebSocket ----
    const ws = new WebSocket(
      `ws://localhost:8009/ws/${selectedSymbol}`
    );

    ws.onopen = () => {
      console.log("✅ WebSocket Connected");
    };

    ws.onmessage = (event) => {

    const message = JSON.parse(event.data);

    // =========================
    // HISTORY
    // =========================
    if (message.type === "history") {

      // Current Timestamp
      const now = new Date();

      // MarketStart Time
      const MarketStart = new Date();
      MarketStart.setHours(9, 15, 0 , 0);

      // MarketEnd Time
      const MarketEnd = new Date();
      MarketEnd.setHours(15, 30, 0, 0);

      // startTs & endTs
      const startTs = Math.floor(MarketStart.getTime()/ 1000);
      const endTs = Math.floor(MarketEnd.getTime()/ 1000);
      
      // filtering data
      const todayCandles = message.data.filter((candle)=>{
          const t = Number(candle.time);
          return t >= startTs && t <= endTs;
      })

      candleSeries.setData(todayCandles);
      chart.timeScale().fitContent();

      return;

    }

    // =========================
    // LIVE
    // =========================
    if (message.type === "live") {

      
      const raw = message.data;

      const candle = {
        time: Number(raw.time || raw.start),
        open: Number(raw.open),
        high: Number(raw.high),
        low: Number(raw.low),
        close: Number(raw.close),
      };
      console.log(
        "LIVE:",
        candle,
        new Date(candle.time * 1000).toLocaleString("en-IN")
      );

      candleSeries.update(candle);
    }
  };

    ws.onclose = () => {
      console.log("❌ WebSocket Closed");
    };

    // ---- Resize Chart ----
    const handleResize = () => {

      chart.applyOptions({
        width: chartContainerRef.current.clientWidth,
      });
    };

    window.addEventListener("resize", handleResize);

    // ---- Cleanup ----
    return () => {

      if (
        ws.readyState === WebSocket.OPEN ||
        ws.readyState === WebSocket.CONNECTING
      ) {
        ws.close();
      }

      chart.remove();

      window.removeEventListener(
        "resize",
        handleResize
      );
    };

  }, [selectedSymbol]);

  return (

    <div
      style={{
        width: "100%",
        minHeight: "100vh",

        display: "flex",
        justifyContent: "center",
        alignItems: "center",

        backgroundColor: "#020617",

        padding: "30px",

        boxSizing: "border-box",
      }}
    >

      <div
        style={{
          width: "95%",
          maxWidth: "1400px",

          background: "#0f172a",

          border: "1px solid #1e293b",

          borderRadius: "16px",

          padding: "20px",

          boxShadow: "0 0 20px rgba(0,0,0,0.4)",
        }}
      >

        <div
          style={{
            color: "white",

            fontSize: "22px",
            fontWeight: "bold",

            marginBottom: "20px",
          }}
        >
         {selectedSymbol} Live Chart
        </div>
          <select
            value={selectedSymbol}
            onChange={(e) =>
              setSelectedSymbol(e.target.value)
            }
            style={{
              marginBottom: "20px",
              padding: "10px",
              borderRadius: "8px",
              background: "#1e293b",
              color: "white",
              border: "1px solid #334155",
              fontSize: "16px",
            }}
          >
            {symbols.map((symbol) => (
              <option key={symbol} value={symbol}>
                {symbol}
              </option>
            ))}
          </select>
        <div
          ref={chartContainerRef}
          style={{
            width: "100%",
            height: "500px",

            borderRadius: "12px",

            overflow: "hidden",
          }}
        />

      </div>

    </div>
  );
}