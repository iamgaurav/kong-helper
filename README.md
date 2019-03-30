# Kong Helper

Helper Container to periodically check and update Kong with the services, routes and their plugins.

# Requirements

Kong version supported 1.1.x

###Sample Config

```
{
   "services": {
     "example_api": {
       "upstream": "example_api",
       "port": 8080,
       "hostname": ["api.example.com"],
       "path": ["/core"],
       "protocol": "http",
       "methods": ["GET","POST","PUT","PATCH","DELETE","HEAD","OPTIONS"],
       "plugins": [
         {
           "name": "cors",
           "config": {
             "origins": "*"
           },
           "run_on": "first"
         }
       ]
     }
   }
}
```

### Disclaimer

This has not been tested on production environments. 