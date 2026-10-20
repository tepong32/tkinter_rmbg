# Versioned release packages

Keep each shipped app version in its own directory, with separate documentation for each dependency/backend variant:

```text
releases/
  v{app-version}/
    windows-x64-cpu/
      README.md
      requirements-lock-*.txt
      THIRD_PARTY_NOTICES.md
      LICENSES/
      SHA256SUMS.txt
```

Use `packaging/PACKAGE_README_TEMPLATE.md` to create the package README. Every package must include its own README, the exact dependency lock used to build it, third-party notices and license texts, and an artifact checksum. Record the executable filename, build date, source commit, platform, backend, model download or bundle behavior, known limitations, and the actual package checksum. Do not overwrite documentation for an older version when publishing a new release.

Create one package variant per dependency/backend combination that is actually supported. The current profile is Windows x64 with the CPU ONNX Runtime backend. A future GPU package must have its own lock file and its own release documentation.
