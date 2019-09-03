
# 数据读取


```python
import pandas as pd
import numpy as np

iris_data = pd.read_csv("../dataset/iris/iris.data", 
                        header=None, 
                        names = ["花萼长度", "花萼宽度", "花瓣长度", "花瓣宽度", "类别"], 
                        encoding = 'gbk');
pd.set_option("display.max_rows", 5)  # 设置最大显示5行数据
```


```python
iris_data.head()
```


```python
iris_data.tail()

```

# 数据切片与删除


```python
iris_data[:50]
```


```python
DataFrame = iris_data[:5].copy()         # 建立数据副本，以便多次修改
DataFrame.drop(index=[1,3])
```


```python
DataFrame = iris_data[:5].copy()         # 建立数据副本，以便多次修改
DataFrame.drop(columns=["花萼宽度", "花瓣宽度"])

```

# 基本赋值


```python
DataFrame = iris_data[:5].copy()         # 建立数据副本，以便多次修改
DataFrame.loc[0, "类别"] = "新类别名"    # 修改第0行类别标签列的数据
```


```python
DataFrame = iris_data[:5].copy()    # 建立数据副本，以便多次修改
DataFrame.loc[1] = "新数据"         # 修改第1行的数据
```


```python
DataFrame = iris_data[:5].copy()    # 建立数据副本，以便多次修改
DataFrame.loc[:, "花萼长度"] = 10   # 修改第1列的数据
```


```python
DataFrame = iris_data[:5].copy()    # 建立数据副本，以便多次修改

```

# index 检索 iloc[左闭右开]


```python
DataFrame.iloc[-1]                     # 最后一行
DataFrame.iloc[:, 1]                   # 第1列
DataFrame.iloc[:3, :3]                 # 前三行的前三列
DataFrame.iloc[[0,1,3], 1]             # 第0，1，3行的第1列
DataFrame.iloc[[True, False, True]]   # 第0，2行

```

# label 检索 loc[左闭右闭]


```python
# DataFrame.loc[-1]                    # 语法错误！！！
DataFrame.loc[0]                       # 第0行
DataFrame.loc[:, "花萼长度"]           # 所有行的“花萼长度”列
DataFrame.loc[[0,1,3], "类别"]         # 第0，1，3行的“类别”列
DataFrame.loc[[True, False, True]]    # 第0，2行

```

# 条件检索


```python
DataFrame.loc[DataFrame["花萼长度"]>4.8]
```


```python
DataFrame.loc[(DataFrame["花萼长度"]>=5.0) & (DataFrame["花瓣长度"]>=1.4)]
```


```python
df = iris_data.loc[iris_data["花萼长度"].isnull()]
```


```python
df = iris_data.loc[iris_data["类别"].notnull()]
```


```python
df = iris_data.loc[iris_data["花萼长度"].isin([5.0])]

```

# *条件统计


```python
iris_data.loc[iris_data["类别"] == "Iris-versicolor"].count()
```


```python
c1 = sum(iris_data["类别"] == "Iris-setosa")
c2 = sum(iris_data["类别"] == "Iris-versicolor")
c3 = sum(iris_data["类别"] == "Iris-virginica")
print(c1, c2, c3)   # 手动统计各类样本数量
```


```python
iris_data["类别"].value_counts()

```

# 条件赋值


```python
DataFrame = iris_data[:5].copy()    # 建立数据副本，以便多次修改
DataFrame.loc[DataFrame["花萼长度"]>4.8, "类别"] = "大花萼"
```


```python
DataFrame = iris_data[:5].copy()    # 建立数据副本，以便多次修改
DataFrame.loc[DataFrame["花萼长度"]>4.8] = "错误赋值"

```

# 数据分析


```python
iris_data.describe()
iris_data["类别"].describe()
```


```python
iris_data["类别"].count()
```


```python
iris_data.max()
iris_data["花萼长度"].max()
```


```python
iris_data.min()
iris_data["花萼长度"].min()
```


```python
iris_data.mean()
iris_data["花萼长度"].mean()
```


```python
iris_data.median()
iris_data["花萼长度"].median()
```


```python
iris_data.mode()
iris_data["花萼长度"].mode()    # 众数
```


```python
# iris_data.unique()   # 语法错误
iris_data["类别"].unique()       # 列出不同的取值
```


```python
np.sort(iris_data["花萼长度"].unique())  # 默认升序排列
```


```python
# iris_data.value_counts()    # 语法错误
iris_data["类别"].value_counts()
```


```python
iris_data.agg(['max', 'min', 'mean', 'median'])   # agg 聚合操作，可运行多个函数
iris_data["花萼长度"].agg(['max', 'min', 'mean', 'median'])
```


```python
iris_data.groupby(['花萼长度'])['花萼长度'].count()   # 分组，花萼长度由小到大排列
```


```python
iris_data_review = iris_data.groupby(['花萼长度'])['类别'].agg(['min', 'max'])  # 分组
```


```python
iris_data_review.reset_index()
```


```python
iris_data.sort_values(by=['花萼长度', '花瓣长度'])

```

# 空值处理


```python
iris_data.isnull()
iris_data.isnull().sum()
```


```python
iris_data.fillna('Unknown')
iris_data["花萼长度"].fillna('Unknown')
```


```python
mean = iris_data['花萼宽度'].mean()
median = iris_data['花瓣长度'].median()
mode = iris_data['花萼宽度'].mode()
values = {'花萼长度': 0, '花萼宽度': mean, '花瓣长度': 2, '花萼宽度': mode}
iris_data.fillna(value=values)
```


```python
iris_data.dropna()                          # 去掉含缺失项的行
iris_data.dropna(axis='columns')            # 去掉含缺失项的列
iris_data.dropna(how='all')                 # 去掉所有项均缺失的行
iris_data.dropna(thresh=2)                  # 去掉多于2个缺失项的行
```


```python
df = iris_data.replace(5.0, 50)                       # 默认为深复制，保护原数据
df['花萼宽度'] = df['花萼宽度'].replace(3.5, 30.5)
df = df.replace([0, 1, 2, 3], 4)
df = df.replace([0, 1, 2, 3], [4, 3, 2, 1])
df = df.replace({'花萼长度':5.1, '花瓣长度':5.1}, 5)
df = df.replace({'花瓣长度' : {5.1:5.0, 6.2:6.0}})

```

# 数据保存


```python
iris_data.to_csv("../dataset/newdata.csv", na_rep="NA", index = False, encoding='gbk')
```


```python
iris_data = pd.read_csv("../dataset/iris/iris.csv", encoding = "gbk");
iris_data.head()

```

# 创建DataFrame

**pd.DataFrame( data=None, index=None, columns=None, dtype=None, copy=False)**  
    - data：可选数据类型，如:ndarray，series，map，lists，dict，constant和另一个DataFrame
    - index：行标签索引，缺省值np.arrange(n)，不计入df列
    - columns：列标签索引，缺省值np.arrange(n),不计入df行
    - dtype：每列的数据类型
    - copy：默认值False，引用/复制数据


```python
df = pd.DataFrame()   # 空数据帧
df = pd.DataFrame(['a','b','c','d'])  # 从一维列表创建
df = pd.DataFrame([['Alex',10],['Bob',12],['Clarke',13]], dtype=float)   # 从二维列表创建，浮点型数字
df = pd.DataFrame({'Name':['Tom', 'Jack', 'Steve', 'Ricky'],'Age':[28,34,29,42]})  # 从字典创建，字典键默认为列标签
```
