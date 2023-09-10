from flask import Flask, render_template, request
from deap import base, creator, tools, algorithms
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

app = Flask(__name__)

# 在app.py中的全局变量定义后面添加这行，将box_size传递给evalBox函数
toolbox.register("evaluate", evalBox, box_size=box_size)

# 定义评估函数
def evalBox(individual):
    # 计算外箱的形状
    shape = np.array(individual) * box_size
    # 计算每个维度上可以摆放的小盒子数量
    boxes_in_length = shape[0] // box_size[0]
    boxes_in_width = shape[1] // box_size[1]
    boxes_in_height = shape[2] // box_size[2]
    
    total_boxes = boxes_in_length * boxes_in_width * boxes_in_height
    # 打印摆放模式
    ##print(f"Individual: {individual}, Boxes: {boxes_in_length}x{boxes_in_width}x{boxes_in_height}")
    # 检查长宽高是否接近，如果差异过大则增大惩罚
    max_difference = 10  # 允许的最大差异值
    if abs(shape[0] - shape[1]) > max_difference or \
       abs(shape[0] - shape[2]) > max_difference or \
       abs(shape[1] - shape[2]) > max_difference:
        return 1e9, 1e9
    # 如果不是40个盒子，返回一个很大的惩罚值
    if total_boxes != 40:
        return 1e9, 1e9
    
    # 计算外箱的体积
    volume = np.prod(shape)
    # 计算外箱的形状的方差，我们希望这个值尽可能小，以使外箱的形状更方正
    variance = np.var(shape)
    
    return volume, variance


toolbox.register("evaluate", evalBox)
toolbox.register("mate", tools.cxTwoPoint)

# 添加锦标赛选择策略
toolbox.register("select", tools.selTournament, tournsize=3)

# 运行遗传算法
pop = toolbox.population(n=100)
result = algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.1, ngen=200)

# 打印最优解
best_individual = tools.selBest(pop, 1)[0]
print('Best individual: ', best_individual)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None  # 初始化result变量
    if request.method == 'POST':
        # 获取用户输入的小盒尺寸和装箱数量
        box_size = np.array([float(request.form['length']), float(request.form['width']), float(request.form['height'])])
        box_count = int(request.form['box_count'])
        
        # 在这里调用你的遗传算法函数来计算结果
        # result = your_genetic_algorithm(box_size, box_count)

    return render_template('index.html', result=result)  # 传递result给模板

if __name__ == '__main__':
    app.run(debug=True)

