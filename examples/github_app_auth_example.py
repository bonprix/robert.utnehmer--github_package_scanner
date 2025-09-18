#!/usr/bin/env python3
"""
Example: Using GitHub App Authentication with the GitHub IOC Scanner

This example demonstrates how to configure and use GitHub App authentication
instead of personal access tokens for enterprise environments.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path

# Add the src directory to the path so we can import the scanner
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from github_ioc_scanner.github_app_auth import GitHubAppAuth, create_github_app_auth


def create_example_config():
    """Create an example GitHub App configuration file."""
    
    config = {
        'auth': {
            'environment': 'production',
            'providers': {
                'github': {
                    'production': {
                        'appId': 234923,  # Your GitHub App ID
                        'clientId': 'Iv1.dd79d13de9c49d2e',  # Your GitHub App Client ID
                        'clientSecret': '4acd05d...',  # Your GitHub App Client Secret
                        'privateKey': '''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890abcdef...
... (Your GitHub App Private Key) ...
-----END RSA PRIVATE KEY-----'''
                    }
                }
            }
        }
    }
    
    return config


def example_github_app_setup():
    """Example of setting up GitHub App authentication."""
    
    print("🔧 GitHub App Authentication Setup Example")
    print("=" * 50)
    
    # Step 1: Create example configuration
    config = create_example_config()
    
    # Write to temporary file for demonstration
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config, f, default_flow_style=False)
        config_path = f.name
    
    print(f"📝 Example configuration created at: {config_path}")
    print("\n📋 Configuration structure:")
    print(yaml.dump(config, default_flow_style=False))
    
    try:
        # Step 2: Test GitHub App authentication (will fail with example data)
        print("\n🧪 Testing GitHub App authentication...")
        
        try:
            github_app_auth = GitHubAppAuth(config_path)
            print("✅ GitHub App configuration loaded successfully")
            
            # This would fail with example data, but shows the process
            # token = github_app_auth.get_token('your-org')
            # print(f"✅ Got installation token: {token[:10]}...")
            
        except Exception as e:
            print(f"⚠️  Authentication test failed (expected with example data): {e}")
        
        # Step 3: Show how to use with CLI
        print("\n🚀 Usage with CLI:")
        print(f"   python3 -m src.github_ioc_scanner.cli \\")
        print(f"     --org your-organization \\")
        print(f"     --github-app-config {config_path} \\")
        print(f"     --enable-sbom")
        
        print("\n📊 Benefits of GitHub App Authentication:")
        print("  • Higher rate limits (5000 requests/hour per installation)")
        print("  • Fine-grained permissions")
        print("  • Automatic token refresh")
        print("  • Enterprise-friendly")
        print("  • Audit trail")
        
    finally:
        # Clean up
        os.unlink(config_path)


def example_github_app_permissions():
    """Show required GitHub App permissions."""
    
    print("\n🔐 Required GitHub App Permissions")
    print("=" * 40)
    
    permissions = {
        "Repository permissions": [
            "Contents: Read (to access repository files)",
            "Metadata: Read (to access repository information)",
            "Pull requests: Read (if scanning PR-related content)"
        ],
        "Organization permissions": [
            "Members: Read (to discover teams)",
            "Administration: Read (to list repositories)"
        ]
    }
    
    for category, perms in permissions.items():
        print(f"\n📋 {category}:")
        for perm in perms:
            print(f"  • {perm}")


def example_github_app_creation():
    """Show how to create a GitHub App."""
    
    print("\n🏗️  Creating a GitHub App")
    print("=" * 30)
    
    steps = [
        "1. Go to GitHub Settings > Developer settings > GitHub Apps",
        "2. Click 'New GitHub App'",
        "3. Fill in basic information:",
        "   - App name: 'Your Organization IOC Scanner'",
        "   - Homepage URL: Your organization's security page",
        "   - Webhook URL: Not required for this use case",
        "4. Set permissions (see permissions example above)",
        "5. Generate and download private key",
        "6. Install the app in your organization",
        "7. Note the App ID, Client ID, and Client Secret"
    ]
    
    for step in steps:
        print(f"  {step}")
    
    print(f"\n📝 Configuration file location:")
    print(f"  Default: ~/github/apps.yaml")
    print(f"  Custom: Use --github-app-config flag")


def example_configuration_formats():
    """Show different configuration file formats."""
    
    print("\n📄 Configuration File Formats")
    print("=" * 35)
    
    # YAML format (recommended)
    yaml_config = """
# ~/github/apps.yaml
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
          -----END RSA PRIVATE KEY-----
"""
    
    print("📋 YAML Format (Recommended):")
    print(yaml_config)
    
    print("\n🔧 Environment Variables Alternative:")
    print("  export GITHUB_APP_ID=234923")
    print("  export GITHUB_APP_CLIENT_ID=Iv1.dd79d13de9c49d2e")
    print("  export GITHUB_APP_CLIENT_SECRET=your_secret")
    print("  export GITHUB_APP_PRIVATE_KEY_PATH=/path/to/private-key.pem")


def main():
    """Run all GitHub App authentication examples."""
    
    print("🔐 GitHub App Authentication Examples")
    print("=" * 60)
    
    try:
        example_github_app_setup()
        example_github_app_permissions()
        example_github_app_creation()
        example_configuration_formats()
        
        print("\n🎯 Summary")
        print("=" * 20)
        print("✅ GitHub App authentication provides:")
        print("  • Higher rate limits")
        print("  • Better security")
        print("  • Enterprise compliance")
        print("  • Automatic token management")
        
        print("\n🚀 Next Steps:")
        print("  1. Create your GitHub App")
        print("  2. Configure ~/github/apps.yaml")
        print("  3. Install app in your organization")
        print("  4. Run scanner with --github-app-config flag")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)