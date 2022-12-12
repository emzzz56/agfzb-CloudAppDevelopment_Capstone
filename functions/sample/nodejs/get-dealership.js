/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    
    let dbListPromise = getAllRecords(cloudant,'dealerships');

    if (params.state) {
        dbListPromise = getMatchingRecords(cloudant,'dealerships', {'state':params.state});
    }
    
    return dbListPromise;
}

 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                   data = result.result.docs;
                   output = data.map((row) => { 
                       return {
                          id: row.id,
                          city: row.city,
                          state: row.state,
                          st: row.st,
                          address: row.address,
                          zip: row.zip,
                          lat: row.lat,
                          long: row.long
                        }
                   });
                   resolve({result:output});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }

 function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
             .then((result)=>{
                 data = result.result.rows;
                   output = data.map((row) => { 
                       return {
                          id: row.doc.id,
                          city: row.doc.city,
                          state: row.doc.state,
                          st: row.doc.st,
                          address: row.doc.address,
                          zip: row.doc.zip,
                          lat: row.doc.lat,
                          long: row.doc.long
                        }
                   });
               resolve({result:output});
               //resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }