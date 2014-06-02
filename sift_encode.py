import os
import time
from subprocess import call

root = "."

def watch(root):
    '''watching the current directory'''
    before = [paths for paths in os.walk('.')] 
    while True:
        after = [paths for paths in os.walk('.')] 
        added = [paths for paths in after if paths not in before]   
        removed = [paths for paths in before if paths not in after]
        for paths in added:
            if 'streamers' in paths[0]:
                print paths[0], ': Is a streaming directory' 
            else:
                crawl_folder(paths)
        before = after
        time.sleep(10)

def crawl_folder(paths):
    '''crawl filesystem and apply encoding function'''
    root, dirs, files = paths
    if any('.mts' in contents.lower() for contents in files):
        try:
            new_files= os.path.join(root, 'streamers')
            os.mkdir(new_files) 
        except OSError:
            return 'Files are already encoded or encoding, do not proceed.'
        else:
            filepaths = [os.path.join(root, contents) for contents in files]
            map(encode, filepaths) 

def encode(contents):
        if contents.lower().endswith('.mts'): #check to see if MPEG transit stream
            new_name = contents[:-4]+'_streamer.mp4'
            command = "ffmpeg -v verbose -i "+ contents +" -acodec copy -vf 'field, scale=iw/2:ih, setsar=1' -vcodec libx264 -g 60 -crf 30 -threads 8 -preset slow -y streamers/" + new_name 
            call(command, shell=True) #call ffmpeg and place new file in new dict
        #Beware files only play in VLC

if __name__=='__main__':
    watch(root)
