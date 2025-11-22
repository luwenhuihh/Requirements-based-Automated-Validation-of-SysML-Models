# Requirements-based Automated Validation of SysML Models: A Tool Chain Solution

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Generic badge](https://img.shields.io/badge/Status-Research_Artifact-green.svg)](https://github.com/luwenhuihh/Requirements-based-Automated-Validation-of-SysML-Models/)

## 📖 Project Overview

This repository contains the implementation code, system models, and experimental data for the paper **"Requirements-based Automated Validation of SysML Models: A Tool Chain Solution"**.

We propose a novel **Requirements-Automated Validation ENgine (RAVEN)**, an integrated tool chain that bridges the gap between natural language requirements and executable SysML models. This repository serves as a **standardized benchmark** for the community, featuring a representative aerospace system: the **Radar-like Reconnaissance (RR) System**.

The tool chain automates the following loop:
1.  **Formalization:** Parses natural language requirements.
2.  **Test Generation:** Automatically generates test cases (inputs/expected outputs).
3.  **Simulation:** Drives the SysML model simulation.
4.  **Verification:** Compares model outputs against requirements to generate verdicts.

## 📂 Repository Structure

The repository is organized as follows:

| File Name | Description |
| :--- | :--- |
| `RR_System_Model.mdzip` | **The SysML Model.** The core "Radar-like Reconnaissance (RR)" system model created in MagicDraw/Cameo.|
| `RR_System_Requirements.xls` | **Input Requirements.** The Excel file containing the 20 functional requirements used for the case study . |
| `TestDataGeneration.py` | **Test Generator.** Python script that parses the Excel requirements and generates the test case suite using logic like Boundary Value Analysis. |
| `Report_Generation.py` | **Verifier & Reporter.** Python script that analyzes simulation logs, compares them with expected results, and generates the final Word report. |
| `README.md` | This file. |

## 🛠️ Prerequisites

To run the tool chain and simulation, you need the following environment:

### Software
*   **SysML Modeling Tool:** MagicDraw  19.0 or later.
*   **Python:** Version 3.8+.

### Python Libraries
Install the required dependencies using pip:

```bash
pip install pandas openpyxl python-docx tkinter
```
🚀 Usage Guide
Step 1: Generate Test Cases
Run the test generation script to parse the requirements and create the test suite.
```bash
python TestDataGeneration.py
Input: RR_System_Requirements.xls

Output: Generates an intermediate Excel file containing test inputs and expected outputs.

Step 2: Model Simulation (SysML)
Open RR_System_Model.mdzip in MagicDraw.

Configure the simulation to read from the generated Excel file.

Run the simulation. The model will execute the logic and write actual outputs back to the Excel file.

Step 3: Verify and Report
Run the reporting script to validate the results.

python Report_Generation.py
Input: The spreadsheet containing both "Expected Outputs" and populated "Model Outputs".

Output: A comprehensive test report (Word document) with Pass/Fail verdicts.

📊 Case Study: RR System
The Radar-like Reconnaissance (RR) System serves as the System Under Test (SUT). It includes:

20 Functional Requirements: Covering mode management, performance parameters, and subsystem logic.

Seeded Faults: The model includes versions with deliberate faults (Logic, Performance, Boundary) to demonstrate validation capabilities.
