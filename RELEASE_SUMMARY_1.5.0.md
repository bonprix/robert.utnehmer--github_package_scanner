# Release 1.5.0 - Repository Cleanup & Shai Hulud Attack Response

## ✅ Repository Cleanup Completed

### 📁 Documentation Organization
- **Moved to `docs/`**:
  - `BATCH_SIZE_OPTIMIZATION_SUMMARY.md`
  - `FILECONTENT_LEN_FIX_SUMMARY.md`
  - `MEMORY_LOGGING_CLEANUP_SUMMARY.md`
  - `SHAI_HULUD_EXPANSION_SUMMARY.md`
  - `RELEASE_NOTES_1.4.1.md`

### 🧹 Test Code Cleanup
- **Removed temporary test files**:
  - `test_aggressive_batch_sizing.py`
  - `test_memory_logging_levels.py`
  - `test_file_content_len_fix.py`
  - `test_final_rate_limit_validation_summary.py`
  - `test_end_to_end_rate_limit_validation.py`
  - `test_complete_rate_limit_workflow_validation.py`
  - `test_enhanced_logging_config.py`
  - `test_file_content_len_fix_simple.py`

### 🗑️ Artifact Cleanup
- Removed development log file: `github-ioc-scan.log`
- Clean root directory structure
- Organized project for better maintainability

## 🚨 Critical Security Update

### 🛡️ Shai Hulud Worm Attack Coverage
- **500+ new malicious packages** added to IOC database
- **Worm payload detection** for self-propagating malware
- **Cross-platform coverage**: Mobile, web frameworks, development tools
- **Security tool impersonation** detection

## 📦 Release Artifacts

### Built Successfully
- `github_ioc_scanner-1.5.0-py3-none-any.whl`
- `github_ioc_scanner-1.5.0.tar.gz`

### Version Update
- **Previous**: 1.4.1
- **Current**: 1.5.0

## 📚 Documentation Updates

### New Documentation
- `docs/RELEASE_NOTES_1.5.0.md` - Comprehensive release notes
- `docs/SHAI_HULUD_EXPANSION_SUMMARY.md` - Attack analysis

### Updated Documentation
- `CHANGELOG.md` - Added 1.5.0 release notes
- `pyproject.toml` - Version bump to 1.5.0

## 🚀 Ready for Release

The repository is now clean, organized, and ready for the 1.5.0 release with critical security updates for the Shai Hulud worm attack.

### Next Steps
1. **Tag the release**: `git tag v1.5.0`
2. **Push to repository**: `git push origin v1.5.0`
3. **Publish to PyPI**: `twine upload dist/*`
4. **Create GitHub release** with release notes

### Critical Security Notice
This release addresses a critical supply chain attack. Organizations should update immediately to protect against the Shai Hulud worm and its 500+ compromised npm packages.