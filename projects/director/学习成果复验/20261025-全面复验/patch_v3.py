from pathlib import Path
p=Path(__file__).with_name('make_studio.py')
t=p.read_text(encoding='utf-8')
t=t.replace("default='v2'", "default='v3'")
t=t.replace("(1.35,.36,.08)","(1.35,.56,.08)")
t=t.replace(".0065,M['blue'],pack)",".001,M['blue'],pack)")
t=t.replace(".018,M['blue'],pack)",".0015,M['blue'],pack)")
t=t.replace("(0,0,.043)","(0,0,.067)").replace("bow.location=(0,0,.056)","bow.location=(0,.13,.08)")
t=t.replace(" return root,head,limbs", " upper=empty(name+' upper body pivot',root);upper.location=(0,0,.88)\n for ob in list(root.children):\n  if ob!=upper and ('shirt' in ob.name or 'button' in ob.name or 'neck' in ob.name or ob==head):\n   ob.parent=upper;ob.location.z-=.88\n return root,head,limbs,upper")
start=t.index(' return path(f,[(1,origin)');end=t.index('\ndef packstate',start)
t=t[:start]+''' keys=[(1,origin),(145,origin),(176,(side*.75,1.46,0)),(208,(side*.75,1.46,0)),(264,origin)]
 if idx==1:keys += [(360,origin),(400,(1.4,1.22,0)),(432,(1.4,1.22,0)),(504,(0,.66,0)),(624,(0,.66,0)),(660,(side*.60,.65,0))]
 else:keys += [(648,origin),(660,(side*.60,.65,0))]
 keys += [(696,(side*.60,.65,0)),(792,(-1.03+side*.58,1.80,0)),(850,(-1.03+side*.58,1.75,0)),(942,origin),(1080+idx*48,origin),(1176+idx*24,(-1.75,2.15,0)),(1236+idx*12,(-1.75,2.65,0)),(1296,(0,3.1,0)),(1440,(0,3.1,0))]
 return path(f,keys)'''+t[end:]
t=t.replace("(624,(0,0,.946)),(684,(0,.20,1.15))", "(648,(0,0,.946)),(660,(0,.20,.946)),(696,(0,.20,1.15))")
t=t.replace("lidangle=-math.radians(105)*smooth((f-432)/36)*(1-smooth((f-480)/78));key(lidhinge,loc=(0,.70*(1-smooth((f-432)/36))+.22,.026),rot=(lidangle,0,0))", "lidangle=0;lidpos=path(f,[(1,(1.4,1.94,-.156)),(400,(1.4,1.94,-.156)),(432,(1.4,1.94,.32)),(504,(0,.22,.32)),(558,(0,.22,.05)),(1440,(0,.22,.05))]);key(lidhinge,loc=lidpos,rot=(0,0,0))")
t=t.replace("for idx,(root,head,limbs) in enumerate(people)","for idx,(root,head,limbs,upper) in enumerate(people)")
t=t.replace("if 150<f<236:yaw=math.pi", "if 150<f<236:yaw=math.pi\n  if idx==1 and 380<f<433:yaw=math.pi")
t=t.replace("  key(root,rp,rot=(0,0,yaw))", "  bend=.20 if 289<f<696 else .08\n  if idx==1 and 380<f<433:bend=.72\n  if 176<f<270:bend=.12\n  key(root,rp,rot=(0,0,yaw));key(upper,rot=(bend,0,0))")
t=t.replace("(side*.16,-.18,.937)","(side*.45,.20,.937)")
t=t.replace("shoulder=transform(rp,yaw,(arm_side*.20,0,1.39));hand=transform(rp,yaw,(arm_side*.22,-.28,.99))", "shoulder=transform(rp,yaw,Vector((0,0,.88))+Matrix.Rotation(bend,3,'X')@Vector((arm_side*.20,0,.51)));hand=transform(rp,yaw,(arm_side*.22,-.28,.99))")
start=t.index('   elif 289<f<433:');end=t.index('   diff=hand-shoulder',start)
t=t[:start]+'''   elif idx==1 and 400<=f<558:
    hand=pp+lidpos+Vector((arm_side*.38,-.10,.02))
   elif 289<f<558 and arm_side==-side:hand=Vector((side*.48,.18,.98))
   elif 558<=f<624:
    if idx==1:hand=Vector((arm_side*.09,.16,1.035))
    elif arm_side==-side:hand=Vector((side*.48,.18,.98))
   elif 624<=f<660:
    if arm_side==-side:hand=pp+Vector((side*.49,.18,.04))
   elif 660<=f<792:hand=pp+pq@Vector((side*.49,arm_side*.09,.05))
   elif 792<=f<850:
    if idx==0:hand=blend(pp+pq@Vector((-.49,arm_side*.09,.05)),transform(rp,yaw,(arm_side*.22,-.24,1.0)),smooth((f-792)/24))
    elif arm_side==-side:hand=pp+pq@Vector((.43,.0,.05))
   elif 966+idx*36<=f<=1014+idx*36 and arm_side==-side:hand=keyp+Vector((0,0,.025))
   elif f>=1044+idx*48:hand=bpos+Matrix.Rotation(yaw,3,'Z')@Vector((arm_side*.17,-.05,.09))
'''+t[end:]
t=t.replace("if length>.70 and f%24==1:","if length>.70:")
t=t.replace("Both arm segments together measure 60cm.","Both arm segments together measure 70cm; test all baked frames.")
t=t.replace("Targets over 0.70m sampled each second", "Targets over 0.70m sampled every three frames")
p.write_text(t,encoding='utf-8')
