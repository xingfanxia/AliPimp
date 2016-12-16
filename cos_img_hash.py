#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import glob
from PIL import Image

EXTS = ['png', 'jpg', 'gif']
total = 0

master = Image.open('original_image.jpg')
master = master.resize((20, 20), Image.ANTIALIAS).convert('L')

avg = reduce(lambda x, y: x + y, master.getdata()) / 400
master_data = map(lambda x: 0 if x>avg else 1, master.getdata())
#print master_data

def cos_dist(a, b):
    if len(a) != len(b):
        return None
    part_up = 0.0
    a_sq = 0.0
    b_sq = 0.0
    for x, y in zip(a,b):
        part_up += x*y
        a_sq += x**2
        b_sq += y**2
    part_down = math.sqrt(a_sq*b_sq)
    if part_down == 0.0:
        return None
    else:
        return part_up / part_down

images = []
for ext in EXTS:
    #fill in images list
    images.extend(glob.glob('similar_Images/*.%s' % ext))
    
    #print repr(images)
    dists = []
    for f in images:
        if f == "image.png":
            continue
        im = Image.open(f)
        im = im.resize((20, 20), Image.ANTIALIAS).convert('L')
        avg = reduce(lambda x, y: x + y, im.getdata()) / 400

        #这里还有问题，得出的像素是反的，所以我把">"号变成了"<"号
        im_data = map(lambda x: 0 if x<avg else 1, im.getdata())
        
        dist = cos_dist(master_data, im_data)
        
        print "image: %s\t avg: %f\t dist:%s\t" % (f, avg, dist)
        print im_data
        
        dists.append((f, dist))

for f, dist in sorted(dists, key=lambda i: i[1]):
    print "%f\t%s" % (dist, f)
    total += dist
avg = total/len(dists)
print "the average is: ", avg
if avg < 0.5:
    print "this image might be unique!"
else:
    print "Care! This iamge might have been taken from Internet!"
        
