import json, re, subprocess

d = json.load(open('canalqa_audit.json'))
gl = d['glossary_es_en']
pr = {p['id']: p['correct'] for p in d['model_predictions']}


def tr(s):
    s = re.sub(r'^(el|la|los|las) ', '', s.lower())
    m = re.fullmatch(r'(\w+) de (\w+)', s)
    if m and m.group(1) in gl:
        s = m.group(2) + ' ' + m.group(1)
    m = re.fullmatch(r'(\w+) (\w+)', s)
    if m and m.group(1) in gl and m.group(2) in gl and gl[m.group(2)] in ('maximum',):
        s = m.group(2) + ' ' + m.group(1)
    return ' '.join(gl.get(w, w) for w in s.split())


leaks = {}
for c in d['corpus']:
    t = c['text']
    if c['lang'] == 'en':
        m = re.search(r"'(.+?)'.*?'(.+?)'", t)
        if not m:
            continue
        q = re.search(r'.*the (.+?) of (.+?)[.?]$', m.group(1))
        leaks[(q.group(2).lower(), q.group(1).lower())] = (c['doc_id'], m.group(2))
    else:
        m = re.search(r"(?:¿[Cc]uál es|Indique) (.+) de (.+)[.?] Respuesta registrada: '(.+?)'.+entrada de \2 \((.+)\)\.$", t)
        if m:
            leaks[(m.group(4).lower(), tr(m.group(1)))] = (c['doc_id'], m.group(3))

ex = []
for b in d['benchmark']:
    q = re.search(r'.*the (.+?) of (.+?)[.?]$', b['question'])
    k = (q.group(2).lower(), q.group(1).lower())
    if k in leaks:
        ex.append(b['id'])
        print(b['id'], b['question'], '|', b['gold'], '<-', *leaks[k])

rest = [b['id'] for b in d['benchmark'] if b['id'] not in ex]
acc = sum(pr[i] for i in rest) / len(rest)
print(len(ex), 'excluded,', sum(pr[i] for i in rest), '/', len(rest), 'correct, honest', round(acc, 4), flush=True)
json.dump({'excluded_ids': ex, 'honest_accuracy': round(acc, 4)}, open('report.json', 'w'), indent=1)
subprocess.run(['python3', 'open_seal.py', 'report.json'])
