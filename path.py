import folium

origins = [(114.054037, 22.567977), (114.101319, 22.542184), (114.230907, 22.736640)]
best_point = (114.07317542105262, 22.605001631578947)

m = folium.Map(location=[best_point[1], best_point[0]], zoom_start=12)
for i, origin in enumerate(origins):
    folium.Marker([origin[1], origin[0]], popup=f'起点{i+1}').add_to(m)
    folium.PolyLine([[origin[1], origin[0]], [best_point[1], best_point[0]]], color='blue').add_to(m)
folium.Marker([best_point[1], best_point[0]], popup='最佳聚会点', icon=folium.Icon(color='red')).add_to(m)
m.save('meeting_map.html')