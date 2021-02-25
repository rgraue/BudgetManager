# BudgetManager
A Python Gui to keep track of finacial records and dislpay key visualizations.

# Install and Running
Enusre that you are running the latest edition of Python 3

install Pyinstaller

`pip install pyinstaller`

make BudgetManager into an executable

`pyinstaller --onefile ./scripts/budgetClient.py`

The executable will then be in the `dist` folder within the project repo.

# .ssh key
Budget Manager utilizes am id_rsa ssh key. If you already have one then budget manager will run just fine. if not....

run `ssh-keygen` in a powershell and follow the given instructions. Do not change the file name, but rather just hit `enter`.