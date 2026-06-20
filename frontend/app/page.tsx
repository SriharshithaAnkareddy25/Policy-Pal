import {
  ArrowRight,
  BookOpenCheck,
  BrainCircuit,
  CheckCircle2,
  FileSearch,
  Files,
  Menu,
  Quote,
  ScanText,
  ShieldCheck,
  Sparkles,
  UploadCloud,
} from "lucide-react";

import { ButtonLink } from "@/src/components/ui/button";
import { BrandMark } from "@/src/components/shared/brand-mark";

const features = [
  { icon: FileSearch, title: "Smart clause retrieval", copy: "Find the exact language that matters across long, dense documents." },
  { icon: BrainCircuit, title: "AI question answering", copy: "Ask plain-language questions and get direct, document-grounded answers." },
  { icon: BookOpenCheck, title: "Explainable decisions", copy: "See the clauses and reasoning behind every answer, not just a verdict." },
  { icon: Files, title: "Multi-format analysis", copy: "Work with PDF, DOCX, and email documents in one focused workspace." },
];

const steps = [
  [UploadCloud, "Upload document", "Add a policy, agreement, or HR document."],
  [ScanText, "Process", "Text is extracted and prepared for analysis."],
  [FileSearch, "Retrieve", "Relevant clauses are matched to your question."],
  [Sparkles, "Generate", "AI builds an answer using retrieved evidence."],
  [ShieldCheck, "Decide", "Review the decision, confidence, and clauses."],
] as const;

export default function Home() {
  return (
    <main className="min-h-screen overflow-hidden bg-white text-ink">
      <header className="sticky top-0 z-50 border-b border-navy/10 bg-white/95 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 lg:px-8">
          <BrandMark />
          <nav className="hidden items-center gap-7 text-sm font-medium text-stone md:flex" aria-label="Primary navigation">
            <a href="#features" className="transition-colors hover:text-navy">Features</a>
            <a href="#how-it-works" className="transition-colors hover:text-navy">How it works</a>
            <a href="#preview" className="transition-colors hover:text-navy">Dashboard preview</a>
            <a href="#pricing" className="transition-colors hover:text-navy">Pricing</a>
          </nav>
          <div className="hidden items-center gap-2 sm:flex">
            <ButtonLink href="/dashboard" variant="ghost">Sign in</ButtonLink>
            <ButtonLink href="/dashboard">Get started <ArrowRight size={16} /></ButtonLink>
          </div>
          <button className="icon-button sm:!hidden" aria-label="Open navigation"><Menu size={20} /></button>
        </div>
      </header>

      <section className="relative border-b border-navy/10 bg-[#fffaf4] px-5 pb-16 pt-14 sm:pt-20 lg:px-8 lg:pb-24">
        <div className="hero-grid absolute inset-0 opacity-45" aria-hidden="true" />
        <div className="relative mx-auto max-w-7xl text-center">
          <p className="mb-7 text-xs font-bold uppercase text-flame">Document intelligence, made accountable</p>
          <h1 className="brand-title text-navy">POLICY PAL</h1>
          <p className="mx-auto mt-7 max-w-3xl text-3xl font-semibold leading-tight text-navy sm:text-5xl">Understand complex documents instantly</p>
          <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-stone sm:text-lg">Upload insurance policies, contracts, legal agreements, and HR documents. Ask questions naturally and receive explainable answers with supporting clauses.</p>
          <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <ButtonLink href="/dashboard" size="lg">Try PolicyPal <ArrowRight size={18} /></ButtonLink>
            <ButtonLink href="#preview" variant="secondary" size="lg">View demo</ButtonLink>
          </div>

          <div id="preview" className="dashboard-preview mx-auto mt-14 max-w-5xl text-left">
            <div className="flex items-center justify-between border-b border-navy/10 px-4 py-3 sm:px-5">
              <div className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-flame" /><span className="text-xs font-semibold text-navy">Benefit policy review</span></div>
              <span className="status-pill"><CheckCircle2 size={13} /> Analysis complete</span>
            </div>
            <div className="grid min-h-[390px] md:grid-cols-[220px_1fr]">
              <aside className="hidden border-r border-navy/10 bg-[#f7f8fa] p-4 md:block">
                <span className="eyebrow">Source document</span>
                <div className="mt-3 rounded-md border border-navy/10 bg-white p-3">
                  <div className="flex items-center gap-2"><span className="file-icon">PDF</span><div><p className="text-xs font-semibold text-navy">Health_Policy.pdf</p><p className="mt-0.5 text-[11px] text-stone">42 pages</p></div></div>
                </div>
                <div className="mt-6 space-y-3 text-xs text-stone"><p className="font-semibold text-navy">Analysis trail</p><p>01 · Text extracted</p><p>02 · 128 clauses indexed</p><p>03 · 8 matches retrieved</p></div>
              </aside>
              <div className="p-5 sm:p-8">
                <div className="question-chip"><Quote size={15} /> Does this policy cover knee surgery?</div>
                <div className="mt-6 grid gap-5 lg:grid-cols-[1fr_210px]">
                  <div>
                    <div className="flex items-center justify-between"><span className="eyebrow">Decision</span><span className="confidence">92% confidence</span></div>
                    <h2 className="mt-3 text-3xl font-semibold text-navy">Covered after waiting period</h2>
                    <p className="mt-4 text-sm leading-6 text-stone">Knee surgery is covered when medically necessary, provided the 24-month waiting period for specified procedures has been completed.</p>
                    <div className="mt-6 border-l-2 border-tangerine bg-[#fff8ee] p-4 text-sm leading-6 text-navy">“Surgical treatment for joint conditions is admissible after completion of the applicable waiting period.”</div>
                  </div>
                  <div className="border-t border-navy/10 pt-5 lg:border-l lg:border-t-0 lg:pl-5 lg:pt-0">
                    <span className="eyebrow">Referenced clauses</span>
                    <div className="mt-3 space-y-2">{["Clause 4.2", "Clause 8.1", "Clause 10.3"].map((item) => <div key={item} className="clause-row"><CheckCircle2 size={14} />{item}</div>)}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="section-shell">
        <div className="section-heading"><div><span className="eyebrow">Built for scrutiny</span><h2>Every answer earns your trust.</h2></div><p>PolicyPal turns document analysis into a clear, reviewable workflow your team can confidently act on.</p></div>
        <div className="mt-12 grid gap-px overflow-hidden rounded-lg border border-navy/10 bg-navy/10 md:grid-cols-2 lg:grid-cols-4">
          {features.map(({ icon: Icon, title, copy }, index) => <article key={title} className="feature-card"><span className="feature-number">0{index + 1}</span><Icon size={24} /><h3>{title}</h3><p>{copy}</p></article>)}
        </div>
      </section>

      <section id="how-it-works" className="border-y border-white/10 bg-navy text-white">
        <div className="section-shell">
          <div className="section-heading light"><div><span className="eyebrow text-tacao">A transparent workflow</span><h2>From upload to evidence.</h2></div><p>Five deliberate steps keep every answer grounded in the document you provide.</p></div>
          <ol className="mt-14 grid gap-8 md:grid-cols-5">
            {steps.map(([Icon, title, copy], index) => <li key={title} className="process-step"><div className="process-icon"><Icon size={21} /></div><span>0{index + 1}</span><h3>{title}</h3><p>{copy}</p></li>)}
          </ol>
        </div>
      </section>

      <section id="pricing" className="section-shell text-center">
        <span className="eyebrow">Start analyzing</span><h2 className="mx-auto mt-3 max-w-2xl text-4xl font-semibold text-navy sm:text-5xl">Clarity for the documents that matter.</h2>
        <p className="mx-auto mt-5 max-w-xl leading-7 text-stone">Bring one document and one important question. PolicyPal will help you find the language behind the answer.</p>
        <div className="mt-8"><ButtonLink href="/dashboard" size="lg">Open your workspace <ArrowRight size={18} /></ButtonLink></div>
      </section>

      <footer className="border-t border-navy/10 px-5 py-8"><div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 sm:flex-row"><BrandMark /><p className="text-xs text-stone">Explainable document intelligence for better decisions.</p></div></footer>
    </main>
  );
}
