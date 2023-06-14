const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let state = params.__ow_query ? new URLSearchParams(params.__ow_query).get('state') : null;
    let allDealershipsPromise;

    if(state) {
        allDealershipsPromise = getDealershipsByState(cloudant, 'dealerships', state);
    } else {
        allDealershipsPromise = getAllDealerships(cloudant, 'dealerships');
    }

    return allDealershipsPromise;
}

function getAllDealerships(cloudant, dbname) {
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
            .then((result) => {
                if(result.result.rows.length === 0) {
                    reject({statusCode: 404, error: 'The database is empty.'});
                }
                const dealerships = result.result.rows.map(row => {
                    let dealership = row.doc;
                    delete dealership._id;
                    delete dealership._rev;
                    return dealership;
                });
                resolve({ result: dealerships });
            })
            .catch(err => {
                console.log(err);
                reject({statusCode: 500, error: 'Something went wrong on the server.'});
            });
    });
}

function getDealershipsByState(cloudant, dbname, state) {
    return new Promise((resolve, reject) => {
        const selector = {
            "state": state
        };
        cloudant.postFind({ db: dbname, selector: selector })
            .then((result) => {
                if(result.result.docs.length === 0) {
                    reject({statusCode: 404, error: 'No dealerships found for the given state.'});
                }
                const docs = result.result.docs.map(doc => {
                    delete doc._id;
                    delete doc._rev;
                    return doc;
                });
                resolve({ result: docs });
            })
            .catch(err => {
                console.log(err);
                reject({statusCode: 500, error: 'Something went wrong on the server.'});
            });
    });
}