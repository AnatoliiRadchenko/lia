#
# author: Anatolii Radchenko
# description: python library
# @ Rome 2025
#
class Libra:
  def __init__(self,debug=False):
    self.isDebug = debug
    self.colors = { 
        "red":'\033[91m',
        "green":'\033[92m',
        "grey":'\033[90m',
        "cend": '\033[0m'
    }
    self.dbLang={}
    self.importModule("os")
    self.importModule("json")
    self.importModule("platform")
    self.importModule("subprocess")
    self.osType = platform.system() # Windows Linux

    
  def changeLanguage(self,_arg):
    with open('lang/'+_arg+'.json', 'r') as f:
        self.dbLang  = json.load(f)

  def cprint( self,_msg, _color = 'green' ): print( self.colors[ _color ] + _msg + self.colors['cend'] )
  def clearScreen(self): 
      os.system('cls' if self.osType == "Windows" else 'clear')
  def lang(self,_tag): return _tag if _tag not in self.dbLang else self.dbLang[_tag] 
  def pressEnter(self):
    _input = 1
    while _input!='': _input=input('press Enter')  
  def debug(self,msg):
    if(self.isDebug): print(': '+msg)
  def su(self):
    self.debug('su')
    subprocess.run(["sh", "-c", "sudo -v"])
  def importModule(self,name):
    try:
        globals()[name] = __import__(name)  # Tentativo di importare il modulo
    except ImportError:
        self.debug("Il modulo 'requests' non è installato. Installo automaticamente...")
        #from subprocess import call
        self.su()
        result = subprocess.run(["sh", "-c", "sudo dnf install -y pip || sudo apt install pip -y"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        result = subprocess.run(["sh", "-c", "pip install "+name],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        globals()[name] = __import__(name)
