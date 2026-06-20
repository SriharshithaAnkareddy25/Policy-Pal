import { NextResponse } from "next/server";
const API_URL=process.env.POLICYPAL_API_URL||"http://127.0.0.1:8000/api/v1";
export async function POST(request:Request){
  try{
    const token=process.env.BEARER_TOKEN;
    const isUpload=request.headers.get("content-type")?.includes("multipart/form-data");
    const body=isUpload?await request.formData():JSON.stringify(await request.json());
    const endpoint=isUpload?"/process-upload":token?"/hackrx/run":"/process-document";
    const response=await fetch(`${API_URL}${endpoint}`,{
      method:"POST",
      headers:{...(!isUpload?{"Content-Type":"application/json"}:{}),...(!isUpload&&token?{Authorization:`Bearer ${token}`}:{})},
      body,
      cache:"no-store",
    });
    const data=await response.json().catch(()=>({detail:"The analysis service returned an unreadable response."}));
    return NextResponse.json(data,{status:response.status});
  }catch(error){
    const detail=error instanceof Error?error.message:"Unable to connect to the analysis service.";
    return NextResponse.json({detail},{status:502});
  }
}
