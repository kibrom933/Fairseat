"""Builds the static Fairseat site. Run: python3 build.py  (no dependencies)
Edit page bodies in PAGES below; header, footer and <head> are shared."""
import datetime, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://fairseat.netlify.app"
NAV = [("calculator.html", "Seat receipt"), ("vendor-check.html", "Vendor check"), ("ai-act.html", "AI Act"), ("method.html", "Method"), ("about.html", "About")]
UPDATED = "11 November 2026"


def page(slug, title, desc, body, script=""):
    nav = "".join(f'<a href="/{h}"{" aria-current=page" if h == slug else ""}>{t}</a>' for h, t in NAV)
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{'' if slug == 'index.html' else slug}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="preload" href="/fonts/serif.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css"></head><body>
<header><div class="wrap"><nav><a class="logo" href="/">Fair<i>seat</i></a>{nav}</nav></div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap"><span>Fairseat is run independently from Denmark. No cookies, no tracking, no ads.</span>
<span><a href="/about.html#money">How we make money</a> · <a href="/method.html">How we review</a></span></div></footer>
{script}</body></html>
"""
    (ROOT / slug).write_text(html, encoding="utf-8")


INDEX = """
<section class="hero">
<div>
<p class="eyebrow">AI tools for freelancers and small teams in Europe</p>
<h1>Does that AI tool <em>earn its seat?</em></h1>
<p class="lede">Most AI subscriptions are sold per seat, per month, with the real price three clicks away and the privacy terms further still. Fairseat gives you the receipt: what it costs a year, how many seats sit idle, and where your data goes.</p>
<p class="bar"><a class="btn" href="/calculator.html">Print your seat receipt</a> <a class="btn ghost" href="/vendor-check.html">Check a vendor</a></p>
</div>
<div class="receipt" aria-label="Example receipt">
<h4>Seat receipt</h4><div class="sub">example · 5-person studio</div>
<div class="r"><span>Meeting notes × 5</span><span>€ 1,080</span></div>
<div class="r"><span>Writing assistant × 5</span><span>€ 1,200</span></div>
<div class="r"><span>Image tool × 2</span><span>€ 720</span></div>
<div class="r t"><span>Per year</span><span>€ 3,000</span></div>
<div class="r w"><span>Idle seats (4 of 12)</span><span>€ 912</span></div>
<div class="r s"><span>If billed annually</span><span>− € 504</span></div>
</div>
</section>

<div class="cols">
<a href="/calculator.html"><span class="num">01</span><h3>Seat receipt</h3><p>Enter what you pay. See the yearly total, the cost of seats nobody uses, and what annual billing would save. Runs in your browser; nothing is sent.</p></a>
<a href="/vendor-check.html"><span class="num">02</span><h3>Vendor check</h3><p>Twelve questions to ask before you put client data into an AI tool. Ends with a ready-to-send email asking the vendor for whatever you could not find.</p></a>
<a href="/ai-act.html"><span class="num">03</span><h3>The AI Act, for small teams</h3><p>What applies to a business that only <i>uses</i> AI tools, with the dates as they stand after the 2026 Digital Omnibus.</p></a>
</div>

<h2>What we will not do</h2>
<div class="narrow">
<ul class="plain">
<li><b>Review a tool we have not paid for and used.</b> There are no reviews on this site yet for exactly that reason. When the first ones come, they will show the invoice date and the plan we tested.</li>
<li><b>Fill a gap with a guess.</b> When a vendor does not say where data is processed or how long it is kept, the review says <i>not stated</i>.</li>
<li><b>Hide the commission.</b> Links that pay us will be labelled as ads, next to the link, every time. <a href="/about.html#money">Details</a>.</li>
<li><b>Rank by payout.</b> The scoring method is published before the first score is. <a href="/method.html">Read it</a>.</li>
</ul>
</div>
"""

CALC = """
<p class="eyebrow">Tool 01</p>
<h1>Seat <em>receipt</em></h1>
<p class="lede">Add the AI tools you pay for. You get the yearly total, the cost of idle seats, and the saving from annual billing. Your numbers stay in this browser.</p>
<div class="calc">
<div>
<div class="bar noprint"><div style="width:120px"><label for="cur">Currency</label><select id="cur"><option>€</option><option>kr</option><option>$</option><option>£</option></select></div></div>
<div id="rows"></div>
<div class="bar noprint"><button id="add">Add a tool</button><button class="ghost" id="csv">Download CSV</button><button class="ghost" onclick="print()">Print</button><button class="ghost" id="clear">Clear</button></div>
<p class="src">Monthly price is the per-seat price on monthly billing. Annual-plan price is the per-seat, per-month price when billed yearly; leave it empty if you do not know it. "Used" is how many seats were actually used in the last 30 days: most admin consoles show it.</p>
</div>
<div class="receipt" id="rc" aria-live="polite"></div>
</div>
<h2>Reading the receipt</h2>
<div class="narrow">
<p><b>Idle seats</b> are licences bought for someone who tried the tool twice and stopped. If the idle line is more than a fifth of the total, drop seats before you negotiate price.</p>
<p><b>Annual billing</b> usually lowers the per-seat price, but it removes your ability to drop seats mid-year. Take the saving only for tools where the used-seat count has been stable for three months.</p>
<p><b>What the receipt cannot see:</b> usage-based charges (credits, tokens, minutes), VAT, and price changes at renewal. Check the invoice, not the pricing page.</p>
</div>
"""

CALC_JS = r"""<script>
const R=document.getElementById('rows'),K='fairseat.rows.v1';let cur='€';
const F=['name','month','annual','seats','used'],L=['Tool','Monthly / seat','Annual plan / seat / mo','Seats','Used'];
function row(d={}){const e=document.createElement('div');e.className='row';
 F.forEach((f,i)=>{const w=document.createElement('div'),id='f'+Math.random().toString(36).slice(2);
  w.innerHTML=`<label for="${id}">${L[i]}</label>`;const inp=document.createElement('input');inp.id=id;inp.dataset.f=f;
  if(i){inp.type='number';inp.min=0;inp.step=i<3?'0.01':'1';inp.inputMode='decimal'}inp.value=d[f]??'';w.appendChild(inp);e.appendChild(w)});
 const x=document.createElement('button');x.className='x noprint';x.textContent='Remove';x.onclick=()=>{e.remove();calc()};e.appendChild(x);R.appendChild(e)}
function data(){return [...R.children].map(e=>{const o={};e.querySelectorAll('input').forEach(i=>o[i.dataset.f]=i.dataset.f=='name'?i.value:(i.value===''?null:+i.value));return o})}
const fm=n=>cur+' '+Math.round(n).toLocaleString('en');
function calc(){const d=data();let y=0,idle=0,save=0,ts=0,ti=0,html='<h4>Seat receipt</h4><div class="sub">'+new Date().toISOString().slice(0,10)+'</div>';
 const rr=(a,b,c='')=>`<div class="r ${c}"><span></span><span></span></div>`;const el=document.getElementById('rc');el.innerHTML=html;
 const add=(a,b,c='')=>{const r=document.createElement('div');r.className='r '+c;const s1=document.createElement('span'),s2=document.createElement('span');s1.textContent=a;s2.textContent=b;r.append(s1,s2);el.appendChild(r)};
 d.forEach(o=>{const s=o.seats||0,m=o.month||0,u=o.used==null?s:Math.min(o.used,s);if(!s||!m)return;const yr=m*s*12;y+=yr;idle+=m*(s-u)*12;ts+=s;ti+=s-u;
  if(o.annual&&o.annual<m)save+=(m-o.annual)*s*12;add((o.name||'Unnamed')+' × '+s,fm(yr))});
 if(!y){add('Add a tool to start','');return}
 add('Per year',fm(y),'t');add('Per month',fm(y/12));add('Per seat, per year',fm(y/ts));
 if(ti)add(`Idle seats (${ti} of ${ts})`,fm(idle),'w');if(save)add('If billed annually','− '+fm(save),'s');
 try{localStorage.setItem(K,JSON.stringify({cur,d}))}catch(e){}}
R.addEventListener('input',calc);document.getElementById('add').onclick=()=>{row();calc()};
document.getElementById('cur').onchange=e=>{cur=e.target.value;calc()};
document.getElementById('clear').onclick=()=>{R.innerHTML='';row();calc()};
document.getElementById('csv').onclick=()=>{const q=s=>'"'+String(s??'').replace(/"/g,'""')+'"';const t=[F.join(',')].concat(data().map(o=>F.map(f=>q(o[f])).join(','))).join('\n');
 const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/csv'}));a.download='seat-receipt.csv';a.click()};
let saved=null;try{saved=JSON.parse(localStorage.getItem(K))}catch(e){}
if(saved&&saved.d&&saved.d.length){cur=saved.cur||'€';document.getElementById('cur').value=cur;saved.d.forEach(row)}
else{[{name:'Example: meeting notes',month:18,annual:15,seats:5,used:3},{name:'Example: writing assistant',month:20,annual:17,seats:5,used:5}].forEach(row)}
calc();
</script>"""

QS = [
    ("loc", "Where is the data processed and stored?", "Look for a named region (for example EU, Germany, US). 'Global infrastructure' is not an answer.", "In which countries or regions is customer data processed and stored, and can we choose an EU region on our plan?"),
    ("train", "Is your data used to train models?", "Check the default, not the opt-out. Check whether it differs between free, team and enterprise plans.", "Is customer content (inputs, outputs, uploads) used to train or improve any model, by you or by a sub-processor, on our plan by default?"),
    ("keep", "How long is data kept?", "A number of days for content, and a separate answer for logs and backups.", "What are the retention periods for customer content, logs and backups, and can we configure them?"),
    ("dpa", "Is there a data processing agreement?", "For GDPR you need a DPA (Art. 28) if the tool processes personal data for you. Self-serve signing is a good sign.", "Do you offer a data processing agreement under GDPR Art. 28 on our plan, and how do we sign it?"),
    ("sub", "Are sub-processors listed?", "A public list with names, purposes and locations, including which AI model providers are used.", "Please share your current list of sub-processors, including model providers, with their purpose and location."),
    ("xfer", "How are transfers outside the EU covered?", "Typically the EU-US Data Privacy Framework or Standard Contractual Clauses. It should be named.", "Which transfer mechanism covers any processing outside the EEA (Data Privacy Framework certification, SCCs, other)?"),
    ("del", "Can you delete your data, and is it confirmed?", "Self-serve deletion of single items and of the whole account, with a stated time until backups are purged.", "How do we delete individual items and the whole workspace, and how long until deletion reaches backups?"),
    ("exp", "Can you export your data?", "A standard format (CSV, JSON, Markdown, audio files) without contacting sales.", "In which formats can we export all our data, and is export available on our plan?"),
    ("sec", "Is there independent security evidence?", "SOC 2 Type II or ISO 27001 report, available at least under NDA. A badge without a report is a claim.", "Can you share a current SOC 2 Type II or ISO 27001 certificate/report?"),
    ("acc", "Can you control who has access?", "SSO or at least enforced two-factor, roles, and a way to remove a leaver in one place.", "Does our plan include SSO or enforced 2FA, role-based access and central user removal?"),
    ("price", "Is the full price public?", "Per-seat price, minimum seats, and any usage caps or credits stated on the pricing page.", "What are the minimum seat count, usage limits and overage charges on our plan?"),
    ("out", "Can you leave without penalty?", "Monthly cancellation or a clear annual term; seats can be reduced; no auto-upgrade.", "What are the cancellation terms, and can we reduce seats during the term?"),
]

VC = """
<p class="eyebrow">Tool 02</p>
<h1>Vendor <em>check</em></h1>
<p class="lede">Twelve things to find out before client or staff data goes into an AI tool. Answer from the vendor's own pages: pricing, privacy policy, DPA, trust centre. Nothing you enter leaves this page.</p>
<div class="narrow">
<div style="margin:24px 0"><label for="vn">Vendor or tool name</label><input id="vn" placeholder="Name of the tool" autocomplete="off"></div>
<div id="qs">""" + "".join(
    f'<div class="q" data-k="{k}"><b>{i + 1}. {t}</b><p>{h}</p><span class="seg" role="radiogroup" aria-label="{t}">'
    + "".join(f'<label><input type="radio" name="{k}" value="{v}"><span>{l}</span></label>' for v, l in (("y", "Stated, fine"), ("p", "Stated, not fine"), ("n", "Not stated")))
    + "</span></div>" for i, (k, t, h, _) in enumerate(QS)) + """</div>
<h2>Result</h2>
<p><span class="score" id="sc">0</span> <span class="eyebrow">of 12 answered and fine</span></p>
<p id="verdict" class="note">Answer the questions to see what is missing.</p>
<h3>Email to the vendor</h3>
<p class="src">Built from everything you marked <i>not stated</i> or <i>not fine</i>. Copy it into your own mail; Fairseat sends nothing.</p>
<textarea id="mail" rows="14" readonly></textarea>
<div class="bar"><button id="copy">Copy email</button><button class="ghost" onclick="print()">Print checklist</button></div>
<p class="src">General information, not legal advice. Whether you need a DPA or a transfer mechanism depends on whether personal data is involved.</p>
</div>
"""

VC_JS = "<script>const Q=" + repr({k: q for k, _, _, q in QS}).replace("'", '"') + r""";
const st={};function upd(){let ok=0,miss=[],bad=[];for(const k in Q){if(st[k]=='y')ok++;else if(st[k]=='n')miss.push(k);else if(st[k]=='p')bad.push(k)}
 const n=Object.keys(st).length;document.getElementById('sc').textContent=ok;const v=document.getElementById('verdict');
 v.textContent=n<12?`${12-n} question${12-n==1?'':'s'} left.`:miss.length+bad.length==0?'Everything is stated and acceptable. Keep the pages you checked as evidence, with today\'s date.':
  (st.train!='y'||st.dpa!='y'||st.loc!='y')?'Do not put personal or client data in yet: location, training use or the DPA is unresolved. Send the email below first.':
  'The essentials are covered. Ask for the remaining points before you commit to an annual plan.';
 const name=document.getElementById('vn').value.trim()||'[tool]';const ask=miss.concat(bad);
 document.getElementById('mail').value=ask.length?`Subject: Questions before we adopt ${name}\n\nHello,\n\nWe are a small team evaluating ${name}. Before we can use it with client data, we need written answers to the following:\n\n`+ask.map((k,i)=>`${i+1}. ${Q[k]}`).join('\n')+`\n\nA link to the relevant documentation is enough where it exists.\n\nThank you,\n[your name]`:'';}
document.getElementById('qs').addEventListener('change',e=>{st[e.target.name]=e.target.value;upd()});document.getElementById('vn').addEventListener('input',upd);
document.getElementById('copy').onclick=async e=>{try{await navigator.clipboard.writeText(document.getElementById('mail').value);e.target.textContent='Copied'}catch(x){document.getElementById('mail').select()}};
</script>"""

ACT = f"""
<p class="eyebrow">Guide · checked {UPDATED}</p>
<h1>The EU AI Act, if you only <em>use</em> AI tools</h1>
<div class="narrow">
<p class="lede">You run a small business. You did not build an AI system; you subscribe to a few. This is what the Act asks of you, with the dates as they stand after the Digital Omnibus on AI was published in the Official Journal on 24 July 2026.</p>
<div class="note">General information, not legal advice. We link the sources at the bottom; where they disagree or are unclear, we say so.</div>

<h2>You are a "deployer"</h2>
<p>The Act calls a business that uses an AI system under its own authority a <i>deployer</i>. The company that makes the tool is the <i>provider</i> and carries most of the obligations. Personal, non-professional use is outside the Act.</p>

<h2>The dates</h2>
<table>
<tr><th>From</th><th>What</th><th>Does it touch a small deployer?</th></tr>
<tr><td class="d">2 Feb 2025</td><td>Prohibited practices (Art. 5) and AI literacy (Art. 4)</td><td>Yes. See below.</td></tr>
<tr><td class="d">2 Aug 2025</td><td>Rules for general-purpose AI model providers</td><td>No. This is for model makers.</td></tr>
<tr><td class="d">2 Aug 2026</td><td>Transparency duties (Art. 50) in general</td><td>Yes, if you publish realistic AI-made media or run a chatbot.</td></tr>
<tr><td class="d">2 Dec 2026</td><td>Machine-readable marking of AI output (Art. 50(2)) for systems already on the market; new ban on AI that generates non-consensual intimate imagery or child sexual abuse material</td><td>Mostly a provider duty. The ban applies to everyone.</td></tr>
<tr><td class="d">2 Dec 2027</td><td>High-risk systems listed in Annex III (was 2 Aug 2026)</td><td>Only if you use AI for things like hiring, credit or access to education.</td></tr>
<tr><td class="d">2 Aug 2028</td><td>High-risk AI inside regulated products, Annex I (was 2 Aug 2027)</td><td>Rarely.</td></tr>
</table>

<h2>What you need to do now</h2>
<h3>1. Help your people understand the tools</h3>
<p>Article 4 has applied since February 2025. The Omnibus softened it: you must take measures to <i>support the development of</i> AI literacy among the people using AI for you, and the text now says this does not mean guaranteeing a particular level for any individual. For a five-person team, a written one-page note is a reasonable measure: which tools are approved, what must never be pasted into them, and that output is checked by a human before it goes to a client.</p>
<h3>2. Stay away from the banned uses</h3>
<p>The ones a small business could stumble into: inferring employees' emotions at work, and manipulative or exploitative techniques that cause harm. From 2 December 2026, tools that produce non-consensual intimate imagery are banned as well.</p>
<h3>3. Label what needs a label</h3>
<p>Since 2 August 2026, if you publish image, audio or video that is AI-generated or manipulated and could pass for real (a "deep fake"), you must disclose that it is artificial. Text published to inform the public on matters of public interest needs the same disclosure unless a human has reviewed it and someone holds editorial responsibility. If customers talk to a chatbot on your site, they must be told it is an AI unless that is obvious; making that possible is the provider's job, switching it on is yours. The Commission published guidelines on these duties on 20 July 2026.</p>
<h3>4. Check whether anything you do is "high-risk"</h3>
<p>Screening job applicants, evaluating employees, deciding on credit, or grading students with AI falls under Annex III. Those rules now start on 2 December 2027. If that is you, the duties are real (human oversight, following the provider's instructions, keeping logs, informing the people affected) and you should take advice well before then.</p>

<h2>GDPR is still the bigger job</h2>
<p>None of this replaces data protection law. For an ordinary meeting-notes or writing tool, the questions that matter day to day are where data is processed, whether it trains a model, how long it is kept, and whether you have a data processing agreement. The <a href="/vendor-check.html">vendor check</a> walks through them.</p>

<h2>A one-page policy you can adapt</h2>
<ul class="plain">
<li>We use these AI tools for work: [list]. Other tools need a yes from [name] first.</li>
<li>We do not paste client personal data, passwords or contracts into a tool that is not on the list.</li>
<li>A person reads and takes responsibility for anything an AI tool wrote before it leaves the company.</li>
<li>Realistic AI-made images, audio or video are labelled as AI-generated when published.</li>
<li>We do not use AI to assess job applicants or staff.</li>
<li>Reviewed every six months by [name]. Last review: [date].</li>
</ul>

<h2>Sources</h2>
<ul class="src">
<li><a href="https://fpf.org/blog/the-ai-act-implementation-timeline-what-changes-under-the-ai-omnibus">Future of Privacy Forum: The AI Act implementation timeline under the AI Omnibus</a> (updated 5 Aug 2026): adoption and publication dates, new high-risk dates, amended Article 4 wording.</li>
<li><a href="https://www.gibsondunn.com/eu-ai-act-omnibus-agreement">Gibson Dunn: EU AI Act Omnibus agreement</a> (27 May 2026): Article 50 unaffected apart from the 50(2) grace period; new prohibition.</li>
<li><a href="https://eur-lex.europa.eu/eli/reg/2024/1689/oj">Regulation (EU) 2024/1689 on EUR-Lex</a>: the Act itself; Articles 3, 4, 5, 26 and 50.</li>
</ul>
<p class="src">The two secondary sources describe the scope of the Article 50(2) postponement slightly differently. We follow the reading that it covers systems placed on the market before 2 August 2026.</p>
</div>
"""

METHOD = """
<p class="eyebrow">Method</p>
<h1>How a tool <em>earns</em> a score</h1>
<div class="narrow">
<p class="lede">Published before the first review, so the method cannot be bent to fit a verdict.</p>
<h2>Before we write</h2>
<ul class="plain">
<li>We buy the plan a small team would buy, with our own money, and use it for real work for at least two weeks.</li>
<li>Every review states the plan, the price paid, the invoice month and the version tested.</li>
<li>Vendors do not see a review before it is published and cannot pay for placement.</li>
</ul>
<h2>The score, out of 100</h2>
<table>
<tr><th>Part</th><th>Points</th><th>What we look at</th></tr>
<tr><td>Does the job</td><td class="d">35</td><td>The same fixed tasks for every tool in a category, with the outputs shown.</td></tr>
<tr><td>Real cost</td><td class="d">20</td><td>Yearly cost for 1, 5 and 15 seats, including minimums, caps and overage.</td></tr>
<tr><td>Data and privacy</td><td class="d">25</td><td>The twelve points in the <a href="/vendor-check.html">vendor check</a>. "Not stated" scores zero for that point.</td></tr>
<tr><td>Leaving</td><td class="d">10</td><td>Export formats, cancellation, reducing seats.</td></tr>
<tr><td>Running it</td><td class="d">10</td><td>Setup time, admin controls, support response to one real question.</td></tr>
</table>
<h2>After we publish</h2>
<ul class="plain">
<li>Each review carries a "last checked" date. Prices and privacy terms are re-checked at least every six months.</li>
<li>Corrections are listed at the bottom of the page with a date. We do not edit silently.</li>
<li>If a vendor tells us something is wrong and shows evidence, we fix it and note it.</li>
</ul>
<h2>What a score is not</h2>
<p>It is one small team's experience on one plan. It is not a security audit and not legal advice.</p>
</div>
"""

ABOUT = """
<p class="eyebrow">About</p>
<h1>Who is behind <em>Fairseat</em></h1>
<div class="narrow">
<p class="lede">Fairseat is an independent site run from Denmark. It exists because buying AI tools for a small business in Europe means answering questions most review sites skip: what it really costs per year, and what happens to the data.</p>
<h2 id="money">How we make money</h2>
<p>Today: we do not. There are no ads and no affiliate links on the site.</p>
<p>When reviews are published, some links to vendors will be affiliate links. If you buy through one, the vendor may pay us a commission, at no extra cost to you. Each such link will be marked <b>Ad: affiliate link</b> right next to it. A tool can get a poor score and still have an affiliate link; a tool with no affiliate programme can get the top score.</p>
<h2>Privacy</h2>
<p>This site sets no cookies and loads nothing from third parties: no analytics, no fonts from other servers, no embeds. The calculator and the vendor check run in your browser. The calculator remembers your rows in your browser's local storage so they are there next time; use Clear to remove them.</p>
<h2>Corrections</h2>
<p>If something here is wrong or out of date, we want to know. A contact address will be added with the first review.</p>
</div>
"""

page("index.html", "Fairseat · Does that AI tool earn its seat?", "The real yearly cost, idle seats and privacy terms of AI tools, for freelancers and small teams in Europe.", INDEX)
page("calculator.html", "Seat receipt: AI tool cost calculator · Fairseat", "See what your AI subscriptions cost per year, what idle seats cost, and what annual billing saves. Runs in your browser.", CALC, CALC_JS)
page("vendor-check.html", "Vendor check: 12 questions before you buy an AI tool · Fairseat", "A GDPR-minded checklist for AI tools, with a ready-to-send email for whatever the vendor has not stated.", VC, VC_JS)
page("ai-act.html", "The EU AI Act for small teams that use AI tools · Fairseat", "What deployers must do and when, updated for the 2026 Digital Omnibus: AI literacy, labelling, banned uses, high-risk dates.", ACT)
page("method.html", "How we review · Fairseat", "Fairseat's published scoring method: paid plans, fixed tasks, real yearly cost, twelve privacy points.", METHOD)
page("about.html", "About · Fairseat", "Who runs Fairseat, how it makes money, and what it does with your data (nothing).", ABOUT)
page("404.html", "Not found · Fairseat", "Page not found.", '<h1>That page has no <em>seat</em></h1><p class="lede">It may have moved. <a href="/">Go to the front page</a>.</p>')

(ROOT / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#15171c"/><rect x="5" y="19" width="22" height="7" fill="#ffe14d"/><text x="16" y="18" font-family="Georgia,serif" font-style="italic" font-size="20" text-anchor="middle" fill="#fffefb">f</text></svg>')
today = datetime.date(2026, 11, 11).isoformat()
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"<url><loc>{SITE}/{'' if s == 'index.html' else s}</loc><lastmod>{today}</lastmod></url>\n" for s in ["index.html"] + [h for h, _ in NAV]) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
(ROOT / "netlify.toml").write_text('[build]\n  publish = "."\n\n[[headers]]\n  for = "/fonts/*"\n  [headers.values]\n    Cache-Control = "public, max-age=31536000, immutable"\n\n[[headers]]\n  for = "/*"\n  [headers.values]\n    X-Content-Type-Options = "nosniff"\n    Referrer-Policy = "strict-origin-when-cross-origin"\n    Content-Security-Policy = "default-src \'self\'; script-src \'self\' \'unsafe-inline\'; style-src \'self\'; img-src \'self\' data: blob:; frame-ancestors \'none\'"\n')
print("built")
