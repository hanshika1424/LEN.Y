let analyzeButton = document.getElementById("analyze-button");
analyzeButton.addEventListener("click", analyzeMessage);

function analyzeMessage() {

    let phone = document.getElementById("phone-number").value;

    if (phone == "") {
        alert("Please enter your phone number.");
        return;
    }

    let message = document.getElementById("message").value;

    if (message == "") {
        alert("Please paste a message.");
        return;
    }

    let lines = message.split("\n");

    let messageID = lines[0].replace("Message ID:", "").trim();
    let customerID = lines[1].replace("Customer ID:", "").trim();
    let department = lines[2].replace("Department:", "").trim();
    let sender = lines[3].replace("Sender:", "").trim();
    let timestamp = lines[4].replace("Time:", "").trim();
    let body = lines.slice(5).join("\n").trim();

    let data = {
        phone_number: phone,
        message_id: messageID,
        customer_id: customerID,
        department: department,
        sender_id: sender,
        timestamp: timestamp,
        message_body: body
    };

    document.getElementById("result").innerHTML =
        "<h3>Extracted Information</h3>" +
        "Phone Number: " + phone + "<br>" +
        "Message ID: " + messageID + "<br>" +
        "Customer ID: " + customerID + "<br>" +
        "Department: " + department + "<br>" +
        "Sender: " + sender + "<br>" +
        "Time: " + timestamp + "<br><br>" +
        "<b>Message Body:</b><br>" +
        body;

    console.log(data);

    fetch("http://127.0.0.1:5000/verify", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    })

    .then(response => response.json())

    .then(result => {

        document.getElementById("result").innerHTML +=
            "<hr>" +
            "<h3>Verification Result</h3>" +
            "Verdict: " + result.final_verdict + "<br>" +
            "Confidence Score: " + result.confidence_score + "%<br>" +
            "Database Check: " + result.db_check.reason;

        if (result.final_verdict == "VERIFIED") {
            document.getElementById("result").style.color = "green";
        }
        else if (result.final_verdict == "SUSPICIOUS") {
            document.getElementById("result").style.color = "orange";
        }
        else if (result.final_verdict == "BLOCKED") {
            document.getElementById("result").style.color = "red";
        }

    })

    .catch(error => {

        console.log(error);

    });

}