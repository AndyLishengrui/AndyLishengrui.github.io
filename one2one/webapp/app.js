import { mdToHtml } from './mdlite.js';

const articleEl = document.getElementById('article');
const tocEl = document.getElementById('toc');
const notesPanel = document.getElementById('notesPanel');
const notesArea = document.getElementById('notesArea');

const btnPrev = document.getElementById('btnPrev');
const btnNext = document.getElementById('btnNext');
const btnNotes = document.getElementById('btnNotes');
const progressEl = document.getElementById('progress');
const searchInput = document.getElementById('searchInput');
const btnExport = document.getElementById('btnExport');
const importFile = document.getElementById('importFile');

const STORE_KEY_NOTES = 'one2one_notes';
const STORE_KEY_SCROLL = 'one2one_scroll';

// 页面滚动时给头部添加投影，增强层次；并更新阅读进度
const headerEl = document.querySelector('.app-header');
window.addEventListener('scroll', ()=>{
  if(window.scrollY > 4) headerEl.classList.add('scrolled');
  else headerEl.classList.remove('scrolled');
  const h=document.documentElement; const ratio = (h.scrollTop)/(h.scrollHeight - h.clientHeight + 0.0001);
  if(progressEl){ progressEl.style.width = (ratio*100).toFixed(2) + '%'; }
});

function toast(msg){
  const tpl = document.getElementById('toastTpl');
  const node = tpl.content.cloneNode(true).firstElementChild;
  node.textContent = msg;
  document.body.appendChild(node);
  setTimeout(()=>node.remove(), 1800);
}

async function loadMarkdown(){
  // 通过本地轻量静态服务提供内容（或同目录下直接访问）
  const res = await fetch('../一对一20251029.md');
  const md = await res.text();
  const html = mdToHtml(md);
  articleEl.innerHTML = html;
  buildToc();
  observeHeadings();
  restoreScroll();
}

function buildToc(){
  tocEl.innerHTML = '';
  const heads = articleEl.querySelectorAll('h1,h2,h3');
  heads.forEach((h) => {
    const id = h.id || h.textContent.trim();
    h.id = id;
    const a = document.createElement('a');
    a.href = '#'+id;
    a.textContent = h.textContent;
    a.onclick = (e)=>{
      e.preventDefault();
      document.getElementById(id)?.scrollIntoView({behavior:'smooth', block:'start'});
      setActiveToc(id);
    };
    tocEl.appendChild(a);
  });
}

function currentHeadingIndex(){
  const heads = [...articleEl.querySelectorAll('h1,h2,h3')];
  const y = window.scrollY + 90;
  let idx = 0;
  for(let i=0;i<heads.length;i++){
    if(heads[i].getBoundingClientRect().top + window.scrollY <= y) idx = i;
    else break;
  }
  return idx;
}

function gotoIndex(delta){
  const heads = [...articleEl.querySelectorAll('h1,h2,h3')];
  if(!heads.length) return;
  let idx = currentHeadingIndex() + delta;
  idx = Math.max(0, Math.min(heads.length-1, idx));
  const id = heads[idx].id;
  document.getElementById(id)?.scrollIntoView({behavior:'smooth', block:'start'});
  setActiveToc(id);
}

btnPrev.onclick = ()=> gotoIndex(-1);
btnNext.onclick = ()=> gotoIndex(1);

btnNotes.onclick = ()=>{
  notesPanel.classList.toggle('show');
};

searchInput.addEventListener('input', ()=>{
  const q = searchInput.value.trim();
  const paras = articleEl.querySelectorAll('p, h1, h2, h3');
  paras.forEach(el=>{
    el.style.background = '';
    if(!q) return;
    if(el.textContent.includes(q)) el.style.background = 'rgba(126,165,247,0.12)';
  });
});

// 笔记存取
function loadNotes(){
  notesArea.value = localStorage.getItem(STORE_KEY_NOTES) || '';
}
notesArea.addEventListener('input', ()=>{
  localStorage.setItem(STORE_KEY_NOTES, notesArea.value);
});
btnExport.onclick = ()=>{
  const blob = new Blob([JSON.stringify({notes: notesArea.value}, null, 2)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'one2one_notes.json';
  a.click();
};
importFile.onchange = (e)=>{
  const f = e.target.files?.[0];
  if(!f) return;
  const rd = new FileReader();
  rd.onload = ()=>{
    try{
      const obj = JSON.parse(rd.result);
      if(typeof obj.notes === 'string'){
        notesArea.value = obj.notes;
        localStorage.setItem(STORE_KEY_NOTES, obj.notes);
        toast('笔记已导入');
      }
    }catch(err){ toast('导入失败'); }
  };
  rd.readAsText(f);
};

// 滚动位置记忆
function restoreScroll(){
  const id = sessionStorage.getItem(STORE_KEY_SCROLL);
  if(id){
    document.getElementById(id)?.scrollIntoView({behavior:'instant', block:'start'});
  }
}
window.addEventListener('scroll', ()=>{
  const heads = [...articleEl.querySelectorAll('h1,h2,h3')];
  const idx = currentHeadingIndex();
  const id = heads[idx]?.id;
  if(id){ sessionStorage.setItem(STORE_KEY_SCROLL, id); }
});

// 目录高亮：IntersectionObserver
function setActiveToc(id){
  [...tocEl.querySelectorAll('a')].forEach(a=>{
    a.classList.toggle('active', a.getAttribute('href') === '#'+id);
  });
}

function observeHeadings(){
  const heads = [...articleEl.querySelectorAll('h1,h2,h3')];
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(en=>{
      if(en.isIntersecting){
        setActiveToc(en.target.id);
      }
    });
  }, {rootMargin: '-60% 0px -35% 0px', threshold: 0});
  heads.forEach(h=>io.observe(h));
}

loadNotes();
loadMarkdown();


