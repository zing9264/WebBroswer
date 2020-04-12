
console.log("test")

//URL = "http://172.16.217.132:9200/sitedb/instance/_search"
URL = "http://127.0.0.1:9200/sitedb/_search"

page = 1
pageSize = 5;
var searchTextValue = ''

pageContent = document.querySelector('.NonDisplay-Page').textContent;
if(pageContent != '')
	page = pageContent
console.log(page)


divText = document.querySelector('.NonDisplay');
textContent = decodeURIComponent(divText.textContent)
//console.log(divText.textContent)

if(divText.textContent != ''){
	document.querySelector('input[name="search"]').value = textContent;
	searchTextValue = textContent;
	fetchData(searchTextValue)
}


searchBtn = document.querySelector('input[name="searchBtn"]');
searchBtn.addEventListener("click", searchFn);

function searchFn(){
	searchText = document.querySelector('input[name="search"]');
	console.log(searchText.value)

	page = 1;
	pageContent = ''
	document.querySelector('.NonDisplay-Page').textContent = '';
	document.querySelector('.NonDisplay').textContent = '';
	searchTextValue = searchText.value
	fetchData(searchText.value)
}


function fetchData(searchText){

	data ={
	    "query": {
	        "query_string" : {
	          "query" : "",
	          "fields" : ["title", "content"],
	          "analyzer": "ik_max_word"
	        }
	    },
	    "size": 1000,
	    "from": 0,
	    "highlight": {
	      "pre_tags": ["<span>", "<tag2>"],
	      "post_tags": ["</span>", "</tag2>"],
	      "fields": {
	        "title": {},
	        "content": {},
	        "URL": {}
	      }
	    }
	}

	data['query']['query_string']['query'] = searchText
	//console.log(data)

	fetch(URL, {
			headers: {
		      'content-type': 'application/json'
		    },
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


    pagecount = Math.ceil(result.length / pageSize)
    start = (page - 1) * pageSize

    document.querySelectorAll('.page > a').forEach(e => e.remove());;
    var pageDiv = document.querySelector('.page');
    for(var i=0; i<pagecount; i++){
	    var link = document.createElement("a")
	    link.href = window.location.origin + "/search/" + encodeURIComponent(searchTextValue) + "/" + (i+1)
	    node = document.createTextNode(i+1);
		link.appendChild(node);
	    
	    if(page == i+1){
	    	link.href = "javascript:return false;";
	    	link.classList.add("currentPage");
	    }
	    pageDiv.appendChild(link);
	}

    for (var i=start; i<result.length && i<start+pageSize; i++){
    	//console.log(result[i]['_source']['title'])
    	//console.log(result[i]['_source']['content'])
    	//console.log(result[i]['_source']['URL'])

    	var para = document.createElement("div");
    	para.classList.add("resultHtmlList");
    	var br = document.createElement("br");

    	var link = document.createElement("a");
    	var node = document.createTextNode(result[i]['_source']['URL']);
    	link.appendChild(node);
    	link.href = result[i]['_source']['URL'];
    	para.appendChild(link);
    	para.appendChild(br);

    	var p = document.createElement("p");
    	node = document.createTextNode(result[i]['_source']['title']);
    	link = document.createElement("a");
    	link.href = result[i]['_source']['URL'];
    	link.classList.add("titleStyle");
    	link.appendChild(node);
    	p.appendChild(link);
		para.appendChild(p);

		//console.log(result[i]['highlight']['content'][0])
		p = document.createElement("p");
		if(typeof(result[i]['highlight']['content']) == 'undefined')
			p.innerHTML = (result[i]['_source']['content']);
		else
			p.innerHTML = result[i]['highlight']['content'][0];

		para.appendChild(p);

		para.classList.add("fadeInUp");
		element.appendChild(para);
    }

    if(pageContent == '')
    	window.history.pushState(null, null, window.location.origin + "/search/" + encodeURIComponent(searchTextValue) + "/" + 1);
    else
    	window.history.pushState(null, null, window.location.origin + "/search/" + encodeURIComponent(searchTextValue) + "/" + pageContent);
}

