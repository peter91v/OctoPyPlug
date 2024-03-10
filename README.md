# OctoPyPlug
Solang es keine automatisierte installation gib muss Manuell durchgeführt werden:
    python.exe -m pip install --upgrade pip
    pip install flask
    pip install flask_cors
    pip install --editable src/octoplug
    für test:
        ordner erstellen (Bsp.: google_rcp)
        cd google_rcp
        git clone git@github.com:grpc/grpc.git
        cd .\google_rcp\grpc\examples\python\auth
        cp credentials  ..\..\..\..\..\OctoPyPlug\src\octoplug\octopyplug