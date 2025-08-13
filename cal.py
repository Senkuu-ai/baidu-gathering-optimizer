import requests
import numpy as np
import time  # 增加延时模块

BAIDU_API_KEY = 'pPKOMy6VZM7bfdpCLEW8tBMPeMwTfqWn'

def get_travel_time(origin, destination, mode='driving'):
    print(f"请求出发点 {origin} 到目的地 {destination}，方式：{mode}")
    if mode == 'driving':
        uri = '/directionlite/v1/driving'
        url = 'http://api.map.baidu.com' + uri
    elif mode == 'walking':
        uri = '/directionlite/v1/walking'
        url = 'http://api.map.baidu.com' + uri
    elif mode == 'transit':
        uri = '/directionlite/v1/transit'
        url = 'http://api.map.baidu.com' + uri
    else:
        raise ValueError('不支持的交通方式')
    # 注意：百度API要求坐标格式为“纬度,经度”
    params = {
        'ak': BAIDU_API_KEY,
        'origin': f'{origin[1]},{origin[0]}',
        'destination': f'{destination[1]},{destination[0]}',
        'region': '深圳',
        'output': 'json'
    }
    print(f"请求参数: {params}")
    response = requests.get(url, params=params)
    data = response.json()
    # print(f"API返回: {data}")
    try:
        time_sec = int(data['result']['routes'][0]['duration'])
        print(f"耗时：{time_sec}秒")
    except Exception:
        print("API返回异常，耗时设为无穷大")
        time_sec = float('inf')
    time.sleep(0.5)  # 增加延时，防止并发超限
    return time_sec

def find_best_meeting_point(origins, modes, area_center, area_radius=1.0, grid_num=200):
    print("开始搜索最佳聚会点...")
    lats = np.linspace(area_center[0] - area_radius, area_center[0] + area_radius, grid_num)
    lngs = np.linspace(area_center[1] - area_radius, area_center[1] + area_radius, grid_num)
    best_point = None
    min_time_diff = float('inf')
    total = grid_num * grid_num
    count = 0
    for lat in lats:
        for lng in lngs:
            count += 1
            print(f"进度：{count}/{total}，评估候选点: ({lat}, {lng})")
            # 强制转换为float，避免numpy.float64类型导致API报错
            times = [get_travel_time(origin, (float(lat), float(lng)), mode) for origin, mode in zip(origins, modes)]
            print(f"各人到达时间: {times}")
            time_diff = max(times) - min(times)
            print(f"当前时间差: {time_diff}")
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                best_point = (float(lat), float(lng))
                print(f"更新最佳点: {best_point}，最小时间差: {min_time_diff}")
    print("搜索结束")
    return best_point, min_time_diff

# 示例输入
origins = [(114.054037, 22.567977), (114.101319, 22.542184), (114.230907, 22.736640)]
modes = ['driving', 'driving', 'driving']
area_center = (114.075807, 22.633949)

best_point, min_time_diff = find_best_meeting_point(origins, modes, area_center)
print(f'最佳聚会点：{best_point}，三人到达时间差：{min_time_diff}秒')