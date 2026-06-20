import type { AnalysisRequest, AnalysisResponse } from "@/src/types";
export async function analyzeDocument(payload:AnalysisRequest):Promise<AnalysisResponse>{
  const response=await fetch("/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  const data=await response.json().catch(()=>({}));
  if(!response.ok) throw new Error(data.detail||"Analysis failed. Please check the document URL and try again.");
  return data as AnalysisResponse;
}

export async function analyzeUpload(file:File,questions:string[]):Promise<AnalysisResponse>{
  const formData=new FormData();
  formData.append("document",file);
  formData.append("questions",JSON.stringify(questions));
  const response=await fetch("/api/analyze",{method:"POST",body:formData});
  const data=await response.json().catch(()=>({}));
  if(!response.ok) throw new Error(data.detail||"The uploaded document could not be analyzed.");
  return data as AnalysisResponse;
}
