import { useMemo, useState } from "react";
import {
  PlaneTakeoff, MapPin, CalendarDays, Wallet, Users, Sparkles, Compass,
  Mountain, Utensils, Waves, CheckCircle2, CircleAlert, LoaderCircle,
  ArrowRight, ArrowLeft, RefreshCw, Send, ShieldCheck, Clock3, Hotel,
  TrainFront, Leaf, Menu
} from "lucide-react";

const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const interestOptions = [
  { name: "Nature", icon: Leaf },
  { name: "Adventure", icon: Mountain },
  { name: "Local food", icon: Utensils },
  { name: "Culture", icon: Compass },
  { name: "Beaches", icon: Waves },
  { name: "Relaxation", icon: Sparkles },
];

function todayISO() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
function dateLabel(value) {
  if (!value) return "";
  return new Date(`${value}T12:00:00`).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}
function parseError(data, fallback) {
  if (data?.detail) return typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail);
  return data?.message || fallback;
}

export default function App() {
  const [form, setForm] = useState({
    origin: "Haldwani", destination: "Rishikesh", start_date: "", end_date: "",
    budget: "10000", travelers: "1", interests: ["Nature", "Adventure", "Local food"]
  });
  const [threadId, setThreadId] = useState("");
  const [status, setStatus] = useState("idle");
  const [approval, setApproval] = useState(null);
  const [finalData, setFinalData] = useState(null);
  const [error, setError] = useState("");
  const [feedback, setFeedback] = useState("");
  const [busy, setBusy] = useState(false);
  const [mobileMenu, setMobileMenu] = useState(false);

  const itinerary = useMemo(() => {
    const raw = approval?.itinerary?.content ?? approval?.itinerary ?? finalData?.itinerary ?? "";
    return typeof raw === "string" ? raw : raw?.content || "";
  }, [approval, finalData]);

  function update(key, value) {
    setForm(old => ({ ...old, [key]: value }));
  }
  function toggleInterest(name) {
    setForm(old => ({
      ...old,
      interests: old.interests.includes(name)
        ? old.interests.filter(item => item !== name)
        : [...old.interests, name]
    }));
  }
  async function request(path, body) {
    const response = await fetch(`${API_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(parseError(data, `Request failed (${response.status})`));
    return data;
  }
  async function createTrip(event) {
    event.preventDefault();
    setError("");
    setApproval(null);
    setFinalData(null);
    setFeedback("");
    setBusy(true);
    setStatus("planning");
    try {
      const data = await request("/trips", {
        ...form,
        budget: Number(form.budget),
        travelers: Number(form.travelers)
      });
      setThreadId(data.thread_id);
      setApproval(data.approval_request || null);
      setFinalData(data.result || null);
      setStatus(data.status || "completed");
    } catch (e) {
      setError(`${e.message}. Check that your FastAPI server is running at ${API_URL}.`);
      setStatus("idle");
    } finally {
      setBusy(false);
    }
  }
  async function submitDecision(approved) {
    if (!threadId) return;
    setError("");
    setBusy(true);
    try {
      const data = await request(`/trips/${encodeURIComponent(threadId)}/approval`, {
        approved,
        feedback: approved ? "" : feedback.trim()
      });
      setApproval(data.approval_request || null);
      setFinalData(data.result || data);
      setStatus(data.status || "completed");
      if (data.status === "waiting_for_approval" && data.approval_request) setFeedback("");
    } catch (e) {
      setError(`${e.message}. Your trip thread is ${threadId}.`);
    } finally {
      setBusy(false);
    }
  }
  function newTrip() {
    setThreadId(""); setApproval(null); setFinalData(null); setError("");
    setFeedback(""); setStatus("idle");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const hasApproval = status === "waiting_for_approval" && approval;
  const completed = status === "completed" && !approval;
  const isPlanning = status === "planning";

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#" onClick={e => { e.preventDefault(); newTrip(); }}>
          <span className="brand-mark"><Compass size={22} strokeWidth={2.4}/></span>
          <span>roamwise<span className="brand-dot">.</span></span>
        </a>
        <nav className={mobileMenu ? "nav-links open" : "nav-links"}>
          <a href="#how-it-works" onClick={() => setMobileMenu(false)}>How it works</a>
          <a href="#planner" onClick={() => setMobileMenu(false)}>Plan a trip</a>
          <span className="api-pill"><span className="status-dot"/> AI trip planner</span>
        </nav>
        <button className="mobile-menu" onClick={() => setMobileMenu(v => !v)} aria-label="Toggle menu"><Menu size={22}/></button>
      </header>

      <main>
        <section className="hero">
          <div className="hero-copy">
            <div className="eyebrow"><Sparkles size={15}/> YOUR PERSONAL AI TRAVEL TEAM</div>
            <h1>Less planning.<br/><span>More exploring.</span></h1>
            <p>Tell us where you want to go. Your AI research team will pull together transport, stays and experiences into one thoughtful itinerary.</p>
            <div className="hero-points">
              <span><CheckCircle2 size={16}/> Built around your budget</span>
              <span><CheckCircle2 size={16}/> You approve before it’s final</span>
            </div>
            <a className="primary-link" href="#planner">Plan my trip <ArrowRight size={17}/></a>
          </div>
          <div className="hero-art">
            <div className="art-orbit orbit-one"></div><div className="art-orbit orbit-two"></div>
            <div className="sun"></div>
            <div className="mountain mountain-back"></div><div className="mountain mountain-front"></div>
            <div className="lake"></div>
            <div className="art-card floating-card">
              <span className="float-icon"><Sparkles size={18}/></span>
              <div><b>Your next adventure</b><small>Thoughtfully planned by AI</small></div>
            </div>
            <div className="art-card budget-card"><span className="budget-check"><CheckCircle2 size={17}/></span><div><small>Budget-aware plans</small><b>Every rupee counts</b></div></div>
            <div className="art-caption"><MapPin size={14}/> FIND YOUR WAY OUT THERE</div>
          </div>
        </section>

        <section className="planner-section" id="planner">
          <div className="section-heading">
            <div><div className="eyebrow">START YOUR JOURNEY</div><h2>Where to next?</h2><p>A few details are all we need to get started.</p></div>
            <div className="step-badge"><span>01</span> Trip details</div>
          </div>
          <div className="planner-grid">
            <form className="form-card" onSubmit={createTrip}>
              <div className="card-title"><span className="title-icon"><MapPin size={19}/></span><div><h3>Your trip</h3><p>Make it yours. Change any field.</p></div></div>
              <div className="field-row">
                <label className="field"><span>FROM</span><div className="input-wrap"><PlaneTakeoff size={17}/><input required minLength="2" maxLength="150" value={form.origin} onChange={e => update("origin", e.target.value)} placeholder="Starting city"/></div></label>
                <label className="field"><span>DESTINATION</span><div className="input-wrap"><MapPin size={17}/><input required minLength="2" maxLength="150" value={form.destination} onChange={e => update("destination", e.target.value)} placeholder="Where to?"/></div></label>
              </div>
              <div className="field-row">
                <label className="field"><span>DEPARTURE</span><div className="input-wrap"><CalendarDays size={17}/><input required type="date" min={todayISO()} value={form.start_date} onChange={e => { update("start_date", e.target.value); if (form.end_date && form.end_date <= e.target.value) update("end_date", ""); }}/></div></label>
                <label className="field"><span>RETURN</span><div className="input-wrap"><CalendarDays size={17}/><input required type="date" min={form.start_date || todayISO()} value={form.end_date} onChange={e => update("end_date", e.target.value)}/></div></label>
              </div>
              <div className="field-row">
                <label className="field"><span>TOTAL BUDGET (₹)</span><div className="input-wrap"><Wallet size={17}/><input required type="number" min="1" max="100000000" value={form.budget} onChange={e => update("budget", e.target.value)} placeholder="10000"/></div></label>
                <label className="field"><span>TRAVELERS</span><div className="input-wrap"><Users size={17}/><select value={form.travelers} onChange={e => update("travelers", e.target.value)}>{Array.from({length: 10}, (_, i) => <option key={i+1} value={i+1}>{i+1} {i === 0 ? "traveler" : "travelers"}</option>)}</select></div></label>
              </div>
              <div className="interest-header"><div><h4>What are you into?</h4><p>Pick all that sound like you.</p></div><span>{form.interests.length} selected</span></div>
              <div className="interest-grid">
                {interestOptions.map(({name, icon: Icon}) => <button type="button" key={name} className={`interest-chip ${form.interests.includes(name) ? "selected" : ""}`} onClick={() => toggleInterest(name)}><Icon size={17}/>{name}{form.interests.includes(name) && <CheckCircle2 size={14} className="chip-check"/>}</button>)}
              </div>
              {error && <div className="error-box"><CircleAlert size={18}/><span>{error}</span></div>}
              <button className="submit-button" type="submit" disabled={busy || !form.interests.length || !form.start_date || !form.end_date || form.end_date <= form.start_date}>
                {busy && isPlanning ? <><LoaderCircle className="spin" size={18}/> Researching your trip…</> : <><Sparkles size={18}/> Build my itinerary <ArrowRight size={18}/></>}
              </button>
              <p className="form-note"><ShieldCheck size={14}/> Your itinerary stays a draft until you approve it.</p>
            </form>

            <aside className="side-column">
              <div className="side-note"><div className="note-icon"><Sparkles size={20}/></div><h3>A little planning.<br/>A lot more possibility.</h3><p>Our AI team researches options, compares your budget, and builds a day-by-day plan for you to review.</p><div className="note-divider"/><div className="note-feature"><span><TrainFront size={17}/></span><div><b>Getting there</b><small>Transport options and estimated fares</small></div></div><div className="note-feature"><span><Hotel size={17}/></span><div><b>Places to stay</b><small>Accommodation ideas for your budget</small></div></div><div className="note-feature"><span><Mountain size={17}/></span><div><b>Things to do</b><small>Experiences picked for your interests</small></div></div></div>
              <div className="trust-card"><div className="trust-icon"><Clock3 size={18}/></div><div><b>Made for real-world plans</b><p>Prices and availability can change. Always verify bookings with the provider.</p></div></div>
            </aside>
          </div>
        </section>

        {(isPlanning || hasApproval || completed || (status === "completed" && finalData)) && (
          <section className="results-section" aria-live="polite">
            {isPlanning && <div className="loading-card"><div className="loader-emblem"><LoaderCircle className="spin" size={30}/></div><h2>Your trip is coming together</h2><p>Our research team is comparing transport, stays and experiences. This can take a little while.</p><div className="loading-steps"><span><CheckCircle2 size={15}/> Planning research</span><span><LoaderCircle className="spin" size={15}/> Researching options</span><span>Building your itinerary</span></div></div>}
            {hasApproval && <div className="itinerary-card">
              <div className="result-header"><div><div className="eyebrow"><Sparkles size={14}/> YOUR FIRST DRAFT IS READY</div><h2>Take a look at your trip.</h2><p>Review the plan below. Approve it, or tell the AI what you’d like changed.</p></div><span className="review-status"><Clock3 size={14}/> Awaiting review</span></div>
              <div className="trip-meta"><span><MapPin size={15}/>{form.origin} → {form.destination}</span><span><CalendarDays size={15}/>{dateLabel(form.start_date)} – {dateLabel(form.end_date)}</span><span><Wallet size={15}/>₹{Number(form.budget).toLocaleString("en-IN")} budget</span></div>
              {approval.evaluation_feedback && <div className="feedback-banner"><ShieldCheck size={18}/><div><b>Planner's quality check</b><p>{approval.evaluation_feedback}</p></div></div>}
              <article className="markdown-content">{renderMarkdown(itinerary)}</article>
              <div className="decision-panel"><div className="decision-heading"><span className="decision-icon"><Compass size={20}/></span><div><h3>How does it look?</h3><p>Not quite right? Give the planner clear feedback.</p></div></div>
                <label className="field feedback-field"><span>CHANGE REQUEST (OPTIONAL IF APPROVING)</span><textarea rows="3" maxLength="2000" value={feedback} onChange={e => setFeedback(e.target.value)} placeholder="e.g. Reduce accommodation costs, add more nature activities, avoid early morning travel…"/></label>
                <div className="decision-actions"><button className="secondary-button" disabled={busy || !feedback.trim()} onClick={() => submitDecision(false)}><RefreshCw size={17}/> Request changes</button><button className="approve-button" disabled={busy} onClick={() => submitDecision(true)}>{busy ? <LoaderCircle className="spin" size={17}/> : <CheckCircle2 size={17}/>} Approve itinerary</button></div>
                <p className="form-note"><ShieldCheck size={14}/> Approval confirms your plan in this app; it does not book or pay for anything.</p>
              </div>
            </div>}
            {completed && <div className="complete-card"><div className="complete-icon"><CheckCircle2 size={32}/></div><div className="eyebrow">TRIP STATUS UPDATED</div><h2>{finalData?.approved ? "Your itinerary is approved!" : "This planning run has ended."}</h2><p>{finalData?.approved ? "Your plan is ready. Remember to verify travel times, prices and availability before booking." : "The workflow finished without an active approval request."}</p>{itinerary && <article className="markdown-content">{renderMarkdown(itinerary)}</article>}<button className="submit-button new-trip-button" onClick={newTrip}>Plan another trip <ArrowRight size={18}/></button></div>}
            {status === "completed" && !approval && !finalData?.approved && !finalData?.itinerary && <div className="error-box"><CircleAlert size={18}/> Workflow ended without an itinerary approval. Check the API response.</div>}
          </section>
        )}

        <section className="how-section" id="how-it-works"><div className="eyebrow">SIMPLE BY DESIGN</div><h2>From “what if” to “let’s go”.</h2><div className="how-grid"><div className="how-card"><span>01</span><Compass size={23}/><h3>Tell us the basics</h3><p>Destination, dates, budget and the things you love.</p></div><div className="how-card"><span>02</span><Sparkles size={23}/><h3>Let AI do the legwork</h3><p>Specialized researchers find options and build your itinerary.</p></div><div className="how-card"><span>03</span><CheckCircle2 size={23}/><h3>Review and refine</h3><p>You stay in control. Approve the plan or ask for changes.</p></div></div></section>
      </main>
      <footer><a className="brand footer-brand" href="#"><span className="brand-mark"><Compass size={19}/></span><span>roamwise<span className="brand-dot">.</span></span></a><span>Made for the journey, powered by AI.</span><a href="#planner" className="back-top">Back to top <ArrowLeft size={14}/></a></footer>
    </div>
  );
}

function renderMarkdown(text) {
  if (!text) return <p>No itinerary content was returned by the API.</p>;
  const lines = text.replace(/\r/g, "").split("\n");
  const nodes = [];
  let list = [];
  let listType = "";
  const flushList = () => {
    if (list.length) {
      const Tag = listType === "ol" ? "ol" : "ul";
      nodes.push(<Tag key={`list-${nodes.length}`}>{list.map((item, i) => <li key={i}>{inlineFormat(item)}</li>)}</Tag>);
      list = []; listType = "";
    }
  };
  lines.forEach((line, i) => {
    const trimmed = line.trim();
    if (!trimmed || /^---+$/.test(trimmed) || /^\|/.test(trimmed)) { flushList(); return; }
    const heading = trimmed.match(/^(#{1,4})\s+(.*)$/);
    if (heading) {
      flushList();
      const level = Math.min(heading[1].length, 4);
      const Tag = `h${level}`;
      nodes.push(<Tag key={i}>{inlineFormat(heading[2])}</Tag>);
    } else if (/^[-*]\s+/.test(trimmed)) {
      if (listType && listType !== "ul") flushList();
      listType = "ul"; list.push(trimmed.replace(/^[-*]\s+/, ""));
    } else if (/^\d+\.\s+/.test(trimmed)) {
      if (listType && listType !== "ol") flushList();
      listType = "ol"; list.push(trimmed.replace(/^\d+\.\s+/, ""));
    } else {
      flushList();
      nodes.push(<p key={i}>{inlineFormat(trimmed)}</p>);
    }
  });
  flushList();
  return nodes;
}
function inlineFormat(text) {
  const parts = text.split(/(\*\*.*?\*\*|\*.*?\*|`.*?`)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) return <strong key={i}>{part.slice(2, -2)}</strong>;
    if (part.startsWith("*") && part.endsWith("*")) return <em key={i}>{part.slice(1, -1)}</em>;
    if (part.startsWith("`") && part.endsWith("`")) return <code key={i}>{part.slice(1, -1)}</code>;
    return part;
  });
}
