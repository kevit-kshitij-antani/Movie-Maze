const express = require('express');
const homepage = require('./routes/homepage')
require('./db/mongoose');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(homepage);

app.listen(port, function () {
    console.log(`Server is up on port ${port}`);
})