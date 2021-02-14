/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://192.168.1.4:5000', // the running FLASK api server url
  auth0: {
    url: '', // the auth0 domain prefix
    audience: '', // the audience set for the auth0 app
    clientId: '', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
