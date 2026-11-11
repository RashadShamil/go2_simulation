#!/usr/bin/env python3
"""Generate a lightweight office Gazebo SDF world and SVG floor plan.

Only Python standard-library modules are required.
Coordinates are in metres, with the room centred at (0,0).
"""
import argparse
import json
import math
import re
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent


def rgb(hexcode):
    s = hexcode.lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", s):
        raise ValueError(f"Invalid colour: {hexcode}")
    return " ".join(f"{int(s[i:i+2],16)/255:.4f}" for i in (0, 2, 4)) + " 1"


def box(world, name, xyz, size, colour, collision=True, visual_h=None):
    if min(size) <= 0:
        raise ValueError(f"Invalid size for {name}: {size}")
    model = ET.SubElement(world, "model", name=re.sub(r"[^A-Za-z0-9_]", "_", name))
    ET.SubElement(model, "static").text = "true"
    ET.SubElement(model, "pose").text = " ".join(map(str, (*xyz, 0, 0, 0)))
    link = ET.SubElement(model, "link", name="link")
    if collision:
        col = ET.SubElement(link, "collision", name="collision")
        ET.SubElement(ET.SubElement(ET.SubElement(col, "geometry"), "box"), "size").text = " ".join(map(str, size))
    visual = ET.SubElement(link, "visual", name="visual")
    vh = size[2] if visual_h is None else visual_h
    if vh != size[2]:
        ET.SubElement(visual, "pose").text = f"0 0 {(vh-size[2])/2} 0 0 0"
    ET.SubElement(ET.SubElement(ET.SubElement(visual, "geometry"), "box"), "size").text = f"{size[0]} {size[1]} {vh}"
    material = ET.SubElement(visual, "material")
    ET.SubElement(material, "ambient").text = rgb(colour)
    ET.SubElement(material, "diffuse").text = rgb(colour)


def build(cfg, sdf_path, svg_path):
    r = cfg["room"]
    w, d, h = (float(r[k]) for k in ("width_m", "depth_m", "height_m"))
    t = float(r["wall_thickness_m"])
    vh = float(r.get("wall_visual_height_m", h))
    door = float(r["door_center_x_m"])
    gap = float(r["door_width_m"])
    left, right = door-gap/2, door+gap/2
    if not (min(w, d, h, t, vh, gap) > 0 and vh <= h and -w/2 < left < right < w/2):
        raise ValueError("Invalid room or door dimensions")
    start = cfg["robot_start"]
    x0, y0 = float(start["x_m"]), float(start["y_m"])
    if not (-w/2+.5 < x0 < w/2-.5 and -d/2+.5 < y0 < d/2-.5):
        raise ValueError("Go2 start position lies outside safe office area")
    for item in cfg["furniture"]:
        x, y = map(float, item["center_m"])
        sx, sy, sz = map(float, item["size_m"])
        if min(sx,sy,sz)<=0 or abs(x)+sx/2 >= w/2-t or abs(y)+sy/2 >= d/2-t:
            raise ValueError(f"Invalid or out-of-bounds furniture: {item['name']}")
        if abs(x-x0)<sx/2+.43 and abs(y-y0)<sy/2+.30:
            raise ValueError(f"Go2 starts inside furniture: {item['name']}")
    sdf = ET.Element("sdf", version="1.8")
    world = ET.SubElement(sdf, "world", name="office_lab")
    physics = ET.SubElement(world, "physics", name="default", type="ignored")
    ET.SubElement(physics, "max_step_size").text = "0.001"
    ET.SubElement(physics, "real_time_factor").text = "1"
    ET.SubElement(world, "gravity").text = "0 0 -9.81"
    plugins = [("gz-sim-physics-system","Physics"),
               ("gz-sim-user-commands-system","UserCommands"),
               ("gz-sim-scene-broadcaster-system","SceneBroadcaster"),
               ("gz-sim-contact-system","Contact"),
               ("gz-sim-sensors-system","Sensors")]
    for filename, cls in plugins:
        p = ET.SubElement(world, "plugin", filename=filename, name="gz::sim::systems::"+cls)
        if cls == "Sensors":
            ET.SubElement(p, "render_engine").text = "ogre"
    sun = ET.SubElement(world, "light", name="sun", type="directional")
    ET.SubElement(sun, "pose").text = "0 0 6 0 0 0"
    ET.SubElement(sun, "diffuse").text = "0.9 0.9 0.9 1"
    ET.SubElement(sun, "specular").text = "0.1 0.1 0.1 1"
    ET.SubElement(sun, "direction").text = "-0.5 0.3 -0.8"
    # Flat collision plane + a thin visual-only floor. Both sit at world Z=0.
    ground=ET.SubElement(world,"model",name="ground_plane")
    ET.SubElement(ground,"static").text="true"
    link=ET.SubElement(ground,"link",name="link")
    for typ in ("collision","visual"):
        elem=ET.SubElement(link,typ,name=typ)
        plane=ET.SubElement(ET.SubElement(elem,"geometry"),"plane")
        ET.SubElement(plane,"normal").text="0 0 1"
        ET.SubElement(plane,"size").text="40 40"
    box(world,"office_floor",(0,0,0),(w,d,0.005),"#DFE4DB",collision=False)
    wall="#E0E5E9"
    box(world,"north_wall",(0,d/2,h/2),(w,t,h),wall,visual_h=vh)
    box(world,"west_wall",(-w/2,0,h/2),(t,d,h),wall,visual_h=vh)
    box(world,"east_wall",(w/2,0,h/2),(t,d,h),wall,visual_h=vh)
    box(world,"south_wall_left",((-w/2+left)/2,-d/2,h/2),(left+w/2,t,h),wall,visual_h=vh)
    box(world,"south_wall_right",((right+w/2)/2,-d/2,h/2),(w/2-right,t,h),wall,visual_h=vh)
    for item in cfg["furniture"]:
        x,y=map(float,item["center_m"])
        sx,sy,sz=map(float,item["size_m"])
        box(world,item["name"],(x,y,sz/2),(sx,sy,sz),item.get("color","#AAB3B6"))
    ET.indent(sdf, space="  ")
    sdf_path.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(sdf).write(sdf_path,encoding="unicode",xml_declaration=True)

    # Simple scalable floor-plan drawing. Real dimensions must be measured.
    scale=100
    pad=55
    X=lambda x: pad+(x+w/2)*scale
    Y=lambda y: pad+(d/2-y)*scale
    lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(w*scale+2*pad)}" height="{int(d*scale+2*pad)}">',
           '<rect width="100%" height="100%" fill="#f7f8fa"/>',
           f'<rect x="{pad}" y="{pad}" width="{w*scale}" height="{d*scale}" fill="#e3e9e0" stroke="#52636c" stroke-width="6"/>']
    for item in cfg["furniture"]:
        x,y=map(float,item["center_m"])
        sx,sy,_=map(float,item["size_m"])
        lines.append(f'<rect x="{X(x-sx/2)}" y="{Y(y+sy/2)}" width="{sx*scale}" height="{sy*scale}" fill="{escape(item.get("color","#aab3b6"))}" stroke="#4e6170"/>')
        lines.append(f'<text x="{X(x)}" y="{Y(y)}" font-size="12" text-anchor="middle">{escape(item["name"])}</text>')
    lines.append(f'<circle cx="{X(x0)}" cy="{Y(y0)}" r="14" fill="#e77949"/>')
    lines.append(f'<text x="{X(x0)}" y="{Y(y0)+30}" font-size="14" text-anchor="middle">Go2 start</text>')
    lines.append(f'<line x1="{X(left)}" y1="{Y(-d/2)}" x2="{X(right)}" y2="{Y(-d/2)}" stroke="#1c9a78" stroke-width="8"/>')
    lines.append("</svg>")
    svg_path.write_text("\n".join(lines),encoding="utf-8")
    print("SDF:",sdf_path)
    print("Floorplan:",svg_path)
    print(f"Start pose: {x0}, {y0}, yaw={start.get('yaw_deg',0)} deg")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config",type=Path,default=ROOT/"config/office_example.json")
    parser.add_argument("--sdf",type=Path,default=ROOT/"worlds/office_lab.sdf")
    parser.add_argument("--svg",type=Path,default=ROOT/"worlds/office_floorplan.svg")
    args=parser.parse_args()
    build(json.loads(args.config.read_text()),args.sdf,args.svg)


if __name__=="__main__":
    main()
