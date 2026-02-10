"""
Icon utilities for the desktop UI.
Uses standard Qt icons to avoid emoji glyphs.
"""

from PyQt5.QtWidgets import QApplication, QStyle
from PyQt5.QtGui import QIcon

ICON_MAP = {
    'app': QStyle.SP_ComputerIcon,
    'dashboard': QStyle.SP_ComputerIcon,
    'upload': QStyle.SP_ArrowUp,
    'data_table': QStyle.SP_FileDialogDetailedView,
    'history': QStyle.SP_BrowserReload,
    'report': QStyle.SP_FileDialogInfoView,
    'user': QStyle.SP_DirHomeIcon,
    'refresh': QStyle.SP_BrowserReload,
    'view': QStyle.SP_FileDialogContentsView,
    'delete': QStyle.SP_TrashIcon,
    'info': QStyle.SP_MessageBoxInformation,
    'success': QStyle.SP_DialogApplyButton,
    'error': QStyle.SP_MessageBoxCritical,
    'chart': QStyle.SP_FileDialogContentsView,
    'flow': QStyle.SP_ArrowRight,
    'pressure': QStyle.SP_ArrowUp,
    'temperature': QStyle.SP_TitleBarShadeButton,
    'count': QStyle.SP_FileDialogListView,
    'download': QStyle.SP_DialogSaveButton,
}


def get_icon(name: str, size: int = 16) -> QIcon:
    style = QApplication.style()
    sp = ICON_MAP.get(name, QStyle.SP_FileIcon)
    icon = style.standardIcon(sp)
    if size:
        return QIcon(icon.pixmap(size, size))
    return icon
