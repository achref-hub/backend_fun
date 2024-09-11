const fs = require('fs');
const csv = require('csv-parser');

async function importHollydays(csvFilePath, pool, tableName, callback) {
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
    const query = `INSERT INTO ${tableName} (Gouvernorat,Black_Friday,Saint_Valentin,Soldes_Hiver,Soldes_Été,Mother_Day,Woman_Day,Father_Day,Noël) VALUES ?`;

    const values = results.map(row => [
        row.Gouvernorat,
        row.Black_Friday,
        row.Saint_Valentin,
        row.Soldes_Hiver,
        row.Soldes_Été,
        row.Mother_Day,
        row.Woman_Day,
        row.Father_Day,
        row.Noël
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

module.exports = importHollydays;
