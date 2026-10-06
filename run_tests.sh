#!/usr/bin/env bash
set -e

echo "===================================================================="
echo "Coffee Agriculture PLN Reasoning System — Verification Suite"
echo "===================================================================="

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

VENV_DIR="$PROJECT_ROOT/.venv-metta"
PYTHON_BIN="$VENV_DIR/bin/python"
PYTEST_BIN="$VENV_DIR/bin/pytest"
METTA_BIN="$VENV_DIR/bin/metta"

if [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR."
    echo "Please set up the environment with:"
    echo "  uv python install 3.12"
    echo "  uv venv .venv-metta --python 3.12"
    echo "  uv pip install -p .venv-metta hyperon streamlit pytest"
    exit 1
fi

echo "Environment Information:"
echo "  Python Version:  $($PYTHON_BIN --version)"
echo "  Hyperon Version: $($PYTHON_BIN -c 'import hyperon; print(hyperon.__version__)')"
echo "  Pytest Version:  $($PYTEST_BIN --version | head -n 1)"
echo ""

echo "--------------------------------------------------------------------"
echo "1. Running Native MeTTa Script Verifications..."
echo "--------------------------------------------------------------------"
$METTA_BIN metta/tests/test_pln_core.metta
echo "  ✓ Core MeTTa formulas test passed."
$METTA_BIN examples/agriculture_pln_demo.metta
echo "  ✓ 4-operation Agricultural PLN demo executed successfully."
$METTA_BIN examples/agriculture_forward.metta
echo "  ✓ Agricultural Forward Chaining executed successfully."
$METTA_BIN examples/agriculture_backward.metta
echo "  ✓ Agricultural Backward Chaining executed successfully."
$METTA_BIN examples/agriculture_revision.metta
echo "  ✓ Agricultural Conflicting Evidence Revision executed successfully."

echo ""
echo "--------------------------------------------------------------------"
echo "2. Running Comprehensive Pytest Suite (Domain, Semantic & Negatives)..."
echo "--------------------------------------------------------------------"
PYTHONPATH=. "$PYTEST_BIN" -v

echo ""
echo "===================================================================="
echo "ALL TESTS PASSED! System is 100% verified and reproducible."
echo "===================================================================="
