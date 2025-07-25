import io
import base64
import matplotlib.pyplot as plt
import numpy as np
from typing import Sequence

def scatter_with_regression(
    x: Sequence[float],
    y: Sequence[float],
    xlabel: str,
    ylabel: str
) -> str:
    """
    Plot x vs y scatter, draw red dotted regression line,
    label axes, and return a base64 PNG (<100 KB).
    """
    # Compute regression
    slope, intercept = np.polyfit(x, y, 1)

    # Create figure
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    # Regression line
    x_arr = np.array(x)
    ax.plot(
        x_arr,
        slope * x_arr + intercept,
        linestyle='--',
        color='red'
    )
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Encode to base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=80, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{img_b64}"
