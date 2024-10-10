# Memory Mangemant Simulator

## Overview

This project simulates a memory management system in Python. It includes classes for managing memory blocks, pools, and arenas, and provides tools for analyzing and tracking memory usage. The project is structured into several modules, each with specific responsibilities, and includes unit tests to ensure the correctness of the implementation.

## Modules

The project is organized into the following main components:

### Function Files:

* [`analyzer.py`](vscode-file://vscode-app/c:/Users/Gabri/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.esm.html): Contains the [`MemoryAnalyzer`](vscode-file://vscode-app/c:/Users/Gabri/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.esm.html) class which defines memory analysis functionalities.
* `manager.py`: Contains the `MemoryManager` class which manages memory operations.
* `memory.py`: Contains the `Block, Pool, & Arena` classes which represents memory objects.

### Test Files:

* `test_analyzer.py`: Contains unit tests for the [`MemoryAnalyzer`](vscode-file://vscode-app/c:/Users/Gabri/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.esm.html) class.
* `test_manager.py`: Contains unit tests for the `MemoryManager` class.
* `test_memory.py`: Contains unit tests for the `Memory` class.
* `test.py`: Contains additional tests for the project.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/YourUsername/Memory-Management-Simulator.git
cd Memory-Management-Simulator
```

1. Create a virtual environment and activate it:

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

1. Install the required dependencies:

```sh
pip install -r requirements.txt
```

### Usage

1. **Analyze Memory** : Use the [`MemoryAnalyzer`](vscode-file://vscode-app/c:/Users/Gabri/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.esm.html) class to analyze memory usage.
2. **Manage Memory** : Use the `MemoryManager` class to manage memory operations.
3. **Track Memory** : Use the `Memory` class to track memory objects.

#### Example Usage

the `test.py` file contains an example usage of the analyzer working with the manager and memory objects, which created the `Memory_log.txt` file for illustration purposes. Such as returning this summarized output after the 30 seconds.

```
    2024-10-08 23:42:36,145 - Type: memory.Arena, Count: 3, Size: 144 bytes
    2024-10-08 23:42:36,145 - Type: memory.Pool, Count: 157, Size: 7536 bytes
    2024-10-08 23:42:36,145 - Type: memory.Block, Count: 1861, Size: 89328 bytes
```

## Acknowledgements

This project uses the following libraries and frameworks:

* [`pympler`](vscode-file://vscode-app/c:/Users/Gabri/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.esm.html) for memory analysis and tracking
* [`logging`](vscode-file://vscode-app/c:/Users/Gabri/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.esm.html) for logging memory usage information
* [`unittest`](vscode-file://vscode-app/c:/Users/Gabri/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.esm.html) for unit testing
