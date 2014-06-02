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
                print 'streaming directory, ignoring...' 
            else:
                crawl_folder(paths)
        before = after
        time.sleep(10)

def crawl_folder(paths):
    '''crawl filesystem and apply encoding function'''
    root, dirs, files = paths
    for filename in files: #search the folder for a file with .mts extension
        if '.MTS' in filename:
            try:
                new_files= os.path.join(root, 'streamers')
                os.mkdir(new_files) 
            except OSError:
                pass
            finally:
                map(encode, files, root) 
                break   

def encode(contents, root):
        if contents.lower().endswith('.mts'): #check to see if MPEG transit stream
            new_contents = os.path.join(root, contents)
            new_name = contents[:-4]+'_streamer.mp4'
            command = "ffmpeg -v verbose -i "+ new_contents +" -acodec copy -vf 'field, scale=iw/2:ih, setsar=1' -vcodec libx264 -g 60 -crf 30 -threads 8 -preset slow -y streamers/" + new_name 
            call(command, shell=True) #call ffmpeg and place new file in new dict
        #Beware files only play in VLC

if __name__=='__main__':
    watch(root)
