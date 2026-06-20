import type { DocumentItem, HistoryItem } from "@/src/types";
export const documents:DocumentItem[]=[
  {name:"Employee Health Policy 2026",type:"PDF",date:"Jun 20, 2026",status:"Ready"},
  {name:"Vendor Services Agreement",type:"DOCX",date:"Jun 18, 2026",status:"Ready"},
  {name:"Renewal confirmation",type:"EML",date:"Jun 16, 2026",status:"Processing"},
  {name:"Information Security Addendum",type:"PDF",date:"Jun 12, 2026",status:"Ready"},
];
export const history:HistoryItem[]=[
  {date:"Jun 20, 10:42 AM",document:"Employee Health Policy",question:"Does this cover knee surgery?",decision:"Covered",confidence:92},
  {date:"Jun 18, 3:16 PM",document:"Vendor Services Agreement",question:"Can either party terminate early?",decision:"Conditional",confidence:88},
  {date:"Jun 12, 11:05 AM",document:"Security Addendum",question:"What is the breach notice period?",decision:"72 hours",confidence:96},
];
