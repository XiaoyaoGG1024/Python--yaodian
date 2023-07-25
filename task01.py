# -*- coding: utf-8 -*-
# @Time : 2022/4/25 15:57 
# @Author : 逍遥哥哥每天都要努力啊！ 
# @File : task01.py

#月均消费次数，月均消费金额，客单价，消费趋势
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
data=pd.read_excel("./data/春晓药店2018年销售数据 (1.csv).xlsx",dtype=object)
#数据清洗
#数据清洗过程包括：选择子集、列明重命名、缺失数据处理，数据类型转换，数据排序，异常值处理
#"购药时间"更改为”销售时间“ rename()
data.rename(columns={"购药时间":"销售时间"},inplace=True)
#缺失值处理
#删除 dropna()
dataNew=data.dropna()
#数据类型转换，读取数据时object,对数值类型进行数据类型转换
#销售数量', '应收金额', '实收金额'转为float  astype()
dataNew["销售数量"]=dataNew["销售数量"].astype(float)
dataNew['应收金额']=dataNew['应收金额'].astype(float)
dataNew['实收金额']=dataNew['实收金额'].astype(float)
#第一一个处理方法，传入原始数据
def getdate(times):
    dateList=[]#接受处理后的日期
    for i in times:
        dateList.append(i.split(" ")[0]) #通过for循环，将销售时间传入list
    datetime=pd.Series(dateList)#将list转换成Series
    return   datetime

dataNew.loc[:,"销售时间"]=getdate(dataNew.loc[:,"销售时间"])#调用getdate函数,处理销售时间
#转换日期数据时将不能转换的数据转换为nan
dataNew["销售时间"]=pd.to_datetime(dataNew["销售时间"],errors='coerce')
#删除销售时间转换过程中空值
data1=dataNew.dropna()
#数据排序
dataNew=data1.sort_values(by="销售时间",ascending=True)
#重置行索引
dataNew=dataNew.reset_index(drop=True)
#异常值处理
#将销售数量大于0的子集重新赋值给datanew
dataNew=dataNew.loc[dataNew["销售数量"]>0]
dataNew=dataNew.reset_index(drop=True)
# print(dataNew.describe())
#构建模型及数据可视化

#月均消费次数：月均消费次数=总消费次数/月份数
#总消费次数：同一天内同一个人发生的所有消费算作一次
#计算总消费次数
#根据销售时间和社保卡号检查消费重复情况
dataNew.duplicated(["销售时间","社保卡号"])
#删除销售时间和社保卡号重复的数据,只做统计次数，不用考虑保留哪一个
kpi1_df=dataNew.drop_duplicates(["销售时间","社保卡号"])
#将形状大小数据的行存入变量存入total_times(总消费次数)
total_times=kpi1_df.shape[0]
#计算月份数 销售时间跨度/30，重置索引
kpi1_df=kpi1_df.sort_values(by="销售时间",ascending=True).reset_index()
startTime=kpi1_df.loc[0,"销售时间"]
endTime=kpi1_df.loc[total_times-1,"销售时间"]
#计算两个时间相差的天数
total_days=(endTime-startTime).days
#计算总月份数
month=round((total_days/30),1)
#计算月均消费次数（取整）
kpi1=int(total_times/month)

#月均消费金额：总消费金额/月份数
#计算总消费金额
total_money=dataNew["实收金额"].sum()
#月均消费金额=总消费金额/月份数(保留两位)
kpi2=round(total_money/month,2)
#客单价=总消费金额/总消费次数
kpi3=round(total_money/total_times,2)

#消费趋势
#1.csv.分析个人日消费金额（条形图）
#复制一份数据（深拷贝）
groupdf=dataNew.copy(deep=True)
#分组统计
df1=groupdf.groupby(["销售时间","社保卡号"])["实收金额"].sum()
# plt.figure(figsize=(10,7),dpi=180)
# plt.plot(df1.values)
# plt.show()
#个人消费金额差距较大，最高消费超过2500，大部分消费低于500，个人日均消费在100以内

#2.分析药店日消费金额（条形图）
#分组统计,按销售时间分组
df2=groupdf.groupby(["销售时间"]).sum()
# plt.figure(figsize=(10,7),dpi=180)
# plt.title("日销售金额")
# plt.xlabel("日期")
# plt.ylabel("金额")
# plt.bar(df2.index,df2["实收金额"])
#绘制水平线
# plt.axhline(df2["实收金额"].mean(),color="red",lineStyle="--")
#绘制网格线
# plt.grid(linestyle="--",alpha=0.2)
# plt.show()

#3.分析日用户数（折线图）
df3=df1.reset_index().groupby("销售时间")["社保卡号"].count().reset_index()
# plt.figure()
# plt.plot(df3["销售时间"],df3["社保卡号"])
# plt.show()

#4.分析药店月销售金额(条形图)
df4=groupdf.groupby("销售时间")["实收金额"].sum().reset_index()
df4_1=df4.groupby(df4["销售时间"].dt.month).sum().reset_index()
plt.figure()
plt.title("月销售金额")
plt.xlabel("月份")
plt.ylabel("金额")
plt.bar(df4_1["销售时间"],df4_1["实收金额"])
plt.axhline(df4_1["实收金额"].mean(),color="red",lineStyle="--")
plt.grid(linestyle="--",alpha=0.2)
plt.show()
#5.分析月用户数(折现图)
df5=groupdf.groupby("销售时间")["社保卡号"].count().reset_index()
df5.index=df5["销售时间"]
df5_1=df5.groupby(df5.index.month).sum()
# plt.figure()
# plt.title("月用户总数")
# plt.xlabel("月份")
# plt.ylabel("数量")
# plt.plot(df5_1.index,df5_1["社保卡号"])
# plt.axhline(df5_1["社保卡号"].mean(),color="red",lineStyle="--")
# plt.grid(linestyle="--",alpha=0.2)
# plt.show()
#6.分析药店销售情况（销量）,(将销量前十的药品绘制条形图)
df6=groupdf.groupby("商品名称").count().sort_values(by="销售数量",ascending=False).head(10).reset_index()
# plt.figure(figsize=(10,7),dpi=100)
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.title("药店销售前十")
# plt.xlabel("商品名称")
# plt.ylabel("数量")
# plt.bar(df6["商品名称"],df6["销售数量"])
# plt.axhline(df6["销售数量"].mean(),color="red",lineStyle="--")
# plt.grid(linestyle="--",alpha=0.2)
# plt.xticks(rotation=-20)
# plt.show()