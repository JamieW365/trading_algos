# trading_algos

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

A collection of algorithmic trading strategies, backtested and documented in individual notebooks.

# Project Folder Overview

This repository contains a collection of quantitative finance mini-projects exploring trading algorithms, portfolio optimization, and related analytical workflows.  
Each mini-project includes a short summary in this file and links to its own detailed report.

---

# Contents
- [Trading Algorithms](#trading-algorithms)
  - [TA Project 1](#ta-project-1)
  - [TA Project 2](#ta-project-2)
  - [TA Project 3](#ta-project-3)
  - [TA Project 4](#ta-project-4)
  - [TA Project 5](#ta-project-5)
- [Portfolio Optimization](#portfolio-optimization)
  - [PO Project 1](#po-project-1)
  - [PO Project 2](#po-project-2)
  - [PO Project 3](#po-project-3)
  - [PO Project 4](#po-project-4)
  - [PO Project 5](#po-project-5)

---

## Trading Algorithms

### TA Project 1
**Short description:** _Add a brief summary here._  
**Full report:** [TA Project 1 Report](./trading_algorithms/ta_project_1.md)

### TA Project 2
**Short description:** _Add a brief summary here._  
**Full report:** [TA Project 2 Report](./trading_algorithms/ta_project_2.md)

### TA Project 3
**Short description:** _Add a brief summary here._  
**Full report:** [TA Project 3 Report](./trading_algorithms/ta_project_3.md)

### TA Project 4
**Short description:** _Add a brief summary here._  
**Full report:** [TA Project 4 Report](./trading_algorithms/ta_project_4.md)

### TA Project 5
**Short description:** _Add a brief summary here._  
**Full report:** [TA Project 5 Report](./trading_algorithms/ta_project_5.md)

---

## Portfolio Optimization

### PO Project 1
**Short description:** _Add a brief summary here._  
**Full report:** [PO Project 1 Report](./portfolio_optimization/po_project_1.md)

### PO Project 2
**Short description:** _Add a brief summary here._  
**Full report:** [PO Project 2 Report](./portfolio_optimization/po_project_2.md)

### PO Project 3
**Short description:** _Add a brief summary here._  
**Full report:** [PO Project 3 Report](./portfolio_optimization/po_project_3.md)

### PO Project 4
**Short description:** _Add a brief summary here._  
**Full report:** [PO Project 4 Report](./portfolio_optimization/po_project_4.md)

### PO Project 5
**Short description:** _Add a brief summary here._  
**Full report:** [PO Project 5 Report](./portfolio_optimization/po_project_5.md)

---


## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         trading_algos and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── trading_algos   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes trading_algos a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

