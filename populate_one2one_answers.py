import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent
foundation_dir = root / 'data' / 'answers'
done_dir = root / 'done2one' / 'data' / 'answers'

def norm(s):
    return re.sub(r"[\s\u3000\uFF0C\uFF1A\uFF08\)\(\.,]","", s).lower()

# Build index from foundation files
index = []
for p in foundation_dir.glob('foundation_*.json'):
    try:
        j = json.loads(p.read_text())
    except Exception as e:
        print(f"跳过无法解析的文件: {p}: {e}")
        continue
    answers = j.get('answers', {})
    for k,v in answers.items():
        ref = v.get('reference') or ''
        text = v.get('text') or v.get('zh') or ''
        if not ref or not text:
            continue
        index.append({'source_file': p.name, 'key': k, 'reference': ref, 'text': text, 'norm_ref': norm(ref)})

print(f"Found {len(index)} reference entries in foundation answers.")

# Helper to try match
num_matched = 0
for p in done_dir.glob('*.json'):
    try:
        j = json.loads(p.read_text())
    except Exception as e:
        print(f"跳过无法解析的one2one文件: {p}: {e}")
        continue
    refs = j.get('refs', [])
    if not refs:
        continue
    answers = j.get('answers', {})
    modified = False
    for r in refs:
        if r in answers and answers[r].get('has_data'):
            continue
        nr = norm(r)
        # try exact norm match on reference
        candidate = None
        for ent in index:
            if nr == ent['norm_ref']:
                candidate = ent
                break
        # try substring match
        if not candidate:
            for ent in index:
                if nr in ent['norm_ref'] or ent['norm_ref'] in nr:
                    candidate = ent
                    break
        # try numeric match on chapter:verse
        if not candidate:
            m = re.search(r"(\d+[:：]\d+)", r)
            if m:
                num = m.group(1).replace('：',':')
                for ent in index:
                    if num in ent['norm_ref']:
                        candidate = ent
                        break
        if candidate:
            answers[r] = {
                'reference': candidate['reference'],
                'text': candidate['text'],
                'has_data': True,
                'source_file': candidate['source_file']
            }
            modified = True
            num_matched += 1
        else:
            # leave placeholder
            answers.setdefault(r, {'reference': r, 'text':'', 'has_data': False})
    if modified:
        # backup
        bak = p.with_suffix('.json.bak')
        if not bak.exists():
            bak.write_text(p.read_text())
        j['answers'] = answers
        j['has_data'] = any(v.get('has_data') for v in answers.values())
        p.write_text(json.dumps(j, ensure_ascii=False, indent=2))
        print(f"更新: {p.name} (matched some refs)")
    else:
        print(f"未更新: {p.name} (未找到匹配)")

print(f"完成。共匹配并填充 {num_matched} 条经文。")
