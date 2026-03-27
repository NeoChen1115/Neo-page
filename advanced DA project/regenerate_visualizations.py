"""
仅重新生成可视化图表，不需要重新训练模型
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 从已保存的CSV文件重新生成图表
def regenerate_visualizations():
    """从results目录中的CSV文件重新生成图表"""
    
    results_folder = 'results'
    vis_folder = os.path.join(results_folder, 'visualizations')
    
    # 读取模型对比结果
    comparison_df = pd.read_csv(os.path.join(results_folder, 'model_comparison.csv'))
    
    # 提取股票和模型
    stocks = []
    for csv_file in os.listdir(results_folder):
        if csv_file.endswith('_predictions.csv'):
            stock_name = csv_file.replace('_predictions.csv', '')
            stocks.append(stock_name)
    
    stocks.sort()
    
    # 为每个股票生成对比图
    for stock_name in stocks:
        print(f"  Regenerating visualization for {stock_name}...")
        
        # 读取预测结果
        predictions_csv = os.path.join(results_folder, f'{stock_name}_predictions.csv')
        if not os.path.exists(predictions_csv):
            continue
        
        pred_df = pd.read_csv(predictions_csv)
        dates = pred_df['Date'].values
        
        # 提取每个模型的预测
        models = [col.replace('_Predictions', '') for col in pred_df.columns if '_Predictions' in col]
        actual = pred_df['Actual'].values
        
        # 生成2x2图表
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle(f'{stock_name} - Model Prediction Comparison', fontsize=16, fontweight='bold')
        axes_flat = axes.flatten()
        
        for idx, model_name in enumerate(models):
            if idx >= 4:
                break
            
            ax = axes_flat[idx]
            predictions = pred_df[f'{model_name}_Predictions'].values
            
            # 计算RMSE
            rmse = np.sqrt(np.mean((actual - predictions) ** 2))
            
            # 绘图
            min_len = min(len(actual), len(predictions), len(dates))
            x_dates = dates[:min_len]
            
            ax.plot(range(min_len), actual[:min_len], label='Actual', marker='o', linewidth=2, markersize=3)
            ax.plot(range(min_len), predictions[:min_len], label='Predicted', marker='s', linewidth=2, markersize=3)
            ax.set_title(f'{model_name}\nRMSE: {rmse:.4f}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # 设置日期标签
            step = max(1, min_len // 10)
            tick_positions = range(0, min_len, step)
            tick_labels = [str(x_dates[i])[:10] for i in tick_positions]
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(tick_labels, rotation=45, ha='right')
        
        # 隐藏多余的subplot
        if len(models) < 4:
            for idx in range(len(models), 4):
                axes_flat[idx].axis('off')
        
        plt.tight_layout()
        
        # 保存
        viz_path = os.path.join(vis_folder, f'{stock_name}_comparison.png')
        plt.savefig(viz_path, dpi=300, bbox_inches='tight')
        print(f"    Saved: {stock_name}_comparison.png")
        plt.close()
    
    # 生成全局对比图
    print("  Regenerating global comparison...")
    
    model_rmses = {}
    for model in comparison_df['Model'].unique():
        model_data = comparison_df[comparison_df['Model'] == model]
        avg_rmse = model_data['RMSE'].mean()
        model_rmses[model] = avg_rmse
    
    fig, ax = plt.subplots(figsize=(10, 6))
    models_list = list(model_rmses.keys())
    rmses_list = list(model_rmses.values())
    
    bars = ax.bar(models_list, rmses_list, color=['#1f77b4', '#ff7f0e', '#2ca02c'][:len(models_list)], alpha=0.7)
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
    print(f"    Saved: model_performance_comparison.png")
    plt.close()
    
    print("\n✅ All visualizations regenerated successfully!")

if __name__ == "__main__":
    print("="*60)
    print("Regenerating Visualizations (fixing Chinese character issues)")
    print("="*60)
    regenerate_visualizations()
