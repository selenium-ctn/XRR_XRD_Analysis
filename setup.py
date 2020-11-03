from distutils.core import setup
import py2exe,sys,numpy,scipy

sys.argv.append('py2exe')

setup(
console=['XRR_GUI.py'],
options={
  'py2exe': {
     'includes':['numpy','scipy','scipy.integrate'],
     'bundle_files':2,
     'compressed':True
  }
},
zipfile=None)

#http://www.py2exe.org/index.cgi/MatPlotLib