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
from os.path  import join,basename,dirname
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
        # logger.info("img alread exists: ",local_filename)
        return 

    try:
        logger.info(f"requesting.. {url}")
        with requests.get(url, stream=True,timeout=timeout) as r:
            # r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
    except Exception as identifier:
        logger.info(f"{url}  请求失败")
        logger.exception(identifier)
        

def task(abspath,output,assetname,ifuuid,copy,assets_relative_path):
    if abspath.split(".")[-1] not in ["md","markdown",'mdown']:
        return
    newfile=""
    # parse md  by line, extract {img url}
    logger.info(f'abspath:{abspath}')
    with open(abspath) as f:
        line=f.readline()
        while line:
            for t,imgurl in get_img_url(line):
                ext = basename(imgurl).split(".")[-1]
                short_img_name= (str(uuid.uuid4())+"."+ext ) if ifuuid else basename(imgurl)
                
                local_filename =join(output,assetname,short_img_name)
                os.makedirs(os.path.dirname(local_filename), exist_ok=True)                    

                if t=="url":
                    download_file(imgurl,local_filename)
                else:
                    if copy:
                        # copy  file
                        src = os.path.join(dirname(abspath),imgurl)
                        logger.info(f"{src} --> {local_filename}")
                        if os.path.isfile(src):
                            copyfile(os.path.join(os.path.dirname(abspath),imgurl.strip()), local_filename)
                        else:
                            logger.info(f"not found: {src}")


                line = line.replace(imgurl,join(assets_relative_path, ".",assetname, short_img_name))
             

            # append new line to new markdown 
            newfile+=line

            line=f.readline()

         # save back to file
        fullOutputPath=join(output,basename(abspath))
        os.makedirs(os.path.dirname(fullOutputPath), exist_ok=True)                    
        f = open(fullOutputPath, 'w')
        f.write(newfile)
        f.close()



def main(args):
    inputsrc             = args.input
    assetname            = args.assetname
    ifuuid               = args.uuid
    copy                 = args.copy
    assets_relative_path = args.assets_relative_path
    output               = args.output or join(dirname(inputsrc),"..",basename(inputsrc).split(".")[0])

    # not dir just one file
    if not os.path.isdir(inputsrc):
        filename = os.path.abspath(inputsrc)
        # output  =  
        logger.error(f'output:{output}')
        task(filename,output,assetname,ifuuid,copy,assets_relative_path)
    else:
        with ThreadPoolExecutor(max_workers=10) as t: 
            # output  = args.output if  args.output else inputsrc
            for (dirpath, dirnames, filenames) in os.walk(inputsrc):
                
                if args.recursive:
                    for filename in filenames:
                        abspath = os.path.abspath(join(dirpath,filename))
                        f = t.submit(task,abspath,output,assetname,ifuuid,copy,assets_relative_path)
                        # will block
                        if f.result():
                            logger.info(f.result())
                else:
                    if dirpath == inputsrc:
                        for filename in filenames:
                            abspath = os.path.abspath(join(dirpath,filename))
                            f = t.submit(task,abspath,output,assetname,ifuuid,copy,assets_relative_path)
                            # will block
                            if f.result():
                                logger.info(f.result())

def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    main(mainArgs)


def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='指定你 markdown 的目录,或者md 文件')
    parser.add_argument("-o",'--output', type=str,required=False, help='指定你 markdown 的输出目录, 默认覆盖原目录!')
    parser.add_argument("-p",'--assets_relative_path', type=str,required=False,default=".", help='引用相对 assets 的其他路径, 常用于博客上传')
    parser.add_argument("-a",'--assetname', type=str,default="assets",required=False, help='指定你图片输出的目录名,默认叫 assets')
    parser.add_argument("-r",'--recursive',action='store_true', default=False,required=False, help='是否递归目录')
    parser.add_argument("-u",'--uuid',action='store_true', default=False,required=False, help='是否图片使用随机名,否则根据 url 结尾生成,有可能会有重名')
    parser.add_argument("-c",'--copy',action='store_true', default=False,required=False, help='是否将原assets里的图片拷贝到output,原assets 目录名将与参数的 assetname 一致, 一般会与 -u同时使用')
    return parser
