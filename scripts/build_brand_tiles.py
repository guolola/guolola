"""One local square brand mark per technology; no text badges or concept symbols."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]/'assets/icons'
brands=['codex','claude-code','dify','coze','langchain','langgraph','mcp','a2a','pinia','pydantic']
for name in brands:
    raw=(root/'source'/f'{name}.svg').read_text(encoding='utf-8')
    raw=re.sub(r'<\?xml.*?\?>|<!--.*?-->','',raw,flags=re.S).replace('currentColor','#12253f')
    raw=re.sub(r'<svg\b[^>]*>',lambda m:re.sub(r'\s(?:width|height|x|y|style)="[^"]*"','',m[0]).replace('<svg','<svg x="12" y="12" width="40" height="40"'),raw,count=1)
    backing='<rect x="9" y="9" width="46" height="46" rx="9" fill="#bd245b"/>' if name=='pydantic' else ''
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><rect x="1" y="1" width="62" height="62" rx="10" fill="#f0f8ff" stroke="#90d6ff"/>{backing}{raw}</svg>'
    (root/f'tile-{name}.svg').write_text('\n'.join(line.rstrip() for line in svg.splitlines())+'\n',encoding='utf-8')
print('Built',len(brands),'logo-only square tiles')
