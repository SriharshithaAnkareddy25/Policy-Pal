export type AnalysisRequest = { documents: string; questions: string[] };
export type AnalysisResponse = { answers: string[] };
export type DocumentItem = { name:string; type:"PDF"|"DOCX"|"EML"; date:string; status:"Ready"|"Processing" };
export type HistoryItem = { date:string; document:string; question:string; decision:string; confidence:number };
