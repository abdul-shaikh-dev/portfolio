/* Authored illustration of adaptive extraction, not a live model response. */
(() => {
  const figure = document.querySelector('[data-walkthrough="extraction"]');
  if (!figure) return;
  const host = figure.querySelector('.walkthrough-interactive');
  host.innerHTML = `
    <div class="extract-query"><span class="extract-label">Retrieval scope</span><div class="query-fields"><span class="query-resolved">Agreement ID ✓</span><span class="query-resolved">Start date ✓</span><span class="query-notice">Notice period</span></div><span class="query-count">3 fields</span></div>
    <ol class="extraction-route" aria-label="Extraction pipeline">
      <li class="route-store"><svg viewBox="0 0 40 44" aria-hidden="true"><ellipse cx="20" cy="8" rx="16" ry="6"/><path d="M4 8v27c0 8 32 8 32 0V8M4 21c0 8 32 8 32 0"/></svg><div><strong>ChromaDB</strong><small>Retrieve &amp; rerank chunks</small></div></li>
      <li class="route-prompt"><span class="route-icon" aria-hidden="true">≡</span><div><strong>Extraction prompt</strong><small>Field schema + source chunks</small></div></li>
      <li class="route-llm"><span class="route-icon" aria-hidden="true">✳</span><div><strong>LLM</strong><small>Extract from the evidence</small></div></li>
      <li class="route-output"><span class="route-icon" aria-hidden="true">✓</span><div><strong>Attributed fields</strong><small>Value · source · page · context</small></div></li>
    </ol>
    <div class="extract-scene">
      <section class="extract-paper" aria-label="Retrieved source passage"><div class="paper-heading"><span>DEMO AGREEMENT · RETRIEVED CHUNK</span><span class="paper-page">p. 1</span></div><span class="paper-section">01 / Agreement details</span><p class="paper-quote">Agreement <mark>DEMO-001</mark> begins on <mark>1 January 2026</mark>.</p><div class="paper-lines" aria-hidden="true"><i></i><i></i><i></i></div><p class="paper-note">Relevant passage selected from the document.</p></section>
      <div class="extract-transfer" aria-hidden="true"><span>Via LLM</span><span>→</span></div>
      <section class="extract-results" aria-label="Extracted fields"><div class="result-heading"><span class="extract-label">Structured result</span><span class="result-count">2 of 3 found</span></div><dl><div><dt>Agreement ID</dt><dd>DEMO-001 <small>Demo agreement · p. 1</small></dd><dd class="field-context">“Agreement DEMO-001”</dd></div><div><dt>Start date</dt><dd>01 Jan 2026 <small>Demo agreement · p. 1</small></dd><dd class="field-context">“begins on 1 January 2026”</dd></div><div class="result-notice"><dt>Notice period</dt><dd><span class="notice-value">Needs more evidence</span><small class="notice-source">Unresolved</small></dd><dd class="field-context notice-context">No supporting passage in the first pass.</dd></div></dl></section>
    </div>
    <div class="extract-feedback"><span class="feedback-symbol" aria-hidden="true">↶</span><div><strong class="feedback-title">Only the gap goes back.</strong><p class="feedback-copy">Resolved fields stay. The next retrieval searches for the notice period alone.</p></div><button type="button" class="extract-action">Retrieve missing field <span aria-hidden="true">↗</span></button></div><p class="extract-status" role="status"></p>`;
  const get = s => host.querySelector(s);
  const action = get('.extract-action');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const fields = [
    { name:'Agreement ID', value:'DEMO-001', page:'1', quote:'“Agreement DEMO-001”' },
    { name:'Start date', value:'01 Jan 2026', page:'1', quote:'“begins on 1 January 2026”' },
    { name:'Notice period', value:'30 days', page:'7', quote:'“30 days’ written notice”' }
  ];
  // Two authored passes demonstrate the loop. This is not a live model call.
  const stages = [
    {phase:'ready', pass:1, found:0, title:'A schema becomes a search.', copy:'Follow the complete extraction, including a second pass for missing evidence.', duration:900},
    {phase:'query', pass:1, found:0, title:'Search ChromaDB for all requested fields.', copy:'Schema-driven queries retrieve candidate document chunks.', duration:1900},
    {phase:'chunks', pass:1, found:0, title:'Select and rerank the retrieved chunks.', copy:'The agreement-details passage is relevant; unrelated text is left out.', duration:2000},
    {phase:'prompt', pass:1, found:0, title:'Assemble the extraction prompt.', copy:'Combine instructions, the requested field schema, and chunks with source references.', duration:2200},
    {phase:'send', pass:1, found:0, title:'Send the prompt and its evidence to the LLM.', copy:'The model receives the selected context, rather than the entire document.', duration:1700},
    {phase:'llm', pass:1, found:0, title:'Extract values grounded in the supplied text.', copy:'Return values with their document, page, and supporting passage.', duration:1500},
    {phase:'return', pass:1, found:1, title:'The LLM returns attributed fields.', copy:'Answers arrive with the evidence used to extract them.', duration:1000},
    {phase:'return', pass:1, found:2, title:'Two fields found. One still unresolved.', copy:'No notice-period evidence was present in the first prompt.', duration:1600},
    {phase:'gap', pass:2, found:2, title:'Only the missing field starts another pass.', copy:'Retain the existing answers. Narrow the next query to notice period.', duration:2400},
    {phase:'query', pass:2, found:2, title:'Search ChromaDB again for the missing field.', copy:'This query targets notice-period evidence without repeating resolved fields.', duration:1900},
    {phase:'chunks', pass:2, found:2, title:'Retrieve the termination passage.', copy:'Reranking selects new evidence from page 7.', duration:2000},
    {phase:'prompt', pass:2, found:2, title:'Build a smaller, targeted prompt.', copy:'Request only notice period, with the newly retrieved passage and its source.', duration:2200},
    {phase:'send', pass:2, found:2, title:'Send the focused prompt to the LLM.', copy:'Earlier answers remain intact while the missing field is processed.', duration:1700},
    {phase:'llm', pass:2, found:2, title:'Extract from the new evidence.', copy:'The termination clause supplies the notice period and its attribution.', duration:1500},
    {phase:'return', pass:2, found:3, title:'Add the final value and its source.', copy:'Notice period is returned as 30 days, supported by page 7.', duration:1800},
    {phase:'done', pass:2, found:3, title:'All requested fields found. The loop stops.', copy:'Without supporting evidence, fields stay unresolved; real runs also need retry limits.', duration:0}
  ];
  const route = get('.extraction-route');
  const cargo = ['<b>p. 1</b><i></i><i></i>', '<b>Prompt</b><i></i><i></i>', '<b>value + source</b><i></i>'];
  route.querySelectorAll('li').forEach((li,i) => {
    if (i < 3) { const packet = document.createElement('span'); packet.className='route-cargo'; packet.setAttribute('aria-hidden','true'); packet.innerHTML=cargo[i]; li.append(packet); }
  });
  function positionPackets() {
    route.querySelectorAll('li').forEach(li => {
      const packet=li.querySelector('.route-cargo');const destination=li.nextElementSibling;
      if(!packet || !destination)return;
      const from=li.getBoundingClientRect(),to=destination.getBoundingClientRect();
      packet.style.setProperty('--travel-x',`${to.left-from.left}px`);
      packet.style.setProperty('--travel-y',`${to.top-from.top}px`);
    });
  }
  if('ResizeObserver' in window)new ResizeObserver(positionPackets).observe(route);
  const bundle=document.createElement('div');bundle.className='prompt-bundle';bundle.innerHTML='<span>Instructions <b>Use supplied evidence</b></span><span>Field schema <b class="bundle-schema"></b></span><span>Source chunks <b class="bundle-source"></b></span>';
  get('.extract-paper').append(bundle);
  const library=document.createElement('div');library.className='chunk-library';
  library.innerHTML='<span class="library-label">Indexed passages</span><div data-page="1"><span>01</span><p>Agreement details<small>Agreement ID · start date</small></p></div><div data-page="4"><span>04</span><p>Payment terms<small>Invoicing · settlement</small></p></div><div data-page="7"><span>07</span><p>Termination<small>Notice · written communication</small></p></div>';
  get('.extract-paper').append(library);
  const progress=document.createElement('div');progress.className='extract-progress';progress.setAttribute('aria-hidden','true');progress.innerHTML='<span></span>';route.before(progress);
  route.querySelectorAll('li').forEach((li,j)=>{
    const control=document.createElement('button');control.type='button';control.className='route-step';
    [...li.childNodes].filter(n=>!n.classList?.contains('route-cargo')).forEach(n=>control.append(n));li.prepend(control);
    control.title='Jump to this stage';
    control.addEventListener('click',()=>{autoStarted=true;stop();render(([1,3,5,7])[j]+(stages[index].pass===2?8:0));});
  });
  const controls=document.createElement('div');controls.className='extract-controls';
  action.before(controls);controls.append(action);
  const next=document.createElement('button');next.type='button';next.className='extract-next';next.textContent='Next step →';controls.append(next);
  const reset=document.createElement('button');reset.type='button';reset.className='extract-reset';reset.textContent='Reset';controls.append(reset);
  reset.addEventListener('click',()=>{autoStarted=true;stop();render(0);});
  let index=0, timer=null, playing=false, autoStarted=false;
  function stop() { clearTimeout(timer);timer=null;playing=false;figure.classList.add('extraction-paused');updateControls(); }
  function updateControls() {
    action.textContent=playing?'Pause':index===stages.length-1?'Replay example ↶':index===0?'Watch extraction ▶':'Continue ▶';
    action.setAttribute('aria-pressed',String(playing));
    next.disabled=index===stages.length-1;
  }
  function render(i) {
    const previous=stages[index];index=i;const step=stages[i];
    figure.classList.remove('inspecting-evidence');
    progress.firstElementChild.style.width=`${(i/(stages.length-1))*100}%`;
    route.querySelectorAll('.route-step').forEach((button,j)=>button.setAttribute('aria-pressed',String(j===(['query','chunks','ready','gap'].includes(step.phase)?0:['prompt','send'].includes(step.phase)?1:step.phase==='llm'?2:3))));
    library.querySelectorAll('[data-page]').forEach(chunk=>chunk.classList.toggle('chunk-match',chunk.dataset.page===(step.pass===1?'1':'7')));
    figure.dataset.extractionState=step.phase;figure.dataset.extractionPass=String(step.pass);
    get('.query-count').textContent=step.found===3?'All fields resolved':`Pass ${step.pass} · ${step.pass===1?3:1} ${step.pass===1?'fields':'field'}`;
    host.querySelectorAll('.query-fields > span').forEach((chip,j)=>{
      chip.textContent=fields[j].name+(j<step.found?' ✓':'');
      chip.classList.toggle('query-resolved',j<step.found);
      chip.classList.toggle('query-active',j>=step.found && step.phase!=='ready');
    });
    host.querySelectorAll('.extract-results dl > div').forEach((row,j)=>{
      const found=j<step.found;
      row.querySelector('dd').innerHTML=found?`${fields[j].value} <button type="button" class="evidence-link" data-field="${j}" aria-label="Show source for ${fields[j].name}">Page ${fields[j].page} ↗</button>`:`<span>Awaiting evidence</span><small>${step.found && j===2?'Unresolved':''}</small>`;
      row.querySelector('.field-context').textContent=found?fields[j].quote:'';
      row.classList.toggle('field-found',found);
      row.classList.remove('field-arriving','field-selected');
      if(found && j>=previous.found) { void row.offsetWidth;row.classList.add('field-arriving'); }
    });
    const second=step.pass===2 && !['gap','query'].includes(step.phase);
    const awaiting=['ready','query','gap'].includes(step.phase);
    get('.paper-page').textContent=awaiting?'':second?'p. 7':'p. 1';
    get('.paper-section').textContent=awaiting?'Searching document chunks':second?'07 / Termination':'01 / Agreement details';
    get('.paper-quote').innerHTML=awaiting?(step.pass===2?'Find the <mark>notice period</mark>.':'Find <mark>agreement ID</mark>, <mark>start date</mark>, and <mark>notice period</mark>.'):second?'Either party may terminate with <mark>30 days’ written notice</mark>.':'Agreement <mark>DEMO-001</mark> begins on <mark>1 January 2026</mark>.';
    get('.paper-note').textContent=awaiting?'ChromaDB · indexed document chunks':`Retrieved evidence · Demo agreement, page ${second?'7':'1'}`;
    get('.bundle-schema').textContent=step.pass===1?'Agreement ID · Start date · Notice period':'Notice period only';
    get('.bundle-source').textContent=`Demo agreement · p. ${second?'7':'1'}`;
    get('.route-store .route-cargo b').textContent=step.pass===2?'p. 7':'p. 1';
    get('.result-count').textContent=`${step.found} of 3 found`;
    get('.feedback-title').textContent=step.title;get('.feedback-copy').textContent=step.copy;
    if(!playing)get('.extract-status').textContent=`Pass ${step.pass}. ${step.title}`;
    updateControls();
  }
  function schedule() {
    if(!playing)return;
    timer=setTimeout(()=>{ if(index<stages.length-1)render(index+1);if(index===stages.length-1)stop();else schedule(); },stages[index].duration);
  }
  function start() {
    if(playing)return;
    playing=true;figure.classList.remove('extraction-paused');updateControls();schedule();
  }
  action.addEventListener('click',()=>{
    autoStarted=true;
    if(playing){stop();return;}
    if(index===stages.length-1)render(0);
    else render(index);
    if(reduced.matches){render(Math.min(index+1,stages.length-1));return;}
    start();
  });
  host.addEventListener('click',event=>{
    const button=event.target.closest('.evidence-link');if(!button)return;
    stop();
    const field=fields[Number(button.dataset.field)];
    figure.classList.add('inspecting-evidence');
    host.querySelectorAll('.extract-results dl > div').forEach((row,j)=>row.classList.toggle('field-selected',j===Number(button.dataset.field)));
    get('.paper-page').textContent=`p. ${field.page}`;
    get('.paper-section').textContent=`Source for ${field.name}`;
    get('.paper-quote').innerHTML=field.page==='7'?'Either party may terminate with <mark>30 days’ written notice</mark>.':'Agreement <mark>DEMO-001</mark> begins on <mark>1 January 2026</mark>.';
    get('.paper-note').textContent=`Demo agreement · page ${field.page} · illustrative source`;
    get('.feedback-title').textContent=`${field.name}: evidence behind the answer.`;
    get('.feedback-copy').textContent='The extracted value stays linked to its source passage. Continue to return to the extraction loop.';
    get('.extract-status').textContent=`Showing source for ${field.name}, page ${field.page}.`;
    if(innerWidth<701)get('.extract-paper').scrollIntoView({behavior:reduced.matches?'instant':'smooth',block:'center'});
  });
  next.addEventListener('click',()=>{autoStarted=true;stop();render(Math.min(index+1,stages.length-1));});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  reduced.addEventListener('change',()=>{if(reduced.matches)stop();});
  if('IntersectionObserver' in window)new IntersectionObserver(entries=>{
    const visible=entries[0].isIntersecting;
    if(visible&&!autoStarted&&!reduced.matches&&!document.hidden){autoStarted=true;start();}
  },{threshold:.5}).observe(route);
  if('IntersectionObserver' in window)new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)stop();},{threshold:0}).observe(figure);
  render(0);host.hidden=false;positionPackets();figure.querySelector('.walkthrough-fallback').hidden=true;
})();
