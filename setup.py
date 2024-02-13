from cx_Freeze import setup, Executable, sys

# Lista de archivos adicionales (ejemplo: imagenes, fuentes, etc.)
# Si no tienes archivos adicionales, simplemente deja la lista vacia.

additional_files = [
    ("static/icon.ico", "static/icon.ico"),
    (".env", ".env"),
    # ("chromedriver", "chromedriver"),
]  # ruta original del archivo y ruta en la distribucion final

build_options = {
    "packages": [
        "os",
        "dotenv",
        "requests",
        "selenium",
        "urllib3",
        "idna",
        "certifi",
        # Añade otros paquetes segun sea necesario
    ],
    "excludes": ["tkinter"],
    "include_files": additional_files,
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

shortcut_table = [
    (
        "DesktopShortcut",  # Shortcut
        "DesktopFolder",  # Directory_
        "Get my Parking Place",  # Name
        "TARGETDIR",  # Component_
        "[TARGETDIR]\main.exe",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        "icon.ico",  # Icon
        None,  # IconIndex
        None,  # ShowCmd
        "TARGETDIR",  # WkDir
    )
]
msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {"data": msi_data}

setup(
    name="Get my Parking Place",
    version="1.0",
    author="David Castagneto Aguirre",
    description="Automatically reserve a parking space.",
    options={
        "build_exe": build_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[
        Executable(script="main.py", base=base, icon="static/icon.ico")
    ],  # Punto de entrada de tu aplicacion
)
