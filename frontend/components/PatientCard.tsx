"use client";
const styles: Record<string,string> = { LOW:"bg-emerald-100 text-emerald-800", MEDIUM:"bg-amber-100 text-amber-800", HIGH:"bg-orange-100 text-orange-800", CRITICAL:"bg-red-100 text-red-800" };
export function PatientCard({ patient }: { patient: any }) {
 return <div className="rounded-xl border bg-white p-4 shadow-sm"><div className="flex items-center justify-between"><div><h3 className="font-semibold">{patient.full_name}</h3><p className="text-sm text-slate-500">{(patient.chronic_conditions || []).join(", ") || "No conditions listed"}</p></div><span className={`rounded-full px-3 py-1 text-xs font-bold ${styles[patient.risk_level] || styles.LOW}`}>{patient.risk_level}</span></div><p className="mt-3 text-sm">Clinician: {patient.assigned_clinician || "Unassigned"}</p></div>
}
