# DuoAPITool
Tool for making API calls to Duo (Hopefully) 


Install
1. After running git clone, to pull down the repo, browse to https://pipenv.readthedocs.io/en/latest/
Use brew to install the pipenv.

2. CD in to the DuoAPITool directory and then run 'pipenv install' 
this should install the required dependencies.

3. Run 'pipenv run main' at command prompt with the required paramaters:
example: GET <api-hostname> <example call i.e admin/v2/logs/authentication> '{"results": "denied"}' <Ikey> <Skey>

Note: when copying the parameters JSON it mis interprets the speak marks around the string so best to check these are correct.





