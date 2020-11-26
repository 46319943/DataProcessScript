import requests
import json
import time


# 关注区域的左下角和右上角百度地图坐标(经纬度）
Boundary = setting['boundary']
# 定义细分窗口的数量，横向X * 纵向Y
WindowSize = setting['windowSize']


def split_bounds(boundary,
                 windowSize={
                'xNum': 1,
                'yNum': 1
            },
                 windowIndex=0,
                 stringfy=True):
    """
    获取小矩形的左下角和右上角坐标字符串
    :param boundary: 关注区域坐标信息
    :param windowSize:  细分窗口数量信息
    :param windowIndex:  Z型扫描的小矩形索引号
    :return: lat,lng,lat,lng
    """
    offset_x = (boundary['max']['x'] -
                boundary['min']['x']) / windowSize['xNum']
    offset_y = (boundary['max']['y'] -
                boundary['min']['y']) / windowSize['yNum']
    min_x = boundary['min']['x'] + offset_x * (windowIndex %
                                                 windowSize['xNum'])
    min_y = boundary['min']['y'] + offset_y * (windowIndex //
                                                 windowSize['yNum'])
    max_x = (min_x + offset_x)
    max_y = (min_y + offset_y)
    if stringfy:
        return f'{min_y},{min_x},{max_y},{max_x}'
    else:
        return {
            "min": {
                "x": min_x,
                "y": min_y
            },
            "max": {
                "x": max_x,
                "y": max_y
            }
        }


def fetchPOI(keyword, boundary, ws):
    pageNum = 0
    first_it = True

    URL = "http://api.map.baidu.com/place/v2/search?query=" + keyword + \
        "&bounds=" + split_bounds(boundary) + \
        "&output=json" + \
          "&ak=" + API_KEY + \
          "&scope=2" + \
          "&page_size=20" + \
          "&coord_type=wgs84ll" + \
          "&page_num=" + str(pageNum)


            
            
        
        res = None

        total = res['total']

        if first_it:
            print('找到要素', total, '个')
            first_it = False

        # 如果此区域不存在点
        if total == 0:
            break
        # 如果翻页后，此页没有
        elif len(res['results']) == 0:
            break
        # 超过了400个，需要划分小格子。把当前区域划分成4个小格子
        elif total == 400:
            for i in range(4):
                fetchPOI(
                    keyword,
                    split_bounds(boundary, {
                        'xNum': 2.0,
                        'yNum': 2.0
                    }, i, False), ws)
            # 递归完成之后，跳出循环
            break
        else:
            count = len(res['results'])
            for r in res['results']:
                # 访问字段异常
                try:
                    values = [
                        r['name'],
                        float(r["location"]["lat"]),
                        float(r["location"]["lng"]), r["address"], r["area"]
                    ]
                    if r["detail"] == 1:
                        # 有时候没有type字段
                        if 'type' in r["detail_info"]:
                            values.append(r["detail_info"]["type"])
                        # 有时候没有tag字段
                        if 'tag' in r["detail_info"]:
                            values.append(r["detail_info"]["tag"])
                    ws.append(values)
                except Exception as e:
                    print('访问字段异常')
                    print(r)
                    print(e)
                
            print('完成要素：%d / %d' % (20 * pageNum + count, total))
            # 如果等于二十个，需要翻页。否则不用翻页
            if count == 20:
                pageNum += 1
            else:
                break


def requestBaiduApi(keyword, ws):
    # 声明全局变量，从而可以对其进行赋值（Python没有声明关键字的特点
    global API_KEY
    # 添加标题
    ws.append(['名称', '纬度', '经度', '地址', '区县', '一类', '二类'])
    # 循环视口
    windowNum = int(WindowSize['xNum'] * WindowSize['yNum'])
    for i in range(windowNum):
        rect = split_bounds(Boundary, WindowSize, i, stringfy=False)

        print('当前搜索窗口：%d / %d (%s)' % (i + 1, windowNum, keyword))
        fetchPOI(keyword, rect, ws)


def city_bounds(city_name):

    pass



def main():
    pass


if __name__ == '__main__':
    main()