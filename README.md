# Path Traversal — Nuclei Detection Template

## Severity
**High** (CVSS v3: 7.5)

## Impact
An attacker can read arbitrary files from the server's filesystem
outside the intended web root. This includes sensitive files such as
`/etc/passwd`, application configuration files with credentials,
private SSH/TLS keys, and source code. In write-enabled scenarios
severity escalates to Critical.

## Recommendation
- Validate and sanitize all user-supplied file path parameters.
- Use a whitelist of allowed filenames or resolve the absolute path
  and verify it starts with the expected base directory.
- Never pass raw user input to file system APIs.
- Apply the principle of least privilege to the web server process.

---

## Deploy the vulnerable service

### Requirements
- Docker
- Docker Compose

### Steps

```bash
# 1. Clone the repository
git clone https://gitlab.com/<your-username>/path-traversal-nuclei.git
cd path-traversal-nuclei

# 2. Start the vulnerable service
docker-compose up

# 3. Verify it is running
curl http://localhost:5000/download?file=hello.txt
# Expected output: Hello World
```

### Verify the vulnerability manually

```bash
curl "http://localhost:5000/download?file=../../etc/passwd"
# Expected: contents of /etc/passwd
```

---

## Run the Nuclei template

### Prerequisites
Install Nuclei: https://github.com/projectdiscovery/nuclei

```bash
# YAML template
nuclei -t nuclei-template.yaml -u http://localhost:5000

# Code Protocol (Python)
python nuclei-code-template.py http://localhost:5000
```

### Expected output (vulnerable host)
```
[path-traversal-detect] [http] [high] http://localhost:5000/download?file=../../etc/passwd
```
