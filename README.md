# Meeting Point Optimizer

本项目用于自动计算多人聚会的最优集合点，并可视化每个人的路径。支持百度地图和高德地图API，适用于朋友聚会、团队活动等场景，帮助大家公平、便捷地选择集合地点。

## 功能简介

- 输入多个出发点坐标，自动搜索使所有人到达时间差最小且最大耗时最少的聚会点
- 支持多种交通方式（驾车、步行、公交）
- 可视化每个人的路径及最佳聚会点（生成 HTML 地图）
- 支持自定义搜索区域和精度
- 搜索范围和网格划分可在地图上直观展示

## 主要文件说明

- baidu_cal.py：基于百度地图API的最优点计算算法
- gaode_cal.py：基于高德地图API的最优点计算算法
- path.py / area.py：使用 folium 绘制地图，展示所有路径、最佳聚会点、搜索范围和网格
- meeting_map.html / area_map.html：自动生成的可视化地图文件

## 使用方法

1. **准备环境**
   - Python 3.7+
   - 安装依赖：
     ```bash
     pip install requests numpy folium
     ```

2. **配置地图API Key**
   - 在 baidu_cal.py 设置 `BAIDU_API_KEY`
   - 在 gaode_cal.py 设置 `GAODE_API_KEY`

3. **运行计算脚本**
   - 百度地图：
     ```bash
     python baidu_cal.py
     ```
   - 高德地图：
     ```bash
     python gaode_cal.py
     ```
   - 输出最佳聚会点坐标、到达时间差和最大耗时

4. **生成地图可视化**
   ```bash
   python path.py
   # 或
   python area.py
   ```
   - 在项目目录下生成 HTML 地图文件，用浏览器打开即可查看

## 示例

- 出发点：
  - (114.054037, 22.567977)
  - (114.101319, 22.542184)
  - (114.230907, 22.736640)
- 搜索区域自动以三点中心为基准
- 结果：输出最佳聚会点坐标，并在地图上展示所有路径、搜索范围和网格

## 注意事项

- 地图API有访问频率限制，脚本已自动延时处理
- 搜索精度可通过 `grid_num` 参数调整，精度高速度慢
- 交通方式可选 `'driving'`、`'walking'`、`'transit'`
- 可视化文件为 HTML 格式，推荐使用 Chrome 浏览器打开

## 许可证

MIT License

---

如有问题或建议，欢迎提交 Issue 或 PR！