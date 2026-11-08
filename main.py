import pygame, random, json, sys
from pathlib import Path

pygame.init()
pygame.display.set_caption("FISHING LIFE")
W,H=480,800
screen=pygame.display.set_mode((W,H),pygame.SCALED)
clock=pygame.time.Clock()
F=pygame.font.Font(None,26); S=pygame.font.Font(None,20); B=pygame.font.Font(None,38)
SAVE=Path("saves/progress.json"); SAVE.parent.mkdir(exist_ok=True)
FISH=[
("Rô phi","Thường",1,18),("Cá chép","Thường",1.5,24),("Cá trê","Thường",1.2,22),("Cá mè","Thường",1.4,20),("Cá diếc","Thường",.5,15),
("Cá lóc","Khá hiếm",1.8,45),("Cá basa","Khá hiếm",2,40),("Cá tra","Khá hiếm",2.5,48),("Cá chim trắng","Khá hiếm",1.1,42),("Cá trắm cỏ","Khá hiếm",3,55),
("Cá chình","Hiếm",2.2,110),("Bống tượng","Hiếm",1,130),("Tai tượng","Hiếm",3.5,105),("Cá hô","Hiếm",5,160),("Cá lăng","Hiếm",3.2,145),
("Cá vàng","Huyền thoại",.4,280),("Cá koi","Huyền thoại",1.2,350),("Cá rồng","Huyền thoại",2,500),("Cá sấu hỏa tiễn","Huyền thoại",4,420),("Đuối nước ngọt","Huyền thoại",7,600),
("Cá hồi","Thường",2,35),("Cá thu","Khá hiếm",3,65),("Cá ngừ","Hiếm",8,180),("Cá kiếm","Huyền thoại",12,520),("Cá mú","Hiếm",4,155),
("Cá hề","Thường",.2,25),("Cá nóc","Khá hiếm",.8,60),("Cá bướm","Hiếm",.3,120),("Cá thiên thần","Huyền thoại",.5,400),("Cá mặt trăng","Huyền thoại",15,700),
("Cá mòi","Thường",.3,12),("Cá cơm","Thường",.1,10),("Cá nục","Khá hiếm",.5,30),("Cá trích","Khá hiếm",.6,32),("Cá cam","Hiếm",2.5,125),
("Cá chẽm","Hiếm",3,140),("Cá bơn","Khá hiếm",1.4,50),("Cá mập con","Huyền thoại",18,850),("Cá voi mini","Huyền thoại",25,1000),("Cá phát sáng","Huyền thoại",.7,900),
("Cá suối","Thường",.2,20),("Cá tầm","Hiếm",6,220),("Hồi cầu vồng","Huyền thoại",3,480),("Cá trắng","Khá hiếm",1,38),("Lóc bông","Hiếm",4.5,170),
("Chép vàng","Huyền thoại",2,650),("Trê vàng","Hiếm",2,150),("Cá ma","Huyền thoại",.4,950),("Cá cổ đại","Huyền thoại",30,1500),("Thủy quái vực sâu","Huyền thoại",45,2200)]
PLACES=[("Hồ Bình Minh",0,1),("Suối Rừng Xanh",300,1.15),("Sông Quê",700,1.3),("Đầm Sương Mù",1300,1.55),("Hồ Núi Đá",2200,1.8),("Bờ Biển",3500,2.1),("Rạn San Hô",5200,2.5),("Vực Biển Sâu",8000,3.2)]
COL={"Thường":(225,230,215),"Khá hiếm":(110,225,140),"Hiếm":(100,180,255),"Huyền thoại":(225,130,255)}
def fresh(): return dict(money=250,rod=1,line=1,reel=1,bait=1,place=0,fish=[],caught=0,best=0,xp=0,level=1,claimed=[False]*3)
try:
 data=fresh(); data.update(json.loads(SAVE.read_text(encoding="utf8")))
except Exception: data=fresh()
def save(): SAVE.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf8")
state="home"; held=False; note="Chào mừng đến Hồ Bình Minh!"; note_t=3; buttons=[]; bite=0; progress=0; current=None
def txt(v,x,y,font=F,color=(245,245,230),center=False):
 im=font.render(str(v),True,color); screen.blit(im,(x-im.get_width()//2 if center else x,y))
def box(r,c=(17,49,62),b=(95,160,155)):
 pygame.draw.rect(screen,c,r,border_radius=12); pygame.draw.rect(screen,b,r,2,border_radius=12)
def btn(v,r,a,c=(37,105,112)):
 pygame.draw.rect(screen,c,r,border_radius=9); pygame.draw.rect(screen,(130,205,190),r,2,border_radius=9); txt(v,r[0]+r[2]//2,r[1]+r[3]//2-8,S,(255,255,245),True); buttons.append((pygame.Rect(r),a))
def say(v):
 global note,note_t
 note=v; note_t=2.8
def bg():
 screen.fill((24,56,67)); pygame.draw.rect(screen,(105,175,184),(0,0,W,265)); pygame.draw.rect(screen,(245,194,112),(365,55,48,48))
 for x,h in [(0,100),(90,125),(210,90),(330,120),(425,80)]: pygame.draw.polygon(screen,(54,116,111),[(x,265),(x+70,265),(x+34,265-h)])
 pygame.draw.rect(screen,(33,111,133),(0,265,W,H-265))
 for y in range(300,H,38):
  for x in range((y*3)%75,W,100): pygame.draw.rect(screen,(66,151,158),(x,y,35,3))
 pygame.draw.rect(screen,(117,79,48),(30,355,170,18))
 for x in range(45,200,40): pygame.draw.rect(screen,(83,57,42),(x,370,8,85))
 pygame.draw.rect(screen,(40,55,57),(102,307,17,42)); pygame.draw.rect(screen,(238,180,120),(102,289,17,17))
 pygame.draw.line(screen,(40,55,57),(110,312),(193,260),5); pygame.draw.line(screen,(225,220,170),(193,260),(226,390),2)
 pygame.draw.rect(screen,(22,51,62),(0,0,W,64))
def header():
 txt("FISHING LIFE",14,12,B,(255,232,157)); txt(f"Lv.{data['level']}  {data['money']:,} G",W-12,20,S,(255,245,190))
def footer():
 box((10,686,460,104),(12,45,58)); btn("🎣 CÂU CÁ",(18,695,138,36),"cast"); btn("CỬA HÀNG",(169,695,135,36),"shop"); btn("ĐỊA ĐIỂM",(316,695,136,36),"places"); btn("BỘ SƯU TẬP",(18,740,205,34),"collection",(54,88,105)); btn("NHIỆM VỤ",(239,740,213,34),"missions",(54,88,105))
def pick():
 pool=[]
 for f in FISH:
  w={"Thường":55,"Khá hiếm":28,"Hiếm":13,"Huyền thoại":4}[f[1]]
  if data["place"]>=4 and f[1] in ("Hiếm","Huyền thoại"): w*=1.6
  if data["bait"]>=3 and f[1] in ("Hiếm","Huyền thoại"): w*=1.3
  pool.extend([f]*max(1,int(w)))
 return random.choice(pool)
def cast():
 global state,bite,current,progress
 if state not in ("home","caught"): return
 current=pick(); bite=random.uniform(3,8)/(.8+data["bait"]*.15); progress=0; state="waiting"; say("Đã thả cần! Chờ cá cắn câu...")
def land():
 global state
 name,rarity,base,price=current; weight=round(random.uniform(base*.65,base*1.65)*(1+data["rod"]*.025),2)
 value=int(price*PLACES[data["place"]][2]*weight/max(.2,base))
 data["fish"].append(dict(name=name,rarity=rarity,weight=weight,value=value)); data["caught"]+=1; data["best"]=max(data["best"],weight); data["xp"]+=10+value//10
 while data["xp"]>=data["level"]*100:
  data["xp"]-=data["level"]*100; data["level"]+=1; data["money"]+=100; say("LÊN CẤP! +100 vàng")
 state="caught"; save()
def sell():
 total=sum(f["value"] for f in data["fish"])
 if not total: say("Chưa có cá để bán!"); return
 n=len(data["fish"]); data["fish"]=[]; data["money"]+=total; say(f"Đã bán {n} con cá: +{total} G"); save()
def upgrade(k):
 cost={"rod":100,"line":85,"reel":90,"bait":120}[k]*data[k]
 if data[k]>=10: say("Đã đạt cấp tối đa!"); return
 if data["money"]<cost: say("Không đủ vàng!"); return
 data["money"]-=cost; data[k]+=1; say(f"Nâng cấp thành công: cấp {data[k]}"); save()
def draw():
 global buttons
 buttons=[]; bg(); header()
 if state in ("home","waiting","fight","caught"):
  box((16,82,448,76)); txt(PLACES[data["place"]][0],240,95,BIG,(255,238,180),True); txt(f"Đã câu: {data['caught']} • Kỷ lục: {data['best']:.2f} kg",240,137,S,(220,235,220),True)
  if state=="home":
   box((32,490,416,125)); txt("Sẵn sàng cho chuyến câu cá?",240,510,F,(255,255,230),True); txt("Khám phá 50 loài cá tại 8 vùng nước!",240,544,S,(205,225,220),True); btn("THẢ CẦN",(125,565,230,38),"cast")
  elif state=="waiting":
   box((32,490,416,125)); txt("ĐANG CHỜ CÁ CẮN CÂU...",240,515,BIG,(255,238,170),True); txt("Mặt nước gợn sóng... hãy kiên nhẫn",240,560,S,(220,235,225),True); btn("THU CẦN",(150,570,180,34),"cancel",(100,75,65))
  elif state=="fight":
   box((24,475,432,155)); txt("CÁ ĐÃ CẮN CÂU!",240,490,BIG,(255,220,130),True); pygame.draw.rect(screen,(45,65,70),(55,540,370,22),border_radius=8); pygame.draw.rect(screen,(90,220,145),(55,540,int(370*progress),22),border_radius=8); txt("Giữ nút KÉO CÁ để tăng tiến độ",240,570,S,(235,240,220),True); btn("KÉO CÁ",(125,590,230,38),"reel",(45,125,85))
  else:
   box((32,480,416,145)); f=data["fish"][-1]; txt("BẮT ĐƯỢC CÁ!",240,493,BIG,(255,230,130),True); txt(f["name"],240,535,F,COL[f["rarity"]],True); txt(f"{f['rarity']} • {f['weight']} kg • {f['value']} G",240,562,S,(240,240,220),True); btn("CÂU TIẾP",(48,585,175,34),"cast"); btn("BÁN TẤT CẢ",(242,585,185,34),"sell")
  footer()
 elif state=="shop":
  box((18,85,444,585)); txt("CỬA HÀNG NÂNG CẤP",240,105,BIG,(255,230,150),True)
  for i,(k,n,c) in enumerate([("rod","Cần câu",100),("line","Dây câu",85),("reel","Máy câu",90),("bait","Mồi câu",120)]):
   y=165+i*103; box((34,y,412,84),(27,67,76)); txt(f"{n} • Cấp {data[k]}/10",48,y+10,F); txt(f"Giá: {c*data[k]} G",48,y+45,S,(230,215,160)); btn("NÂNG CẤP",(290,y+22,135,38),"up_"+k)
  btn("QUAY LẠI",(140,620,200,40),"back")
 elif state=="places":
  box((18,85,444,585)); txt("BẢN ĐỒ CÂU CÁ",240,105,BIG,(255,230,150),True)
  for i,(name,cost,mult) in enumerate(PLACES):
   y=160+i*61; ok=(i==0 or data["level"]>=i+1); txt(f"{i+1}. {name}",38,y,F,(255,245,220) if ok else (135,145,145)); txt("ĐÃ MỞ" if ok else f"Mở ở cấp {i+1}",38,y+25,S,(130,225,160) if ok else (210,170,130)); btn("ĐI",(355,y+3,70,38),"place_"+str(i),(40,110,100) if ok else (80,80,80))
  btn("QUAY LẠI",(140,650,200,38),"back")
 elif state=="collection":
  box((18,85,444,585)); txt(f"BỘ SƯU TẬP • {len(data['fish'])} cá",240,105,BIG,(255,230,150),True)
  for i,f in enumerate(data["fish"][-9:][::-1]):
   y=160+i*48; txt(f["name"],38,y,F,COL[f["rarity"]]); txt(f"{f['weight']}kg • {f['value']}G",430,y+3,S,(230,225,200))
  if not data["fish"]: txt("Chưa có cá. Hãy thả cần!",240,300,F,(220,230,220),True)
  btn("BÁN TẤT CẢ",(55,625,165,38),"sell"); btn("QUAY LẠI",(245,625,180,38),"back")
 elif state=="missions":
  box((18,85,444,585)); txt("NHIỆM VỤ & THÀNH TÍCH",240,105,BIG,(255,230,150),True)
  for i,(n,target,val) in enumerate([("Bắt 5 con cá",5,data["caught"]),("Bắt 20 con cá",20,data["caught"]),("Đạt cấp 5",5,data["level"])]):
   y=185+i*120; box((35,y,410,90),(27,67,76)); txt(n,52,y+10,F); txt(f"Tiến độ: {min(target,val)}/{target}",52,y+48,S,(210,225,205))
   if val>=target and not data["claimed"][i]: btn("NHẬN +"+str((i+1)*100),(290,y+25,135,38),"claim_"+str(i))
   elif data["claimed"][i]: txt("ĐÃ NHẬN",355,y+34,S,(130,220,150),True)
  btn("QUAY LẠI",(140,610,200,40),"back")
 if note_t>0:
  box((28,69,424,40),(15,53,57),(115,185,165)); txt(note,240,80,S,(255,245,205),True)
def act(a):
 global state,progress
 if a=="cast": cast()
 elif a=="cancel": state="home"; say("Đã thu cần câu.")
 elif a=="reel" and state=="fight": pass
 elif a in ("shop","places","collection","missions"): state=a
 elif a=="back": state="home"
 elif a=="sell": sell()
 elif a.startswith("up_"): upgrade(a[3:])
 elif a.startswith("place_"):
  i=int(a[6:])
  if i==0 or data["level"]>=i+1: data["place"]=i; state="home"; say("Đã đến "+PLACES[i][0]); save()
  else: say("Chưa mở! Hãy tăng cấp.")
 elif a.startswith("claim_"):
  i=int(a[6:]); goals=[(5,data["caught"]),(20,data["caught"]),(5,data["level"])]
  if goals[i][1]>=goals[i][0] and not data["claimed"][i]:
   reward=(i+1)*100; data["money"]+=reward; data["claimed"][i]=True; say(f"Nhận thưởng +{reward} G"); save()
def main():
 global state,bite,progress,note_t,held
 running=True
 while running:
  dt=min(clock.tick(60)/1000,.05)
  if note_t>0: note_t-=dt
  if state=="waiting":
   bite-=dt
   if bite<=0: state="fight"; say("Cá cắn câu! Chạm KÉO CÁ!")
  if state=="fight":
   progress=min(1,progress+dt*(.42+.035*data["reel"])) if held else max(0,progress-dt*.035)
   if progress>=1: land()
   elif random.random()<dt*.025 and progress<.15: state="home"; say("Cá đã thoát! Thử lại nhé.")
  for e in pygame.event.get():
   if e.type==pygame.QUIT: running=False
   elif e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
    if state=="home": running=False
    else: state="home"
   elif e.type in (pygame.MOUSEBUTTONUP,pygame.FINGERUP):
    held=False
   elif e.type in (pygame.MOUSEBUTTONDOWN,pygame.FINGERDOWN):
    p=(int(e.x*W),int(e.y*H)) if e.type==pygame.FINGERDOWN else e.pos
    for r,a in reversed(buttons):
     if r.collidepoint(p): act(a); break
  draw(); pygame.display.flip()
 save(); pygame.quit(); sys.exit()
if __name__=="__main__": main()
