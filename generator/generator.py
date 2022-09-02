'''
根据原始音频文件与字幕文件生成数据集
'''
from locale import normalize
from pathlib import Path
from pydub import AudioSegment, effects
from spleeter.separator import Separator
import random
import glob

RAW_DIR = "D:/raw/"
TRAIN_FILE = "d:/projects/vits-joi/joi/joi_train.txt"
VALID_FILE = "d:/projects/vits-joi/joi/joi_valid.txt"
DATASET = "d:/projects/vit"

separator = None


# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


train_file = open(TRAIN_FILE, "w+", encoding="utf-8")
valid_file = open(VALID_FILE, "w+", encoding="utf-8")
files = [train_file, train_file, train_file, train_file, train_file, train_file, train_file, train_file, train_file, valid_file]

def get_lines(ass_file) -> 'list[tuple[int, int, str]]':
    with open(ass_file, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
    lines = []
    for line in raw_lines:
        line = parse_line(line)
        if line is None:
            continue
        lines.append(line)
    return lines

def parse_line(line: str):
    if not line.startswith('Dialogue'):
        return None
    parts = line.split(',')
    # begin, end, content
    return (parse_time_milliseconds(parts[1]), parse_time_milliseconds(parts[2]), parts[9].replace('\n', ''))

def parse_time_milliseconds(time_str):
    # 0:00:00.17
    parts = time_str.split(':')
    return int(parts[0])*60*60*1000+ int(parts[1])*60*1000+int(float(parts[2])*1000)


def process_one(full_filename):
    audio_filepath = Path(full_filename)
    ass_filepath = audio_filepath.with_suffix('.ass')
    if not ass_filepath.exists():
        return
    audio = AudioSegment.from_file(audio_filepath)
    clips = get_lines(ass_filepath)
    for i, (start, end, content) in enumerate(clips):
        audio[start:end].export('./tmp/temp.wav', format='wav')
        separator.separate_to_file('./tmp/temp.wav','./tmp/')
        vocal = AudioSegment.from_file('./tmp/temp/vocals.wav')
        effects.normalize(vocal)  
        random.choice(files).writelines('joi/'+audio_filepath.stem+'.%05d.wav' % (i)+'|'+content+'\n')
        # 训练需要的格式
        vocal.export('../joi/'+audio_filepath.stem+'.%05d.wav' % (i), codec="pcm_s16le",format="wav", parameters=["-ar", "22050", "-ac", "1"])
    return

def main():
    global separator
    separator = Separator('spleeter:2stems')
    files = glob.glob(RAW_DIR+'/*.mp3')
    for f in files:
        process_one(f)


if __name__ == "__main__":
    main()
