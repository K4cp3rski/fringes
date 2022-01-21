from setuptools import setup
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] 
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
        
venv_path = os.path.parent.absolute() + "/venv/"
if not os.path.isdir(venv_path):
    os.mkdir(venv_path)
    os.system("python3 -m venv fringes_venv")
    os.system("source fringes_venv/bin/activate")
    os.systen("pip install jupyter")
    os.system('ipython kernel install --name "local-venv" --user')
    
        
setup(install_requires=install_requires, py_modules=["backend"])