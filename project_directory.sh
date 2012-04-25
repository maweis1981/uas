#!/bin/bash

redir ()
{
        #tab是真正的步长计算器
        tab=$tab$singletab
        line=${tab%"$singletab"}"|-------"

        #local比较关键，它规定了count是当前的参数列表值
        local count=$#

        for file in "$@"; do
                thisfile=${thisfile:-$PWD}/$file

                #判断当前文件是否为目录，如果是就开始递归   
                if [ -d "$thisfile" ]; then
                        
                        #如果当前目录是分枝列表的最底层，则需进行特殊处理。
                        if [ $count -eq 1 ]; then
                                echo -e $line$file/
                                #将前一个|符号去掉，看看目录树就知道为什么了。
                                tab=${tab%"$singletab"}"\t"
                                redir $(ls $thisfile)
                        else

                                echo -e $line$file/
                                redir $(ls $thisfile)
                        fi
                        
                else
                        echo -e $line$file
                fi
                
                thisfile=${thisfile%/*}
                let count=count-1       
        done
        
        #这一步比较有意思，因为从递归出来的tab结尾可能是TAB也可能是$singletab，所以分成两步来去掉。
        tab=${tab%"\t"}
        tab=${tab%"|"}
        line=${tab%"$singletab"}"|-------"
}


singletab="|\t"
userinput="$@"
if ls $userinput; then

        for file in ${userinput:-.}; do
                echo $file
                echo '|'
                if [ -d "$file" ]; then
                        cd $file
                        redir $(ls)
                        cd ..
                fi
        done
else
        echo "$userinput is wrong"
fi