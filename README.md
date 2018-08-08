# 简介
用于高德地图逆地理编码，[高德逆地理编码API](https://lbs.amap.com/api/webservice/guide/api/georegeo).

# 用法
各个脚本的使用方法：
* `coord2loc.py`: 将经纬度转化为结构化地址。输入参数：
    * `--locfile`: 储存经纬度的文件，纬度在前，经度在后
    * `--s`: 需要处理的起始条目编号
    * `--e`: 需要处理的结束条目编号
* `para.py`: 并行处理
* `fuse.py`: 合并结果。输入参数：
    * `--resdir`: 目标文件所在文件夹

# 联系作者
Junfu Pu, pjh AT mail.ustc.edu.cn
