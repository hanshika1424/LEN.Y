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

    document.getElementById("result-card").style.display = "block";

    document.getElementById("result-status").innerHTML =
        "Message Analysis";

    document.getElementById("confidence").innerHTML =
        "Extracted information";

    document.getElementById("bank-check").innerHTML =
        "Message ID: " + messageID + "<br>" +
        "Customer ID: " + customerID + "<br>" +
        "Phone Number: " + phone;

    document.getElementById("ai-check").innerHTML =
        "Department: " + department + "<br>" +
        "Sender: " + sender + "<br>" +
        "Time: " + timestamp;

    document.getElementById("department-check").innerHTML =
        "Message Body: " + body;

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

        document.getElementById("result-card").style.display = "block";

        document.getElementById("result-status").innerHTML =
    result.final_verdict;

        document.getElementById("confidence").innerHTML =
            "Confidence Score: " + result.confidence_score + "%";

        document.getElementById("bank-check").innerHTML =
            "✓ Database Check: " + result.db_check.reason;

        document.getElementById("recommendation").innerHTML =
            result.final_verdict == "VERIFIED"
            ? "This message appears to be authentic."
            : "Do not click links or share sensitive information.";

        if (result.final_verdict == "VERIFIED") {
            document.getElementById("result-status").style.color = "green";
        }
        else if (result.final_verdict == "SUSPICIOUS") {
            document.getElementById("result-status").style.color = "orange";
        }
        else if (result.final_verdict == "BLOCKED") {
            document.getElementById("result-status").style.color = "red";
        }

    })

    .catch(error => {

        console.log(error);

    });

}
