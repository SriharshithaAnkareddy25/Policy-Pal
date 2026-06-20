import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "PolicyPal | Explainable document intelligence", template: "%s | PolicyPal" },
  description: "Ask complex questions about policies and contracts, with answers grounded in supporting clauses.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
