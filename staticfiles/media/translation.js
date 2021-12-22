
var button = document.getElementById("langBTN").onclick = async () =>{
    var text = document.getElementById("description");
    console.log(text.innerText);
    var url = "http://127.0.0.1:8000/trans?words=" + text.innerText;
    const res = await fetch(url);
    const resJson = await res.json();
    console.log(resJson['result'])
};