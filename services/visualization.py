import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np
import pandas as pd

class VisualizationService:
    @staticmethod
    def create_plot(plot_type: str, data: pd.DataFrame, x: str, y: str) -> str:
        plt.figure(figsize=(10, 6))
        
        if plot_type == "scatter":
            plt.scatter(data[x], data[y], alpha=0.5)
            
            # Add regression line if requested
            if len(data) > 1:
                z = np.polyfit(data[x], data[y], 1)
                p = np.poly1d(z)
                plt.plot(data[x], p(data[x]), "r--", linewidth=1)
        
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f"{y} vs {x}")
        
        # Save to base64
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        plt.close()
        
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"