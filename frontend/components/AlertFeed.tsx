"use client";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { api } from "@/lib/api";
export function AlertFeed() {
 const [alerts,setAlerts]=useState<any[]>([]);
 useEffect(()=>{ api("/api/alerts").then(setAlerts).catch(()=>{}); const channel=supabase.channel("alerts-live").on("postgres_changes",{event:"INSERT",schema:"public",table:"alerts"},p=>setAlerts(a=>[p.new,...a])).subscribe(); return()=>{supabase.removeChannel(channel)};},[]);
 return <div className="space-y-3">{alerts.map(a=><div key={a.id} className="rounded-xl border bg-white p-4"><div className="flex justify-between"><b>{a.title}</b><span className="font-bold">{a.severity}</span></div><p className="mt-1 text-sm text-slate-600">{a.message}</p><p className="mt-2 text-xs text-slate-400">{a.status} · {new Date(a.created_at).toLocaleString()}</p></div>)}{alerts.length===0&&<p className="text-slate-500">No alerts.</p>}</div>
}
