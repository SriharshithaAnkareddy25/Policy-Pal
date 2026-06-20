import Link from "next/link";
import type { AnchorHTMLAttributes, ButtonHTMLAttributes } from "react";
import { cn } from "@/src/lib/cn";

type Variant = "primary" | "secondary" | "ghost" | "danger";
type Size = "md" | "lg" | "icon";
const styles = { primary:"border-tangerine bg-tangerine text-navy hover:bg-[#eb7400]", secondary:"border-navy/15 bg-white text-navy hover:bg-surface", ghost:"border-transparent bg-transparent text-navy hover:bg-surface", danger:"border-red bg-red text-white hover:bg-[#b92820]" };
const sizes = { md:"h-10 px-4 text-sm", lg:"h-12 px-5 text-sm", icon:"h-10 w-10" };
const base = "inline-flex shrink-0 items-center justify-center gap-2 rounded-md border font-semibold transition-colors disabled:pointer-events-none disabled:opacity-50";
export function Button({ variant="primary", size="md", className, ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?:Variant; size?:Size }) { return <button className={cn(base,styles[variant],sizes[size],className)} {...props} />; }
export function ButtonLink({ variant="primary", size="md", className, ...props }: AnchorHTMLAttributes<HTMLAnchorElement> & { href:string; variant?:Variant; size?:Size }) { return <Link className={cn(base,styles[variant],sizes[size],className)} {...props} />; }
