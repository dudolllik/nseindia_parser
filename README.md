# Nseindia rate parser 

Parser Final price from Pre-Open Market table
1. Parsing Final price to pars.csv file in name:rate format
1. Simulating user activity after parsing

## Configurating 

Fill in ~config.ini~ your autentification data
For example 
``` 
[Proxy]
login = "your_proxy_login"
password = "your_proxy_password"
ip = "your_proxy_ip"
port = "your_proxy_port"
type = "http" # or "https"
```

## Running 

`pip3 install -r requirements.txt`
`python3 parser_ns.py`
