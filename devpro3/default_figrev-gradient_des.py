import numpy as np
from matplotlib import pyplot as plt

# 損失関数
def f(x, y):
    return x**2 + 5*y**2 + 6*x*y

# 勾配関数
def df(x, y):
    dzdx = 2*x + 6*y  # f(x, y) の x に関する偏導関数
    dzdy = 10*y + 6*x  # f(x, y) の y に関する偏導関数
    return np.array([dzdx, dzdy])

# パラメータ
s = 0.1                     # ステップサイズ
max_ite = 1000              # 最大反復回数
x0 = 10                     # 初期値(x)
y0 = 10                     # 初期値(y)
x_tr = [x0]                 # xの軌跡(初期値設定)
y_tr = [y0]                 # yの軌跡(初期値設定)

# 勾配降下法による反復計算
for k in range(max_ite):
    x0, y0 = np.array([x0, y0]) - s * df(x0, y0)  # 勾配を降下
    x_tr.append(x0)  # x0の軌跡を追加
    y_tr.append(y0)  # y0の軌跡を追加
    if np.linalg.norm(df(x0, y0)) < 1e-6:  # 勾配が小さくなったら停止
        break
    print(k, x0, y0)

# ここからグラフ描画----------------------------------------------------------------
# 軌跡をnumpy配列に変換
x_tr = np.array(x_tr)
y_tr = np.array(y_tr)

x = np.linspace(-15, 15, 101)
y = np.linspace(-15, 15, 101)
X_mesh, Y_mesh = np.meshgrid(x, y)
z = f(X_mesh, Y_mesh)

fig, ax = plt.subplots(figsize=(7, 7))
ax.contour(X_mesh, Y_mesh, z, levels=50)  # 等高線のレベル数を指定
ax.plot(x_tr, y_tr, marker="o", color='red')  # 軌跡を赤色で描画
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect('equal')
plt.show()
