const {onRequest} = require("firebase-functions/v2/https");
const logger = require("firebase-functions/logger");
const admin = require("firebase-admin");

// Initialize Firebase Admin SDK (if not already initialized)
if (admin.apps.length === 0) {
  admin.initializeApp();
}

const db = admin.database();

exports.logTransaction = onRequest({cors: true}, (request, response) => {
  if (request.method !== "POST") {
    return response.status(405).send("Method Not Allowed");
  }

  const transaction = request.body;

  // Basic validation
  if (!transaction || typeof transaction !== "object") {
    logger.error("Invalid transaction data", {transaction});
    return response.status(400).send("Invalid transaction data");
  }

  // Add a timestamp
  transaction.timestamp = new Date().toISOString();

  // Save to the Realtime Database
  const transactionsRef = db.ref("/transactions");
  transactionsRef.push(transaction)
      .then((snapshot) => {
        logger.info("Transaction logged successfully",
            {transactionId: snapshot.key});
        // Respond with the key of the newly created transaction
        response.status(201).send({status: "success",
          transactionId: snapshot.key});
      })
      .catch((error) => {
        logger.error("Error logging transaction", {error});
        response.status(500).send("Error logging transaction");
      });
});
