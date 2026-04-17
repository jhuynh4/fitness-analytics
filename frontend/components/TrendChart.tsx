"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type TrendChartProps<T> = {
  title: string;
  data: T[];
  dataKey: keyof T;
};

export default function TrendChart<T extends Record<string, string | number>>({
  title,
  data,
  dataKey,
}: TrendChartProps<T>) {
  return (
    <div className="rounded-2xl border p-4 shadow-sm">
      <h2 className="text-lg font-semibold mb-4">{title}</h2>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line
              type="monotone"
              dataKey={String(dataKey)}
              strokeWidth={2}
              dot={{ r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}