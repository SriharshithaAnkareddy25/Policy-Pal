import Link from "next/link";
import { ShieldCheck } from "lucide-react";

export function BrandMark({ inverse = false }: { inverse?: boolean }) {
  return <Link href="/" className={`flex items-center gap-2 font-bold ${inverse ? "text-white" : "text-navy"}`}><span className={`grid h-8 w-8 place-items-center rounded-md ${inverse ? "bg-tangerine text-navy" : "bg-navy text-white"}`}><ShieldCheck size={17} /></span><span>PolicyPal</span></Link>;
}
