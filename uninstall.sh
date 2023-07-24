#!/bin/bash

# Uninstall installed Python packages using pip3
pip3 uninstall tk -y
pip3 uninstall yfinance -y
pip3 uninstall prettytable -y
pip3 uninstall TA-Lib -y
pip3 uninstall alpaca-trade-api -y

echo "Uninstallation completed."
