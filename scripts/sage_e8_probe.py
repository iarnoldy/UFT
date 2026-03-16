# E8 probe: test timing and output size for structure constant extraction
# Just compute first 50 basis elements' brackets (not all 30K pairs)

import time
t0 = time.time()

L = LieAlgebra(QQ, cartan_type=['E', 8])
B = list(L.basis())
keys = list(L.basis().keys())
t1 = time.time()
print("dim:", len(B))
print("basis_time:", round(t1-t0, 2), "s")

# Compute structure constants for first 50 basis elements only
import json
sc = {}
n = min(50, len(B))
for i in range(n):
    for j in range(i+1, n):
        br = L.bracket(B[i], B[j])
        coeffs = {}
        for k_idx, key in enumerate(keys):
            c = br.coefficient(key)
            if c != 0:
                coeffs[str(k_idx)] = int(c)
        if coeffs:
            sc[str(i) + "," + str(j)] = coeffs

t2 = time.time()
print("pairs_computed:", n*(n-1)//2)
print("nonzero_pairs:", len(sc))
print("bracket_time:", round(t2-t1, 2), "s")
print("total_time:", round(t2-t0, 2), "s")

# Estimate full E8 time
full_pairs = 248*247//2
ratio = full_pairs / (n*(n-1)//2)
est = (t2-t1) * ratio
print("est_full_time:", round(est, 1), "s =", round(est/60, 1), "min")

# Show first few structure constants
print("JSON_START")
items = list(sc.items())[:10]
print(json.dumps(dict(items)))
print("JSON_END")
