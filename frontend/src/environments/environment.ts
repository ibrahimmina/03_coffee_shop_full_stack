/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://192.168.1.10:5000', // the running FLASK api server url
  auth0: {
    url: 'fsndcoffeeshopapp.us', // the auth0 domain prefix
    audience: 'https://fsndcoffeeshopapp.us.auth0.com/api/v2/', // the audience set for the auth0 app
    clientId: 'zkK8imAQ3kfxR1M5gjstw53aimM02nVN', // the client id generated for the auth0 app
    callbackURL: 'http://192.168.1.10:8100', // the base url of the running ionic application. 
  }
};
