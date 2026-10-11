import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

function App() {
  const [stocks, setStocks] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/stocks/top10")
      .then((res) => res.json())
      .then((data) => {
        setStocks(data);
        setSelected(data[0]); // default selection
      });
  }, []);

  const chartData =
    selected?.history.map((p, i) => ({
      month: `M${i + 1}`,
      price: p,
    })) || [];

  return (
    <div className="container">
      <h1>📈 RealTicker – Live Stock Dashboard</h1>

      <table>
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Company</th>
            <th>Price</th>
            <th>Change</th>
            <th>Volume</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((s) => (
            <tr
              key={s.ticker}
              onClick={() => setSelected(s)}
              className={selected?.ticker === s.ticker ? "active" : ""}
            >
              <td>{s.ticker}</td>
              <td>{s.company}</td>
              <td>${s.price}</td>
              <td style={{ color: s.change >= 0 ? "#00ff88" : "red" }}>
                {s.change}%
              </td>
              <td>{s.volume}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {selected && (
        <>
          <h2>📊 {selected.company} – 6 Month Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="price"
                stroke="#00ff88"
                strokeWidth={3}
              />
            </LineChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
}

export default App;
