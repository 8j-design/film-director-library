"""Create a small native SVG plan, reread it, edit one attribute, audit the diff.

No rendering, image editing, DCC import, or animation is performed.
"""
from pathlib import Path
import copy
import hashlib
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def el(parent, tag, attrs=None, text=None):
    node = ET.SubElement(parent, f"{{{SVG}}}{tag}", attrs or {})
    if text is not None:
        node.text = text
    return node


def label(parent, x, y, text, size=14, **attrs):
    return el(parent, "text", {"x": str(x), "y": str(y), "font-size": str(size), **attrs}, text)


def rect(parent, ident, x, y, w, h, **attrs):
    return el(parent, "rect", {"id": ident, "x": str(x), "y": str(y),
                             "width": str(w), "height": str(h), **attrs})


def use(parent, ident, href, x=0, y=0, **attrs):
    return el(parent, "use", {"id": ident, "href": "#" + href,
                             "x": str(x), "y": str(y), **attrs})


def anchor(parent, ident, x, y, title):
    group = el(parent, "g", {"id": ident, "transform": f"translate({x} {y})"})
    el(group, "path", {"d": "M -9 0 H 9 M 0 -9 V 9", "stroke": "#485a66", "stroke-width": "2"})
    label(group, -24, -15, title, 11)


def write(root, path):
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


root = ET.Element(f"{{{SVG}}}svg", {"width": "1560", "height": "830", "viewBox": "0 0 1560 830",
    "role": "img", "aria-labelledby": "title description", "font-family": "Microsoft YaHei, sans-serif"})
el(root, "title", {"id": "title"}, "最后一张：三状态平面布局与同尺对象索引 v1")
el(root, "desc", {"id": "description"},
   "辅助布局，不是人物美术、动画或图板验收。尺寸均为提案单位，未测量图板或现实房间。第三视图是第五至第六节拍后的门旁包件状态。")
metadata = {
    "basis": "测试前提与判据-v1.md；助手自拟练习《最后一张》",
    "measurement_status": "assumed relative design units; no physical measurement; not matched to generated board",
    "scale": "same plan scale in all 3 panels: 0.75 screen units per layout unit",
    "room": [600, 420], "door_width": 80, "table": [190, 84],
    "print_face": [160, 48], "package_face": [164, 52], "package_thickness_assumed": 8,
    "person_relative_height_reference": {"C_A": 100, "C_B": 96},
    "person_note": "heights are comparison baselines, not portrait designs or physical dimensions",
    "private_box": [32, 24],
    "package_state_note": "table package face 164x52; wall-leaning upright package footprint 52x8, height164; no transition animation",
    "source_read": ["Krita Storyboard Docker", "Godot Model export considerations", "Godot Advanced Import Settings"],
}
el(root, "metadata", {"id": "layout_metadata"}, json.dumps(metadata, ensure_ascii=False))
rect(root, "page", 0, 0, 1560, 830, fill="#f7f5ee")
label(root, 30, 35, "《最后一张》布局辅助：固定房间 + 对象状态；不代替主美术", 22)
label(root, 30, 62, "全为假设布局单位 u，未量取图板／现实尺寸；三视图同尺。十字只是位置锚点，不是人物模型。", 15)

defs = el(root, "defs")
arrow = el(defs, "marker", {"id": "arrow", "markerWidth": "8", "markerHeight": "8",
    "refX": "7", "refY": "4", "orient": "auto", "markerUnits": "strokeWidth"})
el(arrow, "path", {"d": "M0 0 L8 4 L0 8 Z", "fill": "#737f83"})
room = el(defs, "g", {"id": "ROOM_FIXED"})
rect(room, "ROOM_BOUNDARY", 0, 0, 600, 420, fill="#ede9de", stroke="#505b60", **{"stroke-width": "4"})
# Bottom-right door opening: 80 units. Window and table stay shared by all views.
el(room, "path", {"id": "DOOR_01", "d": "M460 420 H540 M540 420 V340 M460 420 A80 80 0 0 1 540 340",
    "fill": "none", "stroke": "#8d877c", "stroke-width": "2"})
el(room, "line", {"x1": "460", "y1": "420", "x2": "540", "y2": "420", "stroke": "#f7f5ee", "stroke-width": "6"})
label(room, 460, 449, "门80u", 14)
el(room, "path", {"id": "WINDOW_01", "d": "M80 0 H230 M80 5 H230", "stroke": "#718e9b", "stroke-width": "5"})
label(room, 105, 25, "固定窗", 14)
rect(room, "TABLE_01", 190, 155, 190, 84, fill="#d3c4ac", stroke="#8b7c68", **{"stroke-width": "2"})
label(room, 221, 259, "工作台190×84u", 14)
el(room, "path", {"id": "PLAN_SCALE", "d": "M20 400 H120 M20 395 V405 M120 395 V405", "stroke": "#505b60", "stroke-width": "2"})
label(room, 30, 388, "100u标尺", 13)

paper = el(defs, "g", {"id": "PRINT_FACE", "data-width": "160", "data-height": "48"})
rect(paper, "PRINT_SIZE", 0, 0, 160, 48, fill="#f9f7ed", stroke="#797463", **{"stroke-width": "1.5"})
el(paper, "path", {"d": "M12 14 H145 M12 27 H136 M18 38 H149", "stroke": "#646b68", "stroke-width": "2"})
face = el(defs, "g", {"id": "PACKAGE_FACE", "data-width": "164", "data-height": "52"})
rect(face, "PACKAGE_FACE_SIZE", 0, 0, 164, 52, fill="#b8a588", stroke="#776d5c", **{"stroke-width": "1.5"})
rect(face, "PACKAGE_FACE_BAND", 102, 0, 7, 52, fill="currentColor")
standing = el(defs, "g", {"id": "PACKAGE_UPRIGHT_FOOTPRINT", "data-width": "52", "data-depth": "8", "data-height": "164"})
rect(standing, "PACKAGE_FOOTPRINT_SIZE", 0, 0, 52, 8, fill="#b8a588", stroke="#776d5c", **{"stroke-width": "1.5"})
rect(standing, "PACKAGE_FOOTPRINT_BAND", 31, 0, 5, 8, fill="currentColor")
box = el(defs, "g", {"id": "PRIVATE_BOX", "data-width": "32", "data-depth": "24"})
rect(box, "PRIVATE_BOX_SIZE", 0, 0, 32, 24, fill="#c8beaa", stroke="#776d5c", **{"stroke-width": "1.5"})
el(box, "path", {"d": "M16 0 V24 M0 12 H32", "stroke": "#877c68", "stroke-width": "1"})

panels = []
for n, title in enumerate(("A｜节拍1—3：原纸与私人箱", "B｜节拍4：同一纸张完成包装", "C｜节拍5—6：人箱离开、包件留下")):
    x = 30 + n * 510
    label(root, x, 101, title, 17)
    panel = el(root, "g", {"id": f"STATE_{'ABC'[n]}", "transform": f"translate({x} 125) scale(0.75)"})
    use(panel, f"ROOM_{'ABC'[n]}", "ROOM_FIXED")
    panels.append(panel)

use(panels[0], "PRINT_01", "PRINT_FACE", 208, 172)
for i in (0, 1):
    anchor(panels[i], f"C_A_{i}", 160, 190, "C_A")
    anchor(panels[i], f"C_B_{i}", 414, 220, "C_B")
    use(panels[i], f"BOX_A_{i}", "PRIVATE_BOX", 110, 260)
    use(panels[i], f"BOX_B_{i}", "PRIVATE_BOX", 425, 274)
    label(panels[i], 100, 307, "BOX_A", 12)
    label(panels[i], 417, 319, "BOX_B", 12)
use(panels[1], "PACK_01_TABLE", "PACKAGE_FACE", 206, 170, color="#1e3a5f", **{"data-object": "PACK_01"})
el(panels[1], "path", {"id": "PACK_TRANSFER_PATH", "d": "M288 205 L412 275 L412 370 L401 401",
    "fill": "none", "stroke": "#737f83", "stroke-width": "2", "stroke-dasharray": "7 5", "marker-end": "url(#arrow)"})
label(panels[1], 371, 348, "拟搬运路径", 13)
package_final = el(panels[2], "g", {"id": "PACK_01", "transform": "translate(375 400)",
    "color": "#1e3a5f", "data-object": "PACK_01", "data-state": "upright-leaning-at-door", "data-measurement": "assumed"})
use(package_final, "PACK_01_FOOTPRINT", "PACKAGE_UPRIGHT_FOOTPRINT")
label(panels[2], 288, 375, "PACK_01立靠门左侧", 14)
label(panels[2], 260, 395, "占地52×8u；高164u", 13)

label(root, 30, 505, "对象尺寸索引（同一单位，不是实测）：原纸160×48u；包装面164×52u；私人箱占地32×24u。", 16)
use(root, "PRINT_REFERENCE", "PRINT_FACE", 35, 535)
use(root, "PACK_REFERENCE", "PACKAGE_FACE", 235, 533, color="#1e3a5f")
label(root, 35, 607, "原纸：保留同一长宽识别", 14)
label(root, 235, 607, "纸板包件：四周2u余量（提案）", 14)
el(root, "path", {"id": "HEIGHT_REFERENCE_A", "d": "M500 535 V635 M494 535 H506 M494 635 H506", "stroke": "#617c83", "stroke-width": "2"})
el(root, "path", {"id": "HEIGHT_REFERENCE_B", "d": "M585 539 V635 M579 539 H591 M579 635 H591", "stroke": "#877864", "stroke-width": "2"})
label(root, 465, 656, "C_A高100u", 13)
label(root, 558, 656, "C_B高96u", 13)
label(root, 690, 556, "位置十字不表示肩宽、脚印或接触；身高线仅供尺寸比较。", 15)
label(root, 690, 583, "C是立靠状态，俯视只见52×8u占地；包装本体尺寸未变。", 15)
label(root, 690, 610, "A→B→C只是状态与路径提案，未验证抬起、转向、重量或碰撞。", 15)
label(root, 30, 707, "固定门/窗/桌由一个共享ROOM_FIXED定义复用；并非与生成图板量测配准。", 15)
label(root, 30, 737, "不证明可直接导入Blender/Godot，不包含骨骼、真实材质、动作接触、时间或声轨。", 15)
label(root, 30, 767, "本SVG只作平面位置、尺寸与对象状态辅助；主美术由另行生成并审查的叙事板承担。", 15)
label(root, 30, 797, "修改演示v2仅改变最终PACK_01的深蓝带颜色；不是新增剧情或已完成视觉验收。", 14)

original = ROOT / "space_plan.svg"
modified = ROOT / "space_plan_pack_edit.svg"
write(root, original)

# Required real edit: parse the saved original from disk; modify one target attribute.
reread = ET.parse(original).getroot()
target = reread.find(".//*[@id='PACK_01']")
assert target is not None
assert target.attrib["color"] == "#1e3a5f"
target.set("color", "#274f7d")
write(reread, modified)

# Compare separately parsed saved files; do not trust the in-memory construction.
a, b = ET.parse(original).getroot(), ET.parse(modified).getroot()
nodes_a, nodes_b = list(a.iter()), list(b.iter())
assert len(nodes_a) == len(nodes_b)
changes = []
for i, (left, right) in enumerate(zip(nodes_a, nodes_b)):
    assert left.tag == right.tag
    assert (left.text or "") == (right.text or "")
    for attr in sorted(set(left.attrib) | set(right.attrib)):
        if left.get(attr) != right.get(attr):
            changes.append({"element_index": i, "id": left.get("id"), "attribute": attr,
                            "before": left.get(attr), "after": right.get(attr)})
expected = [{"id": "PACK_01", "attribute": "color", "before": "#1e3a5f", "after": "#274f7d"}]
assert [{k: d[k] for k in expected[0]} for d in changes] == expected

ids = [x.get("id") for x in nodes_a if x.get("id")]
assert len(ids) == len(set(ids)), "duplicate SVG IDs"
for node in nodes_a:
    href = node.get("href", "")
    assert not href or (href.startswith("#") and href[1:] in ids), href

fixed_ids = ["ROOM_FIXED", "DOOR_01", "WINDOW_01", "TABLE_01", "PLAN_SCALE", "PRINT_SIZE",
             "PACKAGE_FACE_SIZE", "PACKAGE_FOOTPRINT_SIZE", "PRIVATE_BOX_SIZE", "HEIGHT_REFERENCE_A", "HEIGHT_REFERENCE_B"]
checks = {}
for ident in fixed_ids:
    left = a.find(f".//*[@id='{ident}']")
    right = b.find(f".//*[@id='{ident}']")
    checks[ident] = ET.tostring(left) == ET.tostring(right)
assert all(checks.values())
meta_a = json.loads(a.find(".//*[@id='layout_metadata']").text)
meta_b = json.loads(b.find(".//*[@id='layout_metadata']").text)
assert meta_a == meta_b

result = {
    "status": "pass_structural_edit_check_only",
    "original": original.name, "edited": modified.name,
    "sha256_original": sha(original), "sha256_edited": sha(modified),
    "operation": "reread_original_from_disk_then_change_only_PACK_01_color",
    "element_count": len(nodes_a), "unique_ids": len(ids), "actual_changes": changes,
    "fixed_and_dimension_elements_unchanged": checks,
    "metadata_dimensions_unchanged": meta_a == meta_b,
    "hrefs": "internal references only; all target IDs exist; no external files or scripts",
    "not_verified": ["visual rendering", "generated-board alignment", "animation", "contact", "collision", "DCC import", "viewer feedback"],
}
(ROOT / "layout_edit_verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": result["status"], "elements": len(nodes_a), "changes": changes,
                  "fixed_checks": len(checks), "original": str(original), "edited": str(modified)}, ensure_ascii=False))
