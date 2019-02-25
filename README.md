### HeatMap
- 北京地区二手房平均房价热力图呈现

### 准备数据
- 通过爬虫,从链家网站上获取目标数据(小区名称,平均房价)

### 数据清洗处理
- 通过百度API,反查各小区在百度地图上对应的经纬度
- http://api.map.baidu.com/place/v2/suggestion?query={}&region={}&city_limit={}&output=json&ak={}
  - query:str 需要查询的地点
  - region:str 查询的地区
  - city_limit:bool类型,是否返回查询的region范围的经纬度
  - output:str 返回的数据格式
  - ak:str 百度申请的密钥

### 重写热力图呈现的代码
- 百度提供热力图显示的h5/js demo,http://lbsyun.baidu.com/jsdemo/demo/c1_15.htm
- 将获取到的数据重写到demo对应的数据位置
