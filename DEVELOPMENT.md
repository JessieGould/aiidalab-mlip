# AiiDAlab MLIP App - Development Log

## Project Overview

**Goal**: Create an AiiDAlab application for machine learning interatomic potentials (MLIP) that provides a wizard-based interface for training models and running calculations using aiida-mlip.

**Key Requirements**:
- AiiDA provenance tracking and workgraph capabilities
- Support for MACE, M3GNet, and CHGNet models
- Interactive wizard interface for structure upload, training, predictions, and results
- Integration with existing aiida-mlip plugin

---

## Development Timeline

### Phase 1: Docker Environment Setup

**Date**: January 19, 2026

1. **Docker Installation**
   - Installed Docker Engine 29.1.5 on Ubuntu 24.04 (WSL)
   - Added user to docker group: `sudo usermod -aG docker $USER`

2. **Initial Container Setup**
   ```bash
   docker run -d --name aiidalab-mlip \
     -p 172.20.112.244:8888:8888 \
     -v /home/qoj42292/aiidalab/aiidalab-mlip:/home/jovyan/apps/aiidalab-mlip \
     aiidalab/full-stack:latest
   ```
   - Used WSL IP (172.20.112.244) instead of localhost due to WSL networking
   - Volume mount enables live code editing without container rebuilds

3. **Additional Volume Mount for aiida-mlip**
   ```bash
   docker run -d --name aiidalab-mlip \
     -p 172.20.112.244:8888:8888 \
     -v /home/qoj42292/aiidalab/aiidalab-mlip:/home/jovyan/apps/aiidalab-mlip \
     -v /home/qoj42292/aiida-mlip:/home/jovyan/aiida-mlip \
     aiidalab/full-stack:edge
   ```

---

### Phase 2: App Structure Creation

**Date**: January 19, 2026

**Reference**: Used aiidalab-chemshell as architectural template

**Directory Structure Created**:
```
aiidalab-mlip/
├── setup.cfg                    # Package configuration
├── pyproject.toml              # Build system config
├── start.py                    # App home page banner
├── main.ipynb                  # App entry point
├── example.ipynb               # Simple example notebook
└── src/
    └── aiidalab_mlip/
        ├── __init__.py
        ├── main.py             # MainApp and WizardWidget
        ├── process.py          # Data models (traitlets)
        ├── structure.py        # Step 1: Structure upload
        ├── training.py         # Step 2: MLIP training
        ├── prediction.py       # Step 3: Run calculations
        ├── results.py          # Step 4: View results
        └── common/             # Shared utilities
```

**Key Pattern**: Model-View-Controller with wizard pattern
- Models: traitlets-based data storage (process.py)
- Views: ipywidgets-based UI (wizard step files)
- Controller: MainApp orchestration (main.py)

---

### Phase 3: Dependency Management

**Date**: January 19, 2026

**Issues Encountered**:

1. **Pydantic Version Conflict**
   - Error: `aiida-core` requires pydantic >=2.4 (field_serializer import)
   - Container had: pydantic 1.10.26
   - Fix:
     ```bash
     docker exec aiidalab-mlip pip uninstall -y pydantic
     docker exec aiidalab-mlip pip install 'pydantic>=2.4,<3'
     ```
   - Result: Upgraded to pydantic 2.11.7

2. **Missing aiidalab-widgets-base**
   - Added to setup.cfg dependencies
   - Installed via: `pip install -e /home/jovyan/apps/aiidalab-mlip`

3. **Package Installation After Structure Change**
   - Each container restart requires reinstallation:
     ```bash
     docker exec aiidalab-mlip pip install -e /home/jovyan/apps/aiidalab-mlip
     ```

**Final setup.cfg dependencies**:
```ini
[options]
install_requires =
    aiidalab>=21.09.0
    aiidalab-widgets-base
    aiida-core
    traitlets~=5.0
    ipywidgets~=7.7
```

---

### Phase 4: Wizard UI Implementation

**Date**: January 19-20, 2026

**Critical Discovery**: ChemShell uses multiple inheritance pattern
```python
# Correct pattern (from chemshell)
class StructureWizardStep(ipw.VBox, awb.WizardAppWidgetStep):
    pass

# Initial incorrect attempt
class StructureWizardStep(ipw.VBox):
    state = traitlets.UseEnum(...)  # Manual state attribute doesn't work
```

**Issue**: `AttributeError: 'StructureWizardStep' object has no attribute 'state'`

**Solution**: Inherit from both `ipw.VBox` AND `awb.WizardAppWidgetStep`
- `WizardAppWidgetStep` provides required `state` attribute
- State values must be uppercase: `'SUCCESS'`, `'FAIL'`, `'CONFIGURED'`

**Applied to all four wizard steps**:
- structure.py
- training.py
- prediction.py
- results.py

---

### Phase 5: Structure Upload Implementation

**Date**: January 20, 2026

**Features Implemented**:
```python
# structure.py additions
import tempfile
from ase.io import read as ase_read

def _on_file_upload(self, change):
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='wb', suffix=filename, delete=False) as f:
        f.write(content)
    
    # Read with ASE
    structure = ase_read(temp_path)
    
    # Store in model (direct assignment, not .value)
    self.model.structure = structure
    
    # Set state
    self.state = 'SUCCESS'  # Must be uppercase
```

**Supported formats**: CIF, XYZ, PDB, POSCAR

**Display**:
- Chemical formula
- Number of atoms
- Cell parameters
- Success/error status messages

---

### Phase 6: Python 3.9 Compatibility for aiida-mlip

**Date**: January 20, 2026

**Problem Identified**:
- AiiDAlab container: Python 3.9.13
- aiida-mlip requirement: Python >=3.10
- Blocker: `match` statement syntax (Python 3.10+)

**Verification Process**:
```bash
# Install vermin for version checking
pip install vermin

# Scan aiida-mlip
vermin ~/aiida-mlip/aiida_mlip -t=3.9 --violations
```

**Result**: Only ONE file incompatible: `aiida_mlip/helpers/converters.py`

**Solution Implemented**:

1. **Created compatibility branch**:
   ```bash
   cd ~/aiida-mlip
   git checkout -b python39-compat
   ```

2. **Replaced match statement** in converters.py:
   ```python
   # BEFORE (Python 3.10+)
   match val:
       case bool() if val:
           cmdline_params.append(f"--{key}")
       case bool():
           cmdline_params.append(f"--no-{key}")
       case _:
           cmdline_params.extend((f"--{key}", str(val)))
   
   # AFTER (Python 3.9 compatible)
   if isinstance(val, bool):
       if val:
           cmdline_params.append(f"--{key}")
       else:
           cmdline_params.append(f"--no-{key}")
   else:
       cmdline_params.extend((f"--{key}", str(val)))
   ```

3. **Updated pyproject.toml**:
   ```toml
   # Changed from:
   requires-python = ">=3.10"
   
   # To:
   requires-python = ">=3.9"
   ```

4. **Relaxed janus-core dependency**:
   ```toml
   # Changed from:
   "janus-core<0.9,>=0.8.3"
   
   # To:
   "janus-core>=0.6.2"
   ```
   - Version 0.8.3+ not available for Python 3.9
   - Version 0.7.0 already installed in container

5. **Verified compatibility**:
   ```bash
   vermin ~/aiida-mlip/aiida_mlip/*.py ~/aiida-mlip/aiida_mlip/**/*.py
   # Result: Minimum required versions: 3.9 ✓
   ```

6. **Installed in container**:
   ```bash
   docker exec aiidalab-mlip pip install -e /home/jovyan/aiida-mlip
   ```

7. **Tested imports**:
   ```bash
   docker exec aiidalab-mlip python -c 'from aiida_mlip.calculations.geomopt import GeomOpt; print("✓")'
   # Result: SUCCESS
   ```

**Commits**:
- `7895e12` - Make Python 3.9 compatible: Replace match statement with if/elif
- `098a935` - Update Python requirement to >=3.9
- `933b24a` - Relax janus-core dependency for Python 3.9 compatibility

---

### Phase 7: Prediction Calculations Integration

**Date**: January 20, 2026

**Imports Added** to prediction.py:
```python
from aiida import orm, engine
from aiida_mlip.calculations.geomopt import GeomOpt
from aiida_mlip.calculations.singlepoint import Singlepoint
from ase.io import write as ase_write
import io
```

**Structure Linking** in main.py:
```python
# Observe structure changes and pass to prediction step
def update_prediction_structure(change):
    self.prediction_step._parent_structure = change['new']

model.structure_model.observe(update_prediction_structure, names='structure')
```

**Calculation Builder Implementation**:
```python
def _on_run_click(self, button):
    # Get structure from Step 1
    structure = getattr(self, '_parent_structure', None)
    
    # Convert ASE to AiiDA
    structure_node = orm.StructureData(ase=structure)
    
    # Build calculation
    if calc_type == 'geometry_opt':
        builder = GeomOpt.get_builder()
        builder.struct = structure_node
        builder.arch = orm.Str('mace')
        builder.fmax = orm.Float(0.05)
        builder.steps = orm.Int(500)
    elif calc_type == 'single_point':
        builder = Singlepoint.get_builder()
        builder.struct = structure_node
        builder.arch = orm.Str('mace')
    
    # Set resources
    builder.metadata.options.resources = {'num_machines': 1}
    builder.metadata.options.max_wallclock_seconds = 3600
    
    # Ready for submission (currently dry run)
    # To submit: node = engine.submit(builder)
```

**Current Status**: Builder preparation works, submission commented out pending AiiDA database setup

---

## Technical Decisions

### Why Volume Mounting?
- Live code editing without rebuilds
- Faster development iteration
- Preserves git history on host
- Easy backup and version control

### Why Multiple Inheritance for Wizard Steps?
- `WizardAppWidgetStep` provides required interface
- `ipw.VBox` provides container layout
- Both needed for proper wizard integration
- Pattern established by aiidalab-chemshell

### Why Python 3.9 Compatibility?
- Official AiiDAlab images use Python 3.9
- Building custom image adds complexity
- Match statement easily convertible
- Minimal code changes required

### Why Traitlets for Models?
- AiiDA/AiiDAlab ecosystem standard
- Observable pattern for reactive UI
- Type validation built-in
- Compatible with ipywidgets

---

## Repository Structure

### Main App Repository
**Location**: `/home/qoj42292/aiidalab/aiidalab-mlip`

**Branches**:
- `main` - Current development

**Key Files**:
- `setup.cfg` - Package configuration with dependencies
- `main.ipynb` - Entry point that loads MainApp
- `start.py` - Home page banner widget
- `src/aiidalab_mlip/` - Python package

### aiida-mlip Fork
**Location**: `/home/qoj42292/aiida-mlip`

**Branches**:
- `main` - Original upstream code (Python 3.10+)
- `python39-compat` - Python 3.9 compatible version

**Changes**:
- Single file: `aiida_mlip/helpers/converters.py`
- pyproject.toml: Python version requirement
- pyproject.toml: janus-core dependency

---

## Installation Commands Reference

### Container Management
```bash
# Start container
docker run -d --name aiidalab-mlip \
  -p 172.20.112.244:8888:8888 \
  -v /home/qoj42292/aiidalab/aiidalab-mlip:/home/jovyan/apps/aiidalab-mlip \
  -v /home/qoj42292/aiida-mlip:/home/jovyan/aiida-mlip \
  aiidalab/full-stack:edge

# Stop container
docker stop aiidalab-mlip

# Remove container
docker rm aiidalab-mlip

# View logs (get token)
docker logs aiidalab-mlip 2>&1 | grep "token=" | tail -1
```

### Package Installation in Container
```bash
# Install aiidalab-mlip app
docker exec aiidalab-mlip pip install -e /home/jovyan/apps/aiidalab-mlip

# Install aiida-mlip plugin
docker exec aiidalab-mlip pip install -e /home/jovyan/aiida-mlip

# Verify imports
docker exec aiidalab-mlip python -c "from aiida_mlip.calculations.geomopt import GeomOpt; print('✓')"
```

### Pydantic Fix (if needed)
```bash
docker exec aiidalab-mlip pip uninstall -y pydantic
docker exec aiidalab-mlip pip install 'pydantic>=2.4,<3'
```

---

## Known Issues and Workarounds

### Issue 1: Token Changes on Restart
**Problem**: Jupyter token changes each time container restarts

**Workaround**: 
```bash
# Get new token
docker logs aiidalab-mlip 2>&1 | grep "token=" | tail -1
```

**Permanent Solution**:
```bash
docker exec -it aiidalab-mlip jupyter notebook password
```

### Issue 2: Module Not Found After Restart
**Problem**: Package installation lost on container restart

**Cause**: Packages installed in container, not in base image

**Workaround**: Reinstall after each restart
```bash
docker exec aiidalab-mlip pip install -e /home/jovyan/apps/aiidalab-mlip
docker exec aiidalab-mlip pip install -e /home/jovyan/aiida-mlip
```

**Future Solution**: Create custom Docker image with packages pre-installed

### Issue 3: WSL Networking
**Problem**: localhost:8888 doesn't work from Windows

**Solution**: Use WSL IP address (172.20.112.244)

### Issue 4: Traitlets Attribute Access
**Problem**: `self.model.structure.value = ...` raises AttributeError

**Solution**: Direct assignment without `.value`:
```python
self.model.structure = structure  # Correct
```

---

## Dependencies Installed

### In Container (Python 3.9)
- aiida-core==2.7.2
- aiidalab-widgets-base==2.5.0
- pydantic==2.11.7
- traitlets~=5.9.0
- ipywidgets~=7.7
- ase==3.26.0
- chgnet==0.3.8
- mace-torch==0.3.8
- m3gnet==0.2.4
- janus-core==0.7.0
- aiida-mlip==0.4.1 (from python39-compat branch)

### In Host Virtual Environment
- cookiecutter
- vermin (for Python version checking)

---

## Next Development Steps

### Immediate (Not Yet Implemented)
1. **AiiDA Database Setup**
   ```bash
   docker exec -it aiidalab-mlip verdi quicksetup
   ```

2. **Enable Actual Calculation Submission**
   - Uncomment `node = engine.submit(builder)` in prediction.py
   - Add process monitoring
   - Handle calculation states

3. **Training Workflow Implementation**
   - Connect to Train calcjob
   - Handle training data upload
   - Configure MACE/M3GNet/CHGNet parameters

4. **Results Visualization**
   - Display calculation outputs
   - Structure viewer integration
   - Energy/force plots
   - Trajectory visualization for MD/geomopt

### Medium Term
1. **Custom Docker Image**
   - Pre-install packages
   - Eliminate reinstall on restart
   - Include AiiDA database setup

2. **WorkGraph Integration**
   - Multi-step workflows
   - Training → Validation → Production pipeline

3. **Advanced Features**
   - Fine-tuning from pre-trained models
   - Model comparison tools
   - Batch calculations

### Long Term
1. **Python 3.10+ Support**
   - Wait for AiiDAlab upstream update
   - Merge python39-compat changes or drop fork

2. **Production Deployment**
   - Multi-user setup
   - Resource scheduling
   - Results database

---

## Testing Checklist

- [x] Container starts successfully
- [x] App appears on AiiDAlab home page
- [x] Structure upload (CIF, XYZ, PDB, POSCAR)
- [x] Structure display (formula, atoms, cell)
- [x] Wizard navigation
- [x] Model selection dropdown
- [x] Calculation type selection
- [x] aiida-mlip imports work
- [x] Calculation builder creation
- [ ] AiiDA database connection
- [ ] Actual calculation submission
- [ ] Process monitoring
- [ ] Results retrieval
- [ ] Results visualization

---

## References

- AiiDAlab: https://aiidalab.readthedocs.io/
- aiida-mlip: ~/aiida-mlip
- aiidalab-chemshell: ~/aiidalab/aiidalab-chemshell (reference architecture)
- AiiDA documentation: https://aiida.readthedocs.io/
- ipywidgets: https://ipywidgets.readthedocs.io/
