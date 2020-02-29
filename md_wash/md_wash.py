#coding: utf-8
from .logx import setup_logging
import logging
import argparse
import re
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
import threading
import uuid
from shutil import copyfile
from os.path  import join
# don`t remove this line
setup_logging()

logger = logging.getLogger(__name__)

import sys

# 识别一行多张图片
def get_img_url(line):
    reg = "(\!\[.*\]\(\(.*?\))*\)"
    comp= re.search(reg,line)
    if comp:
        for c in  comp.groups(0):
            reg = "\!\[.*\]\((http.*?)\)"
            comp= re.search(reg,line)
            if comp:
                yield "url",comp.groups(0)[0]
            else: 
                reg = "\!\[.*\]\((.*?)\)"
                comp= re.search(reg,line)
                if comp:
                    yield "other",comp.groups(0)[0]

def download_file(url,local_filename,timeout=10):
    # auto make dir
    os.makedirs(os.path.dirname(leocal_filename), exist_ok=True)
    if os.path.exists(local_filename):
        # print("img alread exists: ",local_filename)
        return 

    try:
        print("requesting..",url)
        with requests.get(url, stream=True,timeout=timeout) as r:
            # r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
            # print("write image to ",local_filename)
    except Exception as identifier:
        print(url , "请求失败")

def task(filename,dirpath,output,assetname,ifuuid,copy):
    if filename.split(".")[-1] not in ["md","markdown",'mdown']:
        return
    print("job:",join(dirpath,filename))
    newfile=""
    # parse md  by line, extract {img url}
    full_path = join(dirpath,filename)
    with open(full_path) as f:
        line=f.readline()
        while line:
            for t,imgurl in get_img_url(line):
                ext = imgurl.split('/')[-1].split(".")[1]
                short_img_name= (str(uuid.uuid4())+"."+ext ) if ifuuid else imgurl.split('/')[-1]
                
                local_filename =output+"/"+assetname+"/"+ short_img_name
                os.makedirs(os.path.dirname(local_filename), exist_ok=True)                    

                if t=="url":
                    download_file(imgurl,local_filename)
                else:
                    if copy:
                        # copy  file
                        src = os.path.join(os.path.dirname(full_path),imgurl.strip())
                        print(f"{src} --> {local_filename}")
                        if os.path.isfile(src):
                            copyfile(os.path.join(os.path.dirname(full_path),imgurl.strip()), local_filename)
                        else:
                            print("not found:",src)


                line = line.replace(imgurl,"./"+assetname+"/"+ short_img_name)
             

            # append new line to new markdown 
            newfile+=line

            line=f.readline()

         # save back to file
        fullOutputPath=output+"/"+filename
        os.makedirs(os.path.dirname(fullOutputPath), exist_ok=True)                    
        f = open(fullOutputPath, 'w')
        # print("save file in ",fullOutputPath)
        f.write(newfile)
        f.close()



def main(args):
    inputdir =  args.input

    assetname   = args.assetname
    ifuuid   = args.uuid
    copy   = args.copy

    # not dir just one file
    # if not os.path.isdir(inputdir):
    #     filename = inputdir
    #     output  = args.output if  args.output else filename.split(".")[-1]
    #     dirpath = "."
    #     task(filename,dirpath,output,assetname,ifuuid,copy)
    # else:
    with ThreadPoolExecutor(max_workers=10) as t: 
        output  = args.output if  args.output else inputdir
        for (dirpath, dirnames, filenames) in os.walk(inputdir):
            
            if args.recursive:
                for filename in filenames:
                    f = t.submit(task,filename,dirpath,output,assetname,ifuuid,copy)
                    # will block
                    if f.result():
                        print(f.result())
            else:
                if dirpath == inputdir:
                    for filename in filenames:
                        f = t.submit(task,filename,dirpath,output,assetname,ifuuid,copy)
                        # will block
                        if f.result():
                            print(f.result())

def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    main(mainArgs)


def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='指定你 markdown 的目录,或者md 文件')
    parser.add_argument("-o",'--output', type=str,required=False, help='指定你 markdown 的输出目录, 默认覆盖原目录!')
    parser.add_argument("-a",'--assetname', type=str,default="assets",required=False, help='指定你图片输出的目录名,默认叫 assets')
    parser.add_argument("-r",'--recursive',action='store_true', default=False,required=False, help='是否递归目录')
    parser.add_argument("-u",'--uuid',action='store_true', default=False,required=False, help='是否图片使用随机名,否则根据 url 结尾生成,有可能会有重名')
    parser.add_argument("-c",'--copy',action='store_true', default=False,required=False, help='是否将原assets里的图片拷贝到output,原assets 目录名将与参数的 assetname 一致, 一般会与 -u同时使用')
    return parser
