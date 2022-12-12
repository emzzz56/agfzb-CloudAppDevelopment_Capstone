import sys 
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict): 

    authenticator = IAMAuthenticator("svSiBPYc-GI-Fc72Mrb7bg0kozHZnXgx5i4-pMoj6Wxe")

    service = CloudantV1(authenticator=authenticator)
    
    service.set_service_url("https://a3e831a7-3fd2-4af1-85d9-47314a35c061-bluemix.cloudantnosqldb.appdomain.cloud")
        
    response = service.post_find(
        db='reviews',
        fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year'],
        selector={'dealership':{'$eq': int(dict["dealerId"])}}
        ).get_result()
    

    try: 
        result={
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':response["docs"]} 
            }
        return result 

    except:  
        return { 
            'statusCode': 404, 
            'message': 'Something went wrong'
            }
