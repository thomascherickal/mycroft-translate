#!/usr/bin/python3

# VERSION 1.2
# Run this file in the Skills repo to extract all translatable strings.

import os
from glob import glob
import json

ftag = "_(\""
btag = "\")"

def main():
    # add old dialog/en-us, vocab/en-us style paths
    paths = glob("mycroft-skills/**/en-us/**.*", recursive=True)

    print("\n pathlist is: " )
    for path in paths:
        print (path)

    # print a count of the paths to aid in debugging
    print("\n there were",  sum('locale/' in s for s in paths), "LOCALE paths added")
    print("\n there were", sum('dialog/' in s for s in paths), "DIALOG paths added")
    print("\n there were", sum('vocab/' in s for s in paths) , "VOCAB paths added")
    print("\n there were", sum('mycroft-skills/' in s for s in paths), " paths added in total")

    # create the tags and pots directories
    if not os.path.exists('tags'):
        os.mkdir('tags')

    if not os.path.exists('pots'):
        os.mkdir('pots')

    d = {}
    for path in paths:
        print(" ======================================== \n")
        print(" Began tagging the path " + path)

        dirpath, file = os.path.split(path)
        print("\n first dirpath is:  " + dirpath)
        dirpath = os.path.split(dirpath)[0].replace('mycroft-skills/', '')
        print("\n second dirpath is: " + dirpath)
        print("\n file is:  " + file)

        skill, subfolder = os.path.split(dirpath)
        print("\n skill is:  " + skill)

        tagpath = os.path.join('tags', skill)
        print("\n tagpath is:  " + tagpath)

        if skill not in d:
            d[skill] = {}

        # write out the files to a `tags` dir
        with open(path, 'r') as source:
            tagdir = os.path.join('tags', skill)
            print("\n tagdir is:  " + tagdir)
            if not os.path.exists(tagdir):
                os.makedirs(tagdir)
            with open(os.path.join(tagdir,file), 'w') as temp:
                linelist = source.readlines()
                for line in linelist:
                    print("line before replace() is:  " + line)
                    line = line.replace(r'"', r'\"').strip("\n")
                    if not line:
                        continue
                    print("line is:  " + line)
                    temp.write('{0}{1}{2}{3}'.format(ftag, line, btag, "\n"))
                    files = d[skill].get(line, []) + [file]
                    d[skill][line] = files

    skilllist = os.listdir('tags')

    # Write occurrence map to occurrences.json
    # This file will be used by the PR generation tool to map strings to files
    with open('occurrences.json', 'w') as fp:
        json.dump(d, fp, indent=2)

    for dir in skilllist:
        print("dir is :  " + dir + "\n \n \n")
        if not os.path.exists('pots/' + dir):
            os.makedirs('pots/' + dir)
            print("\n creating dir: " + ('pots/' + dir))
        gtxtcommand = "xgettext --from-code=utf-8 --keyword=_ --language=Python --add-comments " + \
                    "--output='pots/" + dir +".pot' tags/" + dir + "/*.*"

        print("\n gtxtcommand is:  " + gtxtcommand + "\n")
        exitstatus = os.system(gtxtcommand)
        print("\n exit status: ", exitstatus, "\n")
        print("\n created file: " +  'pots/' + dir + '.pot')

if __name__ == '__main__':
    main()
