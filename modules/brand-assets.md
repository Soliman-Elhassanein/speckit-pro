# Module: Brand assets and derived visuals

- **Part of:** [Spec Kit Universal Adoption and Execution Profile](../speckit-universal-profile.md)
- **Apply when:** the project has shared identity assets (logo, pattern, motif) used on more than one surface. Do not invent a brand requirement for a product without one; record this module N/A with the reason.

The core profile still governs: reuse follows its section 3.6 and rendered evidence follows sections 3.3 and 6–7. Every dimension, opacity, color, and legibility threshold comes from the target's approved design and its own rendered evidence.

1. Identify the editable canonical source, shipped vector/export, and each derived raster/native representation. Define reproducible export commands, dimensions, tool versions, transparency, and ownership. Regenerate derived files when the canonical export changes; do not independently hand-edit them.
2. Preserve approved geometry, motif, stroke/outline structure, and seamless edge continuity where those are identity constraints. Color and opacity may vary only within approved tokens.
3. Share assets/theme tokens across official client and operator surfaces where required. Centralize reusable tiling/tint components rather than duplicating styling logic.
4. Verify alpha masking/tint behavior, vector rendering, light/dark variants, fallback colors, transparency, seams, scale, and accessibility on actual supported renderers. Do not assume embedding styles cross isolated asset boundaries; test the chosen delivery mode.
5. Record surface-specific colors, opacity, tile size, units, and reading constraints in a design-token/surface table. Keep decoration faint enough for readability and large enough for its geometry to remain legible.
6. Validate regenerated exports and affected surfaces in the same coherent unit. Preserve editable provenance and explain intentional format differences.
