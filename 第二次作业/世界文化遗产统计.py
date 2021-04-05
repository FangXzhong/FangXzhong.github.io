"""
还是那个小明，他想出国旅游，但是他的钱只够他去一个国家，
于是他想要知道世界各国的文化遗产数量，方便他决定去哪个国家
"""

import xlrd
import pyecharts.charts as charts
import pyecharts.options as opts

from 世界地图国家中英文对照 import my_dict

# 以下两句代码就是生成一个中英文国家名称对照的字典
Chinese_English_dict = my_dict
English_Chinese_dict = {Chinese_English_dict[item]: item
                        for item in Chinese_English_dict.keys()}

# 从xlsx文件读入数据并进行处理输出
file = xlrd.open_workbook('./data/各国世界文化遗产（截止2019年7月10日）.xlsx')
table = file.sheet_by_index(0)
data = []
for i in range(table.nrows):
    if i == 0:
        continue # 跳过标题行
    data.append([English_Chinese_dict[table.row_values(i)[0].strip()],
                 int(table.row_values(i)[1])])
print(data)

# 开始画图
my_map = charts.Map()
my_map.add('世界文化遗产数量', data, "world")\
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))\
    .set_global_opts(
    title_opts=opts.TitleOpts(title="世界遗产分布分布"),
    visualmap_opts=opts.VisualMapOpts(max_=55, min_=1))

my_map.render('./output/世界文化遗产分布图.html')
