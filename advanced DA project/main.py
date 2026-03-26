import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from data_preprocessing import DataProcessor
from model_training import train_all_models, compare_models, ModelEvaluator
from feature_selection import FeatureSelector


class StockPredictionPipeline:
    """股票预测完整流程"""
    
    def __init__(self, data_folder='.', output_folder='results'):
        self.data_folder = data_folder
        self.output_folder = output_folder
        self.processor = DataProcessor(data_folder)
        self.results = {}
        
        # 创建输出文件夹
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
    def run(self):
        """运行完整的预测流程"""
        print("="*60)
        print("股票价格预测 - 完整流程")
        print("="*60)
        
        # 第一步：加载数据
        print("\n[步骤 1] 加载数据...")
        raw_data = self.processor.load_all_data()
        
        if not raw_data:
            print("✗ 没有找到CSV文件！")
            return
        
        # 显示数据概况
        print("\n数据概况:")
        for stock_name, df in raw_data.items():
            print(f"  {stock_name}: {len(df)} 行 | 日期范围: {df['Date'].min()} ~ {df['Date'].max()}")
        
        # 第二步：预处理数据
        print("\n[步骤 2] 预处理数据...")
        processed_data = {}
        for stock_name, df in raw_data.items():
            processed_data[stock_name] = self.processor.preprocess_stock_data(df, stock_name)
        
        # 第三步：训练模型和评估
        print("\n[步骤 3] 训练模型和评估...")
        all_results = {}
        
        for stock_name, df in processed_data.items():
            print(f"\n--- 处理股票: {stock_name} ---")
            
            # 选择最佳特征组合
            best_features, best_rmse, feature_results = FeatureSelector.find_best_features(df, lookback=30)
            
            # 创建多特征矩阵
            close_prices = df['Close'].values
            dates = df['Date'].values
            
            # 如果最佳特征只有Close，使用原始方法；否则使用多特征
            if best_features == ['Close']:
                X_train_data = None
                X_test_data = None
                train_data, test_data = self.processor.split_data(close_prices, train_ratio=0.8)
            else:
                X, y = FeatureSelector.create_feature_matrix(df, best_features, lookback=30)
                split_idx = int(len(X) * 0.8)
                X_train_data = (X[:split_idx], y[:split_idx])
                X_test_data = (X[split_idx:], y[split_idx:])
                train_data = close_prices[:split_idx + 30]  # 保持兼容性
                test_data = close_prices[split_idx + 30:]
            
            # 分割日期
            train_dates, test_dates = self.processor.split_data(dates, train_ratio=0.8)
            
            # 打印训练信息
            feature_str = '+'.join(best_features)
            print(f"  使用变量: {feature_str}")
            print(f"  特征评估RMSE: {best_rmse:.6f}")
            print(f"  训练集: {len(train_data)} 条数据 | 时间范围: {train_dates[0]} ~ {train_dates[-1]}")
            print(f"  预测集: {len(test_data)} 条数据 | 时间范围: {test_dates[0]} ~ {test_dates[-1]}")
            
            # 为决策树准备Close-only数据（避免多特征问题）
            train_data_dt, test_data_dt = self.processor.split_data(close_prices, train_ratio=0.8)
            
            # 训练模型（LR/LSTM用可能的多特征，DT用Close-only）
            results = train_all_models(train_data, test_data, train_data_dt=train_data_dt, test_data_dt=test_data_dt)
            all_results[stock_name] = {
                'close_prices': close_prices,
                'train_data': train_data,
                'test_data': test_data,
                'results': results,
                'dates': dates,
                'train_dates': train_dates,
                'test_dates': test_dates
            }
            
            # 比较模型
            if results:
                best_model = compare_models(results)
                print(f"✓ {stock_name} 完成")
            else:
                print(f"✗ {stock_name} 没有成功的模型")
        
        self.results = all_results
        
        # 第四步：生成对比表
        print("\n[步骤 4] 生成对比表...")
        self._generate_comparison_report()
        
        # 第五步：保存预测结果
        print("\n[步骤 5] 保存预测结果...")
        self._save_predictions()
        
        # 第六步：生成可视化
        print("\n[步骤 6] 生成可视化...")
        self._generate_visualizations()
        
        print("\n" + "="*60)
        print("✓ 流程完成！")
        print(f"✓ 结果已保存到: {os.path.abspath(self.output_folder)}")
        print("="*60)
    
    def _generate_comparison_report(self):
        """生成模型对比报告"""
        comparison_data = []
        
        for stock_name, stock_results in self.results.items():
            for model_name, model_result in stock_results['results'].items():
                metrics = model_result['metrics']
                comparison_data.append({
                    'Stock': stock_name,
                    'Model': model_name,
                    'MSE': metrics['MSE'],
                    'RMSE': metrics['RMSE'],
                    'MAE': metrics['MAE'],
                    'MAPE': metrics['MAPE']
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_path = os.path.join(self.output_folder, 'model_comparison.csv')
        comparison_df.to_csv(comparison_path, index=False)
        print(f"  模型对比表已保存: model_comparison.csv")
        
        # 打印摘要
        print("\n模型整体性能排名 (按RMSE):")
        print(comparison_df.sort_values('RMSE').to_string(index=False))
    
    def _save_predictions(self):
        """保存所有预测结果"""
        for stock_name, stock_results in self.results.items():
            predictions_list = []
            test_dates = stock_results['test_dates']
            
            for model_name, model_result in stock_results['results'].items():
                y_true = model_result['y_true']
                y_pred = model_result['y_pred']
                
                # 确保长度一致
                min_len = min(len(y_true), len(y_pred))
                
                for i in range(min_len):
                    predictions_list.append({
                        'Date': test_dates[i] if i < len(test_dates) else f"Unknown_{i}",
                        'Stock': stock_name,
                        'Model': model_name,
                        'Index': i,
                        'Actual': y_true[i],
                        'Predicted': y_pred[i],
                        'Error': abs(y_true[i] - y_pred[i])
                    })
            
            if predictions_list:
                predictions_df = pd.DataFrame(predictions_list)
                pred_path = os.path.join(self.output_folder, f'{stock_name}_predictions.csv')
                predictions_df.to_csv(pred_path, index=False)
                print(f"  {stock_name} 预测结果已保存")
    
    def _generate_visualizations(self):
        """生成可视化图表"""
        vis_folder = os.path.join(self.output_folder, 'visualizations')
        if not os.path.exists(vis_folder):
            os.makedirs(vis_folder)
        
        for stock_name, stock_results in self.results.items():
            # 为每个股票生成图表
            fig, axes = plt.subplots(2, 2, figsize=(16, 10))
            fig.suptitle(f'{stock_name} - 模型预测对比', fontsize=16, fontweight='bold')
            
            test_data = stock_results['test_data']
            test_dates = stock_results['test_dates']
            axes_flat = axes.flatten()
            
            for idx, (model_name, model_result) in enumerate(stock_results['results'].items()):
                ax = axes_flat[idx]
                
                y_true = model_result['y_true']
                y_pred = model_result['y_pred']
                
                # 确保长度一致
                min_len = min(len(y_true), len(y_pred), len(test_dates))
                
                # 使用日期作为X轴
                x_dates = test_dates[:min_len]
                
                ax.plot(range(min_len), y_true[:min_len], label='Actual', marker='o', linewidth=2, markersize=3)
                ax.plot(range(min_len), y_pred[:min_len], label='Predicted', marker='s', linewidth=2, markersize=3)
                ax.set_title(f'{model_name}\nRMSE: {model_result["metrics"]["RMSE"]:.4f}')
                ax.set_xlabel('Date')
                ax.set_ylabel('Price')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                # 设置日期标签（每隔一定间隔显示）
                step = max(1, min_len // 10)  # 最多显示10个日期标签
                tick_positions = range(0, min_len, step)
                tick_labels = [str(x_dates[i])[:10] for i in tick_positions]
                ax.set_xticks(tick_positions)
                ax.set_xticklabels(tick_labels, rotation=45, ha='right')
            
            # 如果少于4个模型，隐藏多余的subplot
            if len(stock_results['results']) < 4:
                for idx in range(len(stock_results['results']), 4):
                    axes_flat[idx].axis('off')
            
            plt.tight_layout()
            
            # 保存图表
            viz_path = os.path.join(vis_folder, f'{stock_name}_comparison.png')
            plt.savefig(viz_path, dpi=300, bbox_inches='tight')
            print(f"  {stock_name} 对比图已保存 (使用日期x轴)")
            plt.close()
        
        # 生成全局对比图
        self._generate_global_comparison(vis_folder)
    
    def _generate_global_comparison(self, vis_folder):
        """生成全局模型性能对比图"""
        try:
            # 收集所有RMSE数据
            model_performance = {}
            
            for stock_name, stock_results in self.results.items():
                for model_name, model_result in stock_results['results'].items():
                    if model_name not in model_performance:
                        model_performance[model_name] = []
                    model_performance[model_name].append(model_result['metrics']['RMSE'])
            
            # 计算平均RMSE
            avg_rmse = {model: np.mean(rmses) for model, rmses in model_performance.items()}
            
            # 绘制柱状图
            fig, ax = plt.subplots(figsize=(10, 6))
            models = list(avg_rmse.keys())
            rmses = list(avg_rmse.values())
            
            bars = ax.bar(models, rmses, color=['#1f77b4', '#ff7f0e', '#2ca02c'][:len(models)], alpha=0.7)
            ax.set_ylabel('Average RMSE', fontsize=12)
            ax.set_title('Model Performance Comparison (Average RMSE)', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            
            # 添加数值标签
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.4f}',
                       ha='center', va='bottom')
            
            plt.tight_layout()
            comp_path = os.path.join(vis_folder, 'model_performance_comparison.png')
            plt.savefig(comp_path, dpi=300, bbox_inches='tight')
            print(f"  全局对比图已保存: model_performance_comparison.png")
            plt.close()
            
        except Exception as e:
            print(f"  生成全局对比图失败: {e}")


def main():
    """主函数"""
    # 创建管道
    pipeline = StockPredictionPipeline(data_folder='.', output_folder='results')
    
    # 运行完整流程
    pipeline.run()


if __name__ == "__main__":
    main()
