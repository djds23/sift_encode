import subprocess
import multiprocessing

def encode(contents):
    if contents[0].lower().endswith('.mts'):
        new_name = contents[1][:-4]+'_streamer.mp4'
        command = "ffmpeg -v verbose -i "+contents[0] +" -acodec copy -vf 'field, scale=iw/2:ih, setsar=1' -vcodec libx264 -g 60 -crf 26 -threads 8 -preset slow -y " + new_name
        subprocess.call(command, shell=True)
    
def run_pool(filepaths):
    pool = multiprocessing.Pool(processes=4)
    result = pool.map_async(encode, filepaths)

