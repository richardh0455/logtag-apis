global.fetch = require('node-fetch');
var AWS = require('aws-sdk');
var AmazonCognitoIdentity = require('amazon-cognito-identity-js');

exports.handler = function(event, context, callback) {
    return sendRes(event, context, callback);
};



const sendRes = (event, context, callback) => {

    AWS.config.update({
        region: process.env.AWS_REGION,
    });
    var accountId = context.invokedFunctionArn.match(/\d{3,}/)[0];
    var dashboardId = process.env.dashboardId ;
    var sessionName = event.sessionName;
    var idToken = event.Authorization;

    if (!accountId) {
        var error = new Error("accountId is unavailable");
        callback(error);
    }

    if (!dashboardId) {
        var error = new Error("dashboardId is unavailable");
        callback(error);
    }

    if (!idToken) {
        var error = new Error("idToken is unavailable");
        callback(error);
    }

    var roleArn = 'arn:aws:iam::276219036989:role/Cognito_logtag_identity_poolAuth_Role'; // your cognito authenticated role arn here


    var cognitoIdentity = new AWS.CognitoIdentity();

    var params = {
        IdentityPoolId: 'ap-southeast-2:687f1ba1-1242-4f22-8adf-da49297c8005', // your identity pool id here
        Logins: {
            // your logins here
            'cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_3e18SkGuR': idToken
        }
    };

    cognitoIdentity.getId(params, function(err, data) {
        authenticateAndGenerateURL(err, data, accountId, dashboardId, callback, roleArn, sessionName, idToken, cognitoIdentity )
    });
}

const authenticateAndGenerateURL = (err, data, accountId, dashboardId, callback, roleArn, sessionName, idToken, cognitoIdentity) => {
  if (err) console.log(err, err.stack);
  else {
      data.Logins = {
          // your logins here
          'cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_3e18SkGuR': idToken
      };

      cognitoIdentity.getOpenIdToken(data, function(err, openIdToken) {
          getTokenAndGenerateURL(err, openIdToken, accountId, dashboardId, callback, roleArn, sessionName);
      });
  }

}

const getTokenAndGenerateURL = (err, openIdToken, accountId, dashboardId, callback, roleArn, sessionName) => {
  if (err) {
      console.log(err, err.stack);
      callback(err);
  } else {
      let stsParams = {
          RoleSessionName: sessionName,
          WebIdentityToken: openIdToken.Token,
          RoleArn: roleArn
      }
      var stsClient = new AWS.STS();
      stsClient.assumeRoleWithWebIdentity(stsParams, function(err, data) {
          assumeRoleAndGenerateURL(err, data, accountId, dashboardId, callback, roleArn, sessionName);
      });
  }
}

const assumeRoleAndGenerateURL = (err, data, accountId, dashboardId, callback, roleArn, sessionName) => {
  if (err) {
      console.log(err, err.stack);
      callback(err);
  } else {
      AWS.config.update({
          region: 'us-east-1',
          credentials: {
              accessKeyId: data.Credentials.AccessKeyId,
              secretAccessKey: data.Credentials.SecretAccessKey,
              sessionToken: data.Credentials.SessionToken,
              expiration: data.Credentials.Expiration
          }
      });

      var registerUserParams = {
          // required
          AwsAccountId: accountId,
          // can be passed in from api-gateway call
          Email: 'xyz@xyz.com',
          // can be passed in from api-gateway call
          IdentityType: 'IAM',
          // can be passed in from api-gateway call
          Namespace: 'default',
          // can be passed in from api-gateway call
          UserRole: 'READER',
          IamArn: roleArn,
          SessionName: sessionName
      };

      var quicksight = new AWS.QuickSight();
      quicksight.registerUser(registerUserParams, function(err, data) {
          registerUserAndGenerateURL(err, data, accountId, dashboardId, callback)
      });
  }
}

const registerUserAndGenerateURL = (err, data, accountId, dashboardId, callback) => {
  if (err) {
      console.log(err, err.stack); // an error occurred
      if (err.code && err.code === 'ResourceExistsException') {
          generateURL(accountId, dashboardId, callback);
      } else {
          callback(err);
      }
  } else {
      // successful response
      setTimeout(function() {
          generateURL(accountId, dashboardId, callback);
      }, 2000);
  }

}

const generateURL = (accountId, dashboardId, callback) => {
    AWS.config.update({
        region: process.env.AWS_REGION,
    });

    var getDashboardParams = {
        // required
        AwsAccountId: accountId,
        // required
        DashboardId: dashboardId,
        // required
        IdentityType: 'IAM',
        ResetDisabled: false, // can be passed in from api-gateway call
        SessionLifetimeInMinutes: 600, // can be passed in from api-gateway call
        UndoRedoDisabled: false // can be passed in from api-gateway call
    };

    var quicksightGetDashboard = new AWS.QuickSight();
    quicksightGetDashboard.getDashboardEmbedUrl(getDashboardParams, function(err, data) {
        if (err) {
            console.log(err, err.stack); // an error occurred
            callback(err);
        } else {
            console.log(data);
            var result = {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": JSON.stringify(data),
                "isBase64Encoded": false
            }
            callback(null, result); // successful response
        }
    });

}
