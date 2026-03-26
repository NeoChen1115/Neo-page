# 股票价格预测系统

香港股票价格预测系统，实现了三种机器学习/深度学习模型（线性回归、决策树、LSTM）的对比预测。

---

## 📦 安装

### 前置条件
- Python 3.8+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

---

## 🚀 快速开始

### 运行完整预测

```bash
python main.py
```

**执行流程**：
1. 加载 5 支香港股票数据（2318.HK, 3690.HK, 0288.HK, 0002.HK, 0005.HK）
2. 数据预处理与特征选择
3. 训练三种模型：线性回归、决策树、LSTM
4. 生成预测结果、性能对比和可视化

**运行时间**：约 4-8 分钟（取决于硬件）

---

## 📁 项目结构

```
.
├── main.py                      # 主程序（运行这个！）
├── data_preprocessing.py         # 数据处理
├── model_training.py             # 模型定义
├── feature_selection.py          # 特征选择
├── requirements.txt              # 依赖列表
├── *.HK.csv                      # 股票数据（5个文件）
└── results/                      # 输出目录
    ├── model_comparison.csv      # 模型性能排名
    ├── *_predictions.csv         # 各股票预测结果
    └── visualizations/           # 预测图表
```

---

## 📊 输出文件

### model_comparison.csv
- 所有 15 个模型配置的性能排名
- 按 RMSE 从好到差排序
- 包含 MSE、RMSE、MAE、MAPE 指标

### 预测结果（如 0288.HK_predictions.csv）
| 列 | 说明 |
|----|------|
| Date | 日期 |
| Actual | 实际股价 |
| LR_Pred / DT_Pred / LSTM_Pred | 各模型预测值 |
| 对应_Error | 各模型预测误差 |

### 可视化
- 每支股票对比图（4 个子图显示各模型预测）
- 模型性能对比条形图

---

## 🎯 模型概览

| 模型 | 优点 | 缺点 | 速度 |
|------|------|------|------|
| **线性回归** | 最稳定、最可靠 | 假设线性关系 | ⚡⚡⚡ |
| **决策树** | 可处理非线性 | 某些股票失效 | ⚡⚡ |
| **LSTM** | 学习复杂模式 | 运行慢、需归一化 | ⚡ |

**推荐**：默认使用线性回归，需要更高精度时试用 LSTM

---

## ⚙️ 配置修改

### 只预测某支股票
编辑 `main.py`：
```python
STOCKS = ['2318.HK']  # 只保留一个
```

### 调整 LSTM 参数
编辑 `model_training.py`：
```python
epoch = 200        # 改为 200 epochs
```

### 改变训练/测试比例
编辑 `data_preprocessing.py`：
```python
test_ratio = 0.3   # 改为 30% 测试集
```

---

## 🐛 常见问题

**Q: 缺少模块**
```bash
pip install -r requirements.txt
```

**Q: 找不到数据文件**
确保 5 个 CSV 文件在项目目录中

**Q: LSTM 训练太慢**
- 降低 epochs（改为 50）
- 或使用 GPU（需要 CUDA）

---

## 📚 详细文档

- [决策树改进说明](DT_Improvement_Summary.md)
- [LSTM 分析报告](LSTM_Analysis_Report.md)
- [决策树问题分析](Decision_Tree_Analysis.md)

---

**状态**：✅ 完成  
**推荐环境**：Python 3.10+，Linux/Mac/Windows

