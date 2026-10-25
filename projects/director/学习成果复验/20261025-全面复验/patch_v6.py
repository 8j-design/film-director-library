from pathlib import Path
p=Path(__file__).with_name('make_studio.py');t=p.read_text(encoding='utf-8').replace("default='v5'","default='v6'")
t=t.replace("finalrot=Matrix(((0,-1,0),(0,0,-1),(1,0,0))).to_quaternion()", "finalrot=(Matrix.Rotation(-.10,3,'X')@Matrix(((0,-1,0),(0,0,-1),(1,0,0)))).to_quaternion()")
t=t.replace("(-1.03,1.66,.59)","(-1.03,1.895,.574)")
start=t.index(' if idx==1:keys +=');end=t.index(' keys += [(696',start)
t=t[:start]+" keys += [(558,origin),(624,(side*.35,.66,0)),(648,(side*.35,.66,0)),(660,(side*.60,.65,0))]\n"+t[end:]
t=t.replace("band=cube('Blue cotton band',(0,0,.067),(.037,.45,.007),M['blue'],pack,.002)","bandmesh=bpy.data.meshes.new('Persistent full ribbon mesh');bandmesh.from_pydata([(0,0,0)]*12,[],[(i*2,i*2+1,i*2+3,i*2+2) for i in range(5)]);bandmesh.update();band=bpy.data.objects.new('Blue cotton band',bandmesh);s.collection.objects.link(band);band.parent=pack;band.data.materials.append(M['blue'])\nbandbasis=band.shape_key_add(name='Basis')\n# One baked shape per sampled instant: full ribbon changes position instead of growing from nothing.\n")
t=t.replace("bandt=smooth((f-580)/44);key(band,scale=(1,max(.001,bandt),1));key(bow,scale=(max(.001,smooth((f-624)/24)),)*3)","bandt=smooth((f-580)/44);rise=smooth((f-580)/22);fold=smooth((f-602)/22);tipx=.78*(1-rise)+(.575*(1-fold)+.015*fold)*rise;tipz=-.012+.095*rise-.016*fold;edgez=-.012+.080*rise\n ribbonpath=[(-tipx,tipz),(-.575,edgez),(-.575,-.012),(.575,-.012),(.575,edgez),(tipx,tipz)]\n shape=band.shape_key_add(name='Frame_%04d'%f)\n for j,(xx,zz) in enumerate(ribbonpath):\n  shape.data[j*2].co=(xx,.112,zz);shape.data[j*2+1].co=(xx,.148,zz)\n shape.value=0;shape.keyframe_insert('value',frame=f-3);shape.value=1;shape.keyframe_insert('value',frame=f);shape.value=0;shape.keyframe_insert('value',frame=f+3)\n key(bow,scale=(max(.001,smooth((f-624)/24)),)*3)")
t=t.replace("  key(head,rot=(.20 if f<624 else .08,0,-side*.25 if 320<f<400 else 0))", "  hz=0;pitch=.20 if f<624 else .08\n  if idx==1 and 300<f<340:hz=-.40\n  if idx==0 and 320<f<366:hz=.35\n  if 350<f<420:pitch=.32\n  key(head,rot=(pitch,0,hz))")
t=t.replace("   elif 289<f<558 and arm_side==-side:hand=Vector((side*.48,.18,.98))", "   elif 289<f<400 and arm_side==-side:\n    reach=smooth((f-(330 if idx==0 else 360))/20);hand=blend(hand,(side*.48,.18,.98),reach)\n    hand=blend(hand,pp+lidpos+Vector((side*.49,-.10,.02)),smooth((f-380)/20))")
start=t.index('   elif 558<=f<624:');end=t.index('   elif 660<=f<792:',start)
t=t[:start]+'''   elif 558<=f<660:
    if arm_side==-side:
     h0=pp+lidpos+Vector((side*.49,-.10,.02))
     tip=pp+Vector((side*tipx,.13,tipz+.025))
     hand=blend(h0,tip,smooth((f-558)/22))
     if f>=648:hand=blend(hand,pp+Vector((side*.49,.09,.05)),smooth((f-648)/12))
    else:hand=transform(rp,yaw,(arm_side*.22,-.28,.99))
'''+t[end:]
t=t.replace("48,arm_side", "48,arm_side")
p.write_text(t,encoding='utf-8')
