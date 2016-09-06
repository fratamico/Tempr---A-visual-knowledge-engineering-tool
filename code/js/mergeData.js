// Load text with Ajax synchronously: takes path to file and optional MIME type
function loadTextFileAjaxSync(filePath, mimeType) {
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.open("GET",filePath,false);
    if (mimeType != null) {
        if (xmlhttp.overrideMimeType) {
            xmlhttp.overrideMimeType(mimeType);
        }
    }
    xmlhttp.send();
    if (xmlhttp.status==200) {
        return xmlhttp.responseText;
    } else {
        // TODO Throw exception
        return null;
    }
}

function mergeData(newName, arrayToMerge) {
    var filePath = "processing/json_files/ALL_ACTIONS_FREQUENCY.json";
    var json = loadTextFileAjaxSync(filePath, "application/json");
    json_object = JSON.parse(json);

    //return json;  
}