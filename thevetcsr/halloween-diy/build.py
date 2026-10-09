from pathlib import Path
from math import sin, cos, pi
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
pdfmetrics.registerFont(TTFont("Body", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Head", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'output/pdf/TheVetCSR-Halloween-Front-Desk-DIY-Manual.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(OUT),pagesize=(612,792))
c.setTitle('A Little Boo at the Front Desk | TheVetCSR')
c.setAuthor('TheVetCSR')
INK=HexColor('#202829'); TEAL=HexColor('#175d60'); ORANGE=HexColor('#c25b24'); PAPER=HexColor('#faf7ef')
page=0
style=ParagraphStyle('body',fontName='Body',fontSize=11,leading=16,textColor=INK)
def text(s,x,y,w=508,size=11,color=INK):
    st=ParagraphStyle('local',parent=style,fontName='Head' if size>=15 else 'Body',fontSize=size,leading=size*1.28,textColor=color)
    p=Paragraph(s,st); _,h=p.wrap(w,700); p.drawOn(c,x,y-h); return y-h
def star(x,y,r=6):
    c.setStrokeColor(INK);c.setFillColor(HexColor('#e8bc52'));c.setLineWidth(.7)
    p=c.beginPath()
    for i in range(10):
        rad=r if i%2==0 else r*.43;xx=x+rad*cos(pi/2+i*pi/5);yy=y+rad*sin(pi/2+i*pi/5)
        if i==0:p.moveTo(xx,yy)
        else:p.lineTo(xx,yy)
    p.close();c.drawPath(p,fill=1)
def begin(title,kicker='THEVETCSR / HALLOWEEN WORKSHOP',template=False):
    global page, is_template
    page+=1;is_template=template
    c.setFillColor(white if template else PAPER);c.rect(0,0,612,792,fill=1,stroke=0)
    # a reusable notebook frame, outside the printable workspace
    c.setStrokeColor(HexColor('#e0ddd3'));c.setLineWidth(.5);c.setDash()
    for y in range(65,760,24):
        if not template:c.line(30,y,35,y)
    c.line(31,58,31,752)
    for y in range(85,745,28):
        c.setFillColor(white);c.setStrokeColor(INK);c.setLineWidth(1.4)
        c.circle(22,y,3.5,fill=1);c.arc(6,y-6,29,y+6,35,290)
    c.setFillColor(TEAL);c.rect(42,731,528,24,fill=1,stroke=0)
    text(kicker,51,750,510,8,white)
    c.setFillColor(HexColor('#eee0c4') if not template else HexColor('#f3f3f0'))
    p=c.beginPath();p.moveTo(42,715);p.lineTo(565,719);p.lineTo(570,646);p.lineTo(548,648);p.lineTo(525,644);p.lineTo(42,647);p.close();c.drawPath(p,fill=1,stroke=0)
    text(title,52,704,505,25)
    c.setFillColor(HexColor('#e9c271'));c.saveState();c.translate(52,721);c.rotate(-7);c.rect(-8,-4,64,13,fill=1,stroke=0);c.restoreState()
    c.setStrokeColor(HexColor('#c8c9c4'));c.line(42,48,570,48)
    text('THEVETCSR | A LITTLE BOO AT THE FRONT DESK',42,36,470,7)
    text(str(page).zfill(2),542,36,28,9,TEAL)
    if not template:
        rng=random.Random(page)
        for i in range(15):
            c.setFillColor(HexColor('#cabaa6'));c.circle(rng.uniform(573,595),rng.uniform(73,710),rng.uniform(.4,1.3),fill=1,stroke=0)
        star(584,700);star(584,115,8)
def end():
    if not is_template and page not in [1,7]:
        # restrained original clinic doodles in the footer margin
        c.setStrokeColor(TEAL);c.setLineWidth(1.1);c.setDash()
        c.arc(473,62,497,84,180,180);c.line(473,73,473,87);c.line(497,73,497,87)
        c.bezier(485,62,485,53,516,54,516,74);c.circle(516,77,4)
        star(543,76,7)
    if not is_template and page not in [1,7,11,22,24]:
        # Original vector clinic vignette: festive detail outside the instructions.
        c.setFillColor(HexColor('#f0e1c9'));c.roundRect(65,94,375,75,8,fill=1,stroke=0)
        c.setStrokeColor(INK);c.setLineWidth(1.2)
        c.setFillColor(ORANGE);c.ellipse(84,108,142,151,fill=1)
        c.arc(97,108,127,151,0,360);c.line(113,151,116,160)
        c.setFillColor(INK);c.circle(103,136,2,fill=1);c.circle(123,136,2,fill=1);c.arc(103,116,125,131,180,180)
        # tiny desk phone with receiver and dial
        c.setFillColor(TEAL);c.roundRect(182,107,66,35,6,fill=1)
        c.roundRect(176,146,76,13,5,fill=1)
        c.setFillColor(white)
        for dx in [198,213,228]:
            for dy in [117,129]:c.circle(dx,dy,2,fill=1,stroke=0)
        c.setStrokeColor(INK);c.bezier(250,151,271,128,252,112,269,105)
        ghost(298,107,44,51,True,False)
        star(381,145,8);star(409,115,6)
    c.showPage()
def section(label,body,y):
    # taped label strip with robust spacing and actual text, never baked in
    c.setFillColor(HexColor('#dcebe7'));c.rect(47,y-17,516,22,fill=1,stroke=0)
    c.setFillColor(ORANGE);c.rect(47,y-17,4,22,fill=1,stroke=0)
    y=text(label.upper(),57,y+1,495,9,TEAL)-11
    return text(body,51,y,507,10.5)-23
def bullet(items,y):
    for item in items:y=text('• '+item,53,y,505)-10
    return y
def check(y,label):
    c.setStrokeColor(INK);c.rect(49,y-12,10,10);return text(label,70,y,490)-25
def calibration():
    c.setStrokeColor(INK);c.setLineWidth(.8);c.setDash();c.rect(42,65,72,72)
    text('1 inch square',125,118,180,10)
    text('Print Actual Size / 100%. Measure this square before cutting.',125,98,390,9)
def dashed():c.setStrokeColor(INK);c.setLineWidth(.8);c.setDash(4,3)
def ghost(x,y,w=130,h=150,cat=False,label=True):
    dashed();p=c.beginPath();p.moveTo(x,y);p.lineTo(x,y+h*.65)
    if cat:
        p.lineTo(x+w*.12,y+h);p.lineTo(x+w*.32,y+h*.82);p.curveTo(x+w*.42,y+h*.9,x+w*.58,y+h*.9,x+w*.68,y+h*.82);p.lineTo(x+w*.88,y+h);p.lineTo(x+w,y+h*.65)
    else:p.curveTo(x,y+h*1.1,x+w,y+h*1.1,x+w,y+h*.65)
    p.lineTo(x+w,y)
    for a in [0.8,0.6,0.4,0.2,0]:p.lineTo(x+w*a,y+(12 if int(a*10)%4==0 else 0))
    p.close();c.drawPath(p);c.setDash();c.setFillColor(INK)
    if cat:
        c.setFillColor(INK);c.setStrokeColor(INK)
        c.ellipse(x+w*.16,y+h*.12,x+w*.84,y+h*.64,fill=1,stroke=0)
        c.circle(x+w*.5,y+h*.65,w*.24,fill=1,stroke=0)
        for z in [.28,.60]:
            p=c.beginPath();p.moveTo(x+w*z,y+h*.75);p.lineTo(x+w*(z+.02),y+h*.92);p.lineTo(x+w*(z+.17),y+h*.76);p.close();c.drawPath(p,fill=1,stroke=0)
        c.setFillColor(HexColor('#e8bc52'))
        for z in [.40,.60]:
            c.ellipse(x+w*(z-.055),y+h*.63,x+w*(z+.055),y+h*.68,fill=1,stroke=0)
        c.setFillColor(white);c.circle(x+w*.5,y+h*.59,2,fill=1,stroke=0)
    else:
        c.circle(x+w*.35,y+h*.56,4,fill=1);c.circle(x+w*.65,y+h*.56,4,fill=1)
        c.arc(x+w*.39,y+h*.32,x+w*.61,y+h*.49,180,180)
    c.setFillColor(INK);c.circle(x+w*.5,y+h*.77,2)
    if label:text('TAPE FLAT / OPTIONAL HOLE',x,y-17,w,7)
def card(x,y,w,h,title,sub=''):
    dashed();c.rect(x,y,w,h);c.setDash()
    c.setFillColor(HexColor('#e2eeea'));c.rect(x+8,y+h-12,w-16,5,fill=1,stroke=0)
    c.setFillColor(ORANGE);c.circle(x+w-19,y+18,5,fill=1,stroke=0)
    title_end=text(title,x+14,y+h-23,w-28,15,TEAL)
    if sub:text(sub,x+14,title_end-12,w-28,9.5)
begin('A LITTLE BOO<br/>AT THE FRONT DESK')
text('HALLOWEEN DIY MANUAL',52,622,500,21,ORANGE)
text('Make October a little less scary.',52,582,500,13)
art=ROOT/'cover-art.png'
if art.exists():
    c.drawImage(str(art),133,158,width=348,height=390,preserveAspectRatio=True,anchor='c',mask='auto')
else:
    ghost(345,275,145,190,True);ghost(110,248,160,210)
text('SIX PROJECTS  /  REAL TEMPLATES  /  A LOBBY THAT WORKS',52,148,500,10,TEAL)
text('Print, cut, build, and bring a little kindness to the counter.',52,119,500,11)
text('US Letter | 24 pages | Reusable October workshop',52,87,500,9)
end()

begin('Start small. Make it useful.')
y=section('Choose your route','10 minutes: one welcome sign and one useful desk card.<br/>30 minutes: add the flat ghost display and team notes.<br/>One afternoon: add the pumpkin and seated activity after staffing allows.',620)
y=section('What this is','An original craft and setup manual for veterinary reception teams. It supports seasonal presentation; it is not a clinical protocol, safety certification, or promise of improved patient outcomes.',y)
y=section('What you need','Printer, US Letter paper, scissors, removable tape, ruler, pen, and optional cardstock. Use a stable artificial pumpkin for the cone project. Crayons are optional. No glue gun, carving, glitter, or pet costume is required.',y)
y=section('Before printing','Ask the clinic lead to approve locations and wording. Keep reception readable, exits clear, and cleaning surfaces accessible. Assign one person to setup and one to the final walkthrough.',y)
text('Humans first. Pets always. Halloween comes after both.',48,y,500,16,ORANGE);end()

begin('The build map')
rows=[('PLAN','4-6','Placement, printing, project selection'),('BUILD','7-20','Six projects with instructions and templates'),('RUN','21-23','Launch, reset, and reprint checks'),('VERIFY','24','Research and design rationale')]
y=620
for a,b,d in rows:
    y=section(a+' / pages '+b,d,y)
text('Project index',48,y,500,17);y-=40
for a in ['01  Ghost-pet display: pages 7-8','02  Black-cat welcome display: pages 9-10','03  Cone-wearing pumpkin: pages 11-13','04  Desk signs that do a job: pages 14-15','05  Seated doodle hunt: pages 16-18','06  Team appreciation station: pages 19-20']:
    y=text(a,48,y,500)-12
end()

begin('Plan the lobby before decorating')
y=section('Entrance','Keep door controls, hours, directional signs, and sight lines visible. Place the welcome display on a wall or sign holder away from the door swing.',620)
y=section('Reception','Use a flat paper display behind staff. Keep payment equipment, check-in surfaces, hand hygiene supplies, and client paperwork clear.',y)
y=section('Waiting area','Offer activities from a seat. Keep a calmer waiting option available under clinic policy. Do not put decorations beside carriers or encourage children to approach animals.',y)
y=section('Clinical and quiet spaces','Keep patient-care areas and comfort rooms free of this craft setup. Use removable displays so the team can quickly simplify the public area when needed.',y)
y=section('Clinic lead decides','Local cleaning, infection-control, accessibility, and building rules take priority. Paper is not disinfectable: replace soiled pieces rather than trying to clean them.',y)
end()

begin('Printing and cutting rules',template=True)
y=section('Print correctly','US Letter, portrait, single-sided. Choose Actual Size or 100%; disable Fit to Page for measured craft templates. Measure the calibration square on template pages.',620)
y=section('Understand the marks','Dashed outlines = cut. Dotted lines = fold. Solid artwork stays intact. Hole marks are optional; tape mounting is the default for the ghost display.',y)
y=section('Keep it simple','Print templates in grayscale or black and white. Use cardstock only if your printer supports it. Cut crafts in a staff-only work area and clear scissors and scraps before patients arrive.',y)
y=section('Check the print','If the 1-inch square measures incorrectly, stop and change the printer scale. If a border disappears, confirm US Letter and portrait settings before reprinting.',y)
calibration();end()

begin('Pick your six-project setup')
projects=[('Ghost pets','15-20 min','2 sheets; removable tape'),('Welcome display','5-10 min','1 sheet; sign holder or wall tape'),('Pumpkin cone','20-30 min','2 sheets; cardstock and tape'),('Useful desk cards','10-15 min','1 sheet; holders or wall tape'),('Seated doodle hunt','10 min setup','2 display sheets; player copies'),('Team notes','10-15 min','1 sheet; pen and envelope')]
y=622
for a,b,d in projects:y=section(a+' / '+b,d,y)
text('Times are planning estimates, not tested completion claims. Start with supplies already in the clinic; purchased materials are optional.',48,y,505,10)
end()

begin('01 / Ghost pets, minus the dangling bits')
y=section('Supplies and time','Template on page 8, scissors, removable tape; 15-20 minutes. Print twice for eight ghost pets.',620)
y=section('Build','1. Cut the dashed outer shapes; leave faces intact.<br/>2. Arrange the pieces in a gentle wave on a staff-side wall or board.<br/>3. Tape each piece flat at the top and bottom so it cannot flutter.<br/>4. Step back and confirm the display does not cover clinic information.',y)
y=section('Optional garland route','Only if the clinic lead approves a location inaccessible to animals: punch the marked points and thread a short cord. Secure both cord ends, eliminate loose tails, and keep the entire assembly away from traffic and carriers. If that location is unavailable, use the flat display.',y)
y=section('Reset','If pieces detach or patients show concern near the display, remove or relocate it. Replace damaged or soiled paper. Keep pieces in a labeled flat envelope after October.',y)
text('Finished layout: four flat ghosts in a row',48,y,500,10)
for i in range(4):ghost(65+i*125,95,85,105,i%2==1)
end()

begin('Ghost-pet cutouts','PROJECT 01 / PRINTABLE TEMPLATE',True)
ghost(90,415,155,160);ghost(355,415,155,160,True)
ghost(90,200,155,160,True);ghost(355,200,155,160)
calibration();end()

begin('02 / Black cats welcome')
y=section('Supplies and time','Page 10, paper or cardstock, sign holder or removable tape; 5-10 minutes.',620)
y=section('Build','1. Print page 10.<br/>2. Display the full page without cutting.<br/>3. Position it on a wall or in a stable holder away from patient reach.<br/>4. Confirm hours, check-in instructions, and emergency directions remain visible.',y)
y=section('Make it welcoming','The sign celebrates black cats without asking clients to put animals in costumes, open carriers, or pose for photographs. A photo opportunity is optional and should never delay care.',y)
y=section('Use this front-desk line','“You can leave your cat settled in the carrier. Let us know if they need a quieter wait; we will check what is available.” Adapt this to clinic policy.',y)
y=section('Reset','Replace creased or soiled paper. During sensitive appointments, use the clinic lead\'s preferred quieter display plan.',y)
end()

begin('Black cats welcome','PROJECT 02 / PRINT AND DISPLAY',True)
text('BLACK CATS<br/>WELCOME.',62,585,490,48)
ghost(230,220,155,185,True)
text('All little monsters deserve a kind hello.',70,172,480,19)
text('Keep cats settled in their carriers.<br/>Need a quieter wait? Let our team know.',70,120,480,13)
end()

begin('03 / A pumpkin with a recovery cone')
y=section('Supplies and time','Pages 12-13; cardstock, scissors, ruler, tape, and a stable artificial pumpkin; 20-30 minutes. This cone is for a display object only, never an animal.',620)
y=section('Fit first','Measure around the pumpkin where the cone will sit. The joined inner arc is about 5.2 inches before overlap; a 0.5-inch overlap leaves about 4.7 inches. Choose a pumpkin with a similar neck circumference, or make a paper test first. Dimensions describe the template, not a universal pumpkin fit.',y)
y=section('Build','1. Print both halves at 100%; check the squares.<br/>2. Cut the outer arcs, inner arcs, and straight edges.<br/>3. Join HALF A and HALF B along one straight edge using tape on the back; align the inner and outer arcs.<br/>4. Curl the joined strip into a cone. Dry-fit it around the pumpkin.<br/>5. Overlap the remaining ends by about 0.5 inch and tape. Adjust slightly for fit.<br/>6. Place the pumpkin on a stable staff-side surface.',y)
y=section('If it does not fit','Do not force it or enlarge the print scale. Use a smaller pumpkin, or transfer the two-part shape to larger craft paper and remeasure. The provided template is a small display size.',y)
text('Add a marker face if you like. No carving. No candles.',48,y,500,15,ORANGE);end()

def conehalf(label):
    begin('Pumpkin cone / '+label,'PROJECT 03 / TWO-PART TEMPLATE',True)
    x,y=120,430;r1,r2=120,216;angle=90
    dashed();p=c.beginPath()
    p.moveTo(x+r1,y);p.lineTo(x+r2,y)
    # quarter annulus through cubic approximation
    p.curveTo(x+r2,y+r2*.55228475,x+r2*.55228475,y+r2,x,y+r2)
    p.lineTo(x,y+r1)
    p.curveTo(x+r1*.55228475,y+r1,x+r1,y+r1*.55228475,x+r1,y)
    p.close();c.drawPath(p);c.setDash()
    text(label,x+60,y+140,145,17)
    text('JOIN EDGE',x+8,y+108,90,8)
    text('FINAL OVERLAP EDGE',x+120,y-17,150,8)
    text('Cut the quarter-ring shape. Join A to B at one straight edge with tape on the back. The other edges overlap to close the cone.',48,380,500,12)
    text('Inner radius 1.67 in • Outer radius 3 in<br/>Two halves form a half-ring. Cone height depends on the final overlap.',48,298,500,11)
    text('The pumpkin is the patient. The paper cone is the joke.',48,222,500,15,ORANGE)
    calibration();end()
conehalf('HALF A');conehalf('HALF B')

begin('04 / Desk signs that do a job')
y=section('Supplies and time','Page 15, scissors, paper or cardstock, small holders or tape; 10-15 minutes.',620)
y=section('Build','1. Cut the four cards on their dashed borders.<br/>2. Choose only the cards your clinic needs.<br/>3. Put check-in wording near the actual check-in point.<br/>4. Put the food reminder where staff control treats; do not create a self-serve pet-treat bowl.<br/>5. Keep the calmer-wait card visible without making a service promise.',y)
y=section('Treat policy','These cards do not authorize feeding. Staff should check the clinic\'s policy and patient-specific restrictions before offering a treat. Keep human food and wrappers inaccessible to pets; an inaccessible staff area is the default.',y)
y=section('Tone check','Humor belongs around the work, not at a client\'s expense. Leave the phones joke in a staff-facing spot if the clinic prefers straightforward public wording.',y)
y=section('Reset','Check daily for moved cards, obstructed equipment, and worn paper. Remove any card that no longer matches the clinic\'s process.',y)
end()

begin('Four useful little signs','PROJECT 04 / CUT-APART CARDS',True)
card(48,405,245,175,'CHECK IN HERE','Your little monster has a chart.<br/>Please tell us your pet\'s name.')
card(319,405,245,175,'TREATS? ASK FIRST.','Our team checks before offering any pet treat. Human candy stays away from pets.')
card(48,185,245,175,'A QUIETER WAIT?','Let our team know if your pet is worried. We will check available options.')
card(319,185,245,175,'THE PHONES ARE HAUNTED AGAIN.','A tiny October joke for the staff-side desk.')
calibration();end()

begin('05 / The seated doodle hunt')
y=section('Supplies and time','Display on page 17, player sheet on page 18, pens or crayons; 10 minutes to set up.',620)
y=section('Build','1. Print the display once and the player sheet as needed.<br/>2. Show the display where seated clients can see it, or hand out a second copy.<br/>3. Invite players to find six icons on the illustrated display. Nothing is hidden around the clinic.<br/>4. Keep crayons and sheets in a staff-managed location.<br/>5. Let players take the page home; no prize or treat is required.',y)
y=section('Say it simply','“There is a tiny Halloween hunt on this page if you would like something to do while you wait. You can stay right here.” Participation is optional.',y)
y=section('Answer key','Ghost: top left. Cat: top right. Pumpkin: middle left. Paw: middle right. Bone: bottom left. Heart: bottom right. The answer key matches the six illustrated tiles on page 17.',y)
y=section('Keep the lobby working','Children stay with their caregiver. Do not direct anyone toward patients, carriers, exam rooms, or staff workspaces. Follow clinic policy for shared supplies.',y)
end()

def icon(kind,x,y):
    c.setStrokeColor(INK);c.setFillColor(white);c.setLineWidth(2);c.setDash()
    if kind=='ghost':ghost(x-35,y-42,70,85)
    elif kind=='cat':ghost(x-35,y-42,70,85,True)
    elif kind=='pumpkin':
        c.ellipse(x-42,y-30,x+42,y+30);c.ellipse(x-23,y-30,x+23,y+30);c.line(x,y+30,x+7,y+47);c.circle(x-16,y+5,3,fill=1);c.circle(x+16,y+5,3,fill=1);c.line(x-14,y-12,x+14,y-12)
    elif kind=='paw':
        c.ellipse(x-24,y-30,x+24,y+2)
        for dx,dy in [(-30,16),(-12,29),(12,29),(30,16)]:c.ellipse(x+dx-8,y+dy-10,x+dx+8,y+dy+10)
    elif kind=='bone':
        c.roundRect(x-30,y-10,60,20,8)
        for dx in [-33,33]:
            for dy in [-10,10]:c.circle(x+dx,y+dy,13)
    else:
        p=c.beginPath();p.moveTo(x,y-35);p.curveTo(x-75,y+12,x-25,y+65,x,y+25);p.curveTo(x+25,y+65,x+75,y+12,x,y-35);c.drawPath(p)

begin('Find six friendly Halloween doodles','PROJECT 05 / SEATED DISPLAY',True)
for i,k in enumerate(['ghost','cat','pumpkin','paw','bone','heart']):
    x=170 if i%2==0 else 440;y=535-(i//2)*158
    c.setStrokeColor(HexColor('#cccfc9'));c.roundRect(x-100,y-66,200,132,10);icon(k,x,y)
text('Look from your seat. No exploring the clinic required.',48,115,515,13)
end()

begin('My tiny Halloween hunt','PROJECT 05 / PLAYER SHEET',True)
text('Find each doodle on the display. Tick it off, then draw your own clinic ghost below.',48,622,510,13)
y=555
for name in ['Ghost','Black cat','Pumpkin','Paw print','Bone','Heart']:y=check(y,name)
c.setStrokeColor(INK);c.setDash(4,3);c.rect(48,135,516,195);c.setDash()
text('MY CLINIC GHOST',62,316,480,10,TEAL)
text('Stay with your grown-up. Leave pets settled. Fun is optional.',48,107,510,11)
end()

begin('06 / A little thanks for the team')
y=section('Supplies and time','Page 20, scissors, pen, envelope or tray; 10-15 minutes. Food is optional.',620)
y=section('Build','1. Cut the six cards.<br/>2. Put a few in a staff-only space with a pen.<br/>3. Write a specific thank-you: name the action you appreciated.<br/>4. Give the card privately or leave it where the colleague can find it.<br/>5. Invite participation; do not make it a contest or extra task.',y)
y=section('If you add treats','Keep food in a staff-only area and retain ingredient information. Offer a food-free card option. Do not leave candy, wrappers, ribbons, or loose tags within patient reach.',y)
y=section('Make it specific','“Thank you for moving that appointment so the family had privacy.”<br/>“You caught the missing callback number before the call ended.”<br/>“You kept the desk covered while I took a break.”',y)
y=section('Reset','Remove food waste, restock cards, and keep appreciation voluntary. This activity complements support; it does not replace adequate staffing, breaks, or management follow-through.',y)
end()

begin('No tricks. Just thanks.','PROJECT 06 / TEAM CARDS',True)
phrases=['You made a hard moment gentler.','Thanks for having my back.','Your kindness did not go unnoticed.','You kept the chaos moving.','You make this place less scary.','No tricks. Just thanks.']
for i,p in enumerate(phrases):
    x=48 if i%2==0 else 319;y=447-(i//2)*153
    card(x,y,245,133,p,'For: _____________<br/>Because: __________________')
calibration();end()

begin('Launch without taking over the shift')
y=section('Before the timer','Print and cut in a staff-only workspace. Arrange coverage; stop the craft session whenever reception needs attention. The times below assume preparation is already complete.',620)
y=section('0-5 minutes','Walk the approved placement plan. Put up the welcome display and check-in card.',y)
y=section('5-15 minutes','Mount the ghost pets flat. Place the pumpkin on a stable staff-side surface, if it fits.',y)
y=section('15-25 minutes','Set out the seated activity and staff thank-you cards. Keep food and loose supplies controlled.',y)
y=section('25-30 minutes','Have a second team member walk through the space: entrances, carriers, seating, reception tools, and cleaning access. Remove anything that interferes.',y)
text('A 30-minute route is an estimate. A functioning front desk wins over a finished display.',48,y,500,16,ORANGE);end()

begin('Daily reset / two-minute walkthrough')
y=620
for s in ['Doors, exits, and required signs are clear.','No loose paper, cord, tape, or scraps are within patient reach.','Displays are stable and do not obstruct reception equipment.','Patients can settle without approaching decorations.','Shared activity supplies follow clinic policy.','Human food and waste remain inaccessible to pets.','Soiled or damaged paper has been replaced.','The quieter display plan can be used immediately.']:
    y=check(y,s)
y=section('When something fails','STOP the affected activity. REMOVE the problematic piece. REROUTE to a flat sign, seated page, or food-free note. RECHECK the replacement before returning it to use. Record the fix for next October.',y-15)
text('Date: __________  Checked by: __________<br/>Removed or changed: ______________________________',48,y,500,11)
end()

begin('Reprint, pack away, repeat')
y=section('Quick reprint index','Ghost pets: 8 • Welcome sign: 10 • Cone halves: 12-13<br/>Desk cards: 15 • Doodle display: 17 • Player sheet: 18 • Team cards: 20',620)
y=section('At the end of October','Remove tape according to the surface manufacturer\'s instructions. Discard soiled paper and damaged assemblies. Store clean templates flat, with supplies and a note of what worked. Keep scissors and small parts secured.',y)
y=section('Next-year notes','Best location: ___________________________________<br/><br/>Project worth repeating: __________________________<br/><br/>Project to simplify: ______________________________<br/><br/>Printer setting that worked: ______________________',y)
y=section('Use and scope','These original templates can be printed for your team\'s clinic activities. Do not treat this manual as permission to ignore local policies. Product licensing and distribution terms should be supplied separately by the seller.',y)
end()

begin('Research behind the design')
y=section('Evidence versus design','The sources below inform the hazard and patient-comfort constraints. They do not test or endorse these crafts. Project times, layouts, flat mounting, seated activities, and reset checks are TheVetCSR design choices.',620)
y=section('1 / AAHA','Halloween Safety for Pets: 5 Tips for Dogs and Cats. Updated August 21, 2026. Describes risks from food, noise, costumes, cords, and hanging decorations.<br/><link href="https://www.aaha.org/resources/how-to-have-a-pet-safe-halloween/">aaha.org/resources/how-to-have-a-pet-safe-halloween/</link>',y)
y=section('2 / Feline Veterinary Medical Association','2022 ISFM/AAFP Cat Friendly Veterinary Environment Guidelines. Supports reducing distress through changes to the veterinary environment and consideration of feline senses.<br/><link href="https://catvets.com/resource/isfm-aafp-cat-friendly-veterinary-environment-guidelines/">catvets.com/resource/isfm-aafp-cat-friendly-veterinary-environment-guidelines/</link>',y)
y=section('3 / University of Illinois Veterinary Medicine','Halloween Safety Tips for Pet Owners. Discusses decoration hazards and ensuring costumes do not interfere with vision, breathing, or movement.<br/><link href="https://vetmed.illinois.edu/pet-health-columns/halloween-pet-safety-2/">vetmed.illinois.edu/pet-health-columns/halloween-pet-safety-2/</link>',y)
text('Sources reviewed October 3, 2026. No clinical dosing or at-home emergency treatment instructions are included.',48,y,505,10)
end()
c.save()
assert page==24,page
print(OUT)
