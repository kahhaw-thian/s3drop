#!/usr/bin/env python3
"""
S3Drop Examples - Using S3Drop programmatically.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def drop_and_share_simple(drop_zone, file_path):
    """
    Simple example: Drop a file and get a share link.
    
    Args:
        drop_zone (str): Your S3Drop zone name
        file_path (str): Path to the file to drop
    
    Returns:
        str: Share URL or None if failed
    """
    command = f"python3 s3drop.py {drop_zone} drop '{file_path}' --share"
    success, stdout, stderr = run_command(command)
    
    if success:
        # Extract URL from output (this is a simple example)
        lines = stdout.split('\n')
        for line in lines:
            if line.startswith('https://'):
                return line.strip()
    else:
        print(f"Error: {stderr}")
    
    return None


def drop_with_expiration(drop_zone, file_path, expires='48h'):
    """
    Example: Drop a file with custom expiration time.
    
    Args:
        drop_zone (str): Your S3Drop zone name
        file_path (str): Path to the file to drop
        expires (str): Expiration time (e.g., '48h', '2d')
    
    Returns:
        str: Share URL or None if failed
    """
    command = f"python3 s3drop.py {drop_zone} drop '{file_path}' --share --expires {expires}"
    success, stdout, stderr = run_command(command)
    
    if success:
        lines = stdout.split('\n')
        for line in lines:
            if line.startswith('https://'):
                return line.strip()
    else:
        print(f"Error: {stderr}")
    
    return None

def drop_with_short_url(drop_zone, file_path, service='tinyurl'):
    """
    Example: Drop a file and get a shortened share URL.
    
    Args:
        drop_zone (str): Your S3Drop zone name
        file_path (str): Path to the file to drop
        service (str): URL shortening service ('tinyurl', 'isgd', 'vgd', '1ptco')
    
    Returns:
        str: Shortened share URL or None if failed
    """
    command = f"python3 s3drop.py {drop_zone} drop '{file_path}' --share --short --short-service {service}"
    success, stdout, stderr = run_command(command)
    
    if success:
        lines = stdout.split('\n')
        for line in lines:
            if line.startswith('https://'):
                return line.strip()
    else:
        print(f"Error: {stderr}")
    
    return None


def get_share_link(drop_zone, s3_key, expires='24h'):
    """
    Example: Generate share link for existing file.
    
    Args:
        drop_zone (str): Your S3Drop zone name
        s3_key (str): S3 object key (filename in drop zone)
        expires (str): Expiration time (e.g., '24h', '2d')
    
    Returns:
        str: Share URL or None if failed
    """
    command = f"python3 s3drop.py {drop_zone} share '{s3_key}' --expires {expires}"
    success, stdout, stderr = run_command(command)
    
    if success:
        lines = stdout.split('\n')
        for line in lines:
            if line.startswith('https://'):
                return line.strip()
    else:
        print(f"Error: {stderr}")
    
    return None


def list_drop_zone_files(drop_zone):
    """
    Example: List all files in the drop zone.
    
    Args:
        drop_zone (str): Your S3Drop zone name
    
    Returns:
        list: List of file names or empty list if failed
    """
    command = f"python3 s3drop.py {drop_zone} list"
    success, stdout, stderr = run_command(command)
    
    if success:
        files = []
        lines = stdout.split('\n')
        for line in lines:
            if line.strip().startswith('📄'):
                # Extract filename from the formatted output
                filename = line.split('📄')[1].strip().split()[0]
                files.append(filename)
        return files
    else:
        print(f"Error: {stderr}")
    
    return []


def batch_drop_files(drop_zone, file_paths, expires='24h'):
    """
    Example: Drop multiple files at once.
    
    Args:
        drop_zone (str): Your S3Drop zone name
        file_paths (list): List of file paths to drop
        expires (str): Expiration time for share links
    
    Returns:
        dict: Dictionary mapping file paths to share URLs
    """
    results = {}
    
    for file_path in file_paths:
        print(f"Dropping: {file_path}")
        url = drop_with_expiration(drop_zone, file_path, expires)
        results[file_path] = url
        
        if url:
            print(f"✅ Success: {Path(file_path).name}")
        else:
            print(f"❌ Failed: {Path(file_path).name}")
    
    return results


def main():
    """Example usage of the functions above."""
    # Configuration
    DROP_ZONE = "my-secure-drops"  # Replace with your drop zone name
    
    print("🚀 S3Drop - Examples")
    print("=" * 50)
    
    # Example 1: Drop and share a single file
    print("\n📤 Example 1: Drop and share a single file")
    test_file = "example.txt"
    
    # Create a test file if it doesn't exist
    if not Path(test_file).exists():
        with open(test_file, 'w') as f:
            f.write("This is a test file for S3Drop.")
        print(f"Created test file: {test_file}")
    
    url = drop_and_share_simple(DROP_ZONE, test_file)
    if url:
        print(f"✅ Share URL: {url}")
    else:
        print("❌ Failed to generate share URL")
    
    # Example 2: Drop with custom expiration
    print("\n⏰ Example 2: Drop with 48-hour expiration")
    url = drop_with_expiration(DROP_ZONE, test_file, '48h')
    if url:
        print(f"✅ 48-hour URL: {url}")
    
    # Example 2.5: Drop with shortened URL
    print("\n🔗 Example 2.5: Drop with shortened URL")
    short_url = drop_with_short_url(DROP_ZONE, test_file, 'tinyurl')
    if short_url:
        print(f"✅ Shortened URL: {short_url}")
    else:
        print("❌ Failed to create shortened URL")
    
    # Example 3: Generate share link for existing file
    print("\n🔗 Example 3: Generate share link for existing file")
    url = get_share_link(DROP_ZONE, "example.txt", '12h')
    if url:
        print(f"✅ 12-hour URL: {url}")
    
    # Example 4: List files
    print("\n📁 Example 4: List drop zone files")
    files = list_drop_zone_files(DROP_ZONE)
    if files:
        print("Files in drop zone:")
        for file in files:
            print(f"  - {file}")
    else:
        print("No files found or error occurred")
    
    # Example 5: Batch dropping
    print("\n📦 Example 5: Batch file dropping")
    test_files = ["example.txt"]  # Add more files as needed
    results = batch_drop_files(DROP_ZONE, test_files, '24h')
    
    print("\nBatch dropping results:")
    for file_path, url in results.items():
        status = "✅" if url else "❌"
        print(f"{status} {Path(file_path).name}: {url or 'Failed'}")
    
    # Clean up test file
    if Path(test_file).exists():
        Path(test_file).unlink()
        print(f"\nCleaned up test file: {test_file}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Allow passing drop zone name as argument
        DROP_ZONE = sys.argv[1]
    
    main()