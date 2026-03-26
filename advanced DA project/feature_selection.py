import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')


class FeatureSelector:
    """特征选择器 - 自动选择最佳特征组合"""
    
    @staticmethod
    def get_available_features():
        """获取可用的特征"""
        return {
            'Close': '收盘价',
            'Open': '开盘价',
            'High': '最高价',
            'Low': '最低价',
            'Volume': '交易量',
            '10-day MA': '10日移动平均',
            '20-day MA': '20日移动平均'
        }
    
    @staticmethod
    def create_feature_matrix(df, feature_names, lookback=30):
        """
        创建多特征矩阵
        
        Args:
            df: 数据框
            feature_names: 特征名称列表
            lookback: 回看窗口
        
        Returns:
            X, y
        """
        X, y = [], []
        data = df[feature_names].values
        close_data = df['Close'].values
        
        for i in range(len(data) - lookback):
            # 拼接所有特征的lookback天数据
            features = data[i:i + lookback].flatten()
            X.append(features)
            y.append(close_data[i + lookback])
        
        return np.array(X), np.array(y)
    
    @staticmethod
    def evaluate_feature_combination(df, feature_names, train_ratio=0.8, lookback=30):
        """
        评估特定特征组合的性能
        
        Args:
            df: 数据框
            feature_names: 特征名称列表
            train_ratio: 训练集比例
            lookback: 回看窗口
        
        Returns:
            rmse值
        """
        try:
            X, y = FeatureSelector.create_feature_matrix(df, feature_names, lookback)
            
            if len(X) == 0:
                return float('inf')
            
            # 分割数据
            split_idx = int(len(X) * train_ratio)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            # 使用简单的线性回归快速评估
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            return rmse
        except Exception as e:
            return float('inf')
    
    @staticmethod
    def find_best_features(df, lookback=30, n_features=None):
        """
        找到最佳特征组合
        
        Args:
            df: 数据框
            lookback: 回看窗口
            n_features: 要选择的最佳特征数量（None表示尝试所有组合）
        
        Returns:
            最佳特征名称列表, 最佳RMSE值, 所有结果字典
        """
        available_features = FeatureSelector.get_available_features()
        all_features = [f for f in available_features.keys() if f in df.columns]
        
        # 移除缺失的特征
        all_features = [f for f in all_features if df[f].notna().sum() > 0]
        
        results = {}
        
        # 只尝试使用Close的组合（因为这是目标变量）
        # 以及Close + 其他特征的组合
        feature_combinations = []
        
        # 单特征
        feature_combinations.append(['Close'])
        
        # 双特征
        for i, f in enumerate(all_features):
            if f != 'Close':
                feature_combinations.append(['Close', f])
        
        # 三特征
        for i, f1 in enumerate(all_features):
            if f1 != 'Close':
                for f2 in all_features[i+1:]:
                    if f2 != 'Close':
                        feature_combinations.append(['Close', f1, f2])
        
        print("  正在评估特征组合...")
        best_rmse = float('inf')
        best_features = ['Close']
        
        for combo in feature_combinations:
            # 检查所有特征是否存在
            if all(f in df.columns for f in combo):
                rmse = FeatureSelector.evaluate_feature_combination(df, combo, lookback=lookback)
                feature_str = '+'.join(combo)
                results[feature_str] = rmse
                
                if rmse < best_rmse:
                    best_rmse = rmse
                    best_features = combo
        
        # 显示前5个最佳组合
        if results:
            sorted_results = sorted(results.items(), key=lambda x: x[1])
            print(f"    最佳特征组合: {'+'.join(best_features)} (RMSE: {best_rmse:.6f})")
            print(f"    前3个特征组合:")
            for i, (combo, rmse) in enumerate(sorted_results[:3]):
                print(f"      {i+1}. {combo}: {rmse:.6f}")
        
        return best_features, best_rmse, results


if __name__ == "__main__":
    print("特征选择模块已准备就绪")
