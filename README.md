# cs122a_final_project_repo
 this is the final project repo
 we can separate our jobs, and pushing to this repo
 open a terminal:
 use : 'git clone <repo-url>'
 create your branch : 'git checkout -b your_branch_name'
 edit code and commit with this code : 'git add .' , 'git commit -m "Some commit message"' , 'git push origin your_brach_name'
 DO NOT modify other people's work and the public files, since that will create a git confilict.

# Roles:
Dasheng Yao: 1 - 4
Cindy Feldman: 5 - 8
Mir Ali: 9 - 12

# There is no where like 127.0.0.1:
As you reading this the shell should be up and runing.

steps to use the shell:
 -- install mysql connector in your terminal (use brew / sudo)
 -- I set the sql server running on 127.0.0.1 don't touch that, or make your own branch in git before you push
 -- the code now can properly load the import using command: `python3 project.py import test_data`
 -- develop your code in a separate .py file, I'll import the function and code the sys
 -- if your sql not connecting use the test_connect.py (just hit the run button, it will automatically test your connection)
 -- if your mysql doesn't allow local infiles you need to set local infile on sql side to ON:
 use this code in terminal: 
    `mysql -u root -p` (it will ask for password, if you don't have one just hit enter)
    `SHOW VARIABLES LIKE 'local_infile';`
    `SET GLOBAL local_infile = 1;`
    Then choose onw of the following:
    `sudo systemctl restart mysql`  # Linux
    `brew services restart mysql`   # macOS (if installed via Homebrew)
    After that check again if your infile is setup

    If you think my part has done wrong just send me a message : )
    I think we all get A+++++++++++++++++++++++++++++++++++++++++++++++++++++++++ for this

the + is the separation line, add whatever comments after this :)

# new item: I put the helper functions into the utility
Just use import and use the helper functions, it'll save you a lot of trouble, since it create the cursor, and all you need to do is code up the querys, it'll execute for you, and do automatic close
