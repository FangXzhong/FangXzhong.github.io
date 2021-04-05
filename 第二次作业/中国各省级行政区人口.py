"""
研究人口的小明在北大快乐地学习，有一天他突然想知道中国各省在过去一段时间内的人口数量
以及变化情况，于是他就动手输出了一份可视化代码
"""

import xlrd
import pyecharts.options as opts
import pyecharts.charts as charts

file = xlrd.open_workbook('./data/中国各省级行政区人口数.xlsx')
table = file.sheet_by_index(0)
raw_data = []
for i in range(table.nrows):
    raw_data.append(table.row_values(i))

name_dict = {
    "新疆维吾尔自治区": "新疆",
    "西藏自治区": "西藏",
    "宁夏回族自治区": "宁夏",
    "广西壮族自治区": "广西",
    "内蒙古自治区": "内蒙古"
}

for i in range(len(raw_data)):
    if raw_data[i][0][-1] == '省':
        raw_data[i][0] = raw_data[i][0][:-1]
    elif raw_data[i][0][-1] == '市':
        raw_data[i][0] = raw_data[i][0][:-1]
    elif raw_data[i][0] in name_dict.keys():
        raw_data[i][0] = name_dict[raw_data[i][0]]

    raw_data[i][1] = int(raw_data[i][1])

total_dict = dict()
for i in range(1999, 2016):
    total_dict[i] = list()
for item in raw_data:
    total_dict[item[1]].append([item[0], item[2]])
print(total_dict)

t1 = charts.Timeline()
for i in range(1999, 2016):
    map1 = charts.Map()
    map1.add('人口', total_dict[int(i)], 'china')
    map1.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    map1.set_global_opts(title_opts=opts.TitleOpts(title='{}年人口统计'.format(i)),
                         visualmap_opts=opts.VisualMapOpts(min_=100, max_=12000))
    t1.add(map1, '{}年'.format(i))
t1.render('./output/组合图表.html')
