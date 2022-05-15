import os
import sys
from os.path import exists


def checkDependencies():
    if exists("C:/MinGW") and exists("C:/Program Files (x86)/GnuWin32") and exists("C:/Program Files/CMake"):
        return True
    else:
        return False


def installCmakeBuild(location):
    if not exists(location):
        raise FileNotFoundError(f"[*] {location}, doesnt exists.")
    print("[*] ---- STARTING DOWNLOAD: ---- ")
    print("[*] BUILDING LIBRARY...")
    os.system(f'cmake -S {location} -B {os.getcwd()}/builds -G "MinGW Makefiles" -D CMAKE_INSTALL_PREFIX="{os.getcwd()}/final"')
    print("[*] Build Complete.")
    print("[*] START MAKEFILE GENERATION...")
    os.system('cd builds & make & make install')
    print("[*] Generation Complete.")
    print("[*] ---- DOWNLOAD COMPLETE: ---- ")
    print(f"[*] INSTALLING {location}")
    os.system(f"robocopy {os.getcwd()}/final/include C:/MinGW/include /e /ndl")
    os.system(f"robocopy {os.getcwd()}/final/lib C:/MinGW/lib /e /ndl")
    os.system('rmdir /s /q builds & rmdir /s /q final')
    print(f"[*] {location} has been installed in your MINGW compiler!\n")


def init():
    main = input("[*] MAIN EXECUTABLE NAME: ")
    libraries = input("[*] Dependencies {FORMAT: -l(library-name[version/bits])} & SPACE TO SEPARATE MULTIPLE (BLANK FOR NONE): ")
    cwd = input("[*] ABS CWD (CURRENT WORKING DIRECTORY): ")
    os.system(f"cd {cwd} & mkdir executable")
    compile_file = open(f"{cwd}/compile.bat", 'w')
    compiler_name = ""
    if ".cpp" in main:
        compiler_name += "g++"
    elif ".c" in main:
        compiler_name += "gcc"
    compile_file.write(f"""@ECHO OFF
:: ---------------- THE PARTS YOU CAN EDIT ----------------- :
:: LIBRARIES:
set libraries={libraries}
:: NAME OF COMPILED FILE:
set exe_name=main.exe
:: NAME OF FILE TO BE COMPILED:
set to_compile_name={main}

:: DO NOT EDIT THE REST OF THIS FILE! EDITING THIS FILE MAY CAUSE PROBLEMS!
echo ----- COMPILING... -----
{compiler_name} %to_compile_name% -o executable/%exe_name% %libraries%
echo ----- RUNNING... -----
.\executable\%exe_name%
echo ----- Complete! -----
""")
    compile_file.close()
    if not exists(f"{cwd}/{main}"):
        main_file = open(f"{cwd}/{main}", 'w')
        main_file.write("""// GENERATED BY C/C++ Library Manager:
#include <iostream>
using namespace std;

int main() {
    cout << "Hello World!" << endl;
    return 0;    
}
// A simple Hello World program.
""")
        main_file.close()


def installWithoutCmakeBuild(location):
    if not exists(location):
        raise FileNotFoundError(f"[*] {location}, doesnt exists.")
    print(f"[*] INSTALLING {location}")
    os.system(f'robocopy {location}/include C:/MinGW/include /e /ndl & robocopy {location}/lib C:/MinGW/lib /e /ndl')
    if exists(f'{location}/bin'):
        os.system(f'robocopy {location}/bin C:/MinGW/bin /e /ndl')
    print('[*] INSTALLATION COMPLETE')


def run(function, arg=None):
    try:
        if arg is not None:
            function(arg)
        else:
            function()
    except:
        exit(0)


if not checkDependencies():
    print("""[*] Not all dependencies are installed, you need to install:
MinGW: https://sourceforge.net/projects/mingw/
Gnu-Make: http://gnuwin32.sourceforge.net/packages/make.htm
Cmake: https://cmake.org/download/
to be able to run CLM.
""")
commands_entered = sys.argv

if commands_entered[1] == 'install' and (commands_entered[2] == '--cmake-build-required' or commands_entered[2] == '--cbr'):
    run(installCmakeBuild, commands_entered[3])
elif commands_entered[1] == 'init':
    run(init)
elif commands_entered[1] == 'install' and (commands_entered[2] == '--already-built' or commands_entered[2] == '--ab'):
    run(installWithoutCmakeBuild, commands_entered[3])
else:
    command = ''
    for i in commands_entered:
        command += " " + i
    print(f"[*] I don't know what '{command}' means.")
