// Assemble imagegen character keyframes into a GIF; retain a fixed background.
const sharp=require('sharp');const path=require('path');const fs=require('fs');
const root=path.resolve(__dirname,'../assets');
async function main(){
 const file=path.join(root,'p3-character-keyframes.png');const m=await sharp(file).metadata();
 const w=Math.floor(m.width/2),h=Math.floor(m.height/3),W=1000,H=500,N=64;
 const keys=[];
 for(let i=0;i<6;i++)keys.push(await sharp(file).extract({left:i%2*w,top:Math.floor(i/2)*h,width:w,height:h}).resize(W,H).removeAlpha().raw().toBuffer());
 // Animate the figures only. The sky, city, border and username remain fixed.
 const maskSvg=`<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 724 362"><rect width="724" height="362" fill="black"/><g fill="white"><path d="M502 21Q553 1 592 26Q618 50 607 103L650 128Q682 177 692 241L716 340L675 346L609 331L596 277L578 264L509 284L451 283L453 249L477 222L487 160L512 131Q477 113 481 75Q477 41 502 21Z"/><path d="M329 278Q379 261 420 269L470 239L553 236L597 285L596 351L349 355L343 322Z"/></g></svg>`;
 const mask=await sharp(Buffer.from(maskSvg)).blur(2).greyscale().raw().toBuffer();
 const timeline=[[0,0],[18,0],[27,1],[29,2],[30,3],[32,3],[33,2],[35,1],[45,4],[51,5],[64,0]];
 const frames=[];
 for(let f=0;f<N;f++){
  const end=timeline.findIndex(x=>x[0]>f),a=timeline[end-1],b=timeline[end];
  let t=(f-a[0])/(b[0]-a[0]);t=t*t*(3-2*t);
  const frame=Buffer.alloc(W*H*3),A=keys[a[1]],B=keys[b[1]],base=keys[0];
  for(let p=0;p<W*H;p++){const z=mask[p]/255;for(let c=0;c<3;c++){let k=p*3+c;frame[k]=Math.round(base[k]*(1-z)+(A[k]*(1-t)+B[k]*t)*z);}}
  frames.push(frame);
 }
 await sharp(keys[0],{raw:{width:W,height:H,channels:3}}).png().toFile(path.join(root,'p3-character-still.png'));
 await sharp(Buffer.concat(frames),{raw:{width:W,height:H*N,channels:3,pageHeight:H},limitInputPixels:false}).gif({loop:0,delay:Array(N).fill(100),colours:256,dither:0,effort:7,interFrameMaxError:0}).toFile(path.join(root,'p3-character-motion.gif'));
 console.log('Character GIF',fs.statSync(path.join(root,'p3-character-motion.gif')).size,'bytes');
}
main().catch(e=>{console.error(e);process.exit(1)});
