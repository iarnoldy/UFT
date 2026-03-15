#!/bin/bash
# E₈ Cloud Build Script
# Run on a fresh Ubuntu 22.04 GCP instance
# Usage: bash cloud_build.sh 2>&1 | tee cloud_build.log

set -e
echo "=== E₈ Cloud Build ==="
echo "Started: $(date)"
echo "Cores: $(nproc)"
echo "RAM: $(free -h | grep Mem | awk '{print $2}')"

# 1. Install dependencies
echo -e "\n[1/6] Installing dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq git curl gcc g++ make > /dev/null 2>&1
echo "  Done."

# 2. Install elan (Lean version manager)
echo -e "\n[2/6] Installing elan + Lean..."
curl https://elan-init.lean-lang.org/elan-init.sh -sSf | bash -s -- -y
source ~/.elan/env
lean --version
echo "  Done."

# 3. Clone the project
echo -e "\n[3/6] Cloning project..."
if [ ! -d "dollard-formal-verification" ]; then
    git clone https://github.com/iarnoldy/dollard-formal-verification.git
fi
cd dollard-formal-verification
echo "  Done."

# 4. Fetch mathlib cache (pre-built .olean files)
echo -e "\n[4/6] Fetching mathlib cache (this takes a few minutes)..."
lake update
lake exe cache get
echo "  Done."

# 5. Build with max parallelism
CORES=$(nproc)
echo -e "\n[5/6] Building with LEAN_NUM_THREADS=$CORES..."
echo "  This is the long part. Monitor with: tail -f cloud_build.log"
time LEAN_NUM_THREADS=$CORES lake build 2>&1

# 6. Verify
echo -e "\n[6/6] Verifying..."
E8_COUNT=$(ls .lake/build/lib/lean/clifford/e8_chunk_*.olean 2>/dev/null | wc -l)
echo "  E₈ chunk files built: $E8_COUNT / 31"

if [ "$E8_COUNT" -eq 31 ]; then
    echo -e "\n=== SUCCESS ==="
    echo "All 31 E₈ chunks compiled. E₈ is machine-verified."
else
    echo -e "\n=== INCOMPLETE ==="
    echo "Only $E8_COUNT / 31 chunks built. Check errors above."
fi

echo "Finished: $(date)"
