"""
    author:Fang Xiangzhong
    date:2021.03.31

    要点说明：
    从csv文件中导入词频数据并作可视化处理
"""

import pyecharts.charts as charts
import pyecharts.options as opts

f = open(r'./data/平凡的世界_词频统计结果.csv', encoding='utf-8')
words_freq_list = [(item.split(',')[0].strip(), item.split(',')[1].strip())
                   for item in f.readlines()]

# 删除首行“人物，出现次数”
del words_freq_list[0]

f.close()

# 词云
cloud = charts.WordCloud()
cloud.add('', words_freq_list)
cloud.render('./output/平凡的世界词频统计_词云.html')

# 柱状图
words_freq_dict = {item[0]: int(item[1]) for item in words_freq_list}
bar = charts.Bar()
bar.add_xaxis(list(words_freq_dict.keys()))\
    .add_yaxis(series_name='词频数', y_axis=list(words_freq_dict.values()))
bar.render("./output/词频柱状图.html")

# 极坐标系
name_list = [item[0] for item in words_freq_list]
freq_list = [int(item[1]) for item in words_freq_list]
polar = charts.Polar()
polar.add_schema(angleaxis_opts=opts.AngleAxisOpts(data=name_list, type_="category"))\
    .add('词频', freq_list, type_='bar', stack='stack0')\
    .set_global_opts(title_opts=opts.TitleOpts(title='极坐标词频统计图'))
polar.render('./output/极坐标词频统计图.html')
