"""Place genuine brand marks and distinct Lucide symbols in local SVG badges."""
from pathlib import Path
import re,html
root=Path(__file__).resolve().parents[1]/'assets/icons'
brands={'codex':'codex','claude-code':'claude-code','dify':'dify','coze':'coze','langchain':'langchain','langgraph':'langgraph','mcp':'mcp','a2a':'a2a','pinia':'pinia','pydantic':'pydantic'}
concepts={'llm-api':'brain-circuit','prompt':'message-square','streaming':'waves-horizontal','function-calling':'braces','structured-output':'list-tree','react':'refresh-cw','plan-and-execute':'list-checks','skill':'puzzle','run-trace':'route','human-in-the-loop':'user-check','embedding':'binary','vector-search':'search','chunking':'scissors','context':'layers','hybrid-search':'combine','rerank':'list-filter','sse':'radio','websocket':'plug','restful-api':'server','async-tasks':'timer','http':'globe','tcp-ip':'network'}
def embed(raw,x,y,size,color):
    raw=re.sub(r'<\?xml.*?\?>','',raw,flags=re.S)
    raw=re.sub(r'<!--.*?-->','',raw,flags=re.S)
    raw=raw.replace('currentColor',color)
    return re.sub(r'<svg\b[^>]*>',lambda m:re.sub(r'\s(?:width|height|x|y|style)="[^"]*"','',m[0]).replace('<svg',f'<svg x="{x}" y="{y}" width="{size}" height="{size}"'),raw,count=1)
for slug in list(brands)+list(concepts):
    target=root/f'tag-{slug}.svg'
    old=target.read_text(encoding='utf-8')
    label=html.unescape(re.search(r'<text\b[^>]*>(.*?)</text>',old,re.S)[1])
    brand=slug in brands
    iconfile=brands[slug] if brand else 'lucide-'+concepts[slug]
    raw=(root/'source'/f'{iconfile}.svg').read_text(encoding='utf-8')
    w=max(100,len(label)*8+52);h=40
    bg='#a61e53' if slug=='pydantic' else '#f0f8ff'
    symbol=(f'<rect x="5" y="5" width="30" height="30" rx="6" fill="{bg}"/>' if brand else '')+embed(raw,8,8,24,'#13264c' if brand else '#65ddff')
    result=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect x="1" y="1" width="{w-2}" height="38" rx="6" fill="#102a53" stroke="#326eb8"/>{symbol}<text x="43" y="25" fill="#eef8ff" font-size="13" font-weight="600" font-family="Segoe UI,Arial,sans-serif">{html.escape(label)}</text></svg>'
    target.write_text('\n'.join(line.rstrip() for line in result.splitlines())+'\n',encoding='utf-8')
print('Updated',len(brands),'brand badges and',len(concepts),'concept badges')
