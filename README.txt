ADACORE42
├── _LatexRepports/                      <- LaTeX reports and related packages
│   └── P1_Milestone/
│
├── _Other/                              <- Miscellaneous or supplementary documents
│   ├── andras_analysis/
│   ├── cycy_analysis/
│   ├── dom_analysis/
│   ├── Installation/
│   └── katia_analysis/│
├── data/                                <- Clean and processed data
│   └── newyorker_caption_contest_virgin/
│       ├── data/
│       ├── images/
│       ├── contests.json
│       └── README.md
│
├── src/                                 <- Source code
│   ├── data/                            <- Data loading and preprocessing
│   │   ├── __init__.py
│   │   ├── data_loaders.py
│   │   ├── dataPrepared.pkl
│   │   ├── plots_gui.pkl
│   │   └── README.md
│   │
│   ├── models/                          <- Modeling and GUI code
│   │   ├── gui/
│   │   │   ├── gui.py
│   │   │   ├── plots_gui.py
│   │   │   └── tutorial.ipynb
│   │   ├── __init__.py
│   │   ├── DataPreparation.ipynb
│   │   ├── dummy_methods.py
│   │   └── README.md
│   │
│   ├── scripts/                         <- Helper or runner scripts
│   │   ├── __init__.py
│   │   └── README.md
│   │
│   └── utils/                           <- Utility and helper functions
│       ├── __init__.py
│       └── README.md
│
├── tests/                               <- Unit and integration tests
│   └── README.md
│
├── paths.py                             <- Centralized file paths configuration
├── .gitignore                           <- Files and directories ignored by Git
├── pip_requirements.txt                 <- Python dependencies
├── README.txt                           <- Project overview and structure
└── results.ipynb                        <- Final analysis and visual results