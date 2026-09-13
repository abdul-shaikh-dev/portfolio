/* Authored illustration of adaptive extraction, not a live model response. */
(() => {
  const figure = document.querySelector('[data-walkthrough="extraction"]');
  if (!figure) return;
  const host = figure.querySelector('.walkthrough-interactive');
  host.innerHTML = `
    <div class="demo-toolbar"><span>Interactive evidence story</span><div class="extract-controls"><button type="button" class="extract-action">Watch the flow ▶</button><button type="button" class="extract-next">Next step →</button><button type="button" class="extract-reset">Reset</button></div></div>
    <section class="knowledge-prep" aria-labelledby="prep-title">
      <header class="scene-heading"><span>01 / Knowledge preparation</span><div><h4 id="prep-title">Turn source material into searchable evidence.</h4><p>OCR, passages, embeddings, and source metadata stay connected.</p></div></header>
      <div class="prep-flow" role="img" aria-label="A document is read with OCR, divided into passages, embedded, and stored with source metadata in ChromaDB">
        <div class="source-object prep-object" data-ingest="document"><span class="object-label">Source</span><div class="document-stack" aria-hidden="true"><i></i><i></i><b>PDF</b><small>scanned agreement</small></div></div>
        <div class="chunk-object prep-object" data-ingest="chunks"><span class="object-label">Read &amp; divide</span><div class="scan-sheet" aria-hidden="true"><i></i><span></span><span></span><span></span></div><small>OCR + passages</small></div>
        <div class="embedding-object prep-object" data-ingest="embed"><span class="object-label">Represent meaning</span><div class="embedding-cloud" aria-hidden="true">${Array.from({length:18},(_,i)=>`<i style="--i:${i}"></i>`).join('')}</div><small>Embeddings</small></div>
        <div class="vault-object prep-object" data-ingest="store"><span class="object-label">Index</span><div class="mini-vault" aria-hidden="true"><i></i><i></i><i></i></div><strong>ChromaDB</strong><small>passage + page + source</small></div>
        <span class="prep-packet packet-one" aria-hidden="true">p.1</span><span class="prep-packet packet-two" aria-hidden="true">···</span><span class="prep-packet packet-three" aria-hidden="true">[.18]</span>
      </div>
      <p class="ingestion-handoff"><span aria-hidden="true">↓</span> Indexed knowledge is ready for field-level retrieval</p>
    </section>
    <section class="adaptive-workbench" aria-labelledby="workbench-title">
      <header class="scene-heading workbench-heading"><span>02 / Adaptive extraction</span><div><h4 id="workbench-title">Ask only for what is still missing.</h4><p class="pass-readout">Pass 1 · three fields requested</p></div></header>
      <div class="schema-strip"><span class="extract-label">Requested schema</span><div class="query-fields"><span>Agreement ID</span><span>Start date</span><span>Notice period</span></div><span class="query-count">0 of 3 resolved</span></div>
      <div class="extraction-canvas">
        <svg class="flow-map" viewBox="0 0 1200 430" preserveAspectRatio="none" aria-hidden="true"><path class="flow-path path-evidence" d="M250 210 C330 130 365 130 445 190"/><path class="flow-path path-prompt" d="M640 190 C710 130 735 135 790 195"/><path class="flow-path path-result" d="M880 220 C940 175 970 175 1030 210"/><path class="flow-path path-loop" d="M1080 330 C920 420 380 440 205 315 C145 270 145 225 190 205"/></svg>
        <section class="evidence-vault extraction-node" data-node="store" aria-label="ChromaDB evidence library"><button type="button" class="node-jump" data-jump="store" title="Jump to retrieval"><span>Evidence library</span><strong>ChromaDB</strong><small>Similarity search + reranking</small></button><div class="vault-body" aria-hidden="true"><span></span><span></span><span></span></div><div class="passage-stack"><button type="button" data-page="1"><b>01</b><span>Agreement details<small>ID · start date</small></span></button><button type="button" data-page="4"><b>04</b><span>Payment terms<small>invoice · settlement</small></span></button><button type="button" data-page="7"><b>07</b><span>Termination<small>notice · communication</small></span></button></div></section>
        <section class="prompt-studio extraction-node" data-node="prompt" aria-label="Extraction prompt assembly"><button type="button" class="node-jump" data-jump="prompt" title="Jump to prompt assembly"><span>Composition surface</span><strong>Extraction prompt</strong></button><div class="prompt-sheet"><span class="prompt-piece piece-instruction"><i>01</i><b>Instructions</b><small>Use supplied evidence</small></span><span class="prompt-piece piece-schema"><i>02</i><b>Field schema</b><small class="bundle-schema">3 requested fields</small></span><span class="prompt-piece piece-source"><i>03</i><b>Source passages</b><small class="bundle-source">Awaiting retrieval</small></span></div><span class="evidence-slip" aria-hidden="true"><b>p.1</b><i></i><i></i></span></section>
        <section class="model-studio extraction-node" data-node="llm" aria-label="Language model extraction"><button type="button" class="node-jump model-button" data-jump="llm" title="Jump to model extraction"><span>Grounded extraction</span><span class="model-orbit" aria-hidden="true"><i></i><i></i><b>✳</b></span><strong>LLM</strong><small>Evidence in · structured fields out</small></button><span class="prompt-capsule" aria-hidden="true">schema + sources</span></section>
        <section class="result-ledger extraction-node" data-node="output" aria-label="Attributed extraction results"><button type="button" class="node-jump" data-jump="output" title="Jump to attributed results"><span>Attributed output</span><strong>Structured fields</strong><small>Value · source · page · confidence</small></button><dl><div><dt>Agreement ID</dt><dd>Awaiting evidence</dd><dd class="field-context"></dd></div><div><dt>Start date</dt><dd>Awaiting evidence</dd><dd class="field-context"></dd></div><div><dt>Notice period</dt><dd>Awaiting evidence</dd><dd class="field-context"></dd></div></dl><span class="result-packet" aria-hidden="true">value · source · confidence</span></section>
      </div>
      <div class="loop-caption"><span class="feedback-symbol" aria-hidden="true">↶</span><div><strong class="feedback-title">A schema becomes a search.</strong><p class="feedback-copy">Follow the complete extraction, including a second pass for missing evidence.</p></div></div>
    </section><p class="extract-status" role="status"></p>`;

  const get = selector => host.querySelector(selector);
  const action = get('.extract-action');
  const next = get('.extract-next');
  const reset = get('.extract-reset');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const fields = [
    {name:'Agreement ID', value:'DEMO-001', page:'1', confidence:'96%', quote:'“Agreement DEMO-001”'},
    {name:'Start date', value:'01 Jan 2026', page:'1', confidence:'94%', quote:'“begins on 1 January 2026”'},
    {name:'Notice period', value:'30 days', page:'7', confidence:'92%', quote:'“30 days’ written notice”'}
  ];
  const stages = [
    {phase:'ingest-document',pass:1,found:0,title:'A source document enters the knowledge pipeline.',copy:'PDFs, Word files, images, and scanned pages can provide the source material.',duration:1400},
    {phase:'ingest-chunks',pass:1,found:0,title:'OCR turns pages into usable passages.',copy:'Text is recovered, cleaned, and divided while page and source references remain attached.',duration:1700},
    {phase:'ingest-embed',pass:1,found:0,title:'Each passage receives a semantic representation.',copy:'Embeddings make related evidence discoverable beyond exact keyword matches.',duration:1700},
    {phase:'ingest-store',pass:1,found:0,title:'ChromaDB stores searchable evidence.',copy:'Passages, embeddings, pages, and source metadata stay linked.',duration:1700},
    {phase:'ready',pass:1,found:0,title:'A schema becomes a search.',copy:'Three requested fields define the first retrieval pass.',duration:900},
    {phase:'query',pass:1,found:0,title:'Search ChromaDB for the requested fields.',copy:'Field-aware queries retrieve candidate passages for agreement ID, start date, and notice period.',duration:1800},
    {phase:'chunks',pass:1,found:0,title:'Select the strongest supporting evidence.',copy:'Reranking keeps the agreement-details passage and leaves unrelated context behind.',duration:1900},
    {phase:'prompt',pass:1,found:0,title:'Build the prompt from three visible ingredients.',copy:'Instructions, field schema, and attributed source passages are composed together.',duration:2100},
    {phase:'send',pass:1,found:0,title:'Send a compact evidence bundle to the LLM.',copy:'The model receives the selected passages instead of the entire document.',duration:1600},
    {phase:'llm',pass:1,found:0,title:'Extract only from the supplied evidence.',copy:'The model maps supported text into the requested structure.',duration:1500},
    {phase:'return',pass:1,found:1,title:'The first attributed field arrives.',copy:'Agreement ID returns with its source page and supporting words.',duration:900},
    {phase:'return',pass:1,found:2,title:'Two fields are supported; one remains open.',copy:'The first evidence bundle does not contain the notice period.',duration:1500},
    {phase:'gap',pass:2,found:2,title:'Only the unresolved field loops back.',copy:'Existing answers stay in place while retrieval narrows to notice period.',duration:2300},
    {phase:'query',pass:2,found:2,title:'Run a focused search for notice-period evidence.',copy:'The second pass avoids repeating retrieval for resolved fields.',duration:1800},
    {phase:'chunks',pass:2,found:2,title:'Select the termination passage from page 7.',copy:'Reranking finds the clause that supports the missing value.',duration:1900},
    {phase:'prompt',pass:2,found:2,title:'Compose a smaller second prompt.',copy:'Only notice period and its newly retrieved evidence are included.',duration:2100},
    {phase:'send',pass:2,found:2,title:'Send the focused evidence bundle.',copy:'Earlier answers remain intact while the missing field is processed.',duration:1600},
    {phase:'llm',pass:2,found:2,title:'Extract the value from the new passage.',copy:'The termination clause supplies a grounded answer.',duration:1500},
    {phase:'return',pass:2,found:3,title:'The final field arrives with attribution.',copy:'Notice period is returned as 30 days, supported by page 7.',duration:1700},
    {phase:'done',pass:2,found:3,title:'Every requested field is supported.',copy:'The loop stops. Unsupported fields would remain explicitly unresolved.',duration:0}
  ];
  let index=0,timer=null,playing=false,autoStarted=false;
  function stop(){clearTimeout(timer);timer=null;playing=false;figure.classList.add('extraction-paused');updateControls();}
  function updateControls(){action.textContent=playing?'Pause':index===stages.length-1?'Replay example ↶':index===0?'Watch the flow ▶':'Continue ▶';action.setAttribute('aria-pressed',String(playing));next.disabled=index===stages.length-1;}
  function render(i){
    const previous=stages[index];index=i;const step=stages[i];const ingesting=step.phase.startsWith('ingest-');
    const order=['document','chunks','embed','store'];const ingestIndex=ingesting?order.indexOf(step.phase.replace('ingest-','')):order.length;
    figure.classList.remove('inspecting-evidence');figure.dataset.extractionState=step.phase;figure.dataset.extractionPass=String(step.pass);
    host.querySelectorAll('[data-ingest]').forEach((node,j)=>{node.classList.toggle('is-active',ingesting&&j===ingestIndex);node.classList.toggle('is-complete',j<ingestIndex||!ingesting);});
    get('.ingestion-handoff').classList.toggle('is-ready',!ingesting);
    const active=ingesting?'':['query','chunks','ready','gap'].includes(step.phase)?'store':['prompt','send'].includes(step.phase)?'prompt':step.phase==='llm'?'llm':'output';
    host.querySelectorAll('[data-node]').forEach(node=>node.classList.toggle('is-active',node.dataset.node===active));
    const page=step.pass===1?'1':'7';get('.evidence-slip b').textContent=`p.${page}`;
    get('.bundle-source').textContent=ingesting||['query','ready','gap'].includes(step.phase)?'Awaiting retrieval':`Demo agreement · p. ${page}`;
    get('.bundle-schema').textContent=step.pass===1?'Agreement ID · Start date · Notice period':'Notice period only';
    get('.pass-readout').textContent=step.pass===1?'Pass 1 · three fields requested':'Pass 2 · notice period only';get('.query-count').textContent=step.found===3?'All fields resolved':`${step.found} of 3 resolved`;
    host.querySelectorAll('.query-fields > span').forEach((chip,j)=>{chip.textContent=fields[j].name+(j<step.found?' ✓':'');chip.classList.toggle('query-resolved',j<step.found);chip.classList.toggle('query-active',j>=step.found&&!ingesting&&step.phase!=='ready');});
    get('.passage-stack').querySelectorAll('[data-page]').forEach(p=>{const relevant=p.dataset.page===page;p.classList.toggle('is-relevant',relevant&&['query','chunks','prompt','send','llm','return'].includes(step.phase));p.classList.toggle('is-muted',!relevant&&['query','chunks'].includes(step.phase));});
    host.querySelectorAll('.result-ledger dl > div').forEach((row,j)=>{const found=j<step.found;row.querySelector('dd').innerHTML=found?`${fields[j].value} <button type="button" class="evidence-link" data-field="${j}" aria-label="Show source for ${fields[j].name}, page ${fields[j].page}, ${fields[j].confidence} confidence">p. ${fields[j].page} · ${fields[j].confidence} ↗</button>`:'Awaiting evidence';row.querySelector('.field-context').textContent=found?fields[j].quote:'';row.classList.toggle('field-found',found);row.classList.remove('field-arriving','field-selected');if(found&&j>=previous.found){void row.offsetWidth;row.classList.add('field-arriving');}});
    get('.feedback-title').textContent=step.title;get('.feedback-copy').textContent=step.copy;get('.extract-status').textContent=`Pass ${step.pass}. ${step.title}`;updateControls();
  }
  function schedule(){if(!playing)return;timer=setTimeout(()=>{if(index<stages.length-1)render(index+1);if(index===stages.length-1)stop();else schedule();},stages[index].duration);}
  function start(){if(playing)return;playing=true;figure.classList.remove('extraction-paused');updateControls();schedule();}
  action.addEventListener('click',()=>{autoStarted=true;if(playing){stop();return;}if(index===stages.length-1)render(0);else render(index);if(reduced.matches){render(Math.min(index+1,stages.length-1));return;}start();});
  next.addEventListener('click',()=>{autoStarted=true;stop();render(Math.min(index+1,stages.length-1));});reset.addEventListener('click',()=>{autoStarted=true;stop();render(0);});
  host.querySelectorAll('.node-jump').forEach(button=>button.addEventListener('click',()=>{autoStarted=true;stop();const offset=stages[index].pass===2?8:0;const targets={store:5,prompt:7,llm:9,output:11};render(Math.min(targets[button.dataset.jump]+offset,stages.length-1));}));
  host.addEventListener('click',event=>{const button=event.target.closest('.evidence-link');if(!button)return;stop();const j=Number(button.dataset.field),field=fields[j];figure.classList.add('inspecting-evidence');host.querySelectorAll('.result-ledger dl > div').forEach((row,k)=>row.classList.toggle('field-selected',k===j));host.querySelectorAll('.passage-stack [data-page]').forEach(p=>{p.classList.toggle('is-relevant',p.dataset.page===field.page);p.classList.toggle('is-muted',p.dataset.page!==field.page);});get('.feedback-title').textContent=`${field.name}: evidence behind the answer.`;get('.feedback-copy').textContent=`${field.quote} · Demo agreement, page ${field.page}.`;get('.extract-status').textContent=`Showing source for ${field.name}, page ${field.page}.`;});
  const passages={1:['Agreement details','Supports agreement ID and start date.'],4:['Payment terms','Available in the evidence library, but unrelated to the requested fields.'],7:['Termination','Supports notice period in the focused second pass.']};
  host.querySelectorAll('.passage-stack [data-page]').forEach(button=>button.addEventListener('click',()=>{autoStarted=true;stop();figure.classList.add('inspecting-evidence');host.querySelectorAll('.passage-stack [data-page]').forEach(p=>{p.classList.toggle('is-relevant',p===button);p.classList.toggle('is-muted',p!==button);});const [title,copy]=passages[button.dataset.page];get('.feedback-title').textContent=`Page ${button.dataset.page}: ${title}.`;get('.feedback-copy').textContent=copy;get('.extract-status').textContent=`Inspecting ${title.toLowerCase()} on page ${button.dataset.page}.`; }));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});reduced.addEventListener('change',()=>{if(reduced.matches)stop();});
  if('IntersectionObserver'in window){new IntersectionObserver(entries=>{if(entries[0].isIntersecting&&!autoStarted&&!reduced.matches&&!document.hidden){autoStarted=true;start();}},{threshold:.5}).observe(figure);new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)stop();},{threshold:0}).observe(figure);}
  render(0);host.hidden=false;figure.querySelector('.walkthrough-fallback').hidden=true;
})();
