import requests
import numpy as np
import time  # 增加延时模块

GAODE_API_KEY = 'a939fde28ecc1694742c60828bdb4468'  # 请替换为你的高德地图API Key

def get_travel_time(origin, destination, mode='driving'):
    print(f"请求出发点 {origin} 到目的地 {destination}，方式：{mode}")
    if mode == 'driving':
        url = 'https://restapi.amap.com/v3/direction/driving'
        strategy = 0  # 最快路线
    elif mode == 'walking':
        url = 'https://restapi.amap.com/v3/direction/walking'
        strategy = None
    elif mode == 'transit':
        url = 'https://restapi.amap.com/v3/direction/transit/integrated'
        strategy = None
    else:
        raise ValueError('不支持的交通方式')
    # 高德API要求坐标格式为“经度,纬度”
    params = {
        'key': GAODE_API_KEY,
        'origin': f'{origin[0]},{origin[1]}',
        'destination': f'{destination[0]},{destination[1]}',
    }
    if mode == 'driving' and strategy is not None:
        params['strategy'] = strategy
    if mode == 'transit':
        params['city'] = '深圳'
    print(f"请求参数: {params}")
    response = requests.get(url, params=params)
    data = response.json()
    try:
        if mode == 'driving':
            time_sec = int(data['route']['paths'][0]['duration'])
        elif mode == 'walking':
            time_sec = int(data['route']['paths'][0]['duration'])
        elif mode == 'transit':
            time_sec = int(data['route']['transits'][0]['duration'])
        print(f"耗时：{time_sec}秒")
    except Exception:
        print("API返回异常，耗时设为无穷大")
        time_sec = float('inf')
    time.sleep(0.5)  # 增加延时，防止并发超限
    return time_sec

def find_best_meeting_point(origins, modes, area_center, area_radius=0.06, grid_num=10):
    print("开始搜索最佳聚会点...")
    lats = np.linspace(area_center[1] - area_radius, area_center[1] + area_radius, grid_num)
    lngs = np.linspace(area_center[0] - area_radius, area_center[0] + area_radius, grid_num)
    best_point = None
    min_time_diff = float('inf')
    min_max_time = float('inf')
    total = grid_num * grid_num
    count = 0
    for lat in lats:
        for lng in lngs:
            count += 1
            print(f"进度：{count}/{total}，评估候选点: ({lng}, {lat})")
            times = [get_travel_time(origin, (float(lng), float(lat)), mode) for origin, mode in zip(origins, modes)]
            print(f"各人到达时间: {times}")
            time_diff = max(times) - min(times)
            max_time = max(times)
            print(f"当前时间差: {time_diff}，最大耗时: {max_time}")
            # 优先最大耗时最小，再比较时间差
            if (max_time < min_max_time) or (max_time == min_max_time and time_diff < min_time_diff):
                min_max_time = max_time
                min_time_diff = time_diff
                best_point = (float(lng), float(lat))
                print(f"更新最佳点: {best_point}，最小最大耗时: {min_max_time}，最小时间差: {min_time_diff}")
    print("搜索结束")
    return best_point, min_time_diff, min_max_time

# 示例输入
origins = [(114.054037, 22.567977), (114.101319, 22.542184), (114.230907, 22.736640)]
modes = ['driving', 'driving', 'driving']

area_center = (sum([o[0] for o in origins]) / len(origins)+0.02, sum([o[1] for o in origins]) / len(origins)+0.03)

best_point, min_time_diff, min_max_time = find_best_meeting_point(origins, modes, area_center)
print(f'最佳聚会点：{best_point}，三人到达时间差：{min_time_diff}秒，最大耗时：{min_max_time}秒')