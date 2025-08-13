# S3Drop
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)

**Secure file sharing, simplified.**

S3Drop is a simple, powerful tool for securely sharing files with customers, clients, or team members using AWS S3 presigned URLs. Drop files securely, share with confidence.

<br>

>💔 The Problem We All Face - You need to share a large file with a client. Email bounces back - "File too large." You try Dropbox, but they don't have an account. Google Drive? Same issue. WeTransfer? Files disappear after a week, and your client downloads it too late.

<br>

## ✨ The Solution - S3Drop. You upload your big file to S3 via s3drop command, get a download link, share the link.

- 🔐 **Secure by default** - Private S3 bucket, no public access
- ⏰ **Time-limited links** - URLs expire automatically (default: 24 hours)  
- 🎯 **Simple to use** - Drop files, get secure links instantly
- 👥 **No recipient setup** - Recipients just click the link to download
- 📊 **Audit trail** - AWS CloudTrail logs all access attempts
- 💼 **Professional** - Perfect for business file sharing

<br>

🚀 See It In Action

```
# Upload your file and get a secure link in one command
python3 s3drop.py <s3-bucket-name> drop <meeting-video-recording.mp4> --share

# Output:
✅ File uploaded successfully!
🔗 Secure link: https://tinyurl.com/abc123
📧 Ready to share with your client
⏰ Expires in 24 hours
```



## 🚀 Quick Start

### 1. Install (One time setup)
```bash
# Install AWS CLI
brew install awscli  # macOS
# or download from aws.amazon.com/cli for Windows/Linux

# Configure (enter your AWS keys)
aws configure

# Install dependencies  
pip install boto3 requests

# Download S3Drop
curl -O https://raw.githubusercontent.com/kahhaw-thian/s3drop/main/s3drop.py
```
### 2. Share your first file
```bash
python3 s3drop.py <s3-bucket-name> drop <large-file-name-with extension> --share
```

<br>

## 💰 Transparent Pricing
AWS S3 costs (what you actually pay):

📁 Storage: ~$0.02/GB per month
⬇️ Downloads: First 1GB free monthly, then ~$0.09/GB
🔄 Requests: ~$0.40 per 100,000 operations
Real example: Share a 100MB file with 10 people = Less than 1 cent

No monthly fees. No subscriptions. No surprises.

<br><br>

## �  Usage

### Drop and Share Files

```bash
# Drop a file and get a secure share link (auto-creates S3 bucket if needed)
python3 s3drop.py my-files drop meeting-recording.mp4 --share

# Drop with shortened URL for easier sharing
python3 s3drop.py my-files drop document.pdf --share --short

# Drop with custom expiration (48 hours)
python3 s3drop.py my-files drop document.pdf --share --expires 48h

# Drop and verify the link works
python3 s3drop.py my-files drop video.mp4 --share --verify

# Use different URL shortening service
python3 s3drop.py my-files drop file.pdf --share --short --short-service isgd
```

<br><br>

## 🎓 Advanced Features (When You Need Them)

```
# Get short, clean URLs for email/SMS
python3 s3drop.py my-files drop video.mp4 --share --short

# Output: https://tinyurl.com/abc123
# Instead of: https://your-bucket.s3.amazonaws.com/video.mp4?X-Amz-Algorithm=AWS4...
```

```
# 2 hours for urgent files
python3 s3drop.py my-files drop urgent.pdf --share --expires 2h

# 1 week for project files  
python3 s3drop.py my-files drop project.zip --share --expires 7d
```

```
# Use different AWS profiles for different clients
python3 s3drop.py client-a-files drop proposal.pdf --share --profile client-a
python3 s3drop.py client-b-files drop contract.pdf --share --profile client-b
```




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
