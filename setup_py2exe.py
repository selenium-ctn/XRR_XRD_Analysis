from distutils.core import setup
import py2exe
import matplotlib

setup(
  console=['XRR_GUI.py'],
  data_files=matplotlib.get_py2exe_datafiles(),
  options = {
    'py2exe': {
      'bundle_files': 3,
      'optimize': 2,
      'includes': ['scipy', 'numpy', 'scipy.integrate', 'scipy.sparse.linalg.isolve._iterative'],
    }
  }
)

#http://www.py2exe.org/index.cgi/MatPlotLib