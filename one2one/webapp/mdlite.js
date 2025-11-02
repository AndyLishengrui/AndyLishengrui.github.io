// 极简 Markdown 转 HTML（支持 #/##/###、**加粗**、*斜体*、段落与换行）
// 适配当前内容结构，尽量保持原始换行与空格

function escapeHtml(s){
  return s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
}

function inlineFormat(line){
  // 加粗：**text** → <strong>
  line = line.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  // 斜体：*text* → <em>
  line = line.replace(/(^|\W)\*([^*]+)\*/g, (m, p1, p2) => p1 + '<em>' + p2 + '</em>');
  return line;
}

export function mdToHtml(md){
  const lines = md.split(/\r?\n/);
  const out = [];
  for(let raw of lines){
    let line = raw;
    if(/^###\s+/.test(line)){
      out.push('<h3 id="'+escapeHtml(line.replace(/^###\s+/, '').trim())+'">'+inlineFormat(escapeHtml(line.replace(/^###\s+/, '').trim()))+'</h3>');
      continue;
    }
    if(/^##\s+/.test(line)){
      out.push('<h2 id="'+escapeHtml(line.replace(/^##\s+/, '').trim())+'">'+inlineFormat(escapeHtml(line.replace(/^##\s+/, '').trim()))+'</h2>');
      continue;
    }
    if(/^#\s+/.test(line)){
      out.push('<h1 id="'+escapeHtml(line.replace(/^#\s+/, '').trim())+'">'+inlineFormat(escapeHtml(line.replace(/^#\s+/, '').trim()))+'</h1>');
      continue;
    }
    if(/^---\s*$/.test(line)){
      out.push('<hr/>');
      continue;
    }
    if(line.trim()===''){
      out.push('<p class="spacer"></p>');
      continue;
    }
    // 普通文本保留原有空白与行尾双空格换行语义
    const html = inlineFormat(escapeHtml(line)).replace(/\s\s$/,'<br/>');
    out.push('<p>'+html+'</p>');
  }
  return out.join('\n');
}




