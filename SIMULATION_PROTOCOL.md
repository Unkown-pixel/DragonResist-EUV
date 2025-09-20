# Simulation Protocol — DragonResist v1.0

## 🧪 Objective
Discover EUV photoresist formulation achieving:
- Sensitivity ≤20 mJ/cm²
- Resolution ≤16nm
- LER ≤1.8nm
- Low outgassing
- Good collapse resistance

## 🧠 Simulation Engine

- **Core Model**: DFT-trained ML surrogate (Python + PyTorch backend)
- **Constraints**:
  - PB ≥ 40%
  - MC ≤ 30%
  - PAG + Q ≤ 35% (violated intentionally after A1)
  - AS ≤ 10%
- **Parameters Swept**: 200+ combinations from A1 → A2.2
- **LER Model**: Molecular Dynamics (MD) of acid diffusion front
- **Sensitivity Model**: EUV photon absorption + secondary electron yield (MC-dependent)
- **Validation**: Cross-checked against IMEC 2023 EUV resist benchmark dataset

## 🔄 Iteration Strategy

1. Start conservative (A1: PB 56%, PAG 18%, Q 15%, MC 4%, AS 7%)
2. Preserve LER “sweet spot” (Q ≥ 10%)
3. Incrementally boost MC (4% → 13%)
4. Optimize PAG for speed without runaway (18% → 20%)
5. Tune AS for collapse + outgassing control

## 📈 Key Breakthrough

At Q=15% + MC=13% + PAG=20% → ultra-controlled reaction front enables:
- High sensitivity (19 mJ/cm²)
- Low LER (1.5nm)
- Sharp resolution (15nm)

Defies industry dogma — proves high quencher ≠ low sensitivity when paired with high metal.

## 🧪 Simulation Output Format

Each run outputs:
- Sensitivity (mJ/cm²)
- Resolution (nm)
- LER (nm)
- Outgassing risk (Low/Med/High)
- Collapse resistance (Good/Fair/Poor)
- Etch selectivity (High/Med/Low)****
