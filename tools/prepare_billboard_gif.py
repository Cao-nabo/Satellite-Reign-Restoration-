"""Convert a GIF to a bounded animated poster atlas; never writes into the game."""
import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageOps, ImageChops

def screen_lines(frame):
    # Native Grid ad: opaque RGB dark bands every ~10.67 rows at 512px high.
    width,height=frame.size
    mask=Image.new('L',(1,height*4))
    values=[]
    for y in range(height*4):
        phase=((y+.5)*512/(height*4))%(32/3)
        distance=min(phase,32/3-phase)
        weight=0.38 if distance<.75 else min(1.0,.38+(distance-.75)/1.3*.62)
        values.append(round(255*weight))
    mask.putdata(values);mask=mask.resize((width,height),Image.Resampling.LANCZOS)
    rgb=ImageChops.multiply(frame.convert('RGB'),Image.merge('RGB',(mask,mask,mask)))
    return rgb.convert('RGBA')

def prepare(source, output, category="movies", screen_effect=True, max_frames=64):
    if max_frames not in (16,32,64):
        raise ValueError("Frame limit must be 16, 32 or 64")
    if category not in ("movies","merchandise","commercial"):
        raise ValueError("Unknown billboard category")
    source,output=Path(source),Path(output)
    if source.stat().st_size>32*1024*1024:
        raise ValueError('GIF must be at most 32 MiB')
    if output.exists():
        raise ValueError('Choose a new output folder; existing media is not overwritten')
    with Image.open(source) as gif:
        if gif.format!='GIF':
            raise ValueError('Input must be a GIF animation')
        if gif.width*gif.height>4*1024*1024:
            raise ValueError('GIF dimensions are too large')
        count=getattr(gif,'n_frames',1)
        if count>1000:
            raise ValueError('GIF must have at most 1000 frames')
        durations=[]
        for index in range(count):
            gif.seek(index)
            durations.append(max(20,min(10000,int(gif.info.get('duration',100)))))
        total=sum(durations)
        if total>120000:
            raise ValueError('GIF loop must be at most two minutes')
        # More temporal samples share the same texture ceilings. Keep legacy quality
        # for simple clips; dense clips trade cell resolution for smoother motion.
        frames=16
        while frames<min(count,max_frames) and frames*2<=max(16,total//20):
            frames*=2
        columns=4 if frames==16 else 8
        rows=frames//columns
        cell=(256,128) if frames==16 else (128,64)
        square_cell=(1024//columns,1024//columns)
        version=1 if frames==16 else 2
        targets=[total*i/frames for i in range(frames)]
        atlas=Image.new('RGBA',(1024,cell[1]*rows),(0,0,0,255))
        square=Image.new('RGBA',(1024,square_cell[1]*rows),(0,0,0,255))
        frame=0;until=durations[0]
        for slot,when in enumerate(targets):
            while frame<count-1 and when>=until:
                frame+=1;until+=durations[frame]
            gif.seek(frame)
            # Pillow supplies composited GIF frames, including disposal/transparency.
            for target,frame_cell in ((atlas,cell),(square,square_cell)):
                image=ImageOps.contain(gif.convert('RGBA'),frame_cell,Image.Resampling.LANCZOS)
                canvas=Image.new('RGBA',frame_cell,(0,0,0,255))
                canvas.alpha_composite(image,((frame_cell[0]-image.width)//2,(frame_cell[1]-image.height)//2))
                if screen_effect: canvas=screen_lines(canvas)
                target.paste(canvas,((slot%columns)*frame_cell[0],(slot//columns)*frame_cell[1]))
        output.mkdir(parents=True)
        atlas.save(output/'atlas.png')
        square.save(output/'atlas-square.png')
        metadata={'version':version,'atlas':'atlas.png','columns':columns,'rows':rows,'frames':frames,
                  'frame_seconds':max(.02,total/frames/1000),'width':atlas.width,'height':atlas.height,
                  'rgba_bytes':atlas.width*atlas.height*4,'input_frames':count,'loop_seconds':max(frames*.02,total/1000),'source_loop_seconds':total/1000,
                  'order':'left-to-right, top-to-bottom','audio':False,'category':category,'scanlines':screen_effect,'square_atlas':'atlas-square.png','square_rgba_bytes':square.width*square.height*4}
        (output/'animation.json').write_text(json.dumps(metadata,indent=2)+'\n')
        attributes={'version':str(version),'category':category,'frameSeconds':str(metadata['frame_seconds'])}
        if version==2:
            attributes.update(frames=str(frames),columns=str(columns),rows=str(rows))
        ET.ElementTree(ET.Element('billboard',attributes)).write(output/'clip.xml',encoding='utf-8',xml_declaration=True)
        return metadata

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('gif',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--category',choices=['movies','merchandise','commercial'],default='movies')
    parser.add_argument('--frames',type=int,choices=(16,32,64),default=64,help='Maximum samples; 16 retains larger legacy cells')
    args=parser.parse_args()
    try:
        print(json.dumps(prepare(args.gif,args.output,args.category,max_frames=args.frames),indent=2))
    except (OSError,ValueError) as error:
        parser.exit(1,str(error)+'\n')
