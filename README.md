# reg2bat - Registration Entries to Batch

A simple CL tool that converts `.reg` to `.bat` to skip the prompt and implement it better into automations (e.g., into a image as `RunOnce` file) and overall more flexibility. I used Python for it, as I need a better understanding of it for school reasons.

Example output:

![](https://github.com/5Noxi/reg2bat/blob/main/images/reg2bat.png)  

## Features
`reg2bat` converts the whole exported computer registration entry file (`280 MB (294,215,422 bytes)`) within `3.88` seconds (output removed) - remove the comments from the time module and start/end line to test it yourself. It replaces all root keys with their shorted version:
```py
roots = {
    "HKEY_CLASSES_ROOT": "HKCR",
    "HKEY_CURRENT_CONFIG": "HKCC",
    "HKEY_CURRENT_USER": "HKCU",
    "HKEY_DYN_DATA": "HKDD",  #used in W95, W98, WME
    "HKEY_LOCAL_MACHINE": "HKLM",
    "HKEY_USERS": "HKU"
    #"HKEY_PERFORMANCE_DATA": "HKPD" #WNT
}
```
> [wikipedia | Root keys](https://en.wikipedia.org/wiki/Windows_Registry#Root_keys)  
> [winreg | nf-winreg-regquerymultiplevaluesa](https://learn.microsoft.com/en-us/windows/win32/api/winreg/nf-winreg-regquerymultiplevaluesa)  

It supports:
- `REG_NONE` - No defined type
- `REG_SZ` - UTF-16LE string
- `REG_EXPAND_SZ` - Expandable UTF-16LE string with env vars
- `REG_BINARY` - Arbitrary binary data
- `REG_DWORD` / `REG_DWORD_LITTLE_ENDIAN` - 32-bit unsigned integer
- `REG_DWORD_BIG_ENDIAN` - 32-bit unsigned integer
- `REG_LINK` - Unicode symbolic link to another key
- `REG_MULTI_SZ` - List of UTF-16LE strings (double NUL-terminated)
- `REG_RESOURCE_LIST` - Hardware resource list
- `REG_FULL_RESOURCE_DESCRIPTOR` - Hardware resource descriptor
- `REG_RESOURCE_REQUIREMENTS_LIST` - Hardware resource requirements list
- `REG_QWORD` / `REG_QWORD_LITTLE_ENDIAN` - 64-bit integer
> [sysinfo | registry-value-types](https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-value-types)  
> [wikipedia | Keys and values](https://en.wikipedia.org/wiki/Windows_Registry#Keys_and_values)  

## Usage
```ps
.\reg2bat.py input.reg output.bat
```
## Requirements
> [Python 3.x](https://www.python.org/downloads/)  
