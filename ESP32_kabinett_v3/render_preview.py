"""Render the actual exported STL surfaces; hardware is labelled illustration only."""
from pathlib import Path
import time
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

HERE = Path(__file__).resolve().parent

def load(name):
    return trimesh.load(HERE / name, force='mesh')

def box(extents, center):
    m = trimesh.creation.box(extents=extents)
    m.apply_translation(center)
    return m

def disk(radius, height, center):
    m = trimesh.creation.cylinder(radius=radius, height=height, sections=96)
    m.apply_translation(center)
    return m

def draw(ax, items, elev=17, azim=-66, span=155, center=(0,13,0)):
    # Actual orthographic triangle rasterizer, with a per-pixel depth buffer.
    # Painter sorting cannot correctly render overlapping cap triangulations.
    size=1400
    pixels=np.empty((size,size,3),dtype=np.uint8); pixels[:]=[243,244,242]
    zbuffer=np.full((size,size),np.inf,dtype=np.float64)
    camera=np.array([.40,.22,-1.0]); camera/=np.linalg.norm(camera)
    forward=-camera
    right=np.cross([0,1,0],forward); right/=np.linalg.norm(right)
    up=np.cross(forward,right); up/=np.linalg.norm(up)
    basis=np.column_stack([right,up,forward])
    light=np.array([-.4,.75,-.85]); light/=np.linalg.norm(light)
    target=np.array([0.,0.,15.])
    for mesh, color in items:
        projected=(mesh.vertices-target) @ basis
        projected[:,:2]*=size/span
        projected[:,0]+=size/2
        projected[:,1]=size/2-projected[:,1]
        ts=projected[mesh.faces]
        normals=mesh.face_normals
        intensity=.65+.33*np.maximum(normals @ light,0)
        base=np.array(matplotlib.colors.to_rgb(color))
        cs=(np.clip(base[None,:]*intensity[:,None],0,1)*255).astype(np.uint8)
        for tri,facecolor in zip(ts,cs):
            xmin=max(0,int(np.floor(tri[:,0].min()))); xmax=min(size-1,int(np.ceil(tri[:,0].max())))
            ymin=max(0,int(np.floor(tri[:,1].min()))); ymax=min(size-1,int(np.ceil(tri[:,1].max())))
            if xmax<xmin or ymax<ymin: continue
            x0,y0,z0=tri[0]; x1,y1,z1=tri[1]; x2,y2,z2=tri[2]
            denom=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
            if abs(denom)<1e-8: continue
            xx=np.arange(xmin,xmax+1,dtype=float)[None,:]+.5
            yy=np.arange(ymin,ymax+1,dtype=float)[:,None]+.5
            a=((y1-y2)*(xx-x2)+(x2-x1)*(yy-y2))/denom
            b=((y2-y0)*(xx-x2)+(x0-x2)*(yy-y2))/denom
            c=1-a-b
            depth=a*z0+b*z1+c*z2
            old=zbuffer[ymin:ymax+1,xmin:xmax+1]
            mask=(a>=-1e-7)&(b>=-1e-7)&(c>=-1e-7)&(depth<old)
            old[mask]=depth[mask]
            pixels[ymin:ymax+1,xmin:xmax+1][mask]=facecolor
    ax.imshow(pixels,interpolation='lanczos')
    ax.set_axis_off()
    ax.set_facecolor('#f3f4f2')

def main():
    for _ in range(36):
        if (HERE/'03_Lysdiffusor.stl').exists(): break
        time.sleep(5)
    shell=load('01_Hus_og_front.stl')
    back=load('02_Baklokk.stl')
    diffuser=load('03_Lysdiffusor.stl')
    assembled_back=back.copy()
    assembled_back.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[1,0,0]))
    assembled_back.apply_translation([0,0,36])
    fig=plt.figure(figsize=(9,10),dpi=180,facecolor='#f3f4f2')
    ax=fig.add_axes([.02,.1,.96,.83])
    draw(ax,[(shell,'#fbfaf3'),(assembled_back,'#ededdf'),
             (diffuser,'#8cddd1')],span=146)
    fig.text(.07,.945,'Følelsespanel · avrundet kabinett',fontsize=20,
              color='#213034',weight='bold')
    fig.text(.07,.909,'82 × 126 × 36 mm  |  Forhåndsvisning av STL-modellen',
              fontsize=11,color='#5c696b')
    fig.text(.07,.06,'Faktisk modellgeometri, vist uten skjerm, knapp og elektronikk.\n'
             'Turkis markerer den separate lysdiffusoren; STL-filer har ingen farge.',
              fontsize=10,color='#5c696b',linespacing=1.5)
    fig.savefig(HERE/'Forhandsvisning_kabinett.png',dpi=180,facecolor=fig.get_facecolor())
    plt.close(fig)

    fig=plt.figure(figsize=(15,7),dpi=160,facecolor='#f3f4f2')
    fig.text(.045,.925,'Tre deler som skrives ut separat',fontsize=23,
             color='#213034',weight='bold')
    fig.text(.045,.875,'Hus med front, baklokk og separat diffusor for lysrammen',
             fontsize=12,color='#5c696b')
    items=[('01  Hus og front',shell,'#fbfaf3'),
           ('02  Baklokk',back,'#e4e7df'),
           ('03  Lysdiffusor',diffuser,'#8cddd1')]
    for i,(title,mesh,color) in enumerate(items):
        ax=fig.add_axes([.018+i*.327,.18,.32,.64])
        # CAD Z should face the camera for the shell. Turn the back cover around
        # to expose its skirt in the same reading direction.
        display=mesh.copy()
        if i==1:
            display.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[0,1,0]))
            display.apply_translation([0,0,6.4])
        draw(ax,[(display,color)],span=150,center=(0,14,0),elev=19,azim=-66)
        fig.text(.06+i*.327,.18,title,fontsize=14,color='#213034',weight='bold')
        sub=['Hvit PLA/PETG · 82 × 126 × 33,6 mm',
             'Fire skruehull fra baksiden',
             'Natur/translucent filament · 1,2 mm tykk'][i]
        fig.text(.06+i*.327,.13,sub,fontsize=10,color='#5c696b')
    fig.savefig(HERE/'Forhandsvisning_deler.png',dpi=160,facecolor=fig.get_facecolor())
    plt.close(fig)
    print(HERE/'Forhandsvisning_kabinett.png')
    print(HERE/'Forhandsvisning_deler.png')

if __name__=='__main__': main()
