#!/usr/bin/env python3
"""OG Xbox Cover Downloader - Desktop App."""

from __future__ import annotations

import platform
import sys
from pathlib import Path

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Qt, Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from xbox_cover_downloader import CoverEntry, download_cover, find_matches, get_entries


def get_cache_dir() -> Path:
    """Return the appropriate cache directory for the platform."""
    if platform.system() == "Darwin":  # macOS
        cache_dir = Path.home() / "Library" / "Caches" / "OG Xbox Cover Downloader"
    elif platform.system() == "Windows":
        appdata = Path.home() / "AppData" / "Local"
        cache_dir = appdata / "OG Xbox Cover Downloader" / "Cache"
    else:  # Linux and others
        cache_dir = Path.home() / ".cache" / "og-xbox-cover-downloader"
    
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


class WorkerSignals(QObject):
    finished = Signal(object)
    error = Signal(str)


class SearchWorker(QRunnable):
    def __init__(
        self,
        query: str,
        max_results: int,
        cache_file: Path,
    ):
        super().__init__()
        self.query = query
        self.max_results = max_results
        self.cache_file = cache_file
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        try:
            entries = get_entries(self.cache_file, refresh=False)
            matches = find_matches(
                entries=entries,
                query=self.query,
                max_results=self.max_results,
                exact=False,
                preferred_regions=["USA", "World", "Europe", "Japan"],
            )
            self.signals.finished.emit(("search", matches))
        except Exception as exc:
            self.signals.error.emit(str(exc))


class DownloadWorker(QRunnable):
    def __init__(self, entry: CoverEntry, output_dir: Path):
        super().__init__()
        self.entry = entry
        self.output_dir = output_dir
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        try:
            path = download_cover(self.entry, self.output_dir)
            self.signals.finished.emit(("download", path))
        except Exception as exc:
            self.signals.error.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OG Xbox Cover Downloader")
        self.setGeometry(100, 100, 900, 700)

        self.thread_pool = QThreadPool.globalInstance()
        cache_dir = get_cache_dir()
        self.cache_file = cache_dir / "xbox_cover_index.json"
        self.download_dir = Path.home() / "Downloads"
        self.matches: list[tuple[CoverEntry, float]] = []

        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget()
        main_layout = QVBoxLayout(central)

        # Title
        title = QLabel("OG Xbox Cover Downloader")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)

        # Search Row
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter game title...")
        self.search_input.returnPressed.connect(self.on_search)
        search_layout.addWidget(self.search_input)
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.on_search)
        search_layout.addWidget(self.search_btn)
        main_layout.addLayout(search_layout)

        # Results
        results_label = QLabel("Results:")
        main_layout.addWidget(results_label)
        self.results_list = QListWidget()
        main_layout.addWidget(self.results_list)

        # Download Row
        download_layout = QHBoxLayout()
        self.download_btn = QPushButton("Download Selected")
        self.download_btn.clicked.connect(self.on_download)
        self.download_btn.setEnabled(False)
        download_layout.addWidget(self.download_btn)

        # Folder selection
        download_layout.addSpacing(20)
        download_layout.addWidget(QLabel("Save to:"))
        self.folder_display = QLineEdit()
        self.folder_display.setText(str(self.download_dir))
        self.folder_display.setReadOnly(True)
        download_layout.addWidget(self.folder_display)
        self.folder_btn = QPushButton("Browse")
        self.folder_btn.clicked.connect(self.on_folder_browse)
        download_layout.addWidget(self.folder_btn)

        main_layout.addLayout(download_layout)

        # Status/Log
        status_label = QLabel("Status:")
        main_layout.addWidget(status_label)
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setMaximumHeight(150)
        main_layout.addWidget(self.log_widget)

        self.setCentralWidget(central)

    def log(self, message: str) -> None:
        self.log_widget.append(message)

    def on_folder_browse(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Choose Download Folder",
            str(self.download_dir),
        )
        if folder:
            self.download_dir = Path(folder)
            self.folder_display.setText(str(self.download_dir))
            self.log(f"Download folder set to: {self.download_dir}")

    def on_search(self) -> None:
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Empty Search", "Please enter a game title.")
            return

        self.search_btn.setEnabled(False)
        self.search_input.setEnabled(False)
        self.log(f"Searching for: {query}")

        worker = SearchWorker(query, 10, self.cache_file)
        worker.signals.finished.connect(self.on_search_complete)
        worker.signals.error.connect(self.on_error)
        self.thread_pool.start(worker)

    def on_search_complete(self, result: tuple) -> None:
        task_type, matches = result
        if task_type != "search":
            return

        self.search_btn.setEnabled(True)
        self.search_input.setEnabled(True)

        self.results_list.clear()
        self.matches = matches

        if not matches:
            self.log("No matches found.")
            self.download_btn.setEnabled(False)
            return

        self.log(f"Found {len(matches)} match(es).")
        for idx, (entry, score) in enumerate(matches, 1):
            text = f"{idx}. {entry.title} (score: {score:.2f})"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, entry)
            self.results_list.addItem(item)

        self.download_btn.setEnabled(True)

    def on_download(self) -> None:
        current = self.results_list.currentItem()
        if not current:
            QMessageBox.warning(self, "No Selection", "Select a result to download.")
            return

        entry = current.data(Qt.UserRole)
        if not isinstance(entry, CoverEntry):
            return

        self.download_btn.setEnabled(False)
        self.search_btn.setEnabled(False)
        self.log(f"Downloading: {entry.title}")

        worker = DownloadWorker(entry, self.download_dir)
        worker.signals.finished.connect(self.on_download_complete)
        worker.signals.error.connect(self.on_error)
        self.thread_pool.start(worker)

    def on_download_complete(self, result: tuple) -> None:
        task_type, path = result
        if task_type != "download":
            return

        self.download_btn.setEnabled(True)
        self.search_btn.setEnabled(True)
        self.log(f"Downloaded to: {path}")
        QMessageBox.information(self, "Success", f"Saved to:\n{path}")

    def on_error(self, error_msg: str) -> None:
        self.download_btn.setEnabled(True)
        self.search_btn.setEnabled(True)
        self.search_input.setEnabled(True)
        self.log(f"Error: {error_msg}")
        QMessageBox.critical(self, "Error", error_msg)


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
