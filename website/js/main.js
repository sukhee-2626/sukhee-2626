const $=s=>document.querySelector(s);
const P=[
["plot-docs","plot-docs","Local-first AI office suite for Docs, Sheets, Slides, PDF, Markdown and HTML on Windows, macOS and Linux.","Electron · TypeScript"],
["Thinai","Thinai","Privacy-focused Android app running small language models on-device with a local API.","Dart · On-device AI"],
["MediNexus-AI-Updated","MediNexus AI","Healthcare platform: patient records, appointments, consent management, AI insights and patient portals.","React · TypeScript · Supabase · Gemini"],
["carelens-hospital-agent","CareLens","Hospital AI assistant for document extraction, health timelines, search, FAQ retrieval, appointments and audit trails.","React · TypeScript · Azure AI"],
["CodeGuardAI","CodeGuard","Browser-based GitHub security scanner with vulnerability analysis, security scoring, auto-fixes and Markdown reports.","React · GitHub REST API"],
["CAMPUS-NAV","Campus Navigator","Interactive college map and field-survey app with GPS detection, searchable destinations and saved pins.","React · Express · MySQL/TiDB"],
["SSOFFICE","SSOFFICE","Full-stack office suite: docs, sheets, slides, forms, mail, calendar, drive, tasks, automation and AI.","React · TypeScript · Supabase"],
["VastuAi","VastuAI","Floor-plan analyzer combining Gemini Vision with a custom rule engine, scoring and improvement tips.","React · Flask · Gemini Vision"],
["Place1-Ai","Place1-Ai","AI career copilot with polished frontend, backend API, authentication and database integration.","Next.js · Tailwind · Supabase"],
["prd-craftsman-10","PRD Craftsman","AI product-requirements prompt generator with structured templates.","TypeScript · Generative AI"]];
$("#proj").innerHTML=P.map((p,i)=>`<a class="card" target="_blank" rel="noopener" href="https://github.com/sukhee-2626/${p[0]}"><span class="num">${String(i+1).padStart(2,"0")}</span><h3>${p[1]}</h3><p>${p[2]}</p><span class="tag">${p[3]}</span></a>`).join("");
const H=[
["🥉 Featastiv AI","3rd Prize, Ideathon ThinkTank 2026. AI healthcare scheduling and live queue management.","https://lnkd.in/g5aypTxY"],
["⛓️ MediChain Spark","GDG TechSprint Hackathon 2025. Blockchain medical records with immutable transparency.","https://lnkd.in/gvartgug"],
["🎓 Certificate Portal","Official GDG TechSprint portal with Credential ID and QR verification, instant PDFs.","https://lnkd.in/gqbSV8Ay"],
["📝 AI PRD Generator","Turns raw ideas into structured 11-section PRDs in seconds. Built with Lovable.","https://lnkd.in/gT4379-b"]];
$("#hack").innerHTML=H.map(h=>`<a class="card" target="_blank" rel="noopener" href="${h[2]}"><h3>${h[0]}</h3><p>${h[1]}</p><span class="tag">View →</span></a>`).join("");
const card=(h,p,t)=>`<div class="card"><h3>${h}</h3><p>${p}</p>${t?`<span class="tag">${t}</span>`:""}</div>`;
$("#exp").innerHTML=[
["Orchestration Engineer","Plot XYz.Ai. Building AI-powered products.","Current"],
["Data Analyst Intern","Oasis Infobyte · Virtual. Data-focused internship with exposure to IT infrastructure and support services.","Aug 2026 – Present"],
["Campus Ambassador, E-Cell","IIT Bombay. Supported campus outreach and entrepreneurship initiatives.","Jun 2026 – Present"],
["Media & Creative Team Head","GDG on Campus. Led media and creative activities, event promotion and technical community engagement.","Jun 2025 – Present"],
["Language Intern","GLA University, Mathura. Completed an on-site language internship.","Jun 2026"],
["Desktop Support Technician","Smart Stream Technologies · Part-time. Technical support with exposure to desktop support and data engineering.","Apr – May 2026"]
].map(e=>card(...e)).join("");
$("#edu").innerHTML=[
["B.Sc. Computer Science","Sri Krishna Arts and Science College (SKASC). 1st year, pursuing.","2025 – 2028"],
["12th · Commerce + Computer Science","Higher secondary education.","71.6%"],
["10th","Secondary education.","62%"]
].map(e=>card(...e)).join("");
const S={"Programming":"Python,C++,JavaScript,TypeScript,DSA","AI & Data":"Generative AI,Prompt Engineering,Google Gemini,Azure AI,Data Engineering","Web":"React,Vite,Tailwind CSS,WordPress,Docker","Cloud":"Google Cloud,Supabase,PostgreSQL,MySQL/TiDB,REST APIs","Security":"Cybersecurity,Cisco Networking,Technical Support","Tools":"GitHub,VS Code,Google Workspace,Canva"};
$("#stack").innerHTML=Object.entries(S).map(([k,v])=>`<div class="card"><h3>${k}</h3><div class="chips" style="margin-top:12px">${v.split(",").map((s,i)=>`<span class="chip" style="animation-delay:${i*.2}s">${s}</span>`).join("")}</div></div>`).join("");
$("#cert").innerHTML=[
["Anthropic","AI Fluency Framework & Foundations","Jun 2026"],
["Google","Gen AI Apps with Gemini & Streamlit · Google Cloud Network, Data & Compute · Vertex AI Prompt Design · Generative AI · Speech & Language APIs","Oct 2025"],
["GDG","SKASC Tech Sprint","Jan 2026"],
["Great Learning","WordPress with Docker",""],
["Cisco","Introduction to Cybersecurity","Oct 2024"],
["HackerRank","Python (Basic)","Oct 2024"]
].map(e=>card(...e)).join("");

// typing
const L=["Orchestration Engineer @ Plot XYz.Ai","Building AI-Powered Products","Data Analyst Intern @ Oasis Infobyte","Campus Ambassador, E-Cell IIT Bombay","Media & Creative Head, GDG on Campus","Generative AI · Cloud · Cybersecurity"];
let li=0,ci=0,del=false;const T=$("#type");
(function tick(){const w=L[li];ci+=del?-1:1;T.textContent=w.slice(0,ci);let d=del?35:70;
if(!del&&ci===w.length){del=true;d=1300}else if(del&&ci===0){del=false;li=(li+1)%L.length;d=300}setTimeout(tick,d)})();

// reveal
const io=new IntersectionObserver(e=>e.forEach(x=>x.isIntersecting&&x.target.classList.add("in")),{threshold:.1});
document.querySelectorAll(".reveal").forEach(e=>io.observe(e));

// mouse state
const M={x:innerWidth/2,y:innerHeight/2,nx:0,ny:0};
addEventListener("pointermove",e=>{M.x=e.clientX;M.y=e.clientY;M.nx=e.clientX/innerWidth-.5;M.ny=e.clientY/innerHeight-.5;
const g=$("#glow");g.style.left=e.clientX+"px";g.style.top=e.clientY+"px";
$("#name").style.transform=`rotateY(${M.nx*18}deg) rotateX(${-M.ny*14}deg)`});

// 3D card tilt
document.querySelectorAll(".card").forEach(c=>{
c.addEventListener("pointermove",e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;
c.style.setProperty("--mx",x*100+"%");c.style.setProperty("--my",y*100+"%");
c.style.transform=`rotateY(${(x-.5)*18}deg) rotateX(${(.5-y)*18}deg) translateZ(14px)`});
c.addEventListener("pointerleave",()=>c.style.transform="")});

// 3D point-sphere canvas
const cv=$("#bg"),cx=cv.getContext("2d");let W,Hh,DPR=Math.min(devicePixelRatio||1,2);
function rs(){W=innerWidth;Hh=innerHeight;cv.width=W*DPR;cv.height=Hh*DPR;cx.setTransform(DPR,0,0,DPR,0,0)}rs();addEventListener("resize",rs);
const N=matchMedia("(max-width:700px)").matches?220:420,pts=[];
for(let i=0;i<N;i++){const y=1-2*(i+.5)/N,r=Math.sqrt(1-y*y),t=i*2.399963;pts.push([Math.cos(t)*r,y,Math.sin(t)*r])}
const dust=Array.from({length:70},()=>[Math.random()*2-1,Math.random()*2-1,Math.random()*2-1]);
let ax=0,ay=0,vx=0,vy=0;
function draw(){
cx.clearRect(0,0,W,Hh);
vy+=(M.nx*.04-vy)*.05;vx+=(M.ny*.04-vx)*.05;ay+=.004+vy;ax+=vx*.5;
const R=Math.min(W,Hh)*.34*(innerWidth<700?1.1:1),cxp=W*(innerWidth<700?.5:.72),cyp=Hh*.5;
const cs=Math.cos(ay),sn=Math.sin(ay),cX=Math.cos(ax),sX=Math.sin(ax);
const pr=[];
for(const p of pts){let x=p[0]*cs-p[2]*sn,z=p[0]*sn+p[2]*cs,y=p[1]*cX-z*sX;z=p[1]*sX+z*cX;
const s=1/(1.9-z*.6);pr.push([cxp+x*R*s*1.6,cyp+y*R*s*1.6,z,s])}
cx.lineWidth=.6;
for(let i=0;i<pr.length;i++){const a=pr[i];
for(let j=i+1;j<pr.length;j+=3){const b=pr[j],dx=a[0]-b[0],dy=a[1]-b[1],d=dx*dx+dy*dy;
if(d<1500&&a[2]>-.2){cx.strokeStyle=`rgba(0,201,167,${(1-d/1500)*.35})`;cx.beginPath();cx.moveTo(a[0],a[1]);cx.lineTo(b[0],b[1]);cx.stroke()}}}
for(const p of pr){const dx=p[0]-M.x,dy=p[1]-M.y,d=Math.hypot(dx,dy),near=Math.max(0,1-d/160);
const al=(p[2]+1.2)/2.4;cx.fillStyle=near>0?`rgba(255,255,255,${.6+near*.4})`:(p[2]>0?`rgba(0,201,167,${al})`:`rgba(124,58,237,${al})`);
cx.beginPath();cx.arc(p[0]-dx*near*.08,p[1]-dy*near*.08,(1.1+p[2]*.8+near*2.5)*p[3]*1.4,0,6.283);cx.fill()}
for(const d of dust){d[1]-=.0007;if(d[1]<-1)d[1]=1;
const px=W/2+(d[0]*W/2)+M.nx*-40*(d[2]+1.5),py=Hh/2+d[1]*Hh/2+M.ny*-40*(d[2]+1.5);
cx.fillStyle="rgba(180,200,255,.35)";cx.fillRect(px,py,1.4+d[2],1.4+d[2])}
requestAnimationFrame(draw)}
draw();
