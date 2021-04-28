import jieba.posseg as pseg
from pyecharts import options as opts
from pyecharts.charts import Graph
from tqdm import tqdm


def make_the_data_file(input_file):
    """
    这个函数是对原始文本数据进行处理，并且会在output目录下生成两个csv数据文件用于后续作图
    :param input_file: 待处理的文件
    :return: 函数无返回值，只会在output目录下生成两个csv文件
    """
    file_name = './data/' + input_file
    replace_dict = {item.split('，')[0].strip(): item.split('，')[1].strip()
                    for item in
                    open('./data/replace_dict.txt', encoding='utf-8').readlines()}
    ignore_list = open('data/ignore_list.txt', encoding='utf-8').read()
    node_file = './output/{}-人物节点.csv'.format(str(input_file).split('.')[0])
    link_file = './output/{}-人物连接.csv'.format(str(input_file).split('.')[0])

    line_list = open(file_name, 'r', encoding='GB18030').readlines()

    line_name_list = []  # 每个段落出现的人物列表
    name_cnt_dict = {}  # 统计人物出现次数

    print('正在分段统计……')
    print('已处理词数：')
    pbar = tqdm(line_list)  # 进度条对象
    for i in range(len(line_list)):  # 逐个段落循环处理
        pbar.set_description("已处理{}".format(i))
        pbar.update(1)  # 让进度条更新
        word_gen = pseg.cut(line_list[i])  # peseg.cut返回分词结果，“生成器”类型
        line_name_list.append(list())
        for one in word_gen:
            word = one.word
            flag = one.flag

            if len(word) == 1 or word in ignore_list:  # 跳过单字词以及忽略词
                continue

            if word in replace_dict.keys():  # 替换
                word = replace_dict[word]

            if flag == 'nr':
                line_name_list[-1].append(word)
                if word in name_cnt_dict.keys():
                    name_cnt_dict[word] = name_cnt_dict[word] + 1
                else:
                    name_cnt_dict[word] = 1

    print('基础数据处理完成')

    relation_dict = {}
    name_cnt_limit = 40
    # 统计共现数量
    for line_name in line_name_list:
        for name1 in line_name:
            if name1 in relation_dict.keys():
                pass
            elif name_cnt_dict[name1] >= name_cnt_limit:
                relation_dict[name1] = dict()
            else:  # 跳过出现次数较少的人物
                continue

            # 统计name1的共现数量
            for name2 in line_name:
                if name2 == name1 or name_cnt_dict[name2] < name_cnt_limit:
                    # 不统计name1自身；不统计出现较少的人物
                    continue
                if name2 in relation_dict[name1].keys():
                    relation_dict[name1][name2] = relation_dict[name1][name2] + 1
                else:
                    relation_dict[name1][name2] = 1
    print('共现统计完成，仅统计出现次数达到' + str(name_cnt_limit) + '及以上的人物')

    item_list = list(name_cnt_dict.items())
    item_list.sort(key=lambda x: x[1], reverse=True)

    node = open(node_file, 'w', encoding="utf-8")
    node.write('Name,Weight\n')
    node_cnt = 0  # 累计写入文件的节点数量
    for name, cnt in item_list:
        if cnt >= name_cnt_limit:  # 只输出出现较多的人物
            node.write(name + ',' + str(cnt) + '\n')
            node_cnt = node_cnt + 1
    node.close()
    print('人物数量：' + str(node_cnt))
    print('已写入文件：' + node_file)

    link_cnt_limit = 10
    print('只导出数量达到' + str(link_cnt_limit) + '及以上的连接')

    link = open(link_file, 'w', encoding="utf-8")
    # 连接文件，格式：Source,Target,Weight -> 人名1,人名2,共现数量
    link.write('Source,Target,Weight\n')
    link_cnt = 0  # 累计写入文件的连接数量
    for name1, link_dict in relation_dict.items():
        for name2, name_link in link_dict.items():
            if name_link >= link_cnt_limit:  # 只输出权重较大的连接
                link.write(name1 + ',' + name2 + ',' + str(name_link) + '\n')
                link_cnt = link_cnt + 1
    link.close()
    print('连接数量：' + str(link_cnt))
    print('已写入文件：' + link_file)

    # 对人物进行分类
    data_to_deal = open(node_file, 'r', encoding="utf-8").readlines()
    ultimate_data = list()
    ultimate_data.append(data_to_deal[0].strip() + ',Category')
    del data_to_deal[0]
    category_dict = {"田": 1, "孙": 2, "金": 3}
    for item in data_to_deal:
        if item[0] in category_dict.keys():
            ultimate_data.append(item.strip() + ',{}'.format(category_dict[item[0]]))
        else:
            ultimate_data.append(item.strip() + ',{}'.format(4))
    category_node_file = './output/{}-人物节点-分类.csv'.format(str(input_file).split('.')[0])
    file1 = open(category_node_file, 'w', encoding="utf-8")
    for item in ultimate_data:
        file1.write(item + '\n')
    file1.close()
    print('已写入文件：' + category_node_file)


def make_graph(input_file, node, link):
    node_file_name = node
    link_file_name = link
    out_file_name = './output/关系图-{}人物.html'.format(str(input_file).split('.')[0])

    node_file = open(node_file_name, 'r', encoding="utf-8")
    node_line_list = node_file.readlines()
    node_file.close()
    del node_line_list[0]

    link_file = open(link_file_name, 'r', encoding="utf-8")
    link_line_list = link_file.readlines()
    link_file.close()
    del link_line_list[0]

    categories = [{}, {'name': '田家'}, {'name': '孙家'}, {'name': '金家'}, {'name': '其它'}]
    node_in_graph = []
    for one_line in node_line_list:
        one_line = one_line.strip('\n')
        one_line_list = one_line.split(',')
        node_in_graph.append(opts.GraphNode(
            name=one_line_list[0],
            value=int(one_line_list[1]),
            symbol_size=int(one_line_list[1]) / 20,
            category=int(one_line_list[2])))  # 手动调整节点的尺寸
    link_in_graph = []
    for one_line in link_line_list:
        one_line = one_line.strip('\n')
        one_line_list = one_line.split(',')
        link_in_graph.append(opts.GraphLink(
            source=one_line_list[0],
            target=one_line_list[1],
            value=int(one_line_list[2])))

    c = Graph()
    c.add("",
          node_in_graph,
          link_in_graph,
          edge_length=[10, 50],
          repulsion=5000,
          layout="circular",
          categories=categories,
          is_rotate_label=True,
          linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3)
          )
    c.set_global_opts(title_opts=opts.TitleOpts(title="关系图-平凡的世界人物"))
    c.render(out_file_name)


if __name__ == '__main__':
    file_to_deal = "平凡的世界.txt"
    make_the_data_file(file_to_deal)
    make_graph(file_to_deal,
               './output/{}-人物节点-分类.csv'.format(str(file_to_deal).split('.')[0]),
               './output/{}-人物连接.csv'.format(str(file_to_deal).split('.')[0]))
