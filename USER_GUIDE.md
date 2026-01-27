# AiiDAlab MLIP User Guide

## Overview

The AiiDAlab MLIP app provides an interactive wizard interface for working with machine learning interatomic potentials (MLIP). Use this app to:

- Upload atomic structures
- Train MLIP models (MACE, M3GNet, CHGNet)
- Run predictions (geometry optimization, molecular dynamics, single point calculations)
- View and analyze results

---

## Current Status

### ✅ What Works Now

1. **Structure Upload** (Step 1)
   - Upload CIF, XYZ, PDB, or POSCAR files
   - View structure information (formula, atom count, cell parameters)
   - Automatic structure validation

2. **Model Selection** (Step 2)
   - Choose from MACE, M3GNet, or CHGNet architectures
   - UI ready for training configuration

3. **Prediction Setup** (Step 3)
   - Select calculation type:
     - Geometry Optimization (relax structure to minimum energy)
     - Single Point (calculate energy and forces)
     - Molecular Dynamics (coming soon)
   - Automatic structure transfer from Step 1
   - Calculation builder preparation

### ⏳ Coming Soon

- **Training Workflow**: Submit MLIP training calculations
- **Calculation Submission**: Actually run calculations (requires AiiDA database setup)
- **Results Visualization**: Interactive plots and structure viewing
- **Molecular Dynamics**: Full MD simulation support

---

## Requirements

### System Requirements

- **Operating System**: Linux (tested on Ubuntu 24.04 in WSL)
- **Docker**: Version 20.10 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Disk Space**: 10GB for Docker images and data

### Software Requirements

**Already included in container**:
- Python 3.9
- AiiDA Core 2.7.2
- AiiDAlab widgets
- aiida-mlip (Python 3.9 compatible fork)
- MLIP packages (MACE, M3GNet, CHGNet)
- ASE (Atomic Simulation Environment)

**Required for full functionality** (not yet set up):
- AiiDA database (PostgreSQL)
- RabbitMQ message broker
- Configured AiiDA profile

---

## Installation

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url> /home/qoj42292/aiidalab/aiidalab-mlip
   cd /home/qoj42292/aiidalab/aiidalab-mlip
   ```

2. **Start the Docker container**:
   ```bash
   docker run -d --name aiidalab-mlip \
     -p 172.20.112.244:8888:8888 \
     -v $(pwd):/home/jovyan/apps/aiidalab-mlip \
     -v /home/qoj42292/aiida-mlip:/home/jovyan/aiida-mlip \
     aiidalab/full-stack:edge
   ```
   
   **Note**: Replace `172.20.112.244` with your WSL IP if different. Find it with: `ip addr show eth0`

3. **Install packages in container**:
   ```bash
   # Install the app
   docker exec aiidalab-mlip pip install -e /home/jovyan/apps/aiidalab-mlip
   
   # Install aiida-mlip plugin
   docker exec aiidalab-mlip pip install -e /home/jovyan/aiida-mlip
   ```

4. **Get the access token**:
   ```bash
   docker logs aiidalab-mlip 2>&1 | grep "token=" | tail -1
   ```
   
   You'll see output like:
   ```
   or http://127.0.0.1:8888/?token=abc123...
   ```

5. **Open in browser**:
   ```
   http://172.20.112.244:8888/?token=<your-token-here>
   ```

### Installation Notes

- **Volume mounting**: Your code at `$(pwd)` is mounted in the container, so changes you make are immediately available
- **Persistence**: The container keeps running until you stop it. Your work is saved in the mounted directories.
- **Restart**: If you restart the container, you must reinstall the packages (step 3)

---

## Usage

### Step 1: Upload Structure

1. Click on your app from the AiiDAlab home page
2. In Step 1 "Select Structure":
   - Click "Upload Structure"
   - Select a structure file:
     - **CIF**: Crystallographic Information File
     - **XYZ**: Standard XYZ coordinates
     - **PDB**: Protein Data Bank format
     - **POSCAR**: VASP structure format
3. View structure information displayed below:
   - Chemical formula
   - Number of atoms
   - Unit cell parameters

**Example structures to try**:
- Download from Materials Project: https://materialsproject.org/
- Use your own research structures
- Generate with ASE or other atomistic tools

### Step 2: Train MLIP Model (Coming Soon)

1. Navigate to Step 2 "Train MLIP"
2. Select architecture:
   - **MACE**: Multi-Atomic Cluster Expansion (high accuracy)
   - **M3GNet**: Materials 3-body Graph Network (versatile)
   - **CHGNet**: Crystal Hamiltonian Graph Neural Network (includes magnetic properties)
3. Configure training parameters (UI ready, backend pending)

**Requirements for Training** (future):
- Training dataset (XYZ files with energies/forces)
- Validation dataset
- Test dataset
- Computational resources (GPU recommended)

### Step 3: Run Predictions

1. Navigate to Step 3 "Run Predictions"
2. Ensure structure was uploaded in Step 1
3. Select calculation type:

   **Geometry Optimization**:
   - Relaxes atomic positions to find minimum energy configuration
   - Default convergence: 0.05 eV/Å
   - Maximum 500 steps

   **Single Point**:
   - Calculates energy and forces at current geometry
   - Fast, no structure modification
   - Useful for energy landscapes

   **Molecular Dynamics** (coming soon):
   - Time evolution simulation
   - NVE, NVT, or NPT ensembles
   - Configurable temperature and timesteps

4. Click "Run Calculation"
5. View builder preparation (actual submission requires AiiDA setup)

### Step 4: View Results (Coming Soon)

- Calculation status monitoring
- Structure visualization
- Energy/force plots
- Trajectory analysis
- Export results

---

## Configuration

### Calculation Parameters

**Geometry Optimization** (current defaults):
```python
fmax = 0.05          # Force convergence (eV/Å)
steps = 500          # Maximum optimization steps
```

**Single Point**:
```python
properties = ['energy', 'forces']  # Calculated properties
```

**Resources** (all calculations):
```python
num_machines = 1
max_wallclock_seconds = 3600
```

### Modifying Defaults

Edit `src/aiidalab_mlip/prediction.py`:
```python
builder.fmax = orm.Float(0.01)    # Tighter convergence
builder.steps = orm.Int(1000)     # More steps
```

---

## Troubleshooting

### Cannot Access App

**Problem**: Browser shows "Unable to connect"

**Solutions**:
1. Check container is running:
   ```bash
   docker ps
   ```
2. Verify port binding:
   ```bash
   docker port aiidalab-mlip
   ```
3. Use correct IP (WSL users):
   ```bash
   ip addr show eth0 | grep "inet "
   ```

### Module Not Found Error

**Problem**: `ModuleNotFoundError: No module named 'aiidalab_mlip'`

**Solution**: Reinstall packages in container
```bash
docker exec aiidalab-mlip pip install -e /home/jovyan/apps/aiidalab-mlip
docker exec aiidalab-mlip pip install -e /home/jovyan/aiida-mlip
```

**Why**: Package installation is lost when container restarts

### Structure Not Passing to Step 3

**Problem**: "No structure loaded" message in prediction step

**Solution**: 
1. Verify structure uploaded successfully in Step 1 (green checkmark)
2. Refresh the browser
3. Re-upload structure if needed

### Token Expired

**Problem**: Asked for token after previously accessing

**Solution**: Get new token after container restart
```bash
docker logs aiidalab-mlip 2>&1 | grep "token=" | tail -1
```

**Permanent fix**: Set a password
```bash
docker exec -it aiidalab-mlip jupyter notebook password
```

---

## Advanced Usage

### Using Pre-trained Models

Currently, the app uses MLIP architecture names (`mace`, `m3gnet`, `chgnet`) which use pre-trained models from the respective packages.

**Custom models** (future):
```python
from aiida_mlip.data.model import ModelData

model = ModelData(path='/path/to/model.pth')
builder.model = model
builder.arch = orm.Str('mace')  # Must match model architecture
```

### Running Calculations via Script

For advanced users who want to bypass the UI:

```python
from aiida import orm, engine
from aiida_mlip.calculations.geomopt import GeomOpt
from ase.io import read

# Load structure
structure_ase = read('structure.cif')
structure_node = orm.StructureData(ase=structure_ase)

# Build calculation
builder = GeomOpt.get_builder()
builder.struct = structure_node
builder.arch = orm.Str('mace')
builder.fmax = orm.Float(0.05)
builder.steps = orm.Int(500)
builder.metadata.options.resources = {'num_machines': 1}

# Submit (requires AiiDA database setup)
node = engine.submit(builder)
print(f"Submitted calculation: {node.pk}")
```

### Batch Calculations

Process multiple structures:

```python
from pathlib import Path

structure_dir = Path('structures')
for structure_file in structure_dir.glob('*.cif'):
    structure_ase = read(structure_file)
    structure_node = orm.StructureData(ase=structure_ase)
    
    builder = GeomOpt.get_builder()
    builder.struct = structure_node
    builder.arch = orm.Str('mace')
    # ... configure builder
    
    node = engine.submit(builder)
    print(f"Submitted {structure_file.name}: {node.pk}")
```

---

## What You Need to Enable Full Functionality

### 1. AiiDA Database Setup

**Current status**: Not configured

**Required steps**:
```bash
# Enter container
docker exec -it aiidalab-mlip bash

# Run AiiDA quick setup
verdi quicksetup

# Follow prompts to configure:
# - Profile name (e.g., "mlip")
# - Email for AiiDA
# - Database name
# - Computer configuration
```

**What this enables**:
- Actual calculation submission
- Process tracking and monitoring
- Results storage and retrieval
- Provenance tracking

### 2. Computational Resources

**For training MLIP models**:
- GPU highly recommended (CUDA-compatible)
- 16GB+ RAM
- Training datasets (energies, forces, stresses)

**For predictions**:
- CPU sufficient for small systems
- GPU recommended for large systems (>100 atoms)

### 3. Training Data

**Required for Step 2 (Training)**:
- `train.xyz` - Training set with DFT energies/forces
- `valid.xyz` - Validation set
- `test.xyz` - Test set

**Format** (extended XYZ):
```
8
Lattice="10.0 0.0 0.0 0.0 10.0 0.0 0.0 0.0 10.0" Properties=species:S:1:pos:R:3:forces:R:3 energy=-123.456 pbc="T T T"
O 0.0 0.0 0.0 0.1 0.2 0.3
H 1.0 0.0 0.0 -0.1 0.1 0.0
...
```

### 4. Code Modifications for Submission

**To enable actual calculation submission**, uncomment in `prediction.py`:

```python
# After builder configuration
node = engine.submit(builder)
print(f"Submitted calculation PK: {node.pk}")

# Add monitoring
self.status.value = f"<p style='color: blue;'>⏳ Calculation {node.pk} submitted</p>"
```

**Add results retrieval** in `results.py`:

```python
from aiida.orm import load_node

calc = load_node(pk)
if calc.is_finished_ok:
    results = calc.outputs.results_dict
    final_structure = calc.outputs.final_structure
    # Display results
```

---

## Development Roadmap

### Version 0.1 (Current)
- ✅ Structure upload interface
- ✅ Model selection UI
- ✅ Calculation builder preparation
- ✅ Python 3.9 compatibility

### Version 0.2 (Next)
- ⏳ AiiDA database integration
- ⏳ Actual calculation submission
- ⏳ Basic results display
- ⏳ Training workflow UI

### Version 0.3 (Future)
- Results visualization (plots, trajectories)
- Molecular dynamics support
- Fine-tuning from pre-trained models
- Model comparison tools

### Version 1.0 (Release)
- Complete training pipeline
- Advanced results analysis
- WorkGraph integration
- Batch processing
- Documentation and tutorials

---

## Support and Contributing

### Getting Help

- Check this guide first
- Review DEVELOPMENT.md for technical details
- Check container logs: `docker logs aiidalab-mlip`

### Reporting Issues

Include:
- Steps to reproduce
- Error messages
- Container logs
- Python version: `docker exec aiidalab-mlip python --version`

### Contributing

1. Fork the repository
2. Create a feature branch
3. Follow existing code patterns (see DEVELOPMENT.md)
4. Test in container
5. Submit pull request

---

## Appendix: File Formats

### CIF (Crystallographic Information File)

```cif
data_Crystal
_cell_length_a    5.0
_cell_length_b    5.0
_cell_length_c    5.0
_cell_angle_alpha 90
_cell_angle_beta  90
_cell_angle_gamma 90
_symmetry_space_group_name_H-M 'P 1'
loop_
_atom_site_label
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
Na 0.0 0.0 0.0
Cl 0.5 0.5 0.5
```

### XYZ (Simple Cartesian Coordinates)

```
2
Water molecule
O 0.0 0.0 0.0
H 1.0 0.0 0.0
```

### POSCAR (VASP Format)

```
System Name
1.0
5.0 0.0 0.0
0.0 5.0 0.0
0.0 0.0 5.0
Na Cl
1 1
Direct
0.0 0.0 0.0
0.5 0.5 0.5
```

---

## Glossary

- **MLIP**: Machine Learning Interatomic Potential - learned functions that predict atomic interactions
- **AiiDA**: Automated Interactive Infrastructure and Database for Computational Science
- **CalcJob**: AiiDA's calculation job class for submitting computations
- **Builder**: AiiDA object for configuring calculation parameters
- **Provenance**: Complete record of calculation inputs, outputs, and history
- **WorkGraph**: AiiDA's workflow management system
- **ASE**: Atomic Simulation Environment - Python library for atomistic simulations

---

## Quick Reference

### Essential Commands

```bash
# Start app
docker start aiidalab-mlip

# Stop app
docker stop aiidalab-mlip

# View logs
docker logs aiidalab-mlip

# Get token
docker logs aiidalab-mlip 2>&1 | grep "token=" | tail -1

# Reinstall packages
docker exec aiidalab-mlip pip install -e /home/jovyan/apps/aiidalab-mlip
docker exec aiidalab-mlip pip install -e /home/jovyan/aiida-mlip

# Enter container shell
docker exec -it aiidalab-mlip bash
```

### Access URL

```
http://172.20.112.244:8888/?token=<your-token>
```

Replace `172.20.112.244` with your WSL/Linux IP if different.
