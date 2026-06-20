"use client";
import { AlertCircle, RotateCcw } from "lucide-react";
import { Button } from "@/src/components/ui/button";
export default function ErrorState({reset}:{error:Error;reset:()=>void}){return <div className="flex min-h-[60vh] flex-col items-center justify-center text-center"><span className="grid h-12 w-12 place-items-center rounded-lg bg-red/8 text-red"><AlertCircle/></span><h1 className="mt-4 text-xl font-semibold text-navy">This view could not be loaded</h1><p className="mt-2 max-w-md text-sm text-stone">Your data is safe. Retry the request to return to the workspace.</p><Button className="mt-5" onClick={reset}><RotateCcw size={16}/>Try again</Button></div>}
