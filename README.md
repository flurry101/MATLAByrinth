## **MATLAByrinth** 

<img width="240" alt="Icon" src="MATLabyrinth.png" align="right" />

Accelerating high-fidelity road network modeling for realistic Indian traffic simulations.

[![MIT License](https://img.shields.io/badge/License-MIT-FF9933)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/flurry101/MATLabyrinth?style=social)](https://github.com/flurry101/MATLabyrinth/stargazers)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/flurry101/MATLabyrinth?color=1A237E)](https://github.com/flurry101/MATLabyrinth/pulls)
[![GitHub Forks](https://img.shields.io/github/forks/flurry101/MATLabyrinth?style=social)](https://github.com/flurry101/MATLabyrinth/network/members)
[![Contributors](https://img.shields.io/github/contributors/flurry101/MATLabyrinth?color=138808)](https://github.com/flurry101/MATLabyrinth/graphs/contributors)

---

## Motivation

Urban traffic congestion in Indian cities is exacerbated by the limitations of existing urban planning software. Such software typically assumes ideal road conditions and doesn't account for the chaotic nature of Indian roads  such as potholes, erratic driving behaviors, sudden road closures, and ever-changing traffic patterns. These are common in Indian urban environments but often overlooked in current simulation tools. Manually modeling these intricate and dynamic road features for digital twin creation is both tedious and time-consuming, requiring significant engineering effort. This ultimately delays the ability to perform realistic simulations and impedes the development of effective traffic management solutions, which in turn negatively impacts crisis handling, congestion management, and infrastructure planning.


---

## Getting Started

### ⌗ Pre-requisites
Before you begin, ensure that the following software is installed on your local machine:

- MATLAB (R2025a or later) with Automated Driving Toolbox
- RoadRunner R2025a (or later)
- Python 3.10+
- Git

---

### ⌗ Installation and Usage

#### 1. Clone the Repository

```bash
git clone https://github.com/flurry101/MATLAByrinth.git
cd MATLAByrinth
```
#### 2. Install Dependencies

##### Install MATLAB Engine for Python (One-Time Setup)
This is a one-time administrative task required to allow Python to control MATLAB.
1. Open a new PowerShell terminal as an administrator.
2. Navigate to the MATLAB Engine directory within your MATLAB installation:
```bash
cd "C:\Program Files\MATLAB\R2025a\extern\engines\python"
```
3. Run the installation script. This installs the engine globally for your Python installation.
```bash
python setup.py install
```
4. You can now close the administrator terminal window.

##### Install Python Dependencies

- Open a standard PowerShell terminal in the project's root directory (`MATLAByrinth`).
- Run the following commands to create a virtual environment and install the necessary packages. The main.py script requires this environment to exist.
```bash
# Create a virtual environment in the 'automation' folder
python -m venv automation\venv

# Activate the virtual environment
.\automation\venv\Scripts\Activate.ps1

# Install the required packages in the virtual env
pip install -r automation\requirements.txt

# Generate the necessary python gRPC interface files created from the .proto files present in RoadRunner 2025a\bin\win64\* in mathworks\ folder
python -m grpc_tools.protoc --proto_path="C:\Program Files\RoadRunner R2025a\bin\win64\Proto" --python_out=. --grpc_python_out=. mathworks/roadrunner/core.proto mathworks/roadrunner/import_settings.proto mathworks/roadrunner/export_settings.proto mathworks/scenario/common/geometry.proto mathworks/scenario/common/array.proto mathworks/roadrunner/roadrunner_service_messages.proto mathworks/roadrunner/roadrunner_service.proto
```

**Note:** To get the RoadRunner instance up and running:
- Open a new PowerShell window.
- Navigate to: `cd C:\Program Files\RoadRunner R2025a\bin\win64`. It programmatically starts the RoadRunner application with the API enabled and waits for it to initialize.
- Run `\AppRoadRunner --projectPath "C:\rr" --apiPort 54321` there by replacing `C:\rr` with your cloned folder's  full location.

##### Run the python file
```ps
python automation\main.py
```

---

## Contributing

Contributions are welcome! Here’s a quick start:

- Fork the repository (via GitHub UI)

- Clone your fork
    ```bash
    git clone <your-repository-url>
    cd <your-repository>
    ```

- Create a new branch
   ```bash
   git checkout -b feature-name
   ```

- Make your changes and commit
   ```bash
   git commit -m "add feature description"
   ```
- Push to your fork
   ```bash
   git push origin feature-name
   ```
➡️ Then, go to GitHub and open a Pull Request to the main repo.

---

## License

This project is licensed under the **[MIT License](LICENSE.md)**.


---

Made with 💙 in <span style="color:#FF9933"><strong>India 🇮🇳</strong></span> using <span style="color:#138808"><strong>MATLAB</strong></span>
