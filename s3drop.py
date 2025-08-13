#!/usr/bin/env python3
"""
S3Drop - Secure file sharing via AWS S3 presigned URLs
Drop files securely, share with confidence.

Author: S3Drop Contributors
License: MIT
Website: https://github.com/your-username/s3drop
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
import urllib.parse

import boto3
import requests
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError

__version__ = "1.0.0"


class S3Drop:
    """S3Drop - Secure file sharing using AWS S3 presigned URLs."""
    
    def __init__(self, bucket_name, aws_profile=None, auto_create=True):
        """
        Initialize S3Drop client.
        
        Args:
            bucket_name (str): Name of your S3 bucket
            aws_profile (str): AWS profile to use (optional)
            auto_create (bool): Automatically create bucket if it doesn't exist (default: True)
        """
        self.bucket_name = bucket_name
        self.auto_create = auto_create
        self.s3_client = self._create_s3_client(bucket_name, aws_profile)
    
    def _create_s3_client(self, bucket_name, aws_profile=None):
        """Create and configure S3 client with proper settings."""
        try:
            # Detect bucket region
            bucket_region = self._get_bucket_region(bucket_name, aws_profile)
            
            # Configure S3 client with modern signature version
            config = Config(
                signature_version='s3v4',
                s3={'addressing_style': 'virtual'}
            )
            
            if aws_profile:
                session = boto3.Session(profile_name=aws_profile)
                client = session.client('s3', region_name=bucket_region, config=config)
            else:
                client = boto3.client('s3', region_name=bucket_region, config=config)
            
            print(f"🌍 Connected to bucket in region: {bucket_region}")
            return client
            
        except NoCredentialsError:
            print("❌ AWS credentials not found.")
            print("💡 Run: aws configure")
            sys.exit(1)
    
    def _get_bucket_region(self, bucket_name, aws_profile=None):
        """Get the AWS region where the bucket is located."""
        try:
            # Create temporary client to get bucket location
            if aws_profile:
                session = boto3.Session(profile_name=aws_profile)
                temp_client = session.client('s3')
            else:
                temp_client = boto3.client('s3')
            
            response = temp_client.get_bucket_location(Bucket=bucket_name)
            region = response.get('LocationConstraint')
            
            # Handle special cases
            if region is None:
                region = 'us-east-1'  # Default region
            
            return region
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                if self.auto_create:
                    # Try to auto-create the bucket
                    return self._auto_create_bucket(bucket_name, aws_profile)
                else:
                    print(f"❌ Drop zone '{bucket_name}' does not exist")
                    print("💡 Run: s3drop setup")
                    print("💡 Or use --auto-create flag to create automatically")
                    sys.exit(1)
            else:
                print(f"⚠️ Could not determine bucket region: {e}")
                return 'us-east-1'  # Fallback
    
    def _auto_create_bucket(self, bucket_name, aws_profile=None):
        """
        Automatically create a secure S3 bucket if it doesn't exist.
        
        Args:
            bucket_name (str): Name of the bucket to create
            aws_profile (str): AWS profile to use (optional)
        
        Returns:
            str: AWS region where bucket was created
        """
        try:
            # Get current AWS region from session or use default
            if aws_profile:
                session = boto3.Session(profile_name=aws_profile)
                region = session.region_name or 'us-east-1'
                s3_client = session.client('s3', region_name=region)
            else:
                session = boto3.Session()
                region = session.region_name or 'us-east-1'
                s3_client = boto3.client('s3', region_name=region)
            
            print(f"🪣 Drop zone '{bucket_name}' not found. Creating it...")
            print(f"📍 Region: {region}")
            
            # Create bucket
            if region == 'us-east-1':
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            
            # Configure security settings
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
            
            # Enable versioning
            print("📝 Enabling file versioning...")
            s3_client.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )
            
            print(f"✅ Drop zone '{bucket_name}' created successfully!")
            print("🔐 Your drop zone is private and secure")
            
            return region
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'BucketAlreadyExists':
                print(f"❌ Drop zone name '{bucket_name}' is already taken globally")
                print("💡 Try a different name (must be globally unique)")
                print("💡 Suggestion: add your company name or year")
                print(f"💡 Example: {bucket_name}-mycompany or {bucket_name}-2024")
            elif error_code == 'AccessDenied':
                print(f"❌ Permission denied: Cannot create drop zone '{bucket_name}'")
                print("💡 Check your AWS permissions for S3 bucket creation")
                print("💡 Required permissions: s3:CreateBucket, s3:PutBucketPublicAccessBlock")
            else:
                print(f"❌ Failed to create drop zone: {e}")
            
            print(f"\n💡 Alternative: Create the drop zone manually:")
            print(f"   s3drop setup")
            sys.exit(1)
    
    def upload_file(self, local_file_path, s3_key=None):
        """
        Upload a file to S3.
        
        Args:
            local_file_path (str): Path to local file
            s3_key (str): S3 object key (optional, uses filename if not provided)
        
        Returns:
            str: S3 key of uploaded file
        """
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"File not found: {local_file_path}")
        
        if not s3_key:
            s3_key = os.path.basename(local_file_path)
        
        try:
            file_size = os.path.getsize(local_file_path) / (1024 * 1024)  # MB
            print(f"📤 Dropping {local_file_path} ({file_size:.2f} MB)")
            
            self.s3_client.upload_file(local_file_path, self.bucket_name, s3_key)
            print(f"✅ Drop successful: s3://{self.bucket_name}/{s3_key}")
            return s3_key
            
        except ClientError as e:
            print(f"❌ Drop failed: {e}")
            raise
    
    def generate_share_link(self, s3_key, expiration_hours=24):
        """
        Generate a secure share link for downloading a file.
        
        Args:
            s3_key (str): S3 object key
            expiration_hours (int): Hours until link expires (default: 24)
        
        Returns:
            tuple: (share_url, expiry_datetime)
        """
        try:
            # Verify file exists
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            
            # Generate presigned URL
            expiration_seconds = expiration_hours * 3600
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration_seconds
            )
            
            expiry_time = datetime.now() + timedelta(hours=expiration_hours)
            print(f"🔗 Generated secure share link for: {s3_key}")
            print(f"⏰ Link expires: {expiry_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            return url, expiry_time
            
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                print(f"❌ File not found: {s3_key}")
            else:
                print(f"❌ Error generating share link: {e}")
            raise
    
    def verify_share_link(self, url):
        """
        Verify that a share link is accessible.
        
        Args:
            url (str): Share URL to verify
        
        Returns:
            bool: True if accessible, False otherwise
        """
        try:
            print("🔍 Verifying share link...")
            response = requests.head(url, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                content_length = response.headers.get('content-length')
                if content_length:
                    size_mb = int(content_length) / (1024 * 1024)
                    print(f"✅ Link verified! File size: {size_mb:.2f} MB")
                else:
                    print("✅ Link verified!")
                return True
            else:
                print(f"❌ Link verification failed: HTTP {response.status_code}")
                print("💡 Note: Link may still work for recipients")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Link verification failed: {e}")
            print("💡 Note: Link may still work for recipients")
            return False
    
    def shorten_url(self, long_url, service='tinyurl'):
        """
        Shorten a URL using various free URL shortening services.
        
        Args:
            long_url (str): The long URL to shorten
            service (str): URL shortening service to use ('tinyurl', 'isgd', 'vgd', '1ptco')
        
        Returns:
            str: Shortened URL or original URL if shortening fails
        """
        try:
            print(f"🔗 Shortening URL with {service.upper()}...")
            
            if service == 'tinyurl':
                return self._shorten_with_tinyurl(long_url)
            elif service == 'isgd':
                return self._shorten_with_isgd(long_url)
            elif service == 'vgd':
                return self._shorten_with_vgd(long_url)
            elif service == '1ptco':
                return self._shorten_with_1ptco(long_url)
            else:
                print(f"⚠️ Unknown service '{service}', using original URL")
                return long_url
                
        except Exception as e:
            print(f"⚠️ URL shortening failed: {e}")
            print("💡 Using original URL")
            return long_url
    
    def _shorten_with_tinyurl(self, long_url):
        """Shorten URL using TinyURL API."""
        api_url = "http://tinyurl.com/api-create.php"
        params = {'url': long_url}
        
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        
        short_url = response.text.strip()
        if short_url.startswith('http'):
            print("✅ URL shortened successfully!")
            return short_url
        else:
            raise Exception(f"TinyURL error: {short_url}")
    
    def _shorten_with_isgd(self, long_url):
        """Shorten URL using is.gd API."""
        api_url = "https://is.gd/create.php"
        params = {
            'format': 'simple',
            'url': long_url
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        
        short_url = response.text.strip()
        if short_url.startswith('http'):
            print("✅ URL shortened successfully!")
            return short_url
        else:
            raise Exception(f"is.gd error: {short_url}")
    
    def _shorten_with_vgd(self, long_url):
        """Shorten URL using v.gd API."""
        api_url = "https://v.gd/create.php"
        params = {
            'format': 'simple',
            'url': long_url
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        
        short_url = response.text.strip()
        if short_url.startswith('http'):
            print("✅ URL shortened successfully!")
            return short_url
        else:
            raise Exception(f"v.gd error: {short_url}")
    
    def _shorten_with_1ptco(self, long_url):
        """Shorten URL using 1pt.co API."""
        api_url = "https://1pt.co/addURL"
        data = {'long': long_url}
        
        response = requests.post(api_url, data=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get('status') == 'success':
            short_url = result.get('short')
            if short_url:
                print("✅ URL shortened successfully!")
                return short_url
        
        raise Exception(f"1pt.co error: {result.get('msg', 'Unknown error')}")
    
    def list_files(self):
        """List all files in the S3 bucket."""
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            
            if 'Contents' not in response:
                print("📁 Drop zone is empty")
                return []
            
            files = []
            print(f"📁 Files in your drop zone (s3://{self.bucket_name}):")
            print("-" * 60)
            
            for obj in response['Contents']:
                size_mb = obj['Size'] / (1024 * 1024)
                modified = obj['LastModified'].strftime('%Y-%m-%d %H:%M')
                print(f"📄 {obj['Key']}")
                print(f"   Size: {size_mb:.2f} MB | Modified: {modified}")
                files.append(obj['Key'])
            
            return files
            
        except ClientError as e:
            print(f"❌ Error listing files: {e}")
            raise


def print_banner():
    """Print S3Drop banner."""
    print("""
 ███████╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗ 
 ██╔════╝╚════██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
 ███████╗ █████╔╝██║  ██║██████╔╝██║   ██║██████╔╝
 ╚════██║ ╚═══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝ 
 ███████║██████╔╝██████╔╝██║  ██║╚██████╔╝██║     
 ╚══════╝╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                   
 Secure file sharing, simplified.
""")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='S3Drop - Secure file sharing via AWS S3',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my-drops drop video.mp4 --share
  %(prog)s my-drops drop video.mp4 --share --short
  %(prog)s my-drops share video.mp4 --expires 48h --short
  %(prog)s my-drops list
  %(prog)s setup

For more help: https://github.com/kahhaw-thian/s3drop
        """
    )
    
    parser.add_argument('--version', action='version', version=f'S3Drop {__version__}')
    parser.add_argument('bucket', nargs='?', help='S3 bucket name')
    parser.add_argument('--profile', help='AWS profile to use')
    parser.add_argument('--no-auto-create', action='store_true', 
                       help='Disable automatic bucket creation')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Set up a new S3 bucket for dropping files')
    
    # Drop command (upload)
    drop_parser = subparsers.add_parser('drop', help='Drop a file into your S3 bucket')
    drop_parser.add_argument('file', help='Local file path to drop')
    drop_parser.add_argument('--key', help='Custom S3 key (optional)')
    drop_parser.add_argument('--share', action='store_true', 
                            help='Generate share link after dropping')
    drop_parser.add_argument('--expires', type=str, default='24h', 
                            help='Link expiration (e.g., 24h, 2d, 48h)')
    drop_parser.add_argument('--verify', action='store_true', 
                            help='Verify share link works')
    drop_parser.add_argument('--short', action='store_true',
                            help='Create shortened URL for easier sharing')
    drop_parser.add_argument('--short-service', choices=['tinyurl', 'isgd', 'vgd', '1ptco'],
                            default='tinyurl', help='URL shortening service (default: tinyurl)')
    
    # Share command (generate link)
    share_parser = subparsers.add_parser('share', help='Generate share link for existing file')
    share_parser.add_argument('key', help='S3 object key')
    share_parser.add_argument('--expires', type=str, default='24h', 
                             help='Link expiration (e.g., 24h, 2d, 48h)')
    share_parser.add_argument('--verify', action='store_true', 
                             help='Verify share link works')
    share_parser.add_argument('--short', action='store_true',
                             help='Create shortened URL for easier sharing')
    share_parser.add_argument('--short-service', choices=['tinyurl', 'isgd', 'vgd', '1ptco'],
                             default='tinyurl', help='URL shortening service (default: tinyurl)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List files in your drop zone')
    
    args = parser.parse_args()
    
    # Handle setup command separately
    if args.command == 'setup':
        from setup_bucket import main as setup_main
        setup_main()
        return
    
    if not args.command:
        print_banner()
        parser.print_help()
        return
    
    if not args.bucket:
        print("❌ Bucket name is required")
        print("💡 Usage: s3drop <bucket-name> <command>")
        sys.exit(1)
    
    # Parse expiration time
    def parse_expiration(expires_str):
        """Parse expiration string like '24h', '2d', '48h' into hours."""
        expires_str = expires_str.lower()
        if expires_str.endswith('h'):
            return int(expires_str[:-1])
        elif expires_str.endswith('d'):
            return int(expires_str[:-1]) * 24
        else:
            return int(expires_str)  # Assume hours
    
    # Initialize S3Drop client
    try:
        auto_create = not args.no_auto_create
        s3drop = S3Drop(args.bucket, args.profile, auto_create)
    except Exception as e:
        print(f"❌ Failed to initialize S3Drop: {e}")
        sys.exit(1)
    
    # Execute commands
    try:
        if args.command == 'drop':
            s3_key = s3drop.upload_file(args.file, args.key)
            
            if args.share:
                expires_hours = parse_expiration(args.expires)
                url, expires_at = s3drop.generate_share_link(s3_key, expires_hours)
                
                if args.verify:
                    s3drop.verify_share_link(url)
                
                # Shorten URL if requested
                final_url = url
                if args.short:
                    final_url = s3drop.shorten_url(url, args.short_service)
                
                print(f"\n🔗 Secure Share Link:")
                print(f"{final_url}")
                
                if args.short and final_url != url:
                    print(f"\n📏 Original URL length: {len(url)} characters")
                    print(f"📏 Shortened URL length: {len(final_url)} characters")
                    print(f"💾 Saved: {len(url) - len(final_url)} characters")
                
                print(f"\n📧 Share this link with your recipients!")
                print(f"⏰ Expires: {expires_at.strftime('%Y-%m-%d at %H:%M')}")
        
        elif args.command == 'share':
            expires_hours = parse_expiration(args.expires)
            url, expires_at = s3drop.generate_share_link(args.key, expires_hours)
            
            if args.verify:
                s3drop.verify_share_link(url)
            
            # Shorten URL if requested
            final_url = url
            if args.short:
                final_url = s3drop.shorten_url(url, args.short_service)
            
            print(f"\n🔗 Secure Share Link:")
            print(f"{final_url}")
            
            if args.short and final_url != url:
                print(f"\n📏 Original URL length: {len(url)} characters")
                print(f"📏 Shortened URL length: {len(final_url)} characters")
                print(f"💾 Saved: {len(url) - len(final_url)} characters")
            
            print(f"\n📧 Share this link with your recipients!")
            print(f"⏰ Expires: {expires_at.strftime('%Y-%m-%d at %H:%M')}")
        
        elif args.command == 'list':
            s3drop.list_files()
    
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Operation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()