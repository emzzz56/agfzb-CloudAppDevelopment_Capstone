#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys 
import json
from ibmcloudant.cloudant_v1 import Document, CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict): 

    authenticator = IAMAuthenticator("svSiBPYc-GI-Fc72Mrb7bg0kozHZnXgx5i4-pMoj6Wxe")

    service = CloudantV1(authenticator=authenticator)
    
    service.set_service_url("https://a3e831a7-3fd2-4af1-85d9-47314a35c061-bluemix.cloudantnosqldb.appdomain.cloud")
    
    
    review_doc = Document(
      id=dict["review"]["id"],
      name=dict["review"]["name"],
      dealership=dict["review"]["dealership"],
      review=dict["review"]["review"],
      purchase=dict["review"]["purchase"],
      another=dict["review"]["another"],
      purchase_date=dict["review"]["purchase_date"],
      car_make=dict["review"]["car_make"],
      car_model=dict["review"]["car_model"],
      car_year=dict["review"]["car_year"]
      )
    
    response = service.post_document(db='reviews', document=review_doc).get_result()
    
    try: 
        result={
            'headers': {'Content-Type':'application/json'}, 
            'body': {'data':response} 
            }
        return result 

    except:  
        return { 
            'statusCode': 404, 
            'message': 'Something went wrong'
            }