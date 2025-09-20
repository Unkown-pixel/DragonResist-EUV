Fab Integration Guide — DragonResist v1.0

## 🧪 Spin-Coating
- **Solid Content**: 12 wt% in PGMEA
- **Spin Speed**: 1500 rpm, 60 sec → 65nm film (simulated)
- **Soft Bake**: 100°C, 60 sec (hotplate)

## ☀️ EUV Exposure
- **Dose**: 19 mJ/cm² (calibrated at 13.5nm)
- **Tool**: ASML NXE:3400B or SMEE prototype
- **Focus**: ±50nm (simulated DOF)

## 🧴 Development
- **Developer**: 0.26N TMAH (tetramethylammonium hydroxide)
- **Time**: 30 sec, 23°C
- **Rinse**: DI water, 30 sec

## 🔥 Post-Exposure Bake (PEB)
- **Temp**: 110°C, 60 sec → critical for acid diffusion control

## ⚙️ Etch Transfer
- **Etch Chemistry**: CF₄/O₂ plasma (50:10 sccm)
- **Selectivity**: Resist:Si = 1:3.2 (simulated)
- **Profile**: Vertical (89.5° ± 0.5°)

## 📉 Defect Density (Simulated)
- < 0.05 defects/cm² (for 15nm L/S patterns)
- Main defect type: micro-bridging (fixable with 0.1% surfactant tweak)
