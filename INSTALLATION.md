# AiiDAlab MLIP Installation Guide

## Current Status

The app UI is functional with structure upload working. However, **aiida-mlip integration is blocked** due to Python version incompatibility.

## Known Issues

### Python Version Mismatch
- **AiiDAlab container**: Python 3.9.13
- **aiida-mlip requirement**: Python ≥3.10
- **Blocker**: aiida-mlip uses Python 3.10+ syntax (`match` statements)

### Attempted Workarounds
1. ✗ Tried `aiidalab/full-stack:edge` - still Python 3.9
2. ✗ Manual dependency installation - syntax errors remain
3. ✗ Direct module copy - incompatible with Python 3.9

## Solutions

### Option 1: Wait for Updated AiiDAlab Image (Recommended)
Wait for AiiDAlab to release an image with Python 3.10+.

### Option 2: Custom Docker Image
Build a custom image based on a Python 3.10+ base:

```dockerfile
FROM python:3.11-slim

# Install AiiDA and AiiDAlab
RUN pip install aiida-core aiidalab aiidalab-widgets-base

# Install aiida-mlip
COPY aiida-mlip /tmp/aiida-mlip
RUN pip install /tmp/aiida-mlip

# Set up Jupyter
RUN pip install jupyterlab
WORKDIR /home/jovyan
```

### Option 3: Use Pre-trained Models
Skip training step and use pre-trained MLIP models:
- Download pre-trained MACE/CHGNet/M3GNet models
- Use only prediction calculations (geomopt, MD, singlepoint)
- Models available from Materials Project or model repositories

## Current Functionality

### ✅ Working
- Structure file upload (CIF, XYZ, PDB, POSCAR)
- ASE structure parsing and display
- Wizard UI navigation
- Model selection dropdowns
- Calculation type selection

### ⏳ Pending aiida-mlip
- Training MLIP models
- Running predictions (geometry opt, MD, single point)
- Results visualization
- AiiDA workflow submission

## Development Setup

The app is mounted via volume for live code editing:
```bash
# Container location
/home/jovyan/apps/aiidalab-mlip -> /home/qoj42292/aiidalab/aiidalab-mlip

# Refresh browser to see code changes
```

## Next Steps

1. **Short term**: Document API and prepare workflow integration code
2. **Medium term**: Build custom Docker image with Python 3.11
3. **Long term**: Contribute to AiiDAlab for Python 3.10+ support
