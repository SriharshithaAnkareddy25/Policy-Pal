import type { HTMLAttributes } from "react";
import { cn } from "@/src/lib/cn";
export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) { return <div className={cn("rounded-lg border border-navy/10 bg-white shadow-[0_8px_30px_rgba(3,36,81,.05)]",className)} {...props} />; }
