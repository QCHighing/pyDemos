

```python
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
```

# 1. 绘制3D曲面

### 1.1 创建[3D图形对象](https://matplotlib.org/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.html?highlight=axes3d)


```python
fig = plt.figure()  # 创建图像对象
ax = Axes3D(fig)    # 创建3D的多轴对象
```


### 1.2 绘制曲面 [ax.plot_surface](https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#surface-plots)

```python
Axes3D.plot_surface(X, Y, Z, *args, **kwargs)

参数：
    - X,Y,Z：二维数组类型
    - rcount, ccount：指定x, y方向的贴片数（数字越大网格越密集）
    - color：color-like类型，表面贴片的颜色
    - cmap：colormap类型，表面贴片的色图，建议使用'jet'或 plt.cm.jet
返回：
    - 空
```

### 1.3 设置字体

```python
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使 plt 中的中文字体能够显现
plt.rcParams['axes.unicode_minus'] = False   # 使 plt 中的中文字体能够显现
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
```

### 1.4 设置标题

```python
text = Axes3D.set_title(label, fontdict=None, loc='center', **kwargs)

参数：
    - label：字符串类型，标题文本
    - fontdict：字典类型，默认值为{'fontsize': rcParams['axes.titlesize'],
                                   'fontweight' : rcParams['axes.titleweight'],
                                   'verticalalignment': 'baseline',
                                   'horizontalalignment': loc}
    - loc：字符串类型，标题的位置，'center', 'left', 'right'
    - pad：float类型，标题偏离图像的磅数
返回：
    - text：代表了标题的matplotlib文本实例
```

### 1.5 设置轴

- 设置 x,y,z 轴的范围[a, b]
```python
ax.set_xlim(a, b)
ax.set_ylim(a, b)
ax.set_zlim(a, b)
```

- 设置 x,y,z 轴的刻度类型：{"linear", "log", "symlog", "logit", ...}
```python
ax.set_xscale("linear")
```

- 设置 x,y,z 轴的标签
```python
ax.set_ylabel(ylabel, fontdict=None, labelpad=None, **kwargs)
```

- 关闭网格线
```python
Axes3D.grid(False)
```

### 1.6 开/关坐标轴

- 关闭坐标轴：（轴线，刻度线，刻度标签，网格和轴标签）
```python
Axes3D.set_axis_off()
```

- 开启坐标轴：（轴线，刻度线，刻度标签，网格和轴标签）
```python
Axes3D.set_axis_on()
```

# 2. 曲面

### 2.1 旋转抛物面

 $$f(X) = \sum_{i=1}^n {x_i}^2 ,\quad |x_i|\leq 100$$
 最优状态与最优解：
 $$min \left( f(X^*) \right) =f(0,0,\cdots,0) = 0$$


```python
def func_1():
    name = u"Sphere Model 旋转曲面"
    x = np.arange(-100, 100, 0.1)
    y = np.arange(-100, 100, 0.1)
    x, y = np.meshgrid(x, y)
    z = x**2 + y**2
    return name, x, y, z
```

![iz62PU.png](https://s1.ax1x.com/2018/11/17/iz62PU.png)

### 2.2 Schwefel’s Problem 2.22

$$f(x)=\sum_{i=1}^n |x_i|+\prod_{i=1}^n |x_i| ,\quad |x_i|\leq 10$$
最优状态与最优解：
$$min \left( f(X^*) \right) =f(0,0,\cdots,0) = 0$$


```python
def func_2():
    name = u"Schwefel's Problem 2.22"
    x = np.arange(-10, 10, 0.1)
    y = np.arange(-10, 10, 0.1)
    x, y = np.meshgrid(x, y)   # 转化为网格矩阵
    z = np.abs(x) + np.abs(y) + np.abs(x * y)
    return name, x, y, z
```

![FSYy26.png](https://s1.ax1x.com/2018/11/18/FSYy26.png)

### 2.3 Schwefel's Problem 1.2

$$f(X) = \sum_{j=1}^n \left(\sum_{i=1}^j x_i \right)^2 ,\quad |x_i|\leq 100$$
最优状态与最优解：
$$min \left( f(X^*) \right) =f(0,0,\cdots,0) = 0$$


```python
def func_3():
    name = u"Schwefel's Problem 1.2"
    x = np.arange(-100, 100, 1)
    y = np.arange(-100, 100, 1)
    x, y = np.meshgrid(x, y)   # 转化为网格矩阵
    z = x**2 + (x+y)**2
    return name, x, y, z
```

![FSteiR.png](https://s1.ax1x.com/2018/11/18/FSteiR.png)

### 2.4 Schwefel's Problem 2.21

$$f(X) = \mathop{max}_{i=1}^n \left\{ |x_i| \right\} ,\quad |x_i|\leq 100$$
最优状态与最优解：
$$min \left( f(X^*) \right) =f(0,0,\cdots,0) = 0$$


```python
def func_4():
    name = u"Schwefel's Problem 2.21"
    x = np.arange(-100, 100, 0.1)
    y = np.arange(-100, 100, 0.1)
    x, y = np.meshgrid(x, y)   # 转化为网格矩阵
    z = np.max(np.array([abs(x), abs(y)]), axis=0)  # 两层对应元素之间对比
    return name, x, y, z
```

![FSNzvV.png](https://s1.ax1x.com/2018/11/18/FSNzvV.png)

### 2.5 Generalized Rosenbrock's Function

$$f(X)=\sum_{i=1}^{n-1} \left[ 100(x_{i+1}-x_i^2)^2 + (1-x_i)^2 \right] ,\quad |x_i| \leq 30$$
最优状态与最优解：
$$min \left( f(X^*) \right) =f(1,1,\cdots,1) = 0$$


```python
def func_5():
    name = u"Generalized Rosenbrock's Function"
    x = np.arange(-30, 30, 0.1)
    y = np.arange(-30, 30, 0.1)
    x, y = np.meshgrid(x, y)   # 转化为网格矩阵
    z = 100*(y-x**2)**2 + (1-x)**2
    return name, x, y, z
```

![FSUlUH.png](https://s1.ax1x.com/2018/11/18/FSUlUH.png)

### 2.6 Generalized Rastrigin's Function

$$f(X)=\sum_{i=1}^{n} \left[ x_i^2-10cos(2\pi x_i)+10 \right] ,\quad |x_i| \leq 5.12$$
最优状态与最优解：
$$min \left( f(X^*) \right) =f(0,0,\cdots,0) = 0$$


```python
def func_6():
    name = u"Generalized Rosenbrock's Function"
    x = np.arange(-5.12, 5.12, 0.01)
    y = np.arange(-5.12, 5.12, 0.01)
    x, y = np.meshgrid(x, y)   # 转化为网格矩阵
    f = lambda x : x**2-10*np.cos(2 * np.pi * x) + 10
    z = f(x) + f(y)
    return name, x, y, z
```

![FSU4IJ.png](https://s1.ax1x.com/2018/11/18/FSU4IJ.png)

### 2.7 Ackley Function

$$f(X)=-20 \mathop{exp}\left( -\frac{1}{5}\sqrt{\frac{1}{n}\sum_{i=1}^{n} x_i^2} \right) - \mathop{exp}\left( \frac{1}{n}\sum_{i=1}^{n} cos(2\pi x_i) \right) + 20 + exp(1) ,\quad |x_i| \leq  32.768$$
最优状态与最优解：
$$min \left( f(X^*) \right) =f(0,0,\cdots,0) = 0$$


```python
def func_7():
    name = u"Ackley Function"
    x = np.arange(-40, 40, 0.1)
    y = np.arange(-40, 40, 0.1)
    x, y = np.meshgrid(x, y)   # 转化为网格矩阵
    z = -20 * np.exp(-0.2 * (0.5*(x**2 + y**2))**0.5) - np.exp(0.5 * (np.cos(2*np.pi*x) + np.cos(2*np.pi*y))) + 20 + np.exp(1)
    return name, x, y, z
```

![FSwsGd.png](https://s1.ax1x.com/2018/11/18/FSwsGd.png)

# 3. 示例


```python
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使 plt 中的中文字体能够显现
plt.rcParams['axes.unicode_minus'] = False   # 使 plt 中的中文字体能够显现
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.titleweight'] = 'bold'
```


```python
name, x, y, z = func_7()
```


```python
fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(x, y, z, rcount=50, ccount=50, cmap='jet')
ax.set_title(name, pad=10)
ax.set_xlabel('X轴'), ax.set_ylabel('Y轴'), ax.set_zlabel('Z轴')
plt.show()
```

