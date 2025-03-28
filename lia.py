import json
import yaml
import subprocess
import sys
import os
import platform
import time

os_type = platform.system() # Windows Linux
c = { 
    "red":'\033[91m',
    "green":'\033[92m',
    "grey":'\033[90m'
}

_lang={}
cend = '\033[0m'

def lang(_tag): return _tag if _tag not in _lang else _lang[_tag] 
def _print( _msg, _color = 'green' ): print( c[ _color ] + _msg + cend )

def clearScreen(): 
    os.system('cls' if os_type == "Windows" else 'clear')
    _print(lang('title'))

def load_menu_config(config_file):
    if config_file.endswith('.json'):
        with open(config_file, 'r') as f:
            return json.load(f)
    elif config_file.endswith(('.yaml', '.yml')):
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Formato del file non supportato. Usare JSON o YAML.")

def execute_ansible(playbook_path, inventory=None):
    command = ['ansible-playbook']
    if inventory:
        command.extend(['--inventory', inventory])
    command.append(playbook_path)
    subprocess.run(command)

def execute_terraform(commands):
    terraform_cmd = ['terraform'] + commands
    subprocess.run(terraform_cmd)

def execute_shell_command(command):
    subprocess.run(command)



def show_menu(menu_items, current_level=0, indent=""):
    for index,item in enumerate(menu_items):
        _color = 'green' 
        if 'type' not in item and 'items' not in item:
             _color = 'grey'
        _print(f"{indent} {index+1}. {lang(item if 'text' not in item else item['text'])}", _color)
        '''if 'items' in item:
            show_menu(item['items'], current_level + 1, indent + "  ")
        else:
            pass'''

def changeLanguage(_arg):
    global _lang 
    with open('lang/'+_arg+'.json', 'r') as f:
        _lang  = json.load(f)

def handle_selection(menu_config, _level, menuPre = None):
    while True:
        clearScreen()
        _print("\n"+lang("selectOption")+"\n")
        show_menu(menu_config["items"],_level)
        
        try:
            selected = input(c['green']+"\n"+lang('insertNumberOr')+(lang('exit') if _level == 0 else lang('mainMenu'))+"): ")
            if selected.lower() == '0':
                if _level==0:
                    _print(lang('bye'))
                    break
                else:
                    _level=0
                    menu_config=menuMain
            else:
                if 'type' not in menu_config["items"][int(selected)-1] and 'items' not in menu_config["items"][int(selected)-1]: 
                    _print(lang("menuIsDisabled"),'red')
                    time.sleep(1)
                else:
                    menu_config=menu_config["items"][int(selected)-1]
                    match menu_config['type']:
                        case _:
                        case 'submenu': 
                            #menuPre=menu_config
                            _level +=1
                        case 'function':
                            #print(menu_config)
                            globals()[ menu_config["function"] ](*menu_config["arg"])
                            menu_config=menuMain
        except KeyboardInterrupt:
            _print("\n"+lang('exitProgram')+'.','red')
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        _print(lang('usage'), 'red')
        sys.exit(1)
    
    config_file = sys.argv[1]
    try:
        changeLanguage('it')
        menu_config = load_menu_config(config_file)
        menuMain=menu_config
        handle_selection(menu_config,0)
    except Exception as e:
        _print(lang("error")+": {e}", 'red')