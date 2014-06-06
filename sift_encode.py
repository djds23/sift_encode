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
            encoder.run_pool(filepaths)
                                   #second contents will be altered in the encode function

if __name__=='__main__':
    watch(root)
