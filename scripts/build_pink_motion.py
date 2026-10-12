"""Create editable pixel UI accents. Character illustration is a separate asset."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

OUT=Path(__file__).resolve().parents[1]/'assets'
PINK=(228,117,163);ROSE=(145,64,108);PALE=(255,239,246);LILAC=(202,170,222)
def heart(d,x,y,c,s=2):
    for r,line in enumerate(['0110110','1111111','1111111','0111110','0011100','0001000']):
        for col,v in enumerate(line):
            if v=='1':d.rectangle((x+col*s,y+r*s,x+col*s+s-1,y+r*s+s-1),fill=c)
def star(d,x,y,c):
    d.rectangle((x-1,y-5,x+1,y+5),fill=c);d.rectangle((x-5,y-1,x+5,y+1),fill=c)
def export(frames,name):
    pal=frames[0].quantize(colors=48)
    frames=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
    # GIF scales are exact integer multiples for crisp pixels.
    frames=[f.resize((f.width*2,f.height*2),Image.Resampling.NEAREST) for f in frames]
    frames[0].save(OUT/f'{name}.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True)
    frames[0].convert('RGB').save(OUT/f'{name}-still.png')
    print(name, (OUT/f'{name}.gif').stat().st_size, 'bytes')

def accents():
    frames=[]
    for i in range(48):
        im=Image.new('RGB',(500,24),PALE);d=ImageDraw.Draw(im);t=i/48
        for x in range(7,500,8):d.rectangle((x,12,x+2,12),fill=(245,191,213))
        for j in range(5):
            x=207+j*18;y=7+round(math.sin(t*math.tau+j*.9)*2)
            d.rectangle((x-2,2,x+16,22),fill=PALE)
            heart(d,x,y,PINK if j%2==0 else LILAC,2)
        frames.append(im)
    export(frames,'pink-divider')
    frames=[]
    f=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
    for i in range(48):
        im=Image.new('RGB',(500,70),PALE);d=ImageDraw.Draw(im);t=i/48
        d.rectangle((2,2,497,67),outline=(239,178,205),width=1)
        d.rectangle((5,5,494,64),outline=(252,215,231),width=1)
        for j in range(16):
            x=10+j*31;y=44+round(math.sin(t*math.tau+j*.7)*5)
            star(d,x,y,(244,193,216) if j%2 else LILAC)
        d.rectangle((120,12,380,56),fill=PALE)
        heart(d,133,27,PINK,2);heart(d,353,27,PINK,2)
        d.text((178,25),'see you soon',font=f,fill=ROSE)
        frames.append(im)
    export(frames,'pink-footer')
if __name__=='__main__':accents()
