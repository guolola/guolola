// A single approved illustration, a periodic breathing field, and drifting petals.
// No generated pose swaps. Motion is a native, deterministic compositing layer.
const sharp=require('sharp'),fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'../assets');
const W=1000,H=500,N=120,DT=50,TAU=Math.PI*2;
function weight(x,y,cx,cy,rx,ry){const r=((x-cx)/rx)**2+((y-cy)/ry)**2;return r>=1?0:(1-r)**3;}
async function main(){
 const base=await sharp(path.join(root,'p3-rooftop-blue.png')).resize(W,H,{kernel:'nearest'}).removeAlpha().raw().toBuffer();
 const dx=new Float32Array(W*H),dy=new Float32Array(W*H);
 for(let y=0;y<H;y++)for(let x=0;x<W;x++){
  const k=y*W+x;
  dy[k]=1.0*weight(x,y,570,412,150,83)+.45*weight(x,y,772,242,120,118)+.32*weight(x,y,704,353,86,65);
  dx[k]=.40*weight(x,y,735,111,92,84);
 }
 const frames=[];const error=[];
 for(let f=0;f<N;f++){
  const t=f/N,breath=Math.sin(t*TAU*2),sway=Math.sin(t*TAU),rgb=Buffer.alloc(base.length);
  for(let y=0;y<H;y++)for(let x=0;x<W;x++){
   const i=y*W+x,sx=x-dx[i]*sway,sy=y-dy[i]*breath;
   const x0=Math.max(0,Math.min(W-2,Math.floor(sx))),y0=Math.max(0,Math.min(H-2,Math.floor(sy)));
   if(dx[i]===0&&dy[i]===0){base.copy(rgb,i*3,i*3,i*3+3);continue;}
   const fx=sx-x0,fy=sy-y0;
   for(let c=0;c<3;c++)rgb[i*3+c]=Math.round((base[(y0*W+x0)*3+c]*(1-fx)+base[(y0*W+x0+1)*3+c]*fx)*(1-fy)+(base[((y0+1)*W+x0)*3+c]*(1-fx)+base[((y0+1)*W+x0+1)*3+c]*fx)*fy);
  }
  let layer='';
  // All paths and opacity envelopes are periodic. Petals wrap while invisible.
  for(let j=0;j<21;j++){
   const p=(t+j*.047619)%1,y=12+p*470;
   const lane=j%5===0?937:35+(j*83%490);
   const x=lane+22*Math.sin(p*TAU+j*.6)+p*25;
   const a=.75*Math.pow(Math.sin(Math.PI*p),.7),scale=.48+(j%4)*.17;
   const tilt=18*Math.sin(p*TAU+j);
   layer+=`<g opacity="${a}" transform="translate(${x.toFixed(2)} ${y.toFixed(2)}) rotate(${tilt.toFixed(1)}) scale(${scale})"><path d="M0 4H3V1H9V4H12V7H9V10H3V7H0Z" fill="${j%3?'#f5edff':'#ffd2e6'}"/><path d="M3 3H8V6H3Z" fill="#ffffff"/></g>`;
  }
  for(let j=0;j<9;j++)layer+=`<rect x="${151+j*22}" y="${194+(j%3)*5}" width="${5+j%4}" height="1" fill="#fff" opacity="${.12+.35*((1+Math.sin(t*TAU+j*.91))/2)**4}"/>`;
  const overlay=Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">${layer}</svg>`);
  frames.push(await sharp(rgb,{raw:{width:W,height:H,channels:3}}).composite([{input:overlay}]).removeAlpha().raw().toBuffer());
 }
 const mae=(a,b)=>{let v=0;for(let i=0;i<a.length;i++)v+=Math.abs(a[i]-b[i]);return v/a.length;};
 for(let i=1;i<N;i++)error.push(mae(frames[i-1],frames[i]));
 const seam=mae(frames[N-1],frames[0]);
 console.log('Loop seam MAE',seam.toFixed(4),'normal max',Math.max(...error).toFixed(4));
 if(seam>Math.max(...error)*1.5)throw Error('Visible loop discontinuity');
 await sharp(base,{raw:{width:W,height:H,channels:3}}).png().toFile(path.join(root,'p3-smooth-still.png'));
 await sharp(Buffer.concat(frames),{raw:{width:W,height:H*N,channels:3,pageHeight:H},limitInputPixels:false}).gif({loop:0,delay:Array(N).fill(DT),colours:256,dither:0,effort:7,interFrameMaxError:0}).toFile(path.join(root,'p3-smooth-loop.gif'));
 console.log('Saved 6-second, 20fps smooth loop:',fs.statSync(path.join(root,'p3-smooth-loop.gif')).size,'bytes');
}
main().catch(e=>{console.error(e);process.exit(1)});
