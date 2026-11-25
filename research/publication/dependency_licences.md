<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Dependency licences (M6, 2026-11-25)

Collected from installed metadata on 2026-11-25: Python from `.venv` (`importlib.metadata`, `License-Expression` or `License` field, then trove classifiers), npm from every `package.json` under `demo/node_modules/` (53 packages, nested included), with the runtime or development role taken from `demo/package-lock.json`. None of these packages is committed to the repository; they are installed from `uv.lock` and `demo/package-lock.json`. Licence names are as declared by each package and were not audited against the packages' full licence texts.

Accepted set (brief M6, task 4): MIT, BSD, ISC, Apache-2.0, PSF, MPL-2.0 or similarly permissive.

## Python (locked in `uv.lock`, Python 3.12.1)

| Package | Version | Role | Declared licence | Flag |
|---|---|---|---|---|
| numpy | 2.3.4 | runtime | BSD License (classifier; licence text "Copyright (c) 2005-2025, NumPy Developers") | none; see note 1 |
| scipy | 1.16.2 | runtime | BSD License (classifier) | none; see note 1 |
| jsonschema | 4.25.1 | runtime | MIT | none |
| jsonschema-specifications | 2025.9.1 | runtime (dependency of jsonschema) | MIT | none |
| referencing | 0.37.0 | runtime (dependency of jsonschema) | MIT | none |
| rpds-py | 2026.9.1 | runtime (dependency of jsonschema) | MIT | none |
| attrs | 26.1.0 | runtime (dependency of jsonschema) | MIT | none |
| typing_extensions | 4.16.0 | runtime (dependency of referencing) | PSF-2.0 | none |
| pytest | 8.4.2 | development | MIT | none |
| pluggy | 1.7.0 | development | MIT | none |
| iniconfig | 2.3.1 | development | MIT | none |
| packaging | 26.3 | development | Apache-2.0 OR BSD-2-Clause | none |
| Pygments | 2.21.0 | development | BSD-2-Clause | none |

Note 1. The numpy and scipy binary wheels bundle compiled libraries (for example OpenBLAS, and for scipy a Fortran runtime) whose own licence files ship inside the wheels. They were not reviewed here; the source code of this repository does not redistribute them.

## npm (demo, locked in `demo/package-lock.json`)

Runtime (shipped in the built page): react 19.3.1 (MIT), react-dom 19.3.1 (MIT), scheduler 0.28.0 (MIT). No flag.

Development and build only (not shipped):

| Licence | Packages |
|---|---|
| MIT | @jridgewell/sourcemap-codec 1.6.0, @oxc-project/types 0.156.0, @rolldown/binding-darwin-arm64 1.2.19, @rolldown/pluginutils 1.1.1, @standard-schema/spec 1.1.0, @types/chai 5.2.3, @types/deep-eql 4.0.2, @types/estree 1.0.11, @types/react 19.3.0, @types/react-dom 19.3.0, @vitejs/plugin-react 6.1.2, @vitest/expect 4.1.12, @vitest/mocker 4.1.12, @vitest/pretty-format 4.1.12, @vitest/runner 4.1.12, @vitest/snapshot 4.1.12, @vitest/spy 4.1.12, @vitest/utils 4.1.12, assertion-error 2.0.1, chai 6.3.0, convert-source-map 2.0.0, csstype 3.2.4, es-module-lexer 2.3.2, estree-walker 3.0.3, fdir 6.5.0, fsevents 2.3.3, magic-string 0.30.21, nanoid 3.3.20, obug 2.2.1, pathe 2.0.3, picomatch 4.0.7, postcss 8.5.33, rolldown 1.2.19, stackback 0.0.2, std-env 4.3.0, tinybench 2.9.0, tinyexec 1.4.0, tinyglobby 0.2.17, tinyrainbow 3.2.0, vite 8.3.5, vitest 4.1.12, why-is-node-running 2.3.0 |
| Apache-2.0 | detect-libc 2.1.2, expect-type 1.4.0, typescript 5.9.3 |
| ISC | picocolors 1.1.1, siginfo 2.0.0 |
| BSD-3-Clause | source-map-js 1.2.4 |
| MPL-2.0 | lightningcss 1.33.0, lightningcss-darwin-arm64 1.33.0 |

No flag. MPL-2.0 is in the accepted set; lightningcss is a build tool and none of its files are shipped.

## Build tools outside the repository (not installed by the repository, not redistributed)

| Tool | Version | Declared licence | Flag |
|---|---|---|---|
| typst (Python package) | 0.15.0 | Apache-2.0 | none |
| pypdf | 6.20.0 | BSD-3-Clause | none |
| pillow | 11.3.0 | MIT-CMU | none |
| pandoc | 3.6.3 | GPL-2.0-or-later (from general knowledge of the project; not read from the binary) | **flag**: copyleft, outside the accepted set. Used only as a command-line converter; its output (the PDFs and `manuscript.tex`) is not a derivative of pandoc, and pandoc is not redistributed. Recorded for the owner. |
| Node.js | v22.23.3 | MIT (from general knowledge; not read from the installation) | none |
| Google Chrome (used headless by `demo/tools/a11y_check.mjs`) | system installation | proprietary end-user licence (from general knowledge) | **flag**: not permissive, but only run locally as a test browser and never redistributed. Recorded for the owner. |

## Data

MovieLens 1M (GroupLens): research use, no redistribution; never committed (`data/manifest.json`, README "Data and licences"). Not a code dependency.
