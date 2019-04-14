param([Int32]$nbClient=1)  
function startClient {     
    For ($i=0; $i -lt $nbClient; $i++) {        
        pythonw '.\main_client.py'     
    }  
}  
# pip install -r requirements.txt
# python .\server.py | 
startClient