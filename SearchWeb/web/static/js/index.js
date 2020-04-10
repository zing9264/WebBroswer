
console.log("test")

/*
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
*/

searchBtn = document.querySelector('input[name="searchBtn"]');
searchBtn.addEventListener("click", searchFn);

function searchFn(){

	searchText = document.querySelector('input[name="search"]');
	console.log(searchText.value)

	fetchData(searchText.value)
}



function fetchData(searchText){

	data = {
	  "query" : { "match" : { "title" : "" }}
	}

	data['query']['match']['title'] = searchText
	//console.log(data)

	fetch("http://172.16.217.132:9200/test/instance/_search", {
			contentType: 'application/json',
			method: 'POST',
			body: JSON.stringify(data)
			})
	        .then(_onResponse)
	        .then(_onJsonReady);
}

function _onResponse(response) {
	console.log(response)
	return response.json();
}

function _onJsonReady(json) {
    console.log(json);
    console.log(json['hits']['hits'])
    result = json['hits']['hits']

    var element = document.querySelector('#resultHtml');
    document.querySelectorAll('.resultHtmlList').forEach(e => e.remove());;


    for (var i=0; i<result.length; i++){
    	//console.log(result[i]['_source']['title'])
    	//console.log(result[i]['_source']['content'])
    	//console.log(result[i]['_source']['url'])

    	var para = document.createElement("div");
    	para.classList.add("resultHtmlList");
    	var br = document.createElement("br");

    	var link = document.createElement("a");
    	var node = document.createTextNode(result[i]['_source']['url']);
    	link.appendChild(node);
    	link.href = result[i]['_source']['url'];
    	para.appendChild(link);
    	para.appendChild(br);

    	
    	node = document.createTextNode(result[i]['_source']['title']);
		para.appendChild(node);
		br = document.createElement("br");
		para.appendChild(br);

		node = document.createTextNode(result[i]['_source']['content']);
		para.appendChild(node);

		element.appendChild(para);
    }
}

