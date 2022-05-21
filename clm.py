import os
import sys
from os.path import exists
import shutil


INSTALLED_PATH = "C:/Users/Yaten/PycharmProjects/clm/CLM/"
cmake = f"{INSTALLED_PATH}deps/cmake/bin/cmake.exe"
make = f"{INSTALLED_PATH}deps/make/bin/make.exe"


def checkDependencies():
    if exists("C:/MinGW"):
        return True
    else:
        return False


def installCmakeBuild(location):
    if not exists(location):
        print(f"[*] {location}, doesnt exists.")
    print("[*] ---- STARTING DOWNLOAD: ---- ")
    print("[*] BUILDING LIBRARY...")
    os.system(
        f'{cmake} -S {location} -B {INSTALLED_PATH}/builds -G "MinGW Makefiles" -D CMAKE_INSTALL_PREFIX="{INSTALLED_PATH}/final"')
    print("[*] Build Complete.")
    print("[*] START MAKEFILE GENERATION...")
    os.system(f'cd builds & {make} & {make} install')
    print("[*] Generation Complete.")
    print("[*] ---- DOWNLOAD COMPLETE: ---- ")
    print(f"[*] INSTALLING {location}")
    os.system(f"robocopy {INSTALLED_PATH}/final/include C:/MinGW/include /e /ndl")
    os.system(f"robocopy {INSTALLED_PATH}/final/lib C:/MinGW/lib /e /ndl")
    os.system(f"cd {INSTALLED_PATH}/builds & type nul > .gitignore")
    os.system(f"cd {INSTALLED_PATH}/final & type nul > .gitignore")
    libs = open(f"{INSTALLED_PATH}installed.txt", 'a+')

    name = input("[*] What would you like to name this library?> ")

    installed = open(f"{INSTALLED_PATH}installed.txt", 'r')
    for i in installed.readlines():
        if name in i:
            print(
                "[*] It seems like you already have downloaded this library, please uninstall before installing it again.")
            exit(0)

    loc = os.listdir(f"{INSTALLED_PATH}/final/include")
    fin = f"{name}"

    for i in loc:
        fin += " " + f"C:/MinGW/include/{i}"

    loc = os.listdir(f"{INSTALLED_PATH}/final/lib")
    for i in loc:
        fin += " " + f"C:/MinGW/lib/{i}"

    fin += '\n'
    libs.write(fin)
    libs.close()
    print(f"[*] {location} has been installed in your MINGW compiler!\n")


def init():
    main = input("[*] MAIN EXECUTABLE NAME: ")
    libraries = input(
        "[*] Dependencies {FORMAT: -l(library-name[version/bits])} & SPACE TO SEPARATE MULTIPLE (BLANK FOR NONE): ")
    cwd = input("[*] ABS CWD (CURRENT WORKING DIRECTORY): ")
    os.system(f"cd {cwd} & mkdir executable")
    compile_file = open(f"{cwd}/compile.bat", 'w')
    compiler_name = ""
    if ".cpp" in main:
        compiler_name += "g++"
    elif ".c" in main:
        compiler_name += "gcc"
    compile_file.write(f"""@ECHO OFF
:: ---------------- THE PARTS YOU CAN EDIT -----------------
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

    libs = open(f"{INSTALLED_PATH}installed.txt", 'a+')

    name = input("[*] What would you like to name this library?> ")

    installed = open(f"{INSTALLED_PATH}installed.txt", 'r')
    for i in installed.readlines():
        if name in i:
            print(
                "[*] It seems like you already have downloaded this library, please uninstall before installing it again.")
            exit(0)

    loc = os.listdir(f"{INSTALLED_PATH}/final/include")
    fin = f"{name}"

    for i in loc:
        fin += " " + f"C:/MinGW/include/{i}"

    loc = os.listdir(f"{INSTALLED_PATH}/final/lib")
    for i in loc:
        fin += " " + f"C:/MinGW/lib/{i}"

    fin += '\n'
    libs.write(fin)
    libs.close()

    print('[*] INSTALLATION COMPLETE')


def uninstall(lib):
    file = open(f"{INSTALLED_PATH}installed.txt")
    data = file.readlines()
    loop = data
    file.close()
    write_to = open(f'{INSTALLED_PATH}installed.txt', 'w')
    counter = 0
    for line in loop:
        if line.split()[0] == lib:
            for loc in line.split()[1:]:
                try:
                    shutil.rmtree(loc)
                except:
                    os.remove(loc)

            data.pop(counter)
            fin = ""
            for j in data:
                fin += " " + j

            write_to.write(fin)
            write_to.close()
            exit(0)
        counter += 1


def list_libs():
    libs = open(f"{INSTALLED_PATH}installed.txt", "r")
    for line in libs.readlines():
        print(line.split()[0])
    libs.close()


def run(function, arg=None):
    try:
        if arg is not None:
            function(arg)
        else:
            function()
    except Exception as e:
        print(e)
        exit(0)


if not checkDependencies():
    print("""[*] Not all dependencies are installed, you need to install:
MinGW: https://sourceforge.net/projects/mingw/
Gnu-Make: http://gnuwin32.sourceforge.net/packages/make.htm
Cmake: https://cmake.org/download/
to be able to run CLM.
""")
commands_entered = sys.argv

try:
    if commands_entered[1] == 'install' and (
            commands_entered[2] == '--cmake-build-required' or commands_entered[2] == '--cbr'):
        run(installCmakeBuild, commands_entered[3])
    elif commands_entered[1] == 'init':
        run(init)
    elif commands_entered[1] == 'install' and (
            commands_entered[2] == '--already-built' or commands_entered[2] == '--ab'):
        run(installWithoutCmakeBuild, commands_entered[3])
    elif commands_entered[1] == 'uninstall':
        run(uninstall, commands_entered[2])
    elif commands_entered[1] == 'ls':
        run(list_libs)
    else:
        command = ''
        for i in commands_entered:
            command += " " + i
        print(f"[*] I don't know what '{command}' means.")
except:
    print("[*] I don't know what you want to do, here is your list of commands:\n"
          "--- install [--cmake-build-required][--cbr] [--already-built][--ab] (abs dir of src)   ->   Installs source library into MinGW compiler\n"
          "--- init  ->   Set's up you CWD (current working directory) for C++/C usage.\n"
          "--- uninstall (lib-name)   ->   Uninstalls libraries from MinGW compiler.\n"
          "--- ls   ->   Lists out all libraries currently installed on your MinGW compiler\n")
