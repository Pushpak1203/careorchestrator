"use client";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from "recharts";
export function VitalsChart({ vitals }: { vitals: any[] }) {
 const data = vitals.map(v => ({ ...v, date: new Date(v.recorded_at).toLocaleDateString() }));
 return <div className="h-80 rounded-xl border bg-white p-4"><ResponsiveContainer width="100%" height="100%"><LineChart data={data}><XAxis dataKey="date"/><YAxis/><Tooltip/><Legend/><Line type="monotone" dataKey="blood_glucose" stroke="#2563eb" dot={false}/><Line type="monotone" dataKey="heart_rate" stroke="#dc2626" dot={false}/></LineChart></ResponsiveContainer></div>;
}
