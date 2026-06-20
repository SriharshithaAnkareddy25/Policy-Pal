"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, FileText, History, LogOut, MessageSquareText, Settings, X } from "lucide-react";
import { BrandMark } from "@/src/components/shared/brand-mark";
import { cn } from "@/src/lib/cn";
const items=[
  {href:"/dashboard",label:"Dashboard",icon:BarChart3},
  {href:"/dashboard/documents",label:"Documents",icon:FileText},
  {href:"/dashboard#ask",label:"Ask questions",icon:MessageSquareText},
  {href:"/dashboard/history",label:"Analysis history",icon:History},
  {href:"/dashboard/settings",label:"Settings",icon:Settings},
];
export function Sidebar({open,onClose}:{open:boolean;onClose:()=>void}){
  const pathname=usePathname();
  return <><button aria-label="Close sidebar" onClick={onClose} className={cn("fixed inset-0 z-40 bg-navy/40 lg:hidden",!open&&"hidden")}/><aside className={cn("fixed inset-y-0 left-0 z-50 flex w-64 flex-col bg-navy px-4 py-5 text-white transition-transform lg:translate-x-0",open?"translate-x-0":"-translate-x-full")}>
    <div className="flex items-center justify-between px-2"><BrandMark inverse/><button onClick={onClose} className="grid h-9 w-9 place-items-center rounded-md text-white/70 lg:hidden" aria-label="Close menu"><X size={19}/></button></div>
    <nav className="mt-10 space-y-1" aria-label="Dashboard navigation">{items.map(({href,label,icon:Icon})=>{const active=href==="/dashboard"?pathname===href:pathname.startsWith(href.split("#")[0])&&!href.includes("#");return <Link onClick={onClose} key={label} href={href} className={cn("flex h-11 items-center gap-3 rounded-md px-3 text-sm font-medium text-white/65 transition hover:bg-white/8 hover:text-white",active&&"bg-tangerine text-navy hover:bg-tangerine hover:text-navy")}><Icon size={18}/>{label}</Link>})}</nav>
    <div className="mt-auto border-t border-white/10 pt-4"><button className="flex h-11 w-full items-center gap-3 rounded-md px-3 text-sm text-white/60 hover:bg-white/8 hover:text-white"><LogOut size={18}/>Log out</button><p className="mt-4 px-3 text-[10px] text-white/35">PolicyPal workspace · v1.0</p></div>
  </aside></>;
}
