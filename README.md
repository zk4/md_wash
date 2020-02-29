# 介绍
一个小工具,将 markdown 远程的图片拉到本地来存储,并更新 markdown 文件

1. 将 markdown 文件里的 http 开头的图片 url 地址拉到本地 ./assets 下.
2. 更新 markdown 图片链接为本地链接
3. 清洗你的 markdown, 只抽取将当前文件夹 markdown 里的文件所关联的图片

![demo](https://github.com/zk4/md_wash/blob/master/intro.jpg)
# 安装
```
pip install md_wash
```

# 使用方式

``` bash
usage: md_wash [-h] [-o OUTPUT] [-a ASSETNAME] [-r] [-u] [-c] input

positional arguments:
  input                 指定你 markdown 的目录,或者md 文件

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        指定你 markdown 的输出目录, 默认覆盖原目录! (default: None)
  -a ASSETNAME, --assetname ASSETNAME
                        指定你图片输出的目录名,默认叫 assets (default: assets)
  -r, --recursive       是否递归目录 (default: False)
  -u, --uuid            是否图片使用随机名,否则根据 url 结尾生成,有可能会有重名 (default: False)
  -c, --copy            是否将原assets里的图片拷贝到output,原assets 目录名将与参数的 assetname 一致,
                        一般会与 -u同时使用 (default: False)
```

# 举例
```bash
# demo 1. 将直接覆盖本地
md_wash  ./markdown 

# demo 2. 仅清洗 hello.md, 
#默认输出到  ./markdown/hello/hello.md 图片输出到 ./markdown/hello/assets
md_wash  ./markdown/hello.md  -c

# demo 3. 输出到其他文件
md_wash  ./markdown -c -o ./output

# demo 4. 清洗 markdown,包含子文件
md_wash  -c  -r  ./markdown -o ./markdown_washed
```
