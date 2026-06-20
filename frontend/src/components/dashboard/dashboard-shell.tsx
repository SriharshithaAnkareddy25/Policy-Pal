"use client";
import { useState } from "react";
import { Bell, Menu, Search } from "lucide-react";
import { Sidebar } from "./sidebar";
export function DashboardShell({children}:{children:React.ReactNode}){
 const [open,setOpen]=useState(false);
 return <div className="min-h-screen bg-surface"><Sidebar open={open} onClose={()=>setOpen(false)}/><div className="lg:pl-64"><header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-navy/10 bg-white px-4 sm:px-7"><div className="flex items-center gap-3"><button onClick={()=>setOpen(true)} className="icon-button lg:!hidden" aria-label="Open menu"><Menu size={19}/></button><div className="hidden items-center gap-2 text-sm text-stone sm:flex"><Search size={16}/><span>Search workspace</span><kbd className="ml-3 rounded border border-navy/10 px-1.5 py-0.5 text-[10px]">⌘ K</kbd></div></div><div className="flex items-center gap-3"><button className="icon-button" aria-label="Notifications"><Bell size={18}/></button><div className="grid h-9 w-9 place-items-center rounded-full bg-navy text-xs font-bold text-white">HP</div></div></header><main className="p-4 sm:p-7 lg:p-8">{children}</main></div></div>;
}
