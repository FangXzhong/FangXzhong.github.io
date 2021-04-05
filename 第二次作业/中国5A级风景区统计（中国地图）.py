"""
要点说明：
小明想在暑假里去某个省游玩，但是因为
太穷了，最多只能去一个省，所以他想要知道
每个省里5A级风景区的数量
"""

import pyecharts.charts as charts
import pyecharts.options as opts

file = open('./data/2020年5A级风景区统计.csv', encoding='utf-8')
data = [[item.split(',')[0].strip(), int(item.split(',')[1].strip())]
        for item in file.readlines()]
print(data)

my_map = charts.Map()
my_map.add('景区数量', data, 'china')
my_map.set_global_opts(
    title_opts=opts.TitleOpts(title="2020年中国5A级景区分布"),
    visualmap_opts=opts.VisualMapOpts(max_=25, min_=2))

my_map.render('./output/2020年中国5A级景区分布图.html')
