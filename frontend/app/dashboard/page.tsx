"use client";
import { useEffect,useState } from "react";
import { api } from "@/lib/api";
import { PatientCard } from "@/components/PatientCard";
import { AlertFeed } from "@/components/AlertFeed";
export default function Dashboard(){const [patients,setPatients]=useState<any[]>([]);useEffect(()=>{api("/api/patients").then(setPatients).catch(()=>{})},[]);return <div className="grid gap-6 lg:grid-cols-[1fr_1fr]"><section><h1 className="mb-4 text-2xl font-bold">Patients</h1><div className="grid gap-3">{patients.map(p=><PatientCard key={p.id} patient={p}/>)}</div></section><section><h1 className="mb-4 text-2xl font-bold">Live alerts</h1><AlertFeed/></section></div>}
