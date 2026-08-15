import hashlib

# ---- palettes ----
# each mob: base char->hex map + 8x8 grid (rows of 8 chars, space separated or contiguous)
MOBS = {
 "creeper": {
   "colors": {"G":"#5B8A2C","K":"#232821"},
   "grid":[
     "GGGGGGGG",
     "GKKGGKKG",
     "GKKGGKKG",
     "GGGKKGGG",
     "GGKKKKGG",
     "GGKKKKGG",
     "GGKGGKGG",
     "GGGGGGGG"],
   "eyes":["K"], "accent":"#7FB238"
 },
 "enderman": {
   "colors":{"B":"#161616","E":"#C77BF0","W":"#F0D6FF"},
   "grid":[
     "BBBBBBBB",
     "BBBBBBBB",
     "BBBBBBBB",
     "EWEBBEWE",
     "BBBBBBBB",
     "BBBBBBBB",
     "BBBBBBBB",
     "BBBBBBBB"],
   "eyes":["E","W"], "accent":"#C77BF0"
 },
 "zombie": {
   "colors":{"Z":"#5A8046","D":"#1E2A16"},
   "grid":[
     "ZZZZZZZZ",
     "ZZZZZZZZ",
     "ZDDZZDDZ",
     "ZDDZZDDZ",
     "ZZZDDZZZ",
     "ZZZZZZZZ",
     "ZDDDDDDZ",
     "ZZZZZZZZ"],
   "eyes":["D"], "accent":"#6FA05A"
 },
 "skeleton": {
   "colors":{"S":"#C9C7BE","D":"#2C2C2C"},
   "grid":[
     "SSSSSSSS",
     "SSSSSSSS",
     "SDDSSDDS",
     "SDDSSDDS",
     "SSSDSSSS",
     "SSSSSSSS",
     "SDSDSDSD",
     "SSSSSSSS"],
   "eyes":["D"], "accent":"#E8E3D3"
 },
 "steve": {
   "colors":{"H":"#4A3521","F":"#B07C57","R":"#6E4A2E","W":"#E8E4DA","P":"#4A3D6B","N":"#9A6A48","M":"#7A4E38"},
   "grid":[
     "HHHHHHHH",
     "HHHHHHHH",
     "FFFFFFFF",
     "FRRFFRRF",
     "FWPFFPWF",
     "FFFNNFFF",
     "FFMMMMFF",
     "FFFFFFFF"],
   "eyes":["W","P"], "accent":"#B07C57"
 },
}

def shade(hexc, amt):
    hexc=hexc.lstrip("#")
    r,g,b=int(hexc[0:2],16),int(hexc[2:4],16),int(hexc[4:6],16)
    r=max(0,min(255,r+amt)); g=max(0,min(255,g+amt)); b=max(0,min(255,b+amt))
    return f"#{r:02x}{g:02x}{b:02x}"

def noise(ch,x,y,base):
    # deterministic subtle per-pixel lightness variation for texture
    h=int(hashlib.md5(f"{ch}{x}{y}".encode()).hexdigest(),16)
    amt=(h%3-1)*7  # -7,0,+7
    return shade(base,amt)

CELL=16; PAD=10
def build(name,m):
    grid=m["grid"]; colors=m["colors"]; eyes=m["eyes"]
    W=8*CELL; H=8*CELL
    vbW=W+2*PAD; vbH=H+2*PAD
    parts=[f'<svg viewBox="0 0 {vbW} {vbH}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{name}">']
    parts.append(f'<g>')  # float group
    # idle float
    dur={"creeper":"4.2s","enderman":"5.4s","zombie":"4.8s","skeleton":"5.0s","steve":"4.5s"}[name]
    parts.append(f'<animateTransform attributeName="transform" type="translate" values="0 0; 0 -5; 0 0" dur="{dur}" repeatCount="indefinite"/>')
    for y,row in enumerate(grid):
        for x,ch in enumerate(row):
            base=colors[ch]
            fill=noise(ch,x,y,base)
            px=PAD+x*CELL; py=PAD+y*CELL
            extra=""
            if ch in eyes:
                # eyes get a subtle glow/blink
                extra=f'<animate attributeName="opacity" values="1;1;0.35;1;1" keyTimes="0;0.90;0.94;0.98;1" dur="6s" repeatCount="indefinite"/>' if name in("creeper","steve","zombie","skeleton") else f'<animate attributeName="opacity" values="0.7;1;0.7" dur="2.2s" repeatCount="indefinite"/>'
            parts.append(f'<rect x="{px}" y="{py}" width="{CELL}" height="{CELL}" fill="{fill}">{extra}</rect>')
    # pixel grid lines (subtle) for blocky read
    parts.append(f'<g stroke="#00000022" stroke-width="1">')
    for i in range(9):
        parts.append(f'<line x1="{PAD+i*CELL}" y1="{PAD}" x2="{PAD+i*CELL}" y2="{PAD+H}"/>')
        parts.append(f'<line x1="{PAD}" y1="{PAD+i*CELL}" x2="{PAD+W}" y2="{PAD+i*CELL}"/>')
    parts.append('</g>')
    parts.append('</g>')
    # enderman particles
    if name=="enderman":
        for i,(cx,cy,d,delay) in enumerate([(24,30,"3.2s","0s"),(120,40,"3.8s","-1.1s"),(70,20,"4.4s","-0.6s")]):
            parts.append(f'<rect x="{cx}" y="{cy}" width="5" height="5" fill="#C77BF0" opacity="0.0"><animate attributeName="opacity" values="0;0.9;0" dur="{d}" begin="{delay}" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 6; 0 -10" dur="{d}" begin="{delay}" repeatCount="indefinite"/></rect>')
    parts.append('</svg>')
    return "\n".join(parts)

for name,m in MOBS.items():
    svg=build(name,m)
    open(f"mob_{name}.svg","w").write(svg)
    print("wrote mob_"+name+".svg")

# ---- v2: add outer frame + tuned creeper, regenerate ----
MOBS["creeper"]["colors"]["K"]="#1b201a"
FRAME={"creeper":"#3e5a1e","enderman":"#000000","zombie":"#33472a","skeleton":"#7d7b73","steve":"#2f2213"}

def build2(name,m):
    grid=m["grid"]; colors=m["colors"]; eyes=m["eyes"]
    W=8*CELL; H=8*CELL; vbW=W+2*PAD; vbH=H+2*PAD
    dur={"creeper":"4.2s","enderman":"5.4s","zombie":"4.8s","skeleton":"5.0s","steve":"4.5s"}[name]
    p=[f'<svg viewBox="0 0 {vbW} {vbH}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{name}">']
    p.append('<g>')
    p.append(f'<animateTransform attributeName="transform" type="translate" values="0 0; 0 -5; 0 0" dur="{dur}" repeatCount="indefinite"/>')
    for y,row in enumerate(grid):
        for x,ch in enumerate(row):
            fill=noise(ch,x,y,colors[ch]); px=PAD+x*CELL; py=PAD+y*CELL
            extra=""
            if ch in eyes:
                extra=(f'<animate attributeName="opacity" values="1;1;0.3;1;1" keyTimes="0;0.9;0.94;0.98;1" dur="6s" repeatCount="indefinite"/>'
                       if name!="enderman" else
                       f'<animate attributeName="opacity" values="0.65;1;0.65" dur="2.2s" repeatCount="indefinite"/>')
            p.append(f'<rect x="{px}" y="{py}" width="{CELL}" height="{CELL}" fill="{fill}">{extra}</rect>')
    p.append('<g stroke="#00000022" stroke-width="1">')
    for i in range(9):
        p.append(f'<line x1="{PAD+i*CELL}" y1="{PAD}" x2="{PAD+i*CELL}" y2="{PAD+H}"/>')
        p.append(f'<line x1="{PAD}" y1="{PAD+i*CELL}" x2="{PAD+W}" y2="{PAD+i*CELL}"/>')
    p.append('</g>')
    p.append(f'<rect x="{PAD}" y="{PAD}" width="{W}" height="{H}" fill="none" stroke="{FRAME[name]}" stroke-width="4"/>')
    p.append('</g>')
    if name=="enderman":
        for cx,cy,d,delay in [(24,30,"3.2s","0s"),(120,40,"3.8s","-1.1s"),(70,20,"4.4s","-0.6s")]:
            p.append(f'<rect x="{cx}" y="{cy}" width="5" height="5" fill="#C77BF0" opacity="0"><animate attributeName="opacity" values="0;0.9;0" dur="{d}" begin="{delay}" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 6;0 -10" dur="{d}" begin="{delay}" repeatCount="indefinite"/></rect>')
    p.append('</svg>')
    return "\n".join(p)

for name,m in MOBS.items():
    open(f"mob_{name}.svg","w").write(build2(name,m)); print("v2 mob_"+name)

# ---- torch (animated flame) ----
torch='''<svg viewBox="0 0 60 96" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="torch">
<rect x="24" y="40" width="12" height="52" fill="#6b4a2a"/>
<rect x="24" y="40" width="4" height="52" fill="#815b36"/>
<rect x="30" y="52" width="6" height="6" fill="#5a3d22"/>
<rect x="30" y="70" width="6" height="6" fill="#5a3d22"/>
<g>
 <rect x="22" y="28" width="16" height="14" fill="#F4C430"/>
 <rect x="22" y="28" width="16" height="14" fill="#F4C430"><animate attributeName="opacity" values="1;0.75;1" dur="0.5s" repeatCount="indefinite"/></rect>
 <rect x="26" y="18" width="8" height="12" fill="#F4E37A"><animate attributeName="height" values="12;16;10;14;12" dur="0.6s" repeatCount="indefinite"/><animate attributeName="y" values="18;14;20;16;18" dur="0.6s" repeatCount="indefinite"/></rect>
 <rect x="27" y="10" width="6" height="8" fill="#FFF6C9"><animate attributeName="opacity" values="0.9;0.4;1;0.6;0.9" dur="0.45s" repeatCount="indefinite"/></rect>
 <rect x="20" y="34" width="4" height="6" fill="#E8891A"><animate attributeName="opacity" values="0.6;1;0.6" dur="0.4s" repeatCount="indefinite"/></rect>
 <rect x="36" y="34" width="4" height="6" fill="#E8891A"><animate attributeName="opacity" values="1;0.6;1" dur="0.4s" repeatCount="indefinite"/></rect>
</g>
</svg>'''
open("item_torch.svg","w").write(torch); print("torch")

# ---- diamond gem ----
diamond='''<svg viewBox="0 0 96 96" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="diamond">
<g>
<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="4s" repeatCount="indefinite"/>
<rect x="24" y="24" width="48" height="12" fill="#6BE3D6"/>
<rect x="18" y="36" width="60" height="12" fill="#8CEDE2"/>
<rect x="24" y="48" width="48" height="12" fill="#4FC9BC"/>
<rect x="30" y="60" width="36" height="10" fill="#3BB4A8"/>
<rect x="38" y="70" width="20" height="8"  fill="#2E9C91"/>
<rect x="30" y="30" width="10" height="6" fill="#CFF6F1"/>
<rect x="24" y="24" width="48" height="54" fill="none" stroke="#1c6f68" stroke-width="3"/>
<rect x="30" y="27" width="8" height="4" fill="#FFFFFF"><animate attributeName="opacity" values="1;0.3;1" dur="2.5s" repeatCount="indefinite"/></rect>
</g>
</svg>'''
open("item_diamond.svg","w").write(diamond); print("diamond")
