"""
ChemFlow Analytics Desktop Views Package
"""

from .dashboard_view import DashboardView
from .upload_view import UploadView
from .data_view import DataView
from .history_view import HistoryView
from .report_view import ReportView

__all__ = [
    'DashboardView',
    'UploadView',
    'DataView',
    'HistoryView',
    'ReportView',
]