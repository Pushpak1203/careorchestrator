"use client";
import { useEffect,useState } from "react";
import { api } from "@/lib/api";
import { PatientCard } from "@/components/PatientCard";
import { VitalsChart } from "@/components/VitalsChart";
import { CaregiverPanel } from "@/components/CaregiverPanel";
export default function Patients(){const [patients,setPatients]=useState<any[]>([]);const [selected,setSelected]=useState<any>(null);const [vitals,setVitals]=useState<any[]>([]);const [caregivers,setCaregivers]=useState<any[]>([]);useEffect(()=>{api("/api/patients").then(setPatients).catch(()=>{})},[]);async function choose(p:any){setSelected(p);const [v,c]=await Promise.all([api(`/api/vitals/patient/${p.id}`),api(`/api/caregivers/patient/${p.id}`)]);setVitals(v);setCaregivers(c)} return <div><h1 className="mb-4 text-2xl font-bold">Patients</h1><div className="grid gap-6 lg:grid-cols-3"><div className="space-y-3">{patients.map(p=><button className="block w-full text-left" onClick={()=>choose(p)} key={p.id}><PatientCard patient={p}/></button>)}</div><div className="lg:col-span-2">{selected?<div className="space-y-6"><h2 className="text-xl font-semibold">{selected.full_name}</h2><VitalsChart vitals={vitals}/><CaregiverPanel caregivers={caregivers}/></div>:<p className="text-slate-500">Select a patient.</p>}</div></div></div>}
