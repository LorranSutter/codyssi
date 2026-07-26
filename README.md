# 🧭 Codyssi

[![Dashboard](https://img.shields.io/badge/Dashboard-coding--challenges-blue?style=for-the-badge)](https://github.com/LorranSutter/coding-challenges) <!-- BADGE:START -->[![Solved Challenges](https://img.shields.io/badge/Solved%20Challenges-32-brightgreen?style=for-the-badge&logo=python&logoColor=white)](https://www.codyssi.com/)<!-- BADGE:END -->

This repository contains my solutions for [Codyssi](https://www.codyssi.com/).

Codyssi is a coding competition, with problems released daily and each problem split into three parts of increasing difficulty.

<!-- SUMMARY:START -->
## 📊 Progress

> **Overall: 32/66 parts solved (48%)**

### [2024 — Summer at the Lab](./2024/)

`████████████` **12/12** parts solved (100%)

### [2025 — Journey to Atlantis](./2025/)

`████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░` **20/54** parts solved (37%)

<!-- SUMMARY:END -->

## 🛠️ Setup

### Creating a Virtual Environment

```bash
python3 -m venv .venv
```

### Activating the Virtual Environment

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

Deactivating the Virtual Environment

```bash
deactivate
```

## ✨ Creating a New Problem

To create a new problem structure, use the `new_problem.sh` script:

```bash
./new_problem.sh <year> <problem>
```

Example:
```bash
./new_problem.sh 2025 1
```

This will create:
- A folder structure: `2025/problem01/`
- `main.py` with a template for part 1, part 2 and part 3
- `input.txt` for the problem input
- `input_sample.txt` for sample/test input

## 🚀 Running Solutions

You can run the solutions:

```bash
python3 -m 2025.problem01.main
```

Replace `2025` with the desired year and `problem01` with the specific problem you want to run.

By default this runs against `input.txt`. Pass `--test` to run against `input_sample.txt` instead:

```bash
python3 -m 2025.problem01.main --test
```

## 🔄 Updating Progress Summary

To update the progress summary in this README after solving new parts, run the `generate_readme.py` script:

```bash
python3 generate_readme.py
```
