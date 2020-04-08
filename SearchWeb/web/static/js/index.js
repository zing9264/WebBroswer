
console.log("test")

data = {
  "query" : { "match" : { "content" : "測試" }}
}

fetch("http://172.16.217.132:9200/test/instance/_search", {
		contentType: 'application/json',
		method: 'POST',
		body: JSON.stringify(data)
		})
        .then(_onResponse)
        .then(_onJsonReady);

function _onJsonReady(json) {
    console.log(json);
}

function _onResponse(response) {
	console.log(response)
	return response.json();
}