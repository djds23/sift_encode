import sift_encode

import os
import time
import shutil
import subprocess
import multiprocessing

def test_encode(monkeypatch):
    def mock_call(command, shell):
        assert command == "ffmpeg -v verbose -i ./test.mts -acodec copy -vf 'field, scale=iw/2:ih, setsar=1' -vcodec libx264 -g 60 -crf 30 -threads 8 -preset slow -y ./streamers/test_streamer.mp4" 
    monkeypatch.setattr(subprocess, 'call', mock_call)
    sift_encode.encode(['./test.mts', './streamers/test.mts'])

def test_crawl_folder(monkeypatch, tmpdir):
    test_card_dir = os.path.join(str(tmpdir),'test_card')
    shutil.copytree('test_card',test_card_dir) 
    mts_dir = os.path.join(test_card_dir, 'PRIVATE/a/a')
    test_card_walk = os.walk(mts_dir).next()
    new_files = os.path.join(mts_dir, 'streamers')
    found_path, dirs, files = test_card_walk
    filepaths = [[os.path.join(found_path, contents), os.path.join(new_files, contents)] for contents in files]
    def mock_encode(contents):
        assert contents in filepaths 
    monkeypatch.setattr(sift_encode, 'encode', mock_encode)
    sift_encode.crawl_folder(test_card_walk)
    assert os.path.isdir(new_files)

def test_watch(monkeypatch, tmpdir):
    create_processes(run_watch,move_cards)

def create_processes(*args):
    for _ in args:
        process = multiprocessing.Process(args=[_])
        process.daemon=True
        process.start()

def run_watch(tmpdir):
    def mock_crawl_folder():
        pass
    monkeypatch.setattr(sift_encode, 'crawl_folder', mock_crawl_folder)
    sift_encode.watch(str(tmpdir))
    
def move_cards(tmpdir):
    test_card_dir = os.path.join(str(tmpdir),'test_card')
    shutil.copytree('test_card', test_card_dir)
    time.sleep(15)
    shutil.copytree('test_card_A', test_card_dir)
    time.sleep(15)
 
