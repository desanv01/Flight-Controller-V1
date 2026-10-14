"""Check public identity, local Markdown links and release-source completeness."""
from pathlib import Path
import re,json,sys
from urllib.parse import unquote
root=Path(__file__).resolve().parents[1]
errors=[]
for p in root.rglob('*'):
 if not p.is_file() or '.git' in p.parts:continue
 if p.suffix in {'.md','.json','.csv','.kicad_pro','.kicad_sch','.kicad_pcb','.kicad_sym','.kicad_mod','.svg','.py','.sh','.dat','.parm'}:
  t=p.read_text(encoding='utf-8',errors='replace')
  forbidden='ga'+'muda'
  if forbidden in t.lower() or forbidden in p.relative_to(root).as_posix().lower():errors.append(str(p.relative_to(root))+': old identity')
  if p.suffix=='.md' and 'development/records' not in p.as_posix() and 'development/rework' not in p.as_posix() and 'bench-guides' not in p.as_posix() and '/fabrication/' not in p.as_posix():
   t=re.sub(r'```.*?```','',t,flags=re.S)
   for url in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
    if url.startswith(('http:','https:','#','mailto:')):continue
    f=unquote(url.strip('<>').split('#')[0])
    if f and not (p.parent/f).exists():errors.append(str(p.relative_to(root))+': missing '+f)
for vendor in ['jlcpcb','pcbway']:
 s=root/'fabrication'/vendor/'source/hardware'
 if not list(s.glob('*.kicad_pcb')) or not list(s.glob('*.kicad_sch')) or not list(s.glob('*.kicad_pro')):errors.append(vendor+': incomplete source hierarchy')
print(json.dumps({'errors':errors,'result':'PASS' if not errors else 'FAIL'},indent=2))
sys.exit(bool(errors))
