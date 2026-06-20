import type { Metadata } from "next";
import { DashboardShell } from "@/src/components/dashboard/dashboard-shell";
export const metadata:Metadata={title:"Workspace"};
export default function Layout({children}:{children:React.ReactNode}){return <DashboardShell>{children}</DashboardShell>}
