import AnalysisWindow 
import tkinter as tk
from dataclasses import dataclass, field

@dataclass
class PlotParams:
    peak1_lower_bound : int = 0
    peak1_upper_bound : int = 0
    peak2_lower_bound : int = 0
    peak2_upper_bound : int = 0

    plot_lower_bound : int = None
    plot_upper_bound : int = None

    threshold : int = None
    scale : str = "linear"

    lines = []

    def has_changed(self,other):
        if self.peak1_lower_bound != other.peak1_lower_bound:
            return True
        if self.peak1_upper_bound != other.peak1_upper_bound:
            return True
        if self.peak2_lower_bound != other.peak2_lower_bound:
            return True
        if self.peak2_upper_bound != other.peak2_upper_bound:
            return True
        if self.plot_lower_bound != other.plot_lower_bound:
            return True
        if self.plot_upper_bound != other.plot_upper_bound:
            return True
        if self.threshold != other.threshold:
            return True
        if self.scale != other.scale:
            return True
        return False

if __name__ == '__main__':
    