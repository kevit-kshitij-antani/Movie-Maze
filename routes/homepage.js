// Modules
const express = require('express');
const router = new express.Router();

router.get('/homepage', function(req,res) {
    console.log("hello world");
})

// Export user-Route Module
module.exports = router;