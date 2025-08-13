#!/usr/bin/env python3
"""
S3Drop Setup - Create a secure S3 bucket for file dropping.
"""

import boto3
import sys
from botocore.exceptions import ClientError, NoCredentialsError


def create_drop_zone(bucket_name, region='us-east-1'):
    """
    Create a secure S3 bucket (drop zone) with proper settings.
    
    Args:
        bucket_name (str): Name for the S3 bucket
        region (str): AWS region (default: us-east-1)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        s3_client = boto3.client('s3', region_name=region)
        
        print(f"🪣 Creating S3Drop zone: {bucket_name}")
        print(f"📍 Region: {region}")
        
        # Create bucket
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        
        # Block all public access (security best practice)
        print("🔒 Securing your drop zone...")
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        
        # Enable versioning (recommended)
        print("📝 Enabling file versioning...")
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        
        print(f"✅ Drop zone '{bucket_name}' created successfully!")
        print(f"🔐 Your drop zone is private and secure")
        print(f"📍 Region: {region}")
        
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyExists':
            print(f"❌ Bucket name '{bucket_name}' is already taken globally")
            print("💡 Try a different bucket name (must be globally unique)")
            print("💡 Suggestion: add your company name or year (e.g., mycompany-drops-2024)")
        elif error_code == 'BucketAlreadyOwnedByYou':
            print(f"ℹ️ Drop zone '{bucket_name}' already exists and is owned by you")
            return True
        else:
            print(f"❌ Error creating drop zone: {e}")
        return False
    
    except NoCredentialsError:
        print("❌ AWS credentials not found.")
        print("💡 Run: aws configure")
        return False


def print_setup_banner():
    """Print S3Drop setup banner."""
    print("""
 ███████╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗ 
 ██╔════╝╚════██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
 ███████╗ █████╔╝██║  ██║██████╔╝██║   ██║██████╔╝
 ╚════██║ ╚═══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝ 
 ███████║██████╔╝██████╔╝██║  ██║╚██████╔╝██║     
 ╚══════╝╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                   
 S3Drop Setup - Create your secure drop zone
""")


def main():
    """Main setup function."""
    print_setup_banner()
    print("=" * 60)
    
    # Get bucket name from user
    print("Let's create your secure file drop zone!")
    print()
    bucket_name = input("Enter a unique drop zone name: ").strip()
    
    if not bucket_name:
        print("❌ Drop zone name cannot be empty")
        sys.exit(1)
    
    # Validate bucket name
    if not bucket_name.replace('-', '').replace('.', '').isalnum():
        print("❌ Drop zone name can only contain letters, numbers, hyphens, and periods")
        sys.exit(1)
    
    if len(bucket_name) < 3 or len(bucket_name) > 63:
        print("❌ Drop zone name must be between 3 and 63 characters")
        sys.exit(1)
    
    # Get region
    print("\nCommon AWS regions:")
    print("  us-east-1      (N. Virginia) - Default")
    print("  us-west-2      (Oregon)")
    print("  eu-west-1      (Ireland)")
    print("  ap-southeast-1 (Singapore)")
    print("  ap-southeast-2 (Sydney)")
    
    region = input("\nEnter AWS region (press Enter for us-east-1): ").strip()
    if not region:
        region = 'us-east-1'
    
    # Create drop zone
    print()
    if create_drop_zone(bucket_name, region):
        print("\n" + "=" * 60)
        print("🎉 S3Drop setup complete! Your secure drop zone is ready.")
        print()
        print("🚀 Quick Start Commands:")
        print(f"   s3drop {bucket_name} drop myfile.pdf --share")
        print(f"   s3drop {bucket_name} share existing-file.pdf")
        print(f"   s3drop {bucket_name} list")
        print()
        print("📧 Share files securely:")
        print("   1. Drop your file with --share flag")
        print("   2. Copy the generated secure link")
        print("   3. Send link to recipients via email")
        print("   4. Link expires automatically (default: 24 hours)")
        print()
        print("💡 Pro Tips:")
        print("   - Use --expires 48h for longer access")
        print("   - Use --verify to test links before sharing")
        print("   - Your drop zone is private and secure")
        print("   - Only people with share links can download files")
        print()
        print("📚 Documentation: https://github.com/kahhaw-thian/s3drop")
    else:
        print("❌ Setup failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()