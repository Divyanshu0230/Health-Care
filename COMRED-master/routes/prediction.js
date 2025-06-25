//handling misc disease logic
router.post("/md", function (req, res) {
    console.log("req.body.symptoms:", req.body.symptoms);
    let arrString;
    if (Array.isArray(req.body.symptoms)) {
        // arrString = req.body.symptoms.join(" ");
    } else if (typeof req.body.symptoms === 'string') {
        // arrString = req.body.symptoms;
    } else {
        arrString = "";
    }

    if (!arrString || arrString.trim() === "") {
        return res.render('miscDiseaseResult', { title: "Your Diagnosis Result", prediction: "No symptoms provided.", username: req.user ? req.user.username : "" });
    }

    var spawn = require("child_process").spawn;
    var name = req.body.name;
    var output = "";
    var process = spawn('python3', ["./model_cdss.py", arrString]);

    process.stdout.on('data', function (data) {
        output += data.toString();
    });

    process.stderr.on('data', function (data) {
        console.error('Python error:', data.toString());
    });

    process.on('close', function (code) {
        if (code !== 0) {
            console.error('Python process exited with code', code);
            return res.render('miscDiseaseResult', { title: "Your Diagnosis Result", prediction: "An error occurred in the prediction script.", username: req.user.username });
        }
        var log = new Logs({
            username: req.user.username,
            name: name,
            type: 2,
            input: arrString,
            output: output
        });

        log.save(function (err, result) {
            if (err) {
                console.log(err);
            } else {
                console.log(result);
            }
            return res.render('miscDiseaseResult', { title: "Your Diagnosis Result", prediction: output, username: req.user.username });
        });
    });
}); 