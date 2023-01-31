# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\nunot\OneDrive\Ambiente de Trabalho\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import time
import multiprocessing
import serial
import numpy as np
from datetime import datetime as dt
import os
import csv
import matplotlib.pyplot as plt
import Arduino
import tkinter as tk
import AcquisitionSetupWindow as acq
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataclasses import dataclass, field

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ToolbarWidget = QtWidgets.QWidget(self.centralwidget)
        self.ToolbarWidget.setGeometry(QtCore.QRect(0, 0, 811, 41))
        self.ToolbarWidget.setObjectName("ToolbarWidget")
        self.start_button = QtWidgets.QPushButton(self.ToolbarWidget)
        self.start_button.setGeometry(QtCore.QRect(0, 0, 81, 41))
        self.start_button.setObjectName("start_button")
        self.stop_button = QtWidgets.QPushButton(self.ToolbarWidget)
        self.stop_button.setGeometry(QtCore.QRect(80, 0, 81, 41))
        self.stop_button.setObjectName("stop_button")
        self.restart_button = QtWidgets.QPushButton(self.ToolbarWidget)
        self.restart_button.setGeometry(QtCore.QRect(160, 0, 81, 41))
        self.restart_button.setObjectName("restart_button")
        self.clear_button = QtWidgets.QPushButton(self.ToolbarWidget)
        self.clear_button.setGeometry(QtCore.QRect(730, 0, 81, 41))
        self.clear_button.setAutoDefault(False)
        self.clear_button.setObjectName("clear_button")
        self.PlotdrawWidget = QtWidgets.QWidget(self.centralwidget)
        self.PlotdrawWidget.setGeometry(QtCore.QRect(0, 40, 811, 641))
        self.PlotdrawWidget.setObjectName("PlotdrawWidget")
        self.Metrics = QtWidgets.QListView(self.centralwidget)
        self.Metrics.setGeometry(QtCore.QRect(820, 0, 341, 681))
        self.Metrics.setMouseTracking(True)
        self.Metrics.setObjectName("Metrics")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(820, 0, 341, 681))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.acquisitionMetrics = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.acquisitionMetrics.setContentsMargins(0, 0, 0, 0)
        self.acquisitionMetrics.setObjectName("acquisitionMetrics")
        self.start_time_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.start_time_label.setFont(font)
        self.start_time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.start_time_label.setWordWrap(False)
        self.start_time_label.setObjectName("start_time_label")
        self.acquisitionMetrics.addWidget(self.start_time_label, 1, 0, 1, 1)
        self.count_rate = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.count_rate.setFont(font)
        self.count_rate.setAlignment(QtCore.Qt.AlignCenter)
        self.count_rate.setWordWrap(False)
        self.count_rate.setObjectName("count_rate")
        self.acquisitionMetrics.addWidget(self.count_rate, 7, 1, 1, 1)
        self.n_acquisitions_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.n_acquisitions_label.setFont(font)
        self.n_acquisitions_label.setAlignment(QtCore.Qt.AlignCenter)
        self.n_acquisitions_label.setWordWrap(False)
        self.n_acquisitions_label.setObjectName("n_acquisitions_label")
        self.acquisitionMetrics.addWidget(self.n_acquisitions_label, 4, 0, 1, 1)
        self.n_channel_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.n_channel_label.setFont(font)
        self.n_channel_label.setAlignment(QtCore.Qt.AlignCenter)
        self.n_channel_label.setWordWrap(False)
        self.n_channel_label.setObjectName("n_channel_label")
        self.acquisitionMetrics.addWidget(self.n_channel_label, 3, 0, 1, 1)
        self.time_elapsed_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.time_elapsed_label.setFont(font)
        self.time_elapsed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_elapsed_label.setWordWrap(False)
        self.time_elapsed_label.setObjectName("time_elapsed_label")
        self.acquisitionMetrics.addWidget(self.time_elapsed_label, 6, 0, 1, 1)
        self.acquisition_status_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.acquisition_status_label.setFont(font)
        self.acquisition_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.acquisition_status_label.setWordWrap(False)
        self.acquisition_status_label.setObjectName("acquisition_status_label")
        self.acquisitionMetrics.addWidget(self.acquisition_status_label, 0, 0, 1, 1)
        self.acquisition_status = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.acquisition_status.setFont(font)
        self.acquisition_status.setAlignment(QtCore.Qt.AlignCenter)
        self.acquisition_status.setWordWrap(False)
        self.acquisition_status.setObjectName("acquisition_status")
        self.acquisitionMetrics.addWidget(self.acquisition_status, 0, 1, 1, 1)
        self.start_time = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.start_time.setFont(font)
        self.start_time.setAlignment(QtCore.Qt.AlignCenter)
        self.start_time.setWordWrap(False)
        self.start_time.setObjectName("start_time")
        self.acquisitionMetrics.addWidget(self.start_time, 1, 1, 1, 1)
        self.current_acquisition = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.current_acquisition.setFont(font)
        self.current_acquisition.setAlignment(QtCore.Qt.AlignCenter)
        self.current_acquisition.setWordWrap(False)
        self.current_acquisition.setObjectName("current_acquisition")
        self.acquisitionMetrics.addWidget(self.current_acquisition, 5, 1, 1, 1)
        self.threshold_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.threshold_label.setFont(font)
        self.threshold_label.setAlignment(QtCore.Qt.AlignCenter)
        self.threshold_label.setWordWrap(False)
        self.threshold_label.setObjectName("threshold_label")
        self.acquisitionMetrics.addWidget(self.threshold_label, 8, 0, 1, 1)
        self.n_acquisitions = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.n_acquisitions.setFont(font)
        self.n_acquisitions.setAlignment(QtCore.Qt.AlignCenter)
        self.n_acquisitions.setWordWrap(False)
        self.n_acquisitions.setObjectName("n_acquisitions")
        self.acquisitionMetrics.addWidget(self.n_acquisitions, 4, 1, 1, 1)
        self.n_channels = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.n_channels.setFont(font)
        self.n_channels.setAlignment(QtCore.Qt.AlignCenter)
        self.n_channels.setWordWrap(False)
        self.n_channels.setObjectName("n_channels")
        self.acquisitionMetrics.addWidget(self.n_channels, 3, 1, 1, 1)
        self.preset_time = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.preset_time.setFont(font)
        self.preset_time.setAlignment(QtCore.Qt.AlignCenter)
        self.preset_time.setWordWrap(False)
        self.preset_time.setObjectName("preset_time")
        self.acquisitionMetrics.addWidget(self.preset_time, 2, 1, 1, 1)
        self.threshold = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.threshold.setFont(font)
        self.threshold.setAlignment(QtCore.Qt.AlignCenter)
        self.threshold.setWordWrap(False)
        self.threshold.setObjectName("threshold")
        self.acquisitionMetrics.addWidget(self.threshold, 8, 1, 1, 1)
        self.count_rate_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.count_rate_label.setFont(font)
        self.count_rate_label.setAlignment(QtCore.Qt.AlignCenter)
        self.count_rate_label.setWordWrap(False)
        self.count_rate_label.setObjectName("count_rate_label")
        self.acquisitionMetrics.addWidget(self.count_rate_label, 7, 0, 1, 1)
        self.current_acquisition_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.current_acquisition_label.setFont(font)
        self.current_acquisition_label.setAlignment(QtCore.Qt.AlignCenter)
        self.current_acquisition_label.setWordWrap(False)
        self.current_acquisition_label.setObjectName("current_acquisition_label")
        self.acquisitionMetrics.addWidget(self.current_acquisition_label, 5, 0, 1, 1)
        self.time_elapsed = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.time_elapsed.setFont(font)
        self.time_elapsed.setAlignment(QtCore.Qt.AlignCenter)
        self.time_elapsed.setWordWrap(False)
        self.time_elapsed.setObjectName("time_elapsed")
        self.acquisitionMetrics.addWidget(self.time_elapsed, 6, 1, 1, 1)
        self.preset_time_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.preset_time_label.setFont(font)
        self.preset_time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.preset_time_label.setWordWrap(False)
        self.preset_time_label.setObjectName("preset_time_label")
        self.acquisitionMetrics.addWidget(self.preset_time_label, 2, 0, 1, 1)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 700, 340, 151))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.gridLayoutWidget_3.setFont(font)
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.CountsGrid = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.CountsGrid.setContentsMargins(0, 0, 0, 0)
        self.CountsGrid.setObjectName("CountsGrid")
        self.lower_peak2 = QtWidgets.QTextEdit(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lower_peak2.sizePolicy().hasHeightForWidth())
        self.lower_peak2.setSizePolicy(sizePolicy)
        self.lower_peak2.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lower_peak2.setFont(font)
        self.lower_peak2.setObjectName("lower_peak2")
        self.CountsGrid.addWidget(self.lower_peak2, 1, 2, 1, 1)
        self.lower_peak1 = QtWidgets.QTextEdit(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lower_peak1.sizePolicy().hasHeightForWidth())
        self.lower_peak1.setSizePolicy(sizePolicy)
        self.lower_peak1.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lower_peak1.setFont(font)
        self.lower_peak1.setObjectName("lower_peak1")
        self.CountsGrid.addWidget(self.lower_peak1, 1, 1, 1, 1)
        self.lower_bound_label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lower_bound_label.setFont(font)
        self.lower_bound_label.setAlignment(QtCore.Qt.AlignCenter)
        self.lower_bound_label.setObjectName("lower_bound_label")
        self.CountsGrid.addWidget(self.lower_bound_label, 2, 0, 1, 1)
        self.upper_bound_label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.upper_bound_label.setFont(font)
        self.upper_bound_label.setAlignment(QtCore.Qt.AlignCenter)
        self.upper_bound_label.setObjectName("upper_bound_label")
        self.CountsGrid.addWidget(self.upper_bound_label, 1, 0, 1, 1)
        self.emptyspace = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.emptyspace.setText("")
        self.emptyspace.setObjectName("emptyspace")
        self.CountsGrid.addWidget(self.emptyspace, 0, 0, 1, 1)
        self.peak1_label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.peak1_label.setFont(font)
        self.peak1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.peak1_label.setObjectName("peak1_label")
        self.CountsGrid.addWidget(self.peak1_label, 0, 1, 1, 1)
        self.counts1 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.counts1.setFont(font)
        self.counts1.setObjectName("counts1")
        self.CountsGrid.addWidget(self.counts1, 3, 1, 1, 1)
        self.peak2_label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.peak2_label.setFont(font)
        self.peak2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.peak2_label.setObjectName("peak2_label")
        self.CountsGrid.addWidget(self.peak2_label, 0, 2, 1, 1)
        self.counts_label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.counts_label.setFont(font)
        self.counts_label.setAlignment(QtCore.Qt.AlignCenter)
        self.counts_label.setObjectName("counts_label")
        self.CountsGrid.addWidget(self.counts_label, 3, 0, 1, 1)
        self.upper_peak1 = QtWidgets.QTextEdit(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upper_peak1.sizePolicy().hasHeightForWidth())
        self.upper_peak1.setSizePolicy(sizePolicy)
        self.upper_peak1.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.upper_peak1.setFont(font)
        self.upper_peak1.setObjectName("upper_peak1")
        self.CountsGrid.addWidget(self.upper_peak1, 2, 1, 1, 1)
        self.upper_peak2 = QtWidgets.QTextEdit(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upper_peak2.sizePolicy().hasHeightForWidth())
        self.upper_peak2.setSizePolicy(sizePolicy)
        self.upper_peak2.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.upper_peak2.setFont(font)
        self.upper_peak2.setObjectName("upper_peak2")
        self.CountsGrid.addWidget(self.upper_peak2, 2, 2, 1, 1)
        self.counts2 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.counts2.setFont(font)
        self.counts2.setObjectName("counts2")
        self.CountsGrid.addWidget(self.counts2, 3, 2, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(390, 720, 181, 121))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.PlotRangeGrid = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.PlotRangeGrid.setContentsMargins(0, 0, 0, 0)
        self.PlotRangeGrid.setObjectName("PlotRangeGrid")
        self.plot_min_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.plot_min_label.setFont(font)
        self.plot_min_label.setAlignment(QtCore.Qt.AlignCenter)
        self.plot_min_label.setObjectName("plot_min_label")
        self.PlotRangeGrid.addWidget(self.plot_min_label, 1, 0, 1, 1)
        self.plot_max_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.plot_max_label.setFont(font)
        self.plot_max_label.setAlignment(QtCore.Qt.AlignCenter)
        self.plot_max_label.setObjectName("plot_max_label")
        self.PlotRangeGrid.addWidget(self.plot_max_label, 2, 0, 1, 1)
        self.plot_min_entry = QtWidgets.QPlainTextEdit(self.gridLayoutWidget_2)
        self.plot_min_entry.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.plot_min_entry.setFont(font)
        self.plot_min_entry.setObjectName("plot_min_entry")
        self.PlotRangeGrid.addWidget(self.plot_min_entry, 1, 1, 1, 1)
        self.plot_max_entry = QtWidgets.QPlainTextEdit(self.gridLayoutWidget_2)
        self.plot_max_entry.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.plot_max_entry.setFont(font)
        self.plot_max_entry.setObjectName("plot_max_entry")
        self.PlotRangeGrid.addWidget(self.plot_max_entry, 2, 1, 1, 1)
        self.plot_range_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.plot_range_label.setFont(font)
        self.plot_range_label.setAlignment(QtCore.Qt.AlignCenter)
        self.plot_range_label.setObjectName("plot_range_label")
        self.PlotRangeGrid.addWidget(self.plot_range_label, 0, 0, 1, 2)
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(620, 720, 194, 121))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.ChannelSelectGrid = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.ChannelSelectGrid.setContentsMargins(0, 0, 0, 0)
        self.ChannelSelectGrid.setObjectName("ChannelSelectGrid")
        self.channel_select_label = QtWidgets.QLabel(self.gridLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.channel_select_label.setFont(font)
        self.channel_select_label.setAlignment(QtCore.Qt.AlignCenter)
        self.channel_select_label.setObjectName("channel_select_label")
        self.ChannelSelectGrid.addWidget(self.channel_select_label, 1, 0, 1, 1)
        self.channel_select_counts_label = QtWidgets.QLabel(self.gridLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.channel_select_counts_label.setFont(font)
        self.channel_select_counts_label.setAlignment(QtCore.Qt.AlignCenter)
        self.channel_select_counts_label.setObjectName("channel_select_counts_label")
        self.ChannelSelectGrid.addWidget(self.channel_select_counts_label, 2, 0, 1, 1)
        self.channel_select_channel = QtWidgets.QPlainTextEdit(self.gridLayoutWidget_4)
        self.channel_select_channel.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.channel_select_channel.setFont(font)
        self.channel_select_channel.setObjectName("channel_select_channel")
        self.ChannelSelectGrid.addWidget(self.channel_select_channel, 1, 1, 1, 1)
        self.channel_select_title = QtWidgets.QLabel(self.gridLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.channel_select_title.setFont(font)
        self.channel_select_title.setAlignment(QtCore.Qt.AlignCenter)
        self.channel_select_title.setObjectName("channel_select_title")
        self.ChannelSelectGrid.addWidget(self.channel_select_title, 0, 0, 1, 2)
        self.channel_select_counts = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.channel_select_counts.setAlignment(QtCore.Qt.AlignCenter)
        self.channel_select_counts.setObjectName("channel_select_counts")
        self.ChannelSelectGrid.addWidget(self.channel_select_counts, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1272, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSetup = QtWidgets.QMenu(self.menubar)
        self.menuSetup.setObjectName("menuSetup")
        self.menuAnalysis = QtWidgets.QMenu(self.menubar)
        self.menuAnalysis.setObjectName("menuAnalysis")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAcquisition_Settings = QtWidgets.QAction(MainWindow)
        self.actionAcquisition_Settings.setObjectName("actionAcquisition_Settings")
        self.menuSetup.addAction(self.actionAcquisition_Settings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetup.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
        self.restart_button.setText(_translate("MainWindow", "Restart"))
        self.clear_button.setText(_translate("MainWindow", "Clear"))
        self.start_time_label.setText(_translate("MainWindow", "Start Time"))
        self.count_rate.setText(_translate("MainWindow", "---"))
        self.n_acquisitions_label.setText(_translate("MainWindow", "N.Acquisitions"))
        self.n_channel_label.setText(_translate("MainWindow", "N. Channels"))
        self.time_elapsed_label.setText(_translate("MainWindow", "Time Elapsed"))
        self.acquisition_status_label.setText(_translate("MainWindow", "Acqusition Status"))
        self.acquisition_status.setText(_translate("MainWindow", "Stopped"))
        self.start_time.setText(_translate("MainWindow", "---"))
        self.current_acquisition.setText(_translate("MainWindow", " ---"))
        self.threshold_label.setText(_translate("MainWindow", "Threshold"))
        self.n_acquisitions.setText(_translate("MainWindow", " ---"))
        self.n_channels.setText(_translate("MainWindow", "512"))
        self.preset_time.setText(_translate("MainWindow", "---"))
        self.threshold.setText(_translate("MainWindow", "---"))
        self.count_rate_label.setText(_translate("MainWindow", "Count Rate (Hz)"))
        self.current_acquisition_label.setText(_translate("MainWindow", "Current Acquisition"))
        self.time_elapsed.setText(_translate("MainWindow", "---"))
        self.preset_time_label.setText(_translate("MainWindow", "Preset Time"))
        self.lower_bound_label.setText(_translate("MainWindow", "Upper Bound"))
        self.upper_bound_label.setText(_translate("MainWindow", "Lower Bound"))
        self.peak1_label.setText(_translate("MainWindow", "Region 1"))
        self.counts1.setText(_translate("MainWindow", "---"))
        self.peak2_label.setText(_translate("MainWindow", "Region 2"))
        self.counts_label.setText(_translate("MainWindow", "Counts"))
        self.counts2.setText(_translate("MainWindow", "---"))
        self.plot_min_label.setText(_translate("MainWindow", "Min"))
        self.plot_max_label.setText(_translate("MainWindow", "Max"))
        self.plot_range_label.setText(_translate("MainWindow", "Plot Range"))
        self.channel_select_label.setText(_translate("MainWindow", "Channel"))
        self.channel_select_counts_label.setText(_translate("MainWindow", "Counts"))
        self.channel_select_title.setText(_translate("MainWindow", "Channel Select"))
        self.channel_select_counts.setText(_translate("MainWindow", "---"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSetup.setTitle(_translate("MainWindow", "Setup"))
        self.menuAnalysis.setTitle(_translate("MainWindow", "Analysis"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAcquisition_Settings.setText(_translate("MainWindow", "Acquisition Settings"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
