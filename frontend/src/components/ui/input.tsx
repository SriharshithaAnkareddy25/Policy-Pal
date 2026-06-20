import type { InputHTMLAttributes, TextareaHTMLAttributes } from "react";
import { cn } from "@/src/lib/cn";
const field="w-full rounded-md border border-navy/15 bg-white px-3.5 text-sm text-ink placeholder:text-stone/55 transition focus:border-tangerine focus:outline-none focus:ring-3 focus:ring-tangerine/15";
export function Input({ className,...props }:InputHTMLAttributes<HTMLInputElement>){return <input className={cn(field,"h-11",className)} {...props}/>}
export function Textarea({ className,...props }:TextareaHTMLAttributes<HTMLTextAreaElement>){return <textarea className={cn(field,"min-h-28 resize-y py-3",className)} {...props}/>}
