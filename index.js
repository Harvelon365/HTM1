#! /usr/bin/env node

const path = require("path")
const express = require("express"); const app = express()

express.static.mime.define({'text/html': ['htm1']})

app.use("/css", express.static("css"))
app.get("/", function(req, res) {
	res.sendFile(path.join(__dirname, "helloworld.htm1"))

})

app.listen(8000)
console.info("server alive")

