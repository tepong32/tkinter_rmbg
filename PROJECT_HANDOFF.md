# Rembg Studio project handoff

Updated: 2026-10-20

## Current baseline

- Latest source commit: `079fbe9` (`Package Rembg Studio for offline Windows use`).
- Shipped build profile: Windows x64, CPU ONNX Runtime, one-folder PyInstaller package.
- Baseline model: `u2net`, bundled and copied to the user's writable app data directory on first run.
- Versioned package documentation: `releases/v1.0.0/windows-x64-cpu/`.
- Built archive in the current workspace: `dist/RembgStudio-1.0.0-windows-x64-cpu.zip`; SHA-256 is in `dist/SHA256SUMS.txt`.
- The frozen app passed the offline first-run check using the bundled U-2-Net weights and CPU provider. It has not been checked on a separate clean PC.

The tested sample files were provided outside the repository at:

- `C:/Users/TEMP.MARIZ/Desktop/reference.jpg`
- `C:/Users/TEMP.MARIZ/Desktop/wanted_result.png`
- `C:/Users/TEMP.MARIZ/Desktop/result.png`

They may not be available in a later workspace. Ask the user to reattach them if a side-by-side model comparison is needed.

## Saved model recommendation

The current `u2net` output retained large, semi-transparent parts of the scenery around the foreground hand and along the lower edge. The PNG dimensions and alpha channel were correct; the issue was mask quality rather than output saving.

For the supplied anime illustration/photo composite:

1. Compare **`isnet-anime`** first. rembg describes it as a high-accuracy anime-character segmentation model. The image also contains a photorealistic hand that the target keeps, so check that the model preserves the hand and does not only isolate the anime character.
2. Compare **`birefnet-general-lite`** as the general-purpose candidate for the app. The current rembg installation exposes this model. Prefer it as the app's default only if it improves results on a varied sample set without an unacceptable package-size or speed cost.
3. Keep **`u2net`** as a selectable fallback until comparisons support retiring it.

Official model and behavior references:

- [rembg model list and model-specific license reminder](https://github.com/danielgatis/rembg/blob/main/README.md)
- [rembg removal, alpha matting, and decontamination options](https://github.com/danielgatis/rembg/blob/main/rembg/bg.py)

Do not assume a model's weights share rembg's software license. Before redistributing another model, record its canonical source, exact weight checksum, license/provenance, and required notices. Avoid bundling `bria-rmbg` by default without reviewing its substantially larger download and its model-specific commercial terms.

## Next-run work plan

1. Reattach the three sample images if they are not present in the workspace.
2. Run `isnet-anime`, `birefnet-general-lite`, and `u2net` against the same inputs and save comparison outputs separately. Do not overwrite the shipped v1.0.0 package.
3. Compare the full-resolution outputs on both light and dark checkerboards. Review the alpha mask as well as the composite: background leakage, preserved hand, hair/line detail, edge halos, and lost foreground regions.
4. Record each model's actual download size, packaged size, CPU processing time, model checksum, and license. Select a general default from those results; keep model selection available if the results differ by image type.
5. If a model is selected, generalize `app_model.py` so each supported model has its own bundled resource, filename, checksum, writable cache path, and clear integrity error. Update `remove_bg_with_python.py` to select and initialize the chosen session rather than hard-coding `u2net`.
6. Update the versioned package README, dependency/model notices, license texts, packaging spec, lock/manifest as needed, version metadata, and checksum sidecar. Keep the v1.0.0 docs and archive intact; give the new package a new version.
7. Verify the built package works on first run offline for every bundled model, then process the supplied sample and representative non-anime images. Document the exact verification scope and any remaining limits.

## Auto-assessment direction

Automatic checks can flag suspicious outputs using mask coverage, fragmented regions, weak or noisy edges, and inconsistent results between two models. These are review signals, not proof that the cutout is correct: without a reference mask or user correction, an offline app cannot reliably know which ambiguous regions should be foreground. A practical follow-up is an automatic first pass with a visible confidence/review flag and a simple manual mask correction or model retry.

