import matplotlib.pyplot as plt
import os
import pandas as pd


def plot_results(plot_path, MODEL_NAME, results, observed_species):
    """
    Plot simulation results for N experiments.

    Args:
        plot_path: Directory to save the plot.
        MODEL_NAME: Model name for title/filename.
        results: List of dicts from Experiment.run_all: each has "result", "data", "label".
    """
    
  
    plt.figure(figsize=(10, 8))
    start_range = 1
    end_range = 10
    
    res = results[0]['result']
    for i in range(start_range, end_range):
        var = observed_species[i]
        plt.plot(res['time'], res[var], color=f'C{(i-1) % 10}')
        
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pred_data_path = os.path.join(current_dir, '..', '..', '..', 'data', 'PK_Predictions.csv')
    df_pred = pd.read_csv(pred_data_path)
    for i in range(start_range, end_range):
        var = observed_species[i]
        plt.plot(df_pred['Time'], df_pred[var], label=var,   linestyle='--', linewidth=4, color=f'C{(i-1) % 10}')

    plt.xlabel('Time (hours)')
    plt.ylabel('Concentration (nM)')
    # plt.title(MODEL_NAME)
    plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5))
    plt.subplots_adjust(right=0.7)
    plt.ylim(1e-1, 1e4)
    plt.yscale('log')
    plot_name = os.path.join(plot_path, MODEL_NAME + ".png")
    plt.savefig(plot_name, bbox_inches="tight", dpi=300)
    print(f"Plot saved to: {plot_name}")
    plt.show()
