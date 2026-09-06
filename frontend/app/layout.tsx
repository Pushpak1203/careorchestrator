import "./globals.css";
import Link from "next/link";
export const metadata = { title: "CareOrchestrator", description: "Proactive chronic disease management" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body><header className="border-b bg-white"><nav className="mx-auto flex max-w-7xl gap-6 p-4"><Link href="/">CareOrchestrator</Link><Link href="/dashboard">Dashboard</Link><Link href="/patients">Patients</Link><Link href="/alerts">Alerts</Link></nav></header><main className="mx-auto max-w-7xl p-6">{children}</main></body></html>;
}
