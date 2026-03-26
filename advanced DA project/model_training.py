import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import warnings
warnings.filterwarnings('ignore')

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    LSTM_AVAILABLE = True
except:
    LSTM_AVAILABLE = False
    print("警告: TensorFlow 未安装，LSTM模型不可用")


class LinearRegressionModel:
    """线性回归模型"""
    
    def __init__(self, lookback=30):
        self.model = LinearRegression()
        self.lookback = lookback
        
    def create_features(self, data):
        """
        创建特征（使用过去lookback天的数据）
        
        Args:
            data: 股票close价格数组
        
        Returns:
            X, y
        """
        X, y = [], []
        for i in range(len(data) - self.lookback):
            X.append(data[i:i + self.lookback])
            y.append(data[i + self.lookback])
        return np.array(X), np.array(y)
    
    def train(self, train_data):
        """训练模型"""
        X, y = self.create_features(train_data)
        self.model.fit(X, y)
        return self
    
    def predict(self, test_data):
        """预测"""
        X, y = self.create_features(test_data)
        predictions = self.model.predict(X)
        # 返回完整的y值用于评估（包括过度的预测值）
        return y, predictions


class DecisionTreeModel:
    """决策树模型（改进的超参数）"""
    
    def __init__(self, lookback=30, max_depth=6, min_samples_split=15, min_samples_leaf=5):
        self.model = DecisionTreeRegressor(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42
        )
        self.lookback = lookback
        
    def create_features(self, data):
        """
        创建特征（使用过去lookback天的数据）
        
        Args:
            data: 股票close价格数组
        
        Returns:
            X, y
        """
        X, y = [], []
        for i in range(len(data) - self.lookback):
            X.append(data[i:i + self.lookback])
            y.append(data[i + self.lookback])
        return np.array(X), np.array(y)
    
    def train(self, train_data):
        """训练模型"""
        X, y = self.create_features(train_data)
        self.model.fit(X, y)
        return self
    
    def predict(self, test_data):
        """预测"""
        X, y = self.create_features(test_data)
        predictions = self.model.predict(X)
        return y, predictions


class LSTMModel:
    """LSTM模型（带数据归一化）"""
    
    def __init__(self, lookback=30, epochs=100, batch_size=32):
        self.lookback = lookback
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaler_fitted = False
        
    def create_sequences(self, data, normalize=False):
        """
        创建LSTM的序列数据
        
        Args:
            data: 股票close价格数组
            normalize: 是否进行归一化
        
        Returns:
            X, y (或 X_norm, y_norm)
        """
        if normalize and not self.scaler_fitted:
            # 第一次调用时，对data进行fit_transform
            data_reshaped = data.reshape(-1, 1)
            data_normalized = self.scaler.fit_transform(data_reshaped)
            self.scaler_fitted = True
            data = data_normalized.flatten()
        elif normalize and self.scaler_fitted:
            # 后续调用时，只做transform
            data_reshaped = data.reshape(-1, 1)
            data = self.scaler.transform(data_reshaped).flatten()
        
        X, y = [], []
        for i in range(len(data) - self.lookback):
            X.append(data[i:i + self.lookback])
            y.append(data[i + self.lookback])
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape):
        """构建LSTM模型（改进的架构）"""
        if not LSTM_AVAILABLE:
            raise RuntimeError("LSTM模型不可用，请安装TensorFlow: pip install tensorflow")
        
        self.model = Sequential([
            LSTM(100, activation='relu', input_shape=input_shape, return_sequences=True),
            Dropout(0.1),
            LSTM(50, activation='relu'),
            Dropout(0.1),
            Dense(25, activation='relu'),
            Dense(1)
        ])
        
        self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return self
    
    def train(self, train_data, validation_data=None, verbose=0):
        """
        训练LSTM模型（使用归一化数据）
        
        Args:
            train_data: 训练数据
            validation_data: 验证数据
            verbose: 是否显示训练进度
        """
        # 创建归一化的序列
        X_train, y_train = self.create_sequences(train_data, normalize=True)
        
        if len(X_train) == 0:
            raise ValueError("训练数据不足，无法创建序列")
        
        # 第一次调用时构建模型
        if self.model is None:
            self.build_model((X_train.shape[1], 1))
        
        history = self.model.fit(
            X_train, y_train,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_data=validation_data,
            verbose=verbose
        )
        
        return self
    
    def predict(self, test_data):
        """预测（使用相同的scaler）"""
        if self.model is None:
            raise RuntimeError("模型尚未训练")
        
        # 使用相同的scaler对测试数据进行归一化
        X_test, y_test = self.create_sequences(test_data, normalize=True)
        
        if len(X_test) == 0:
            raise ValueError("测试数据不足，无法创建序列")
        
        # 获取预测（还是归一化的）
        y_pred_normalized = self.model.predict(X_test, verbose=0)
        
        # 反归一化以获得原始价格
        y_test_original = self.scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
        y_pred_original = self.scaler.inverse_transform(y_pred_normalized).flatten()
        
        return y_test_original, y_pred_original


class ModelEvaluator:
    """模型评估类"""
    
    @staticmethod
    def calculate_metrics(y_true, y_pred):
        """
        计算评估指标
        
        Args:
            y_true: 实际值
            y_pred: 预测值
        
        Returns:
            metrics字典
        """
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        
        # 避免MAPE中的除零
        mape = mean_absolute_percentage_error(y_true, y_pred) if np.all(y_true != 0) else np.inf
        
        return {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'MAPE': mape
        }
    
    @staticmethod
    def print_metrics(metrics, model_name=""):
        """打印评估指标"""
        print(f"\n{model_name} 模型评估结果:")
        print(f"  MSE:  {metrics['MSE']:.6f}")
        print(f"  RMSE: {metrics['RMSE']:.6f}")
        print(f"  MAE:  {metrics['MAE']:.6f}")
        print(f"  MAPE: {metrics['MAPE']:.4f}" if metrics['MAPE'] != np.inf else "  MAPE: N/A")


def train_all_models(train_data, test_data, train_data_dt=None, test_data_dt=None):
    """
    训练所有三个模型
    
    Args:
        train_data: 训练集 (close价格或多特征)
        test_data: 测试集 (close价格或多特征)
        train_data_dt: 决策树专用训练数据（如果为None则用train_data）
        test_data_dt: 决策树专用测试数据（如果为None则用test_data）
    
    Returns:
        results字典: 包含每个模型的训练结果和评估指标
    """
    # 如果没有提供决策树专用数据，则使用通用数据
    if train_data_dt is None:
        train_data_dt = train_data
    if test_data_dt is None:
        test_data_dt = test_data
    
    results = {}
    evaluator = ModelEvaluator()
    
    # 1. 线性回归
    print("\n" + "="*50)
    print("1. 训练线性回归模型...")
    print("="*50)
    try:
        lr_model = LinearRegressionModel(lookback=30)
        lr_model.train(train_data)
        y_true, y_pred = lr_model.predict(test_data)
        metrics = evaluator.calculate_metrics(y_true, y_pred)
        evaluator.print_metrics(metrics, "线性回归")
        results['Linear Regression'] = {
            'model': lr_model,
            'y_true': y_true,
            'y_pred': y_pred,
            'metrics': metrics
        }
    except Exception as e:
        print(f"线性回归模型训练失败: {e}")
    
    # 2. 决策树（使用专用数据，通常是Close价格）
    print("\n" + "="*50)
    print("2. 训练决策树模型...")
    print("="*50)
    try:
        dt_model = DecisionTreeModel(lookback=30, max_depth=6, min_samples_split=15, min_samples_leaf=5)
        dt_model.train(train_data_dt)
        y_true, y_pred = dt_model.predict(test_data_dt)
        metrics = evaluator.calculate_metrics(y_true, y_pred)
        evaluator.print_metrics(metrics, "决策树")
        results['Decision Tree'] = {
            'model': dt_model,
            'y_true': y_true,
            'y_pred': y_pred,
            'metrics': metrics
        }
    except Exception as e:
        print(f"决策树模型训练失败: {e}")
    
    # 3. LSTM
    print("\n" + "="*50)
    print("3. 训练LSTM模型...")
    print("="*50)
    try:
        lstm_model = LSTMModel(lookback=30, epochs=100, batch_size=32)
        lstm_model.train(train_data, verbose=0)
        y_true, y_pred = lstm_model.predict(test_data)
        metrics = evaluator.calculate_metrics(y_true, y_pred)
        evaluator.print_metrics(metrics, "LSTM")
        results['LSTM'] = {
            'model': lstm_model,
            'y_true': y_true,
            'y_pred': y_pred,
            'metrics': metrics
        }
    except Exception as e:
        print(f"LSTM模型训练失败: {e}")
    
    return results


def compare_models(results):
    """
    比较所有模型的性能
    
    Args:
        results: 训练结果字典
    """
    print("\n" + "="*50)
    print("模型比较结果")
    print("="*50)
    
    comparison_df = pd.DataFrame({
        model_name: result['metrics']
        for model_name, result in results.items()
    }).T
    
    print(comparison_df)
    
    # 找到最佳模型（基于RMSE）
    best_model = min(results.items(), key=lambda x: x[1]['metrics']['RMSE'])
    print(f"\n✓ 最佳模型: {best_model[0]} (RMSE: {best_model[1]['metrics']['RMSE']:.6f})")
    
    return best_model


if __name__ == "__main__":
    # 测试模型
    print("模型训练模块已准备就绪")
    print("可用模型: 线性回归, ARIMA, LSTM")
