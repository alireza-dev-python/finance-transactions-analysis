# Finance Transactions Analysis

A Python tool that analyzes financial transaction logs to detect high-risk users.

## What it does

This project reads transaction data from a JSON log file, stores it in a SQLite database, and runs an SQL query to find users who had **more than 3 failed transactions within a single hour**. These users are flagged as high-risk.

## Technologies used

- Python 3
- SQLite3
- JSON

## How to run

```bash
python analysis.py