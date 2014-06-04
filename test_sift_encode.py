import sift_encode
import shutil
import os
import subprocess

def test_encode(monkeypatch):
    def mock_call(command, shell):
        assert command == "ffmpeg -v verbose -i ./test.mts -acodec copy -vf 'field, scale=iw/2:ih, setsar=1' -vcodec libx264 -g 60 -crf 30 -threads 8 -preset slow -y ./streamers/test_streamer.mp4" 
    monkeypatch.setattr(subprocess, 'call', mock_call)
    sift_encode.encode(['./test.mts', './streamers/test.mts'])

def test_crawl_folder(monkeypatch, tmpdir):
    def mock_encode(contents):
        pass
    monkeypatch.setattr(sift_encode, 'encode', mock_encode)
    test_card_dir = os.path.join(str(tmpdir),'test_card')
    shutil.copytree('test_card',test_card_dir) 
    mts_dir = os.path.join(test_card_dir, 'PRIVATE/a/a')
    test_card_walk = os.walk(mts_dir).next()
    sift_encode.crawl_folder(test_card_walk)
    assert os.path.isdir(os.path.join(mts_dir, 'streamers'))

