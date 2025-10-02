# reg2bat - Registration Entries to Batch
# Copyright (C) 2025 Noverse - https://discord.gg/E2ybG4j9jU

import sys
#import time

roots = {
    "HKEY_LOCAL_MACHINE": "HKLM",
    "HKEY_CURRENT_USER": "HKCU",
    "HKEY_CLASSES_ROOT": "HKCR",
    "HKEY_USERS": "HKU",
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

            #empty values and type handling
            if value == '""':  
                out, t, d = '/t REG_SZ /d ""', "REG_SZ", ""
            elif value == "hex:":
                out, t, d = '/t REG_BINARY /d ""', "REG_BINARY", ""
            elif value == "hex(2):":
                out, t, d = '/t REG_EXPAND_SZ /d ""', "REG_EXPAND_SZ", ""
            elif value == "hex(7):":
                out, t, d = '/t REG_MULTI_SZ /d ""', "REG_MULTI_SZ", ""
            elif value == "hex(b):":
                out, t, d = '/t REG_QWORD /d ""', "REG_QWORD", ""
            elif value.startswith("dword:"):
                d = str(int(value[6:],16))
                out, t = f"/t REG_DWORD /d {d}", "REG_DWORD"
            elif value.startswith("hex(b):"):
                d = "0x" + value[7:].replace(",","")
                out, t = f"/t REG_QWORD /d {d}", "REG_QWORD"
            elif value.startswith("hex(7):"):
                d = value[7:].replace(",","")
                out, t = f'/t REG_MULTI_SZ /d "{d}"', "REG_MULTI_SZ"
            elif value.startswith("hex(2):"):
                d = value[7:].replace(",","")
                out, t = f"/t REG_EXPAND_SZ /d {d}", "REG_EXPAND_SZ"
            elif value.startswith("hex:"):
                d = value[4:].replace(",","")
                out, t = f"/t REG_BINARY /d {d}", "REG_BINARY"
            else:
                d = value.strip('"')
                out, t = f'/t REG_SZ /d "{d}"', "REG_SZ"

            f.write(f'reg add "{key}" {name} {out} /f\n')
            #f.write("\nexit /b 0\n")
            print(f"[+] {dispname} -> {t} {d}")
        #end = time.time()
        #print(f"{end - start:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: reg2bat.py input.reg output.bat")
    else:
        reg2bat(sys.argv[1], sys.argv[2])
