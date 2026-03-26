import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')


class DataProcessor:
    """
    处理股票数据的预处理和加载类
    """
    
    def __init__(self, data_folder='.'):
        self.data_folder = data_folder
        self.csv_files = self._find_csv_files()
        self.data = {}
        
    def _find_csv_files(self):
        """找到所有CSV文件"""
        csv_files = [f for f in os.listdir(self.data_folder) 
                     if f.endswith('.csv')]
        print(f"找到 {len(csv_files)} 个CSV文件")
        return csv_files
    
    def load_all_data(self):
        """加载所有CSV文件"""
        for csv_file in self.csv_files:
            file_path = os.path.join(self.data_folder, csv_file)
            try:
                df = pd.read_csv(file_path)
                # 提取股票代码
                stock_name = csv_file.split('_')[0]
                self.data[stock_name] = df
                print(f"✓ 已加载: {stock_name} ({len(df)} 条数据)")
            except Exception as e:
                print(f"✗ 加载失败 {csv_file}: {e}")
        
        return self.data
    
    def preprocess_stock_data(self, df, stock_name):
        """
        预处理单只股票的数据
        
        Args:
            df: 原始数据框
            stock_name: 股票名称（用于日志输出）
        
        Returns:
            处理后的数据框
        """
        df = df.copy()
        
        # 转换日期格式
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
        
        # 删除不需要的列（next price不使用）
        if 'Next Price' in df.columns:
            df = df.drop('Next Price', axis=1)
        if 'index' in df.columns:
            df = df.drop('index', axis=1)
        if '20-SMA Change' in df.columns:
            df = df.drop('20-SMA Change', axis=1)
        
        # 处理缺失值
        df['10-day MA'] = df['10-day MA'].fillna(df['Close'])
        df['20-day MA'] = df['20-day MA'].fillna(df['Close'])
        
        # 移除可能的缺失值行
        df = df.dropna()
        
        print(f"  {stock_name} 预处理后: {len(df)} 条数据")
        
        return df
    
    def create_sequences(self, data, seq_length=30):
        """
        为LSTM创建序列数据
        
        Args:
            data: 输入数据 (1D 数组)
            seq_length: 序列长度
        
        Returns:
            X, y 序列对
        """
        X, y = [], []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)
    
    def split_data(self, df, train_ratio=0.8):
        """
        分割训练集和测试集
        
        Args:
            df: 数据框或数组
            train_ratio: 训练集比例
        
        Returns:
            train_df, test_df
        """
        split_idx = int(len(df) * train_ratio)
        
        # 处理 numpy 数组和 DataFrame
        if isinstance(df, np.ndarray):
            train_df = df[:split_idx]
            test_df = df[split_idx:]
        else:
            train_df = df.iloc[:split_idx]
            test_df = df.iloc[split_idx:]
        
        return train_df, test_df
    
    @staticmethod
    def normalize_data(train_data, test_data):
        """
        归一化数据 (用于LSTM)
        
        Args:
            train_data: 训练数据
            test_data: 测试数据
        
        Returns:
            scaler, train_data_norm, test_data_norm
        """
        scaler = MinMaxScaler(feature_range=(0, 1))
        train_data_norm = scaler.fit_transform(train_data.reshape(-1, 1))
        test_data_norm = scaler.transform(test_data.reshape(-1, 1))
        
        return scaler, train_data_norm, test_data_norm


def main():
    """测试数据加载和预处理"""
    processor = DataProcessor('.')
    
    # 加载所有数据
    raw_data = processor.load_all_data()
    
    # 预处理每个股票的数据
    processed_data = {}
    for stock_name, df in raw_data.items():
        processed_data[stock_name] = processor.preprocess_stock_data(df, stock_name)
    
    print("\n数据预处理完成！")
    
    # 显示示例数据
    first_stock = list(processed_data.keys())[0]
    print(f"\n{first_stock} 的前5行数据:")
    print(processed_data[first_stock].head())
    
    return processed_data


if __name__ == "__main__":
    main()
