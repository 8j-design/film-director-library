from pathlib import Path
p=Path(__file__).with_name('make_studio.py');t=p.read_text(encoding='utf-8').replace("default='v4'","default='v5'")
t=t.replace("(1.20,.50,.07),M['wood']", "(1.20,.50,.07),M['darkwood']")
t=t.replace("(504,origin),(558,(0,.66,0)),(624,(0,.66,0))", "(558,origin),(580,(0,.66,0)),(624,(0,.66,0))")
t=t.replace("bandt=smooth((f-558)/45)","bandt=smooth((f-580)/44)").replace("smooth((f-603)/21)","smooth((f-624)/24)")
t=t.replace("    if idx==1:hand=Vector((arm_side*.09,.16,1.035))", "    if idx==1:\n     h0=pp+lidpos+Vector((side*.49,-.10,.02)) if arm_side==-side else transform(roots0[idx],yaw,(arm_side*.22,-.28,.99))\n     hand=blend(h0,(arm_side*.09,.16,1.035),smooth((f-558)/22))")
old="for cx,cy,r in [(-.24,.01,.115),(.22,.015,.085)]:line('Original print bold orbit',[(cx+r*math.cos(t*math.pi/24),cy+r*.8*math.sin(t*math.pi/24),.018) for t in range(49)],.0015,M['blue'],pack)"
new="""for cx,cy,r in [(-.24,.01,.115),(.22,.015,.085)]:
 verts=[];faces=[]
 for j in range(48):
  angle=j*math.pi/24
  for rr in [r-.009,r+.009]:verts.append((cx+rr*math.cos(angle),cy+rr*.8*math.sin(angle),.0152))
 for j in range(48):faces.append((j*2,j*2+1,((j+1)%48)*2+1,((j+1)%48)*2))
 mesh=bpy.data.meshes.new('Flat printed orbit');mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new('Original print flat orbit',mesh);s.collection.objects.link(ob);ob.parent=pack;ob.data.materials.append(M['blue'])"""
assert old in t;t=t.replace(old,new)
p.write_text(t,encoding='utf-8')
