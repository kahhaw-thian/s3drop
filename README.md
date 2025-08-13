# S3Drop

**Secure file sharing, simplified.**

S3Drop is a simple, powerful tool for securely sharing files with customers, clients, or team members using AWS S3 presigned URLs. Drop files securely, share with confidence.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)

💔 The Problem We All Face

You need to share a large file with a customer. Email bounces back - "File too large." You try Dropbox, but they don't have an account. Google Drive? Same issue. WeTransfer? Files disappear after a week, and your client downloads it too late. 


## ✨ The Solution: S3Drop - Upload file to private S3, and get a download link that you can share to anyone with configurable auto-expire download link.

- 🔐 **Secure by default** - Private S3 bucket, no public access
- ⏰ **Time-limited links** - URLs expire automatically (default: 24 hours)  
- 🎯 **Simple to use** - Drop files, get secure links instantly
- 👥 **No recipient setup** - Recipients just click the link to download
- 📊 **Audit trail** - AWS CloudTrail logs all access attempts
- 💼 **Professional** - Perfect for business file sharing

## 🚀 Quick Start

### Prerequisites

1. **AWS Account** - You need an AWS account with S3 access
2. **AWS CLI** - For credential configuration
3. **Python 3.7+** - The script requires Python 3.7 or newer

### Installation

#### 1. Install AWS CLI

**macOS:**
```bash
brew install awscli
```

**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Windows:**
Download and install from [AWS CLI official page](https://aws.amazon.com/cli/)

#### 2. Configure AWS Credentials

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region (e.g., `us-east-1`, `ap-southeast-1`)
- Output format (press Enter for default)

#### 3. Install Python Dependencies

```bash
pip install boto3 requests
```

#### 4. Download S3Drop

```bash
curl -O https://raw.githubusercontent.com/kahhaw-thian/s3drop/main/s3drop.py
chmod +x s3drop.py
```

### Setup Your Drop Zone

S3Drop can automatically create secure drop zones for you:

```bash
# Option 1: Auto-create on first use (recommended)
python3 s3drop.py my-company-drops drop file.pdf --share
# S3Drop will create the drop zone automatically if it doesn't exist

# Option 2: Interactive setup
python3 s3drop.py setup

# Option 3: Manual creation
aws s3 mb s3://my-company-drops-2024
aws s3api put-public-access-block \
    --bucket my-company-drops-2024 \
    --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

## �  Usage

### Drop and Share Files

```bash
# Drop a file and get a secure share link (auto-creates drop zone if needed)
python3 s3drop.py my-drops drop meeting-recording.mp4 --share

# Drop with shortened URL for easier sharing
python3 s3drop.py my-drops drop document.pdf --share --short

# Drop with custom expiration (48 hours)
python3 s3drop.py my-drops drop document.pdf --share --expires 48h

# Drop and verify the link works
python3 s3drop.py my-drops drop video.mp4 --share --verify

# Use different URL shortening service
python3 s3drop.py my-drops drop file.pdf --share --short --short-service isgd
```

### Generate Share Links

```bash
# Generate share link for existing file
python3 s3drop.py my-drops share existing-file.pdf

# Generate shortened share link
python3 s3drop.py my-drops share document.pdf --short

# Custom expiration time (2 days)
python3 s3drop.py my-drops share document.pdf --expires 2d --short
```

### List Your Files

```bash
# List all files in your drop zone
python3 s3drop.py my-drops list
```

### Auto-Creation of Drop Zones

S3Drop automatically creates secure drop zones when they don't exist:

```bash
# First time using a new drop zone name
python3 s3drop.py my-new-drops drop file.pdf --share

# Output:
# 🪣 Drop zone 'my-new-drops' not found. Creating it...
# 📍 Region: us-east-1
# 🔒 Securing your drop zone...
# 📝 Enabling file versioning...
# ✅ Drop zone 'my-new-drops' created successfully!
# 🔐 Your drop zone is private and secure
```

**Auto-creation features:**
- ✅ **Secure by default** - Blocks all public access
- ✅ **Versioning enabled** - File history and recovery
- ✅ **Uses your AWS region** - Optimal performance
- ✅ **Proper permissions** - Only you can access

**Required AWS permissions for auto-creation:**
- `s3:CreateBucket`
- `s3:PutBucketPublicAccessBlock`
- `s3:PutBucketVersioning`

### URL Shortening

S3Drop can create shortened URLs for easier sharing:

```bash
# Create shortened URL (default: TinyURL)
python3 s3drop.py my-drops drop file.pdf --share --short

# Choose different shortening service
python3 s3drop.py my-drops drop file.pdf --share --short --short-service isgd
```

**Available URL shortening services:**
- **tinyurl** - TinyURL.com (default, most reliable)
- **isgd** - is.gd (fast and simple)
- **vgd** - v.gd (same as is.gd)
- **1ptco** - 1pt.co (minimal URLs)

**Example output:**
```
🔗 Shortening URL with TINYURL...
✅ URL shortened successfully!

🔗 Secure Share Link:
https://tinyurl.com/abc123xyz

📏 Original URL length: 245 characters
📏 Shortened URL length: 26 characters
💾 Saved: 219 characters

📧 Share this link with your recipients!
⏰ Expires: 2024-01-15 at 14:30
```

**Benefits of shortened URLs:**
- ✅ **Easier to share** - Copy/paste friendly
- ✅ **Email-friendly** - Won't break in email clients
- ✅ **Professional** - Clean, short appearance
- ✅ **Free services** - No API keys required
- ✅ **Reliable** - Multiple service options

### Using AWS Profiles

If you have multiple AWS accounts:

```bash
python3 s3drop.py my-drops drop file.pdf --share --profile production
```

## 📧 Sharing Files with Recipients

After dropping a file with `--share`, you'll get a secure URL like:

```
https://my-drops.s3.amazonaws.com/meeting-recording.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...
```

### Email Template

```
Hi [Recipient],

I've shared a file with you:

[Click here to download: filename.pdf](PASTE_THE_SECURE_URL_HERE)

This secure link expires in 24 hours.

Best regards,
[Your name]
```

### Professional Formatting

For a cleaner look, use markdown formatting in your emails:

```markdown
**File:** Meeting Recording - January 2024  
**Size:** 125 MB  
**Download:** [Click here](SECURE_URL)  
**Expires:** January 15, 2024 at 3:00 PM  
```

## 🛡️ Security Best Practices

1. **Keep your bucket private** - Never enable public access
2. **Use short expiration times** - Default 24 hours is usually sufficient
3. **Monitor access logs** - Enable CloudTrail for audit trails
4. **Rotate AWS credentials** - Regularly update your access keys
5. **Use IAM roles** - In production, use IAM roles instead of access keys

## 💰 Cost Considerations

AWS S3 pricing (approximate):
- **Storage**: $0.023 per GB per month
- **Data transfer**: First 1 GB free per month, then $0.09 per GB
- **Requests**: $0.0004 per 1,000 requests

Example: Sharing a 100 MB file with 10 downloads costs less than $0.01.

## 🔧 Advanced Usage

### Custom File Names

```bash
# Drop with custom path/name in S3
python3 s3drop.py my-drops drop local-video.mp4 --key "meetings/2024/client-presentation.mp4" --share
```

### Batch Operations

```bash
# Drop multiple files
for file in *.pdf; do
    python3 s3drop.py my-drops drop "$file" --share
done
```

### Integration with Scripts

```python
import subprocess

def drop_and_share(bucket, file_path, expires='24h'):
    """Drop a file and get secure share link."""
    result = subprocess.run([
        'python3', 's3drop.py', bucket, 'drop', file_path,
        '--share', '--expires', expires
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        # Parse output to extract URL
        return result.stdout
    else:
        raise Exception(f"Drop failed: {result.stderr}")
```

## 🆘 Troubleshooting

### Common Issues

**"AWS credentials not found"**
```bash
aws configure list  # Check current configuration
aws configure       # Reconfigure credentials
```

**"Drop zone does not exist"**
- S3Drop will auto-create it by default
- If auto-creation fails, check AWS permissions
- Manual creation: `python3 s3drop.py setup`
- Disable auto-creation: `--no-auto-create` flag

**"Permission denied: Cannot create drop zone"**
- Your AWS user needs `s3:CreateBucket` permission
- Add IAM policy with S3 bucket creation rights
- Alternative: Use `python3 s3drop.py setup` for guided creation

**"Access Denied"**
- Ensure your AWS user has S3 permissions
- Required permissions: `s3:GetObject`, `s3:PutObject`, `s3:ListBucket`

**"Link verification failed"**
- This is often normal due to CORS policies
- The link will still work for end users
- Skip verification with `--no-verify` flag (if implemented)

**"Region errors"**
- Ensure your AWS CLI region matches your bucket region
- Set region: `aws configure set region us-east-1`

### Getting Help

1. Check AWS credentials: `aws sts get-caller-identity`
2. Test S3 access: `aws s3 ls`
3. Verify drop zone access: `aws s3 ls s3://your-drop-zone-name`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
git clone https://github.com/kahhaw-thian/s3drop.git
cd s3drop
pip install -r requirements.txt
```

### Running Tests

```bash
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AWS SDK for Python (Boto3) team
- Contributors and users who provided feedback
- Open source community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/kahhaw-thian/s3drop/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kahhaw-thian/s3drop/discussions)
- **Documentation**: [Wiki](https://github.com/kahhaw-thian/s3drop/wiki)

---

**S3Drop - Secure file sharing, simplified.** 

Made with ❤️ for developers, businesses, and anyone who needs to share files securely.
