META QUEST HOMES — EXTRACTION SNAPSHOT (2026-10-04)

Scope: 22 entries in Quest Home Switcher homes-v2.0.0, Root catalog. Content is attributed to Meta/Oculus by that catalog. These APKs are community-cooked ports, not verified historically original Meta APKs. Do not treat APK build dates, package versions, polygon counts or file size as historical design trends without original-build validation. This is a complete snapshot of that catalog, not proof of every official environment ever released.

Models: scene.glb is a standard glTF 2.0 static scene with baked world placement, UV0/UV1, vertex colors, PNG textures, tint, alpha mask/blend and double-sided flags. Import into Blender using File > Import > glTF 2.0. Unity requires a glTF importer. No Quest or root access is needed to open the models.

The export is STATIC. Animation clips, skeletons, VAT, shader binaries, audio banks, HSTF templates and spatial components remain in source_scene.zip / apk_assets when present. Animations are not exported to playable glTF tracks; navmesh/colliders are not converted into Unity components. Additive blending is recorded in extras, not reproduced by standard glTF. Packed normal/ORM maps need original shader-specific decoding. HDR lightmap PNGs use the extractor's exposure/tonemapping and are not raw HDR radiance. Materials are exported as unlit approximations; original shader behavior and exact lighting are not reproduced. Normals are recalculated by the importing application. Visual fidelity has not been validated in Blender, Unity or on a headset.

source_properties.json preserves extracted shader names, flags and auxiliary texture references. scene.blendmeta.json preserves per-object HSTF components. source_scene.zip preserves the exact internal scene bytes, verified against cookedSceneSha256. apk_assets preserves navigation data, editor session, strings and binary Android manifest where present. Original downloaded APKs are reproducible from the catalog URLs and SHA-256 values, and are not duplicated in the deliverable.

Validation: APK and internal scene SHA-256 checked against the published catalog; glTF image references, binary buffer/accessor bounds, triangle index ranges and GLB lengths checked. Every extractor load report is included. Skipped UI/gizmo or undecoded elements appear explicitly in the load report; export success does not mean full semantic recovery.

Metrics count exported mesh instances/material bindings, not unique authored assets or measured draw calls. Texture/image binding counts differ from deduplicated PNG file counts. Bounds include skyboxes/decorative geometry. These are technical extraction measurements, not a dated historical dataset.

Sources:
https://github.com/nikitat21/Quest-Home-Switcher/releases/tag/homes-v2.0.0
https://github.com/nikitat21/Quest-Home-Editor
https://github.com/xAstroBoy/Quest-Home-Editor (original currently unavailable)

Extractor fixes: accept a string targetId in Cyber City's shellconfig; avoid predecoding unused fallback-material textures and decode unreferenced textures on demand. No source APK or scene bytes are modified. Oceanarium and Storybook static exports cap decoded PNG texture dimensions to 1024 pixels using nearest resampling to stay within available memory; their original compressed textures remain intact in source_scene.zip. Other static exports retain decoded dimensions. Numeric string IDs are accepted throughout JSON asset-reference parsing. Mesh transformations are baked before export. Binary source assets are retained for further reconstruction.
