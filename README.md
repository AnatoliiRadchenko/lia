Lybra infrastructure automation

# Libra Infrastructure Automation (LIA)

It's a little diary of the scripts used daily.

## Presentation

This little startup was born spontaneously. I hope it will help to fix and organize small things and thoughts for both you and me.

> A place to copy-paste your README.md from

## Getting started

Simply run:

```shell
python menu_config.json
```

## Roadmap

Launch shell scripts, ansible playbooks, terraform commands etc.

## Use cases:

```shell
{
    "title": "Main Menu",
    "items": [
        {
            "text": "Infrastructure Management",
            "type": "submenu",
            "items": [
                {
                    "text": "AWS Provisioning",
                    "type": "ansible",
                    "playbook": "aws_provision.yml",
                    "inventory": "aws_inventory"
                },
                {
                    "text": "Terraform Plan",
                    "type": "terraform",
                    "command": ["plan", "-var-file=prod.tfvars"]
                }
            ]
        },
        {
            "text": "System Backup",
            "type": "ansible",
            "playbook": "backup.yml"
        },
        {
            "text": "Network Configuration",
            "type": "submenu",
            "items": [
                {
                    "text": "Configure Router",
                    "type": "shell",
                    "command": ["ssh", "router1.example.com", "config-router.sh"]
                },
                {
                    "text": "Configure Switch",
                    "type": "ansible",
                    "playbook": "switch_config.yml"
                }
            ]
        }
    ]
}
```
