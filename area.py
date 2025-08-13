import folium
import numpy as np

origins = [(114.054037, 22.567977), (114.101319, 22.542184), (114.230907, 22.736640)]
best_point = (114.0962151632653, 22.69517348979592)
area_center = (sum([o[0] for o in origins]) / len(origins)+0.02, sum([o[1] for o in origins]) / len(origins)+0.03)
area_radius = 0.06  # 与算法保持一致
grid_num = 20

m = folium.Map(location=[area_center[1], area_center[0]], zoom_start=13)

# 绘制搜索范围圆形
folium.Circle(
    location=[area_center[1], area_center[0]],
    radius=area_radius * 111000,  # 1度约等于111km
    color='green',
    fill=True,
    fill_opacity=0.07,
    popup='搜索范围'
).add_to(m)

# 绘制网格
lats = np.linspace(area_center[1] - area_radius, area_center[1] + area_radius, grid_num)
lngs = np.linspace(area_center[0] - area_radius, area_center[0] + area_radius, grid_num)
for lat in lats:
    folium.PolyLine([[lat, lngs[0]], [lat, lngs[-1]]], color='gray', weight=1, opacity=0.3).add_to(m)
for lng in lngs:
    folium.PolyLine([[lats[0], lng], [lats[-1], lng]], color='gray', weight=1, opacity=0.3).add_to(m)

# 标记起点和最佳点
for i, origin in enumerate(origins):
    folium.Marker([origin[1], origin[0]], popup=f'起点{i+1}').add_to(m)
folium.Marker([best_point[1], best_point[0]], popup='最佳聚会点', icon=folium.Icon(color='red')).add_to(m)

m.save('area_map.html')