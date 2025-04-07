import requests
import sys
import subprocess

import json
import yaml
import os
import time


for _i in ["ansible","terraform","modules"]: os.makedirs(_i, exist_ok = True)
sys.path.append("modules")
def load_module_from_url(url, module_name):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(f"modules/{module_name}.py", "wb") as f:
            f.write(response.content)
        sys.path.append(".")
        imported_module = __import__(module_name)
        return imported_module
    except Exception as e:
        print(f"Errore durante il download/importazione del modulo: {e}")
        return None
def prepare(target):
    match target:
        case 'ansible':
            # Crea il file di configurazione di Ansible
            if not os.path.exists("ansible/ansible.log"):
                with open("ansible/ansible.log", 'w') as f: f.write("\n")
            if not os.path.exists("ansible/inventory"):
                inventory_file = os.path.join("ansible", "inventory")
                with open(inventory_file, 'w') as f:
                    f.write("[localhost]\nlocalhost ansible_connection=local\n")
            if not os.path.exists("ansible/ansible.cfg"):
                libra.debug('create ansible.cfg')
                ansible_config = [
                    "[defaults]",
                    f"inventory = inventory",
                    f"log_path = {os.path.join('ansible', 'ansible.log')}",
                    "host_key_checking = False",
                    "remote_user = root",
                    "gather_facts = True",
                    "fact_caching = jsonfile",
                    "fact_caching_connection = /tmp/.ansible_fact_cache"
                ]
                config_file = os.path.join("ansible", "ansible.cfg")
                with open(config_file, 'w') as f:
                    f.write('\n'.join(ansible_config))


url = "https://raw.github.com/AnatoliiRadchenko/pythonLibra/main/Libra.py"
Libra = load_module_from_url(url, "Libra")
libra = Libra.Libra(True)


def changeLanguage(_arg): libra.changeLanguage(_arg)
def clearScreen():
    libra.clearScreen()
    libra.cprint(libra.lang('title'))
def _print( _msg, _color = 'green' ): libra.cprint(_msg,_color)

def load_menu_config(config_file):
    if config_file.endswith('.json'):
        with open(config_file, 'r') as f:
            return json.load(f)
    elif config_file.endswith(('.yaml', '.yml')):
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Formato del file non supportato. Usare JSON o YAML.")

def show_menu(menu_items, current_level=0, indent=""):
    for index,item in enumerate(menu_items):
        _color = 'green' 
        if 'type' not in item and 'items' not in item:
             _color = 'grey'
        _print(f"{indent} {index+1}. {libra.lang(item if 'text' not in item else item['text'])}", _color)

def handle_selection(menu_config, _level, menuPre = None):
    while True:
        clearScreen()
        _print("\n"+libra.lang("selectOption")+"\n")
        show_menu(menu_config["items"],_level)
        
        try:
            selected = input(libra.colors['green']+"\n"+libra.lang('insertNumberOr')+(libra.lang('exit') if _level == 0 else libra.lang('mainMenu'))+"): ")
            if selected.lower() == '0':
                if _level==0:
                    _print(libra.lang('bye'))
                    break
                else:
                    _level=0
                    menu_config=menuMain
            else:
                if 'type' not in menu_config["items"][int(selected)-1] and 'items' not in menu_config["items"][int(selected)-1]: 
                    _print(libra.lang("menuIsDisabled"),'red')
                    time.sleep(1)
                else:
                    menu_config=menu_config["items"][int(selected)-1]
                    if 'type' not in menu_config and 'items' in menu_config:
                         menu_config['type']='submenu'
                    print(menu_config)
                    match menu_config['type']:
                        case 'ansible':
                            subprocess.run(["sh", "-c", "sudo -v"], capture_output=True, text=True)
                            prepare('ansible')
                            result = subprocess.run(["sh", "-c", "cd ansible && ansible-playbook "+menu_config['path']])
                            libra.pressEnter()
                            _level=0
                            menu_config=menuMain
                        case 'submenu': 
                            _level +=1
                        case 'function':
                            globals()[ menu_config["function"] ](*menu_config["arg"])
                            menu_config=menuMain
        except KeyboardInterrupt:
            _print("\n"+libra.lang('exitProgram')+'.','red')
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        if not os.path.exists("menu.json"): 
            _print(libra.lang('usage'), 'red')
            sys.exit(1)
        else: config_file = "menu.json"
    else: config_file = sys.argv[1]
    try:
        libra.changeLanguage('it')
        menu_config = load_menu_config(config_file)
        menuMain=menu_config
        handle_selection(menu_config,0)
    except Exception as e:
        _print(libra.lang("error")+": ", 'red')
        print(e)

