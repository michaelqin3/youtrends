const express = require('express');
const cors = require('cors');
const mysql = require('mysql');
require('dotenv').config()

const app = express();

app.use(express.json());

const connection = mysql.createConnection({
    user: "milestone0user",
    password: "longpassword",
    database: "youtube_trends_db",
    socketPath: "/cloudsql/cs348-project-279101:us-central1:cs348project"
});

connection.connect(err => {
    if(err) {
        console.log("not connected")
        console.log(err)
        return err;
    }
    console.log("connected")
})

app.use(cors());

var offset = 0 % 1000

app.get('/getVideos', (req, res) => {
    var sql = `SELECT * FROM videos ORDER BY video_id LIMIT 15 OFFSET ${offset}`;
    offset += 15;
    connection.query(sql, function (err, results) {
        if (err) {
            return res.send(err)
        } else { 
            console.log("sent values")
            return res.json({
                data: results
            })
        }
    })
});

app.get('/', (req, res) => {
    res.send('Hello from App Engineee!');
  });

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log('Listening on port ${PORT}')
});