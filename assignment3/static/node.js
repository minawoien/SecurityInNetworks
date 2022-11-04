let interval;

// Get routing table and update the table
async function getRoutingTable(){
    let response = await fetch('/getNodes');
    if (response.status == 200){
        let result = await response.json();
        document.getElementById('routing').innerHTML = '<tr><th>Guid</th><th>Address</th></tr>';
        for (let [key, value] of Object.entries(result)){
            document.getElementById('routing').innerHTML += '<tr><td>'+key+'</td><td>'+value+'</td></tr>';
        }
    }
}

// Get hash table and update the table
async function getHashTable(){
    let response = await fetch('/getHashTable');
    if (response.status == 200){
        let result = await response.json();
        document.getElementById('hashTable').innerHTML = '<tr><th>Guid</th><th>Public key</th><th>Filename</th><th>Hash value</th><th>Request access</th></tr>';
        for (let [key, value] of Object.entries(result)){
            for (let [filename, hash] of Object.entries(value[1])){
                document.getElementById('hashTable').innerHTML += '<tr id='+key+filename+'><td>'+key+'</td><td>'+value[0]+'</td><td>'+filename+'</td><td>'+hash+'</td><td><input type="submit" value="x" onclick="request(this.parentNode.parentNode.id);"></td></td></tr>';
            }
        }
    }
}

// Request a file
async function request(id){
    guid = id.substring(0,36)
    filename = id.substring(36)
    await fetch('/requestFile', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({guid: guid, filename: filename})
    });
}

// Upload a file
async function uploadFile(){
    let file = document.getElementById("uploadedFile").files[0];
    let formData = new FormData();
    formData.append("file", file)
    await fetch("/uploadFile", {
        method: 'POST',
        body: formData
    });
}

// Get the routing and hash table
function getTables(){
    getRoutingTable()
    getHashTable()
}

// Get the routing and hash table with updated values every second
window.onload = function(){
    interval = setInterval(getTables, 1000);
}
