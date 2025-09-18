# GitHub App Authentication

The GitHub IOC Scanner supports GitHub App authentication as an alternative to personal access tokens. This provides better security, higher rate limits, and enterprise-friendly authentication for organizations.

## Benefits of GitHub App Authentication

- **Higher Rate Limits**: 5,000 requests per hour per installation (vs 5,000 per hour for personal tokens)
- **Fine-grained Permissions**: Only request the permissions your app actually needs
- **Automatic Token Refresh**: Tokens are automatically refreshed when they expire
- **Enterprise-friendly**: Better audit trail and centralized management
- **Organization-scoped**: Tokens are scoped to specific organizations
- **No Personal Dependencies**: Not tied to individual user accounts

## Setting Up GitHub App Authentication

### Step 1: Create a GitHub App

1. Go to GitHub Settings → Developer settings → GitHub Apps
2. Click "New GitHub App"
3. Fill in the basic information:
   - **App name**: "Your Organization IOC Scanner"
   - **Homepage URL**: Your organization's security documentation page
   - **Webhook URL**: Not required for this use case (leave blank)
   - **Webhook secret**: Not required (leave blank)

### Step 2: Configure Permissions

Set the following permissions for your GitHub App:

#### Repository Permissions
- **Contents**: Read (to access repository files and lockfiles)
- **Metadata**: Read (to access repository information)
- **Pull requests**: Read (optional, if scanning PR-related content)

#### Organization Permissions
- **Members**: Read (to discover teams and team memberships)
- **Administration**: Read (to list organization repositories)

### Step 3: Generate and Download Private Key

1. In your GitHub App settings, scroll to "Private keys"
2. Click "Generate a private key"
3. Download the `.pem` file and store it securely

### Step 4: Install the App in Your Organization

1. Go to your GitHub App settings
2. Click "Install App" in the left sidebar
3. Select your organization
4. Choose "All repositories" or select specific repositories
5. Complete the installation

### Step 5: Note Important Information

After creating and installing your app, note these values:
- **App ID**: Found in the app settings (e.g., 234923)
- **Client ID**: Found in the app settings (e.g., Iv1.dd79d13de9c49d2e)
- **Client Secret**: Generate this in the app settings
- **Private Key**: The `.pem` file you downloaded

## Configuration

### Configuration File Format

Create a YAML configuration file (recommended location: `~/github/apps.yaml`):

```yaml
auth:
  environment: production
  providers:
    github:
      production:
        appId: 234923
        clientId: Iv1.dd79d13de9c49d2e
        clientSecret: your_client_secret_here
        privateKey: |
          -----BEGIN RSA PRIVATE KEY-----
          MIIEpAIBAAKCAQEA...
          ... (your private key content) ...
          -----END RSA PRIVATE KEY-----
```

### Alternative Configuration Locations

The scanner will look for configuration files in these locations (in order):
1. `~/github/apps.yaml`
2. `~/.github/apps.yaml`
3. `./github-apps.yaml`
4. `./apps.yaml`

You can also specify a custom location using the `--github-app-config` flag.

## Usage

### Basic Usage

```bash
# Use GitHub App authentication with default config location
python3 -m github_ioc_scanner.cli --org your-organization

# Specify custom config location
python3 -m github_ioc_scanner.cli \
  --org your-organization \
  --github-app-config /path/to/your/config.yaml
```

### Team-First Organization Scan with GitHub App

```bash
python3 -m github_ioc_scanner.cli \
  --org your-organization \
  --team-first-org \
  --github-app-config ~/github/apps.yaml \
  --enable-sbom
```

### Fallback Behavior

If GitHub App authentication fails or is not configured, the scanner will automatically fall back to:
1. `GITHUB_TOKEN` environment variable
2. `gh auth token` command output

## Security Best Practices

### Private Key Security
- Store private keys securely (never commit to version control)
- Use appropriate file permissions (600 or 400)
- Consider using secret management systems in production

### Configuration File Security
```bash
# Set secure permissions on config file
chmod 600 ~/github/apps.yaml
```

### Principle of Least Privilege
- Only grant the minimum permissions required
- Regularly review and audit app permissions
- Consider using separate apps for different use cases

## Troubleshooting

### Common Issues

#### "GitHub App authentication requires 'pyjwt' and 'cryptography' packages"
```bash
pip install pyjwt cryptography
```

#### "No GitHub App installation found for organization"
- Ensure the GitHub App is installed in the target organization
- Check that the organization name is correct
- Verify the app has the required permissions

#### "GitHub App JWT token is invalid"
- Check that the private key is correctly formatted
- Verify the App ID is correct
- Ensure the private key matches the GitHub App

#### "Failed to get installation token"
- Check that the installation ID is correct
- Verify the app is properly installed in the organization
- Ensure the app has the required permissions

### Debug Mode

Enable verbose logging to troubleshoot authentication issues:

```bash
python3 -m github_ioc_scanner.cli \
  --org your-organization \
  --github-app-config ~/github/apps.yaml \
  --verbose
```

### Testing Configuration

Test your GitHub App configuration:

```bash
python3 examples/github_app_auth_example.py
```

## Rate Limits

GitHub Apps have different rate limits compared to personal access tokens:

| Authentication Method | Rate Limit | Scope |
|----------------------|------------|-------|
| Personal Access Token | 5,000/hour | Per user |
| GitHub App | 5,000/hour | Per installation |

For organizations with multiple teams or heavy usage, GitHub Apps can provide better rate limit distribution.

## Migration from Personal Access Tokens

To migrate from personal access tokens to GitHub App authentication:

1. Create and configure your GitHub App (steps above)
2. Test the configuration with a small scan
3. Update your CI/CD pipelines to use `--github-app-config`
4. Remove or rotate personal access tokens

## Enterprise Considerations

### Audit and Compliance
- GitHub Apps provide better audit trails
- Installation events are logged in organization audit logs
- Token usage is tracked per installation

### Centralized Management
- Organization owners can manage app installations
- Permissions can be reviewed and updated centrally
- Apps can be suspended or uninstalled organization-wide

### Integration with Enterprise Systems
- GitHub Apps work with GitHub Enterprise Server
- Can be integrated with enterprise identity providers
- Supports organization-level security policies

## Examples

See the `examples/github_app_auth_example.py` file for comprehensive examples of:
- Configuration file formats
- Permission requirements
- Usage patterns
- Troubleshooting steps

## Support

For issues with GitHub App authentication:
1. Check the troubleshooting section above
2. Enable verbose logging for detailed error messages
3. Verify your GitHub App configuration and permissions
4. Test with the provided example scripts