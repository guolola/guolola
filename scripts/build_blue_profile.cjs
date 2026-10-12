// Native SVG UI and a looping motion layer over the imagegen illustration.
// Requires Node.js and sharp >= 0.35. Set NODE_PATH if sharp is installed elsewhere.
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const out = path.resolve(__dirname, '../assets');
const W=1000,H=500,N=64;
const svg=(w,h,body)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${body}</svg>`;
const text=(x,y,s,size=30,color='#ffffff')=>`<text x="${x}" y="${y}" fill="${color}" font-family="Segoe UI,Microsoft YaHei,Arial,sans-serif" font-size="${size}" font-weight="700">${s}</text>`;
const save=(name,body)=>fs.writeFileSync(path.join(out,name),body);
const motifs={about:'M5 11a7 7 0 1 0 14 0a7 7 0 1 0-14 0M1 32v-3c0-11 22-11 22 0v3',stack:'M0 8L14 0L28 8L14 16ZM0 16L14 24L28 16M0 24L14 32L28 24',projects:'M0 5H10L14 10H30V31H0Z',activity:'M0 18H7L12 3L19 31L24 18H32'};
for(const [i,name,title] of [[1,'about','关于我'],[2,'stack','技术栈'],[3,'projects','项目'],[4,'activity','贡献记录']]){
  save(`section-${name}.svg`,svg(900,72,`<path fill="#063cad" d="M0 0H865L900 72H0Z"/><path fill="#19c8f1" d="M0 0H9V72H0ZM825 0H850L885 72H860Z"/><g transform="translate(27 20)" fill="none" stroke="#c6f8ff" stroke-width="2.5"> <path d="${motifs[name]}"/></g>${text(78,48,title,34)}${text(756,51,'0'+i,49,'#79dbff')}`));
}
for(const [name,label] of [['demo','SoftJL · 在线体验'],['project','SoftJL · 项目仓库'],['repos','全部仓库 ↗']]) save(`link-${name}.svg`,svg(220,46,`<path d="M0 0H204L220 46H0Z" fill="#0755d9"/><path d="M0 0H6V46H0Z" fill="#22d6f5"/>${text(16,29,label,16)}`));
for(const [name,title,index] of [['softjl','SoftJL','01'],['well','井工程数据中心','02'],['components','组件集在线演示','03']]) save(`project-${name}.svg`,svg(900,100,`<rect width="900" height="100" fill="#092455"/><path d="M0 0H12V100H0ZM770 0H800L860 100H830Z" fill="#10bff0"/><path d="M805 0H840L900 100H865Z" fill="#1466e5"/>${text(32,66,title,43)}${text(681,71,index,64,'#31c8ff')}`));
for(const file of fs.readdirSync(path.join(out,'icons')).filter(f=>f.endsWith('.svg')&&!f.startsWith('tile-')&&f!=='vitejs.svg')){
  const raw=fs.readFileSync(path.join(out,'icons',file),'utf8').replace(/<\?xml.*?\?>/s,'').replace(/<svg\b[^>]*>/,m=>m.replace(/\s(?:width|height)="[^"]*"/g,'').replace('<svg','<svg x="12" y="12" width="40" height="40"'));
  save(`icons/tile-${file}`,svg(64,64,`<rect x="1" y="1" width="62" height="62" rx="10" fill="#f0f8ff" stroke="#90d6ff"/><path d="M9 63H53" stroke="#16aff4" stroke-width="2"/>${raw}`));
}
async function encode(frames,width,height,name){
  const buf=Buffer.concat(frames);
  await sharp(buf,{raw:{width,height:height*frames.length,channels:3,pageHeight:height},limitInputPixels:false}).gif({loop:0,delay:Array(frames.length).fill(100),colours:256,dither:0,effort:7,interFrameMaxError:0}).toFile(path.join(out,name));
  console.log(name,fs.statSync(path.join(out,name)).size,'bytes');
}
async function main(){
  // Keep the approved character drawing intact. Only animate a separate SVG layer.
  const base=await sharp(path.join(out,'p3-rooftop-blue.png')).resize(W,H,{kernel:'nearest'}).png().toBuffer();
  const frames=[];
  for(let f=0;f<N;f++){
    const t=f/N;let layer='';
    for(let j=0;j<17;j++){
      const phase=(t+j*.0617)%1;
      const y=18+phase*460;
      let x=30+(j*59%890)+36*Math.sin(phase*Math.PI*2+j);
      if(x>570&&x<940&&y<390) x-=470;
      const alpha=Math.min(1,phase*12,(1-phase)*12)*.76;
      const s=j%3===0?1.15:.7;
      layer+=`<g transform="translate(${Math.round(x)} ${Math.round(y)}) scale(${s})" opacity="${alpha}"><path d="M0 3H3V0H9V3H12V6H9V9H3V6H0Z" fill="${j%3?'#e7f7ff':'#ffd7e9'}"/><path d="M3 3H9V6H3Z" fill="#fff"/></g>`;
    }
    // Tiny glints across the distant water; their intensity is periodic.
    for(let j=0;j<9;j++){
      const a=.13+.45*Math.pow((1+Math.sin(t*Math.PI*2+j*.91))/2,4);
      layer+=`<rect x="${151+j*22}" y="${194+(j%3)*5}" width="${5+j%4}" height="1" fill="#fff" opacity="${a}"/>`;
    }
    frames.push(await sharp(base).composite([{input:Buffer.from(svg(W,H,`<g shape-rendering="crispEdges">${layer}</g>`))}]).removeAlpha().raw().toBuffer());
  }
  await encode(frames,W,H,'p3-rooftop-blue.gif');
  const footer=[],divider=[];
  for(let f=0;f<48;f++){
    let dots='';
    for(let j=0;j<14;j++){const x=18+j*69,y=20+Math.sin(f/48*Math.PI*2+j)*6;dots+=`<path d="M${x} ${y-4}l4 4l-4 4l-4-4Z" fill="#32cfff" opacity="${.35+(j%3)*.2}"/>`;}
    const div=svg(1000,40,`<rect width="1000" height="40" fill="#071d47"/><path d="M0 20H1000" stroke="#134d94"/>${dots}`);
    const foot=svg(1000,100,`<rect width="1000" height="100" fill="#06265c"/><path d="M0 0H15V100H0ZM865 0H895L965 100H935Z" fill="#17c3f6"/><g transform="translate(0 58)">${dots}</g>${text(354,58,'see you soon',34,'#d6f6ff')}`);
    for(const [s,a] of [[div,divider],[foot,footer]]) a.push(await sharp(Buffer.from(s)).removeAlpha().raw().toBuffer());
    if(f===0){await sharp(Buffer.from(div)).png().toFile(path.join(out,'blue-divider-still.png'));await sharp(Buffer.from(foot)).png().toFile(path.join(out,'blue-footer-still.png'));}
  }
  await encode(divider,1000,40,'blue-divider.gif');await encode(footer,1000,100,'blue-footer.gif');
}
main().catch(e=>{console.error(e);process.exit(1)});
