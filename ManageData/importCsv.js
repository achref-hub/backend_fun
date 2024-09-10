const fs = require('fs');
const csv = require('csv-parser');

async function importCSVToDatabase(csvFilePath, pool, tableName, callback) {
    console.log("csvFilePath",csvFilePath);
  // 1. Parse the CSV file
  const results = [];

  // Wrap fs.createReadStream and csv-parser in a promise
  await new Promise((resolve, reject) => {
    fs.createReadStream(csvFilePath)
      .pipe(csv())
      .on('data', (row) => {
        results.push(row);
      })
      .on('end', () => {
        console.log('CSV file successfully processed');
        resolve();
      })
      .on('error', reject);
  });

  // 2. Insert data into MySQL database using the provided pool
  let connection;
  try {
    // Get a connection from the pool
    connection = await pool.getConnection();

    // Prepare SQL query based on the CSV and table structure
    const query = `INSERT INTO ${tableName} (Gouvernorat,Nombre_total_de_colis,Somme_de_Cr_apres_remise,Nombre_de_Colis_Livrés,Somme_de_Cr_apres_remise_des_colis_livrés,Nombre_de_Colis_Retournés,Somme_de_Cr_apres_remise_des_colis_retournés,Nombre_de_Colis_Non_confirmés,Somme_de_Cr_apres_remise_des_colis_non_confirmés,Nombre_hommes,Nombre_de_femmes,Nombre_hommes_livrés,Somme_de_Cr_apres_remise_pour_hommes_livrés,Nombre_hommes_retournés,Somme_de_Cr_apres_remise_pour_hommes_retournés,Nombre_hommes_non_confirmés,Somme_de_Cr_apres_remise_pour_hommes_non_confirmés,Nombre_de_femmes_livrées,Somme_de_Cr_apres_remise_pour_femmes_livrées,Nombre_de_femmes_retournées,Somme_de_Cr_apres_remise_pour_femmes_retournées,Nombre_de_femmes_non_confirmées,Somme_de_Cr_apres_remise_pour_femmes_non_confirmées
      ) VALUES ?`;

    const values = results.map(row => [
        row.Gouvernorat,
        row.Nombre_total_de_colis,
        row.Somme_de_Cr_apres_remise,
        row.Nombre_de_Colis_Livrés,
        row.Somme_de_Cr_apres_remise_des_colis_livrés,
        row.Nombre_de_Colis_Retournés,
        row.Somme_de_Cr_apres_remise_des_colis_retournés,
        row.Nombre_de_Colis_Non_confirmés,
        row.Somme_de_Cr_apres_remise_des_colis_non_confirmés,
        row.Nombre_hommes,
        row.Nombre_de_femmes,
        row.Nombre_hommes_livrés,
        row.Somme_de_Cr_apres_remise_pour_hommes_livrés,
        row.Nombre_hommes_retournés,
        row.Somme_de_Cr_apres_remise_pour_hommes_retournés,
        row.Nombre_hommes_non_confirmés,
        row.Somme_de_Cr_apres_remise_pour_hommes_non_confirmés,
        row.Nombre_de_femmes_livrées,
        row.Somme_de_Cr_apres_remise_pour_femmes_livrées,
        row.Nombre_de_femmes_retournées,
        row.Somme_de_Cr_apres_remise_pour_femmes_retournées,
        row.Nombre_de_femmes_non_confirmées,
        row.Somme_de_Cr_apres_remise_pour_femmes_non_confirmées
    ]);

    // Execute the query
    const [result] = await connection.query(query, [values]);

    console.log('Data inserted successfully:', result.affectedRows);

    // If a callback is provided, call it on success
    if (callback) callback(null, result);
  } catch (err) {
    console.error('Error inserting data:', err);

    // If a callback is provided, call it on error
    if (callback) callback(err);

    // Throw the error if there's no callback for the caller to handle
    throw err;
  } finally {
    if (connection) {
      connection.release(); // Release the connection back to the pool
    }
  }
}

module.exports = importCSVToDatabase;
