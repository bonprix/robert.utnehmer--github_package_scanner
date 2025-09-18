# Troubleshooting Guide

This guide covers common issues and their solutions when using the GitHub IOC Scanner.

## Authentication Issues

### Error: "Authentication failed"

**Problem**: The tool cannot authenticate with GitHub API.

**Solutions**:

1. **Check GitHub Token**:
   ```bash
   # Verify token is set
   echo $GITHUB_TOKEN
   
   # Test token validity
   curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
   ```

2. **Set Token Correctly**:
   ```bash
   # Export token in current session
   export GITHUB_TOKEN="your_token_here"
   
   # Add to shell profile for persistence
   echo 'export GITHUB_TOKEN="your_token_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Use GitHub CLI**:
   ```bash
   # Install and authenticate with gh CLI
   gh auth login
   
   # Verify authentication
   gh auth token
   ```

4. **Token Permissions**: Ensure your token has these scopes:
   - `repo` (for private repositories)
   - `read:org` (for organization access)
   - `read:team` (for team access)

### Error: "Insufficient permissions for organization"

**Problem**: Token doesn't have access to the specified organization.

**Solutions**:
- Ensure you're a member of the organization
- For private organizations, ensure your token has `read:org` scope
- Contact organization admin to verify access permissions

## Rate Limiting Issues

### Error: "Rate limit exceeded"

**Problem**: GitHub API rate limits have been hit.

**Solutions**:

1. **Wait for Reset**: The tool automatically handles rate limits, but you can check status:
   ```bash
   curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit
   ```

2. **Use Authenticated Requests**: Authenticated requests have higher limits (5000/hour vs 60/hour)

3. **Enable Caching**: Ensure cache is working to minimize API calls:
   ```bash
   # Check cache location
   ls -la ~/.cache/github-ioc-scan/  # Linux/macOS
   ls -la %LOCALAPPDATA%\github-ioc-scan\  # Windows
   ```

## IOC Definition Issues

### Error: "No IOC files found in issues/ directory"

**Problem**: The `issues/` directory is missing or empty.

**Solutions**:

1. **Create Issues Directory**:
   ```bash
   mkdir issues
   ```

2. **Add IOC Files**: Create at least one Python file with IOC definitions:
   ```python
   # issues/my_iocs.py
   IOC_PACKAGES = {
       "malicious-package": ["1.0.0"],
   }
   ```

3. **Check File Format**: Ensure files are valid Python with `IOC_PACKAGES` dictionary

### Error: "Malformed IOC file"

**Problem**: IOC definition file has syntax errors.

**Solutions**:

1. **Validate Python Syntax**:
   ```bash
   python -m py_compile issues/your_file.py
   ```

2. **Check IOC Format**:
   ```python
   # Correct format
   IOC_PACKAGES = {
       "package-name": ["1.0.0", "1.0.1"],  # List of versions
       "any-version-bad": None,              # Any version
   }
   
   # Incorrect formats to avoid
   IOC_PACKAGES = {
       "package-name": "1.0.0",  # Should be list, not string
       "package-name": {},       # Should be list or None
   }
   ```

## Repository Access Issues

### Error: "Repository not found"

**Problem**: Specified repository doesn't exist or isn't accessible.

**Solutions**:

1. **Check Repository Name**: Ensure correct spelling and case
2. **Verify Access**: Ensure you have read access to the repository
3. **Check Organization**: Verify organization name is correct

### Error: "Team not found"

**Problem**: Specified team doesn't exist in the organization.

**Solutions**:

1. **List Available Teams**:
   ```bash
   # Use GitHub CLI to list teams
   gh api orgs/YOUR_ORG/teams
   ```

2. **Check Team Membership**: Ensure you're a member of the team
3. **Verify Team Name**: Team names are case-sensitive

## Scanning Issues

### No Results When Expected

**Problem**: Scanner doesn't find IOCs that should be present.

**Debugging Steps**:

1. **Check File Detection**:
   - Verify the repository contains supported package files
   - Check if files are in expected locations

2. **Verify IOC Definitions**:
   - Ensure package names match exactly (case-sensitive)
   - Check version format matches what's in lockfiles

3. **Test with Known IOC**:
   ```python
   # Add a test IOC for a package you know exists
   IOC_PACKAGES = {
       "known-package-in-repo": None,
   }
   ```

### Slow Performance

**Problem**: Scans are taking too long.

**Solutions**:

1. **Use Fast Mode**:
   ```bash
   github-ioc-scan --org myorg --fast
   ```

2. **Check Cache Status**: Ensure caching is working
3. **Limit Scope**: Scan specific repositories instead of entire organization
4. **Network Issues**: Check internet connection and GitHub API status

## Cache Issues

### Cache Not Working

**Problem**: Repeated scans are still slow.

**Debugging Steps**:

1. **Check Cache Directory**:
   ```bash
   # Linux/macOS
   ls -la ~/.cache/github-ioc-scan/
   
   # Windows
   dir %LOCALAPPDATA%\github-ioc-scan\
   ```

2. **Verify Cache Permissions**: Ensure write access to cache directory

3. **Clear Cache** (if corrupted):
   ```bash
   # Linux/macOS
   rm -rf ~/.cache/github-ioc-scan/
   
   # Windows
   rmdir /s %LOCALAPPDATA%\github-ioc-scan\
   ```

### Cache Size Issues

**Problem**: Cache is consuming too much disk space.

**Solutions**:

1. **Check Cache Size**:
   ```bash
   # Linux/macOS
   du -sh ~/.cache/github-ioc-scan/
   
   # Windows
   dir %LOCALAPPDATA%\github-ioc-scan\ /s
   ```

2. **Clear Old Cache**: The tool automatically manages cache, but you can manually clear if needed

## Installation Issues

### Import Errors

**Problem**: `ModuleNotFoundError` when running the tool.

**Solutions**:

1. **Reinstall Package**:
   ```bash
   pip uninstall github-ioc-scanner
   pip install -e .
   ```

2. **Check Python Path**:
   ```bash
   python -c "import sys; print(sys.path)"
   ```

3. **Virtual Environment**: Ensure you're in the correct virtual environment

### Dependency Issues

**Problem**: Missing or incompatible dependencies.

**Solutions**:

1. **Update Dependencies**:
   ```bash
   pip install --upgrade -e .
   ```

2. **Check Requirements**:
   ```bash
   pip check
   ```

3. **Fresh Install**:
   ```bash
   pip uninstall github-ioc-scanner
   pip install -e . --force-reinstall
   ```

## Network Issues

### Connection Timeouts

**Problem**: Requests to GitHub API are timing out.

**Solutions**:

1. **Check GitHub Status**: Visit [GitHub Status](https://www.githubstatus.com/)
2. **Network Connectivity**: Test basic connectivity to GitHub:
   ```bash
   curl -I https://api.github.com
   ```
3. **Proxy Settings**: If behind a corporate proxy, configure appropriately
4. **Retry**: The tool has built-in retry logic, but manual retry may help

### SSL Certificate Issues

**Problem**: SSL certificate verification failures.

**Solutions**:

1. **Update Certificates**: Update system certificates
2. **Corporate Network**: May need to configure certificate bundle for corporate networks
3. **Temporary Workaround**: Only for testing (not recommended for production):
   ```bash
   export PYTHONHTTPSVERIFY=0
   ```

## Getting Help

If you continue to experience issues:

1. **Enable Debug Logging**: Set environment variable for verbose output:
   ```bash
   export GITHUB_IOC_SCANNER_DEBUG=1
   ```

2. **Check Logs**: Look for detailed error messages in the output

3. **Create Issue**: Report bugs with:
   - Full error message
   - Command used
   - Environment details (OS, Python version)
   - Steps to reproduce

4. **Community Support**: Check existing issues and discussions in the repository

## Common Error Messages

### "issues/ directory not found"
- **Cause**: Missing IOC definitions directory
- **Fix**: Create `issues/` directory with IOC definition files

### "No valid IOC definitions found"
- **Cause**: IOC files don't contain valid `IOC_PACKAGES` dictionary
- **Fix**: Ensure IOC files follow correct format

### "GitHub API error: 404"
- **Cause**: Repository, organization, or team not found
- **Fix**: Verify names and access permissions

### "GitHub API error: 403"
- **Cause**: Insufficient permissions or rate limit exceeded
- **Fix**: Check token permissions and wait for rate limit reset

### "Cache database locked"
- **Cause**: Another instance is running or previous instance crashed
- **Fix**: Wait for other instance to complete or restart system