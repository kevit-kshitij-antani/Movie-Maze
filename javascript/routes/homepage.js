// Modules
const express = require("express");
const PythonShell = require("python-shell");
const { moveById } = require("../movieById");

const router = new express.Router();

const pythonScriptPath = "";

router.get("/homepage/:moveById", async function (req, res) {
  if (!req.params.moveById) {
    return res
      .status(400)
      .send({ status: "ERROR", message: "Please provide movie id in params." });
  }
  try {
    const response = await moveById(req.params.moveById);
    return res.send(response);
  } catch (e) {
    return res
      .status(500)
      .send({
        status: "ERROR",
        message: "Something went wrong!!Please try again.",
      });
  }
});

// Export user-Route Module
module.exports = router;