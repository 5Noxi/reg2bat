# reg2bat - Registration Entries to Batch
# Copyright (C) 2025 Noverse

import sys
#import time

roots = {
    "HKEY_CLASSES_ROOT": "HKCR",
    "HKEY_CURRENT_CONFIG": "HKCC",
    "HKEY_CURRENT_USER": "HKCU",
    "HKEY_DYN_DATA": "HKDD",  #used in W95, W98, WME
    "HKEY_LOCAL_MACHINE": "HKLM",
    "HKEY_USERS": "HKU"
    #"HKEY_PERFORMANCE_DATA": "HKPD", #not stored in any hive
}

#start = time.time()

def shortroots(key: str) -> str:
    for full, short in roots.items():
        if key.startswith(full):
            return key.replace(full, short, 1)
    return key

def reg2bat(src, dst):
    for enc in ("utf-16", "utf-8"):
        try:
            lines = open(src, encoding=enc).read().splitlines()
            break
        except UnicodeError:
            continue

    merged, buf = [], "" #buffer for multi line data
    for line in lines:
        line = line.strip()
        if not line or line.startswith((";", "Windows Registry")):
            continue
        if buf:
            buf += line.lstrip() #multi line data
            if not buf.endswith("\\"):
                merged.append(buf.replace("\\", ""))
                buf = ""
        elif line.endswith("\\"): #end if multi line data (if no \)
            buf = line
        else:
            merged.append(line)
        #if buf: merged.append(buf.replace("\\", "")) #possible leftovers

    with open(dst, "w", encoding="utf-8") as f:
        f.write("@echo off\n\n")
        key = None
        for line in merged:
            if line.startswith("[") and line.endswith("]"): #get key
                key = shortroots(line[1:-1])
                continue
            if "=" not in line or not key: #invalid lines
                continue

            name, value = line.split("=", 1) #split value and data
            dispname = name.strip('"')
            if dispname == "@":
                name = "/ve"
            elif " " in dispname:
                name = f'/v "{dispname}"' #only quotes if space (for the looks)
            else:
                name = f"/v {dispname}"

            #default
            out, t, d = None, "REG_SZ", ""

            #handle all types
            if value == '""':
                out, t, d = '/t REG_SZ /d ""', "REG_SZ", ""
            elif value.startswith("dword:"):
                d = str(int(value[6:], 16))
                out, t = f"/t REG_DWORD /d {d}", "REG_DWORD"
            elif value.startswith("hex(b):"):
                d = "0x" + value[7:].replace(",", "")
                out, t = f"/t REG_QWORD /d {d}", "REG_QWORD"
            elif value.startswith("hex(2):"):
                d = value[7:].replace(",", "")
                out, t = f"/t REG_EXPAND_SZ /d {d}", "REG_EXPAND_SZ"
            elif value.startswith("hex(7):"):
                d = value[7:].replace(",", "")
                out, t = f'/t REG_MULTI_SZ /d "{d}"', "REG_MULTI_SZ"
            elif value.startswith("hex:"):
                d = value[4:].replace(",", "")
                out, t = f"/t REG_BINARY /d {d}", "REG_BINARY"

            #rarely used
            elif value.startswith("hex(0):"):
                d = value[7:].replace(",", "")
                out, t = f"/t REG_NONE /d {d}", "REG_NONE"
            elif value.startswith("hex(5):"):
                d = value[7:].replace(",", "")
                out, t = f"/t REG_DWORD_BIG_ENDIAN /d {d}", "REG_DWORD_BIG_ENDIAN"
            elif value.startswith("hex(6):"):
                d = value[7:].replace(",", "")
                out, t = f"/t REG_LINK /d {d}", "REG_LINK"
            elif value.startswith("hex(8):"):
                d = value[7:].replace(",", "")
                out, t = f"/t REG_RESOURCE_LIST /d {d}", "REG_RESOURCE_LIST"
            elif value.startswith("hex(9):"):
                d = value[7:].replace(",", "")
                out, t = f"/t REG_FULL_RESOURCE_DESCRIPTOR /d {d}", "REG_FULL_RESOURCE_DESCRIPTOR"
            elif value.startswith("hex(a):"):
                d = value[7:].replace(",", "")
                out, t = f"/t REG_RESOURCE_REQUIREMENTS_LIST /d {d}", "REG_RESOURCE_REQUIREMENTS_LIST"

            else:
                d = value.strip('"')
                out, t = f'/t REG_SZ /d "{d}"', "REG_SZ"

            f.write(f'reg add "{key}" {name} {out} /f\n')
            print(f"[+] {dispname} -> {t} {d}")
        #f.write("\nexit /b 0\n")
        #end = time.time()
        #print(f"{end - start:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: reg2bat.py input.reg output.bat")
    else:
        reg2bat(sys.argv[1], sys.argv[2])
