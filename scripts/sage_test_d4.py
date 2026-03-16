# Test structure constant extraction with D4 (28-dimensional)
# Run via: python scripts/sagecell_client.py scripts/sage_test_d4.py

L = LieAlgebra(QQ, cartan_type=['D', 4])
B = list(L.basis())
keys = list(L.basis().keys())
print("dim:", len(B))
print("keys_sample:", [str(k) for k in keys[:6]])

# Compute ALL structure constants
import json
sc = {}
for i in range(len(B)):
    for j in range(i+1, len(B)):
        br = L.bracket(B[i], B[j])
        coeffs = {}
        for k_idx, key in enumerate(keys):
            c = br.coefficient(key)
            if c != 0:
                coeffs[str(k_idx)] = int(c)
        if coeffs:
            sc[str(i) + "," + str(j)] = coeffs

print("nonzero_pairs:", len(sc))
print("JSON_START")
print(json.dumps(sc))
print("JSON_END")
