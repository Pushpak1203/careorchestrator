"use client";
export function CaregiverPanel({ caregivers }: { caregivers: any[] }) {
 return <div className="rounded-xl border bg-white p-4"><h2 className="mb-3 text-lg font-semibold">Caregivers</h2><div className="space-y-2">{caregivers.map(c=><div key={c.id} className="border-b pb-2 last:border-0"><div className="font-medium">{c.full_name}</div><div className="text-sm text-slate-500">{c.relationship} · {c.phone}</div></div>)}{caregivers.length===0&&<p className="text-sm text-slate-500">No caregivers assigned.</p>}</div></div>
}
