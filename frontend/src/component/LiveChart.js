import { useEffect, useRef } from "react";
import { createChart, CrosshairMode } from "lightweight-charts";

export default function LiveCandles() {

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
      "ws://localhost:8009/ws/NIFTY50-INDEX"
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

      console.log("HISTORY:", message);

      candleSeries.setData(message.data);

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

  }, []);

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
          NIFTY50 Live Chart
        </div>

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