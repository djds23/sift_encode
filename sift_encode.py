import os
import time
import subprocess

import encoder

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
    found_path, dirs, files = paths
    if any('.mts' in contents.lower() for contents in files):
        try:
            new_files= os.path.join(found_path, 'streamers')
            os.mkdir(new_files) 
        except OSError:
            return 'Files are already encoded or encoding, do not proceed.'
        else:
            filepaths = [[os.path.join(found_path, contents), os.path.join(new_files,contents)] for contents in files]
            encoder.pass_array(filepaths) #filepaths contains both using original file name, but one pointing to streamers
                                   #second contents will be altered in the encode function

def encode_nothing(contents): #NAME CHANGED FOR DELETION, ENCODING TAKES PLACE IN encoder.py CURRENTLY!
        if contents[0].lower().endswith('.mts'): #check to see if MPEG transit stream
            new_name = contents[1][:-4]+'_streamer.mp4'
            command = "ffmpeg -v verbose -i "+ contents[0] +" -acodec copy -vf 'field, scale=iw/2:ih, setsar=1' -vcodec libx264 -g 60 -crf 30 -threads 8 -preset slow -y " + new_name 
            subprocess.call(command, shell=True) #call ffmpeg and place new file in new dict
        #Beware files only play in VLC

if __name__=='__main__':
    watch(root)
