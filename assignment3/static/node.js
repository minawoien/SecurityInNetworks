async function getTables(route, id){
    let response = await fetch('/'+route);
    if (response.status == 200){
        let result = await response.json();
        for (let [key, value] of Object.entries(result)){
            if (typeof(value) == "object"){
                for (let [filename, hash] of Object.entries(value[1])){
                    document.getElementById(id).innerHTML += '<tr><td>'+key+'</td><td>'+value[0]+'</td><td>'+filename+'</td><td>'+hash+'</td><td><input type="submit" value="x" onclick="request();"></td></td></tr>';
                }
            }else {
                document.getElementById(id).innerHTML += '<tr><td>'+key+'</td><td>'+value+'</td></tr>';
            }
        }
    }
}

async function request(key){
    console.log(key)
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
        location.reload(); 
    }
}

window.onload = function(){
    getTables('getNodes', 'routing', false);
    getTables('getHashTable', 'hashTable', true)
}
