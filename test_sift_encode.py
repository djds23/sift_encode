import sift_encode

import os
import time
import shutil
import subprocess
import multiprocessing

def make_folders(tmpdir):
    test_card_dir = os.path.join(str(tmpdir),'test_card')
    shutil.copytree('test_card',test_card_dir) 
    mts_dir = os.path.join(test_card_dir, 'PRIVATE/a/a')
    test_card_walk = os.walk(mts_dir).next()
    new_files = os.path.join(mts_dir, 'streamers')
    found_path, dirs, files = test_card_walk
    filepaths = [[os.path.join(found_path, contents), os.path.join(new_files, contents)] for contents in files]
    return test_card_walk, new_files, filepaths

def test_pass_array(monkeypatch, tmpdir):
    test_card_walk, new_files, filepaths = make_folders(tmpdir)
    sift_encode.pass_array(filepaths)

def test_crawl_folder(monkeypatch, tmpdir):
    test_card_walk, new_files, filepaths = make_folders(tmpdir)
    def mock_encode(contents):
        assert contents == filepaths 
    monkeypatch.setattr(sift_encode, 'pass_array', mock_encode)
    sift_encode.crawl_folder(test_card_walk)
    assert os.path.isdir(new_files)

def test_encode(monkeypatch, tmpdir):
     test_card_walk, new_files, filepaths = make_folders(tmpdir)

'''
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
 '''
