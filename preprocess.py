import argparse
import text
from utils import load_filepaths_and_text

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--out_extension", default="cleaned")
  parser.add_argument("--text_index", default=1, type=int)
  parser.add_argument("--filelists", nargs="+", default=["joi/joi_train.txt", "joi/joi_valid.txt"])
  parser.add_argument("--text_cleaners", nargs="+", default=["chinese_cleaners2"])

  args = parser.parse_args()

  for filelist in args.filelists:
    print("START:", filelist)
    filepaths_and_text = load_filepaths_and_text(filelist)
    cleanedlines = []
    for i in range(len(filepaths_and_text)):
      original_text = filepaths_and_text[i][args.text_index]
      cleaned_text = text._clean_text(original_text, args.text_cleaners)
      if len(cleaned_text) > 0:
        filepaths_and_text[i][args.text_index] = cleaned_text
        cleanedlines.append(filepaths_and_text[i])

    new_filelist = filelist + "." + args.out_extension
    with open(new_filelist, "w", encoding="utf-8") as f:
      f.writelines(["|".join(x) + "\n" for x in cleanedlines])
