import { Activity, FileCheck2, Gauge, MessageSquareText, TrendingUp } from "lucide-react";
import { Analyzer } from "@/src/components/dashboard/analyzer";
import { Card } from "@/src/components/ui/card";
const stats=[
 {label:"Documents processed",value:"24",change:"+6 this month",icon:FileCheck2},
 {label:"Questions asked",value:"137",change:"+18 this week",icon:MessageSquareText},
 {label:"Retrieval accuracy",value:"94.8%",change:"2.4% improvement",icon:Gauge},
 {label:"Active analyses",value:"03",change:"All systems normal",icon:Activity},
];
export default function Dashboard(){return <div className="mx-auto max-w-7xl"><div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><p className="text-xs font-bold uppercase text-tangerine">Workspace overview</p><h1 className="mt-1 text-2xl font-semibold text-navy sm:text-3xl">Welcome to PolicyPal</h1><p className="mt-2 text-sm text-stone">Review documents and get evidence-backed answers.</p></div><div className="flex items-center gap-2 text-xs text-[#17603a]"><span className="h-2 w-2 rounded-full bg-[#36a267]"/>Analysis API operational</div></div>
<section aria-label="Workspace statistics" className="my-7 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{stats.map(({label,value,change,icon:Icon})=><Card key={label} className="p-4"><div className="flex items-start justify-between"><div><p className="text-xs font-medium text-stone">{label}</p><p className="mt-2 text-2xl font-semibold text-navy">{value}</p></div><span className="grid h-9 w-9 place-items-center rounded-md bg-[#fff3e4] text-tangerine"><Icon size={18}/></span></div><p className="mt-3 flex items-center gap-1 text-[11px] text-stone"><TrendingUp size={12}/>{change}</p></Card>)}</section><Analyzer/></div>}
