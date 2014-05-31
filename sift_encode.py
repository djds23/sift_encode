import os
import time
from subprocess import call

root = "."

def watch(root):
    '''watching the current directory'''
    before = set(os.walk('.')) 
    while True:
        after = set(os.walk('.')) 
        added = after - before
        removed = before - after
        for paths in added:
            if 'streamers' in paths[0]:
                print 'streaming directory, ignoring...' 
            else:
                crawl_folder(paths)
        before = after
        time.sleep(10)

def crawl_folder(paths):
    '''crawl filesystem and apply encoding function'''
    root, dirs, files = paths
    for filename in files:
        if '.MTS' in filename:
            try: 
                os.mkdir(root + '/streamers') # consider os.join
            except OSError:
                pass
            finally:
                os.chdir(root)
                map(encode, files)
                break

def encode(contents):
    if contents.lower().endswith('.mts'):
        new_name = contents[:-4]+'_streamer.mp4'
        command = "ffmpeg -v verbose -i "+ contents +" -acodec copy -vf 'field, scale=iw/2:ih, setsar=1' -vcodec libx264 -g 60 -crf 30 -threads 8 -preset slow -y streamers/" + new_name 
        call(command, shell=True) #calll ffmpeg and place new file in new dict
        #Beware files only play in VLC

if __name__=='__main__':
    watch(root)
