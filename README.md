# 数据处理脚本
- 城市数量：105
- 格式处理：所有表格数据存储为CSV格式

# 数据结构
- ChinaSHP
    - 105个城市的行政区边界
- House
    - Origin
        - 原始租房、二手房数据
    - 过滤后的租房、二手房的量化数据
- POI
    - 城市的兴趣点数据，每个多类兴趣点

# 总流程
- POI
    - XLSx格式转为CSV: poi_xls_to_csv.py
    - POI命名更改：house_merge_stat.py中poi_rename函数
    - 将专科、综合医院合并，去除三甲医院，保留普通医院: poi_hospital_classify.py
    - 高新公司、公司分类: poi_company_classify.py
- House
    - 租房过滤: house_filter.py
- Arcpy
    - 展点、裁切。对于POI，同时进行商圈、三甲医院的裁切: arcpy_clip.py
    - 高新公司对应房屋点的核密度计算: arcpy_kde.py
    - 路网距离计算: arcpy_network.py
- House
    - 根据路网距离，计算因子: house_merge_od.py

- 其他
    - 将SHP格式的普通医院、三甲医院单独拷出: poi_copy_hospital.py
    - xls转为xlsx: xls_to_xlsx.py

# 问题数据
- POI
    - CSV
        - Dongguan
            - Company.csv不存在
            - Czone.csv不存在
        - Liupanshui
            - Czone.csv内容错误