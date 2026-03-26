import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

"""
LSTM预测偏低原因分析
"""

# 分析可能的原因
print("="*60)
print("LSTM预测偏低原因分析")
print("="*60)

print("\n可能的原因：")
print("\n1. 【最可能】序列创建问题")
print("   - LSTM在train_data上创建序列: X_train = (N-30, 1, 30)")
print("   - 然后在test_data上创建X_test = (M-30, 1, 30)")
print("   - 如果test_data中前30个点是过往数据，预测就会从低值开始")
print("   - 这会导致整个预测序列系统性偏低")

print("\n2. 【次要原因】数据缩放问题")
print("   - 线性回归和决策树使用原始价格")
print("   - LSTM也使用原始价格（无归一化）")
print("   - 神经网络在大范围数值上容易出现梯度消失/爆炸")

print("\n3. 【可能】模型欠拟合")
print("   - 50个LSTM单元可能不够")
print("   - 训练轮数(50)可能太少")
print("   - Dropout正则化可能太强")

print("\n4. 【少见】多特征处理问题")
print("   - 如果用多特征，序列拆平可能有问题")
print("   - 特征之间的相关性可能没有很好捕捉")

print("\n\n建议的解决方案：")
print("\n✓ 方案1: 数据归一化")
print("  使用MinMaxScaler(0,1)对输入和输出进行归一化")
print("  这样LSTM可以更好地学习")

print("\n✓ 方案2: 改进序列创建")
print("  确保train和test数据分割正确")
print("  避免leakage")

print("\n✓ 方案3: 减少正则化")
print("  降低Dropout比例 (0.2 -> 0.1)")
print("  或增加LSTM单元 (50 -> 100)")

print("\n✓ 方案4: 增加训练轮数")
print("  epochs: 50 -> 100 或 200")

print("\n✓ 方案5: 尝试更简单的LSTM架构")
print("  单层LSTM而不是双层")

print("\n" + "="*60)
