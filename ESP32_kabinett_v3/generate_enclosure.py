"""FeelingsPanel enclosure v3.0.0, inspired by the supplied reference image.

Run with Python 3.12+: pip install numpy trimesh manifold3d matplotlib scipy
No dimensions are inferred as measured dimensions from the illustration.
STL files are exported in their printing orientation, with minimum Z = 0.
"""
from pathlib import Path
import json
import math
import numpy as np
import trimesh

HERE = Path(__file__).resolve().parent
VERSION = "3.0.0"
P = {
    "width": 82.0, "height": 126.0, "depth": 36.0,
    "corner_radius": 8.0, "front_edge_radius": 1.4,
    "wall": 2.4, "front_structure_depth": 9.3,
    "back_thickness": 2.4, "skirt_depth": 4.0,
    "fit_clearance_per_side": 0.30, "skirt_wall": 1.6,
    "display_center_y": 12.0,
    "display_window_w": 33.5, "display_window_h": 43.5,
    "display_pocket_w": 41.5, "display_pocket_h": 66.5,
    "display_front_lip": 2.0,
    "button_center_y": -48.0, "button_hole_d": 12.3,
    "button_nut_clearance_d": 22.0, "button_panel_thickness": 2.4,
    "led_outer_w": 67.0, "led_outer_h": 91.0, "led_outer_r": 8.0,
    "led_inner_w": 45.0, "led_inner_h": 69.0, "led_inner_r": 4.0,
    "led_channel_depth": 7.5, "diffuser_thickness": 1.2,
    "diffuser_clearance_per_side": 0.25,
    "usb_center_y": -27.0, "usb_center_depth": 22.0,
    "usb_opening_y": 14.0, "usb_opening_depth": 8.0,
    "boss_radius": 4.0, "boss_x": 33.5, "boss_y": 55.5,
    "screw_pilot_d": 2.0, "screw_clearance_d": 2.8,
    "screw_head_d": 5.5, "pilot_depth": 9.0,
}


def box(w, h, depth, x=0, y=0, z=0):
    mesh = trimesh.creation.box(extents=[w, h, depth])
    mesh.apply_translation([x, y, z + depth / 2])
    return mesh


def rr_points(w, h, r, segments=32):
    """CCW rounded rectangle, with corresponding vertices at every section."""
    pts = []
    for cx, cy, start in [(w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90),
                          (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)]:
        for a in np.linspace(start, start+90, segments, endpoint=False):
            angle = math.radians(a)
            pts.append([cx + r*math.cos(angle), cy + r*math.sin(angle)])
    return np.array(pts)


def loft_contours(contours, heights):
    n = len(contours[0])
    vertices = np.vstack([np.column_stack([xy, np.full(n, z)])
                          for xy, z in zip(contours, heights)])
    faces = []
    for k in range(len(contours)-1):
        for i in range(n):
            j = (i+1) % n
            a, b, c, d = k*n+i, k*n+j, (k+1)*n+j, (k+1)*n+i
            faces.extend([[a,b,c], [a,c,d]])
    # Convex section caps. Fan triangles without extra centre vertices.
    for i in range(1, n-1):
        faces.append([0, i+1, i])
        start = (len(contours)-1)*n
        faces.append([start, start+i, start+i+1])
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
    assert mesh.is_watertight and mesh.volume > 0
    return mesh


def rr(w, h, r, depth, x=0, y=0, z=0):
    xy = rr_points(w, h, r)
    result = loft_contours([xy,xy], [z,z+depth])
    result.apply_translation([x,y,0])
    return result


def edge_rounded_solid(w, h, r, depth, edge):
    heights = list(np.linspace(0, edge, 13)) + [depth]
    contours = []
    for z in heights:
        inset = edge-math.sqrt(max(0.0, edge**2-(edge-min(z,edge))**2))
        contours.append(rr_points(w-2*inset, h-2*inset, r-inset))
    return loft_contours(contours, heights)


def cyl(radius, depth, x=0, y=0, z=0):
    result = trimesh.creation.cylinder(radius=radius, height=depth, sections=96)
    result.apply_translation([x,y,z+depth/2])
    return result


def cone_frustum(r0, r1, depth, x=0, y=0, z=0):
    angles = np.linspace(0,2*np.pi,96,endpoint=False)
    xy = np.column_stack([np.cos(angles),np.sin(angles)])
    result = loft_contours([r0*xy,r1*xy],[z,z+depth])
    result.apply_translation([x,y,0])
    return result


def union(*meshes):
    return trimesh.boolean.union(list(meshes), engine="manifold")


def subtract(mesh, *cutters):
    return trimesh.boolean.difference([mesh,*cutters],engine="manifold")


def ring(ow,oh,outer_r,iw,ih,inner_r,depth,y=0,z=0):
    return subtract(rr(ow,oh,outer_r,depth,y=y,z=z),
                    rr(iw,ih,inner_r,depth+2,y=y,z=z-1))


def build():
    p=P; w=p['width']; h=p['height']; wall=p['wall']
    shell_depth=p['depth']-p['back_thickness']; sy=p['display_center_y']
    bosses=[(x,y) for x in [-p['boss_x'],p['boss_x']]
                   for y in [-p['boss_y'],p['boss_y']]]
    outer=edge_rounded_solid(w,h,p['corner_radius'],shell_depth,p['front_edge_radius'])
    cavity=rr(w-2*wall,h-2*wall,p['corner_radius']-wall,
              shell_depth+1,z=p['front_structure_depth'])
    shell=subtract(outer,cavity)
    columns=[cyl(p['boss_radius'],shell_depth-p['front_structure_depth'],x,y,
                 p['front_structure_depth']) for x,y in bosses]
    shell=union(shell,*columns)
    # Recess, rather than a through slot: its 1.8 mm floor joins the screen island
    # to the shell and supports four ordinary front-facing 10 mm LED segments.
    led_cavity=ring(p['led_outer_w'],p['led_outer_h'],p['led_outer_r'],
                    p['led_inner_w'],p['led_inner_h'],p['led_inner_r'],
                    p['led_channel_depth']+1,y=sy,z=-1)
    screen_window=rr(p['display_window_w'],p['display_window_h'],0.5,
                     p['front_structure_depth']+2,y=sy,z=-1)
    screen_pocket=rr(p['display_pocket_w'],p['display_pocket_h'],0.8,
                     p['front_structure_depth']+1,y=sy,z=p['display_front_lip'])
    button=cyl(p['button_hole_d']/2,p['front_structure_depth']+2,
               y=p['button_center_y'],z=-1)
    button_nut=cyl(p['button_nut_clearance_d']/2,p['front_structure_depth']+1,
                   y=p['button_center_y'],z=p['button_panel_thickness'])
    # Small opening for the cable connector in the right hand wall.
    port=rr(p['usb_opening_depth'],p['usb_opening_y'],2.0,wall+6)
    port.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
    port.apply_translation([w/2-wall-3,p['usb_center_y'],p['usb_center_depth']])
    pilots=[cyl(p['screw_pilot_d']/2,p['pilot_depth']+1,x,y,
                shell_depth-p['pilot_depth']) for x,y in bosses]
    wires=[cyl(1.8,4,x,-28,z=7) for x in [-18,18]]
    shell=subtract(shell,led_cavity,screen_window,screen_pocket,
                   button,button_nut,port,*pilots,*wires)

    # Rear cover is built back down on the bed; its skirt points upward.
    back=edge_rounded_solid(w,h,p['corner_radius'],p['back_thickness'],0.8)
    clearance=p['fit_clearance_per_side']
    sw=w-2*wall-2*clearance; sh=h-2*wall-2*clearance
    sr=p['corner_radius']-wall-clearance; skirt_t=p['skirt_wall']
    skirt=ring(sw,sh,sr,sw-2*skirt_t,sh-2*skirt_t,sr-skirt_t,
               p['skirt_depth']+0.2,z=p['back_thickness']-0.2)
    boss_reliefs=[cyl(p['boss_radius']+0.5,8,x,y) for x,y in bosses]
    skirt=subtract(skirt,*boss_reliefs)
    back=union(back,skirt)
    holes=[cyl(p['screw_clearance_d']/2,9,x,y,z=-1) for x,y in bosses]
    countersinks=[cone_frustum(p['screw_head_d']/2,p['screw_clearance_d']/2,
                               1.45,x,y,z=-0.05) for x,y in bosses]
    back=subtract(back,*holes,*countersinks)

    dc=p['diffuser_clearance_per_side']
    diffuser=ring(p['led_outer_w']-2*dc,p['led_outer_h']-2*dc,
                  p['led_outer_r']-dc,p['led_inner_w']+2*dc,
                  p['led_inner_h']+2*dc,p['led_inner_r']+dc,
                  p['diffuser_thickness'],y=sy)
    # Shallow coupon reproduces the real ring fit and button mounting plate.
    coupon=rr(34,26,3,3.0)
    coupon=subtract(coupon,cyl(p['button_hole_d']/2,5,x=-7,z=-1),
                    box(4.0,15,2.4,x=10,z=0.6))
    coupon_insert=box(3.5,14.5,1.2,x=10)
    return {'01_Hus_og_front.stl':shell,'02_Baklokk.stl':back,
            '03_Lysdiffusor.stl':diffuser,
            '04_Provebit_knapp_og_passning.stl':coupon,
            '05_Provebit_innlegg.stl':coupon_insert}


def assembled(parts):
    shell=parts['01_Hus_og_front.stl'].copy()
    back=parts['02_Baklokk.stl'].copy()
    # Rotation gives an orientation-preserving transform with outside rear up.
    back.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[1,0,0]))
    back.apply_translation([0,0,P['depth']])
    # Cover is symmetric under Y reflection, so all four screw holes align.
    diffuser=parts['03_Lysdiffusor.stl'].copy()
    return {'hus':shell,'baklokk':back,'diffusor':diffuser}


def validate(parts,assembly):
    results={}
    for name,mesh in parts.items():
        assert mesh.is_watertight, name+' is not watertight'
        assert mesh.is_winding_consistent, name+' has inconsistent normals'
        assert mesh.volume>0, name+' has nonpositive volume'
        assert len(mesh.split())==1,name+' is not one connected solid'
        assert abs(mesh.bounds[0,2])<0.001,name+' is not on the print bed'
        results[name]={'watertight':True,'consistent_normals':True,
                       'connected_solids':1,'triangles':len(mesh.faces),
                       'bounds_mm':mesh.bounds.round(3).tolist(),
                       'dimensions_mm':mesh.extents.round(3).tolist(),
                       'volume_cm3':round(mesh.volume/1000,3)}
    overlaps={}
    names=list(assembly)
    for i,a in enumerate(names):
        for b in names[i+1:]:
            overlap=trimesh.boolean.intersection([assembly[a],assembly[b]],engine='manifold')
            volume=0 if overlap is None or overlap.is_empty else overlap.volume
            assert volume<0.005,f'{a}/{b} overlap: {volume} mm^3'
            overlaps[f'{a}/{b}']=round(float(volume),6)
    # Prove that the screen, button and side connector apertures are open.
    probes={
      'screen_clearance':rr(P['display_window_w']-0.2,P['display_window_h']-0.2,0.6,
                            P['front_structure_depth']+1,y=P['display_center_y'],z=-0.1),
      'button_clearance':cyl(P['button_hole_d']/2-0.1,P['front_structure_depth']+1,
                              y=P['button_center_y'],z=-0.1),
      'pcb_envelope':rr(41.3,66.3,1.0,4.5,y=P['display_center_y'],z=2.1),
      'led_left':box(10,66,2,x=-28,y=12,z=5.5),
      'led_right':box(10,66,2,x=28,y=12,z=5.5),
      'led_top':box(50,10,2,y=52,z=5.5),
      'led_bottom':box(50,10,2,y=-28,z=5.5),
    }
    functional={}
    for name,probe in probes.items():
        hit=trimesh.boolean.intersection([parts['01_Hus_og_front.stl'],probe],engine='manifold')
        volume=0 if hit is None or hit.is_empty else float(hit.volume)
        assert volume<0.005,name+' obstructed'
        functional[name+'_obstruction_mm3']=round(volume,6)
    port_probe=rr(7.8,13.8,2.1,6)
    port_probe.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
    port_probe.apply_translation([37,P['usb_center_y'],P['usb_center_depth']])
    hit=trimesh.boolean.intersection([parts['01_Hus_og_front.stl'],port_probe],engine='manifold')
    volume=0 if hit is None or hit.is_empty else float(hit.volume)
    assert volume<0.005,'side USB opening obstructed'
    functional['usb_aperture_obstruction_mm3']=round(volume,6)
    return {'design_version':VERSION,'parts':results,'assembly_overlap_mm3':overlaps,
            'functional_checks':functional,'parameters_mm':P,
            'physical_test_printed':False}


def main():
    parts=build()
    assembly=assembled(parts)
    report=validate(parts,assembly)
    for name,mesh in parts.items():
        mesh.export(HERE/name)
    scene=trimesh.Scene()
    for key,mesh in assembly.items():
        mesh.visual.face_colors={'hus':[235,236,231,255],
                                 'baklokk':[221,223,218,255],
                                 'diffusor':[111,222,211,255]}[key]
        scene.add_geometry(mesh,node_name=key,geom_name=key)
    scene.export(HERE/'Sammenstilling_for_visning.glb')
    (HERE/'kontrollrapport.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (HERE/'maal_og_parametere.json').write_text(json.dumps(P,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
