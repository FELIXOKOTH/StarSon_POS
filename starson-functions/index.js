/**
 * Import function triggers from their respective submodules:
 *
 * const {onCall} = require("firebase-functions/v2/https");
 * const {onDocumentWritten} = require("firebase-functions/v2/firestore");
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

const {setGlobalOptions} = require("firebase-functions/v1");
const {onRequest} = require("firebase-functions/v2/https");
const logger = require("firebase-functions/logger");

// Import the new transaction logging function
const {logTransaction} = require("./log_transaction");

// Set global options for cost control
setGlobalOptions({maxInstances: 10});

// Export the transaction logging function
exports.logTransaction = logTransaction;

// Example function (can be removed if no longer needed)
exports.helloWorld = onRequest((request, response) => {
  logger.info("Hello logs!", {structuredData: true});
  response.send("Hello from StarSon POS Functions!");
});
