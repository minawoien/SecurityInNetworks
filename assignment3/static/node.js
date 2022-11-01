async function getNodes(){
    let response = await fetch("/getNodes");
    if (response.status == 200){
        let result = await response.json();
        for (let [key, value] of Object.entries(result)){
            console.log(key)
            console.log(value)
            document.getElementById('routing').innerHTML += '<tr><td>'+key+'</td><td>'+value+'</td></tr>';
        } 
        console.log("hei");
        console.log(result);
    }
}

window.onload = function(){
    console.log("hello hello");
    getNodes();
}

async function uploadFile(){
    let file = document.getElementById("uploadedFile").files[0];
    let formData = new FormData();
    formData.append("file", file)
    let response = await fetch("/uploadFile", {
        method: 'POST',
        body: formData
    });
    if (response.status == 200){
        console.log("hell")
    }
}

