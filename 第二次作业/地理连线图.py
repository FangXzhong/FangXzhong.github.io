"""
Author: Fang Xiangzhong
Date: 2021/4/3

要点说明：
这个程序是在一张中国地图上描绘出
各人的行动轨迹图。故事背景是，大学毕业十年
之后，同班的几个要好的同学准备聚一聚，于是
他们约定在某一时间从所在城市出发到北京进行聚会
"""

import pyecharts.options as opts
import pyecharts.charts as charts
import pyecharts.globals as glb

c = charts.Geo()
c.add_schema(maptype='china', itemstyle_opts=opts.ItemStyleOpts(color="grey", border_color="#111"))

# 添加地图上的点，数字是指来自各个城市的人数
c.add('', [('北京', 10), ('上海', 20), ('杭州', 5), ('深圳', 15), ('成都', 2), ('拉萨', 1), ('大庆', 1)],
      type_=glb.ChartType.EFFECT_SCATTER, color='blue')

# 添加连线
c.add('geo', [('上海', '北京'), ('杭州', '北京'), ('深圳', '北京'), ('成都', '北京'), ('拉萨', '北京'), ("大庆", '北京')],
      type_=glb.ChartType.LINES,
      effect_opts=opts.EffectOpts(
          symbol=glb.SymbolType.TRIANGLE, symbol_size=6, color="red"),
      linestyle_opts=opts.LineStyleOpts(curve=0.2)).set_series_opts(
    label_opts=opts.LabelOpts(is_show=False))

# 添加标题
c.set_global_opts(title_opts=opts.TitleOpts(title="同学聚会地理连线图"))

# 输出图像
c.render("./output/地理连线图.html")
