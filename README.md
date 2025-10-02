# reg2bat - Registration Entries to Batch

A simple CL tool which converts `.reg` to `.bat` to skip the prompt and implement it better into automations (e.g., into a image as `RunOnce` file) and overall more flexibility. I used Python for it, as I need a better understanding of it for school reasons.

Example output:

![](https://github.com/5Noxi/reg2bat/blob/main/images/reg2bat.png)

`reg2bat` converts the whole exported computer registration entry file (`280 MB (294,215,422 bytes)`) within `3.88` seconds (remove the comments from the time module and start/end line to test it yourself). It replaces all roots with their shorted version:
```py
roots = {
    "HKEY_LOCAL_MACHINE": "HKLM",
    "HKEY_CURRENT_USER": "HKCU",
    "HKEY_CLASSES_ROOT": "HKCR",
    "HKEY_USERS": "HKU",
}
```
It supports (handles empty data):
- `REG_SZ`
- `REG_EXPAND_SZ`
- `REG_MULTI_SZ`
- `REG_BINARY`
- `REG_DWORD`
- `REG_QWORD`
> [sysinfo | registry-value-types](https://learn.microsoft.com/en-us/windows/win32/sysinfo/registry-value-types)

## Usage
```ps
.\reg2bat.py input.reg output.bat
```
