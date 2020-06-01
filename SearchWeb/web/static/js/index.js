/*
var chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/');

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    console.log(message);
  };

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
  };
*/
console.log("test")

//URL = "http://172.16.217.132:9200/sitedb/instance/_search"
URL = "http://127.0.0.1:9200/sitedb/_search"

page = 1
pageSize = 10;
var searchTextValue = ''

document.getElementById("id_of_textbox")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        document.getElementById("id_of_button").click();
    }
});


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

	//chatSocket.send(JSON.stringify({
        //'message': ""
    //}));
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

	page = parseInt(page)
	if(page-2 > 0)
		i = page-2;
	else
		i = 1;
	if(page+2 <= pagecount)
		end = page+2;
	else
		end = pagecount;

	if(i==1){
		if(pagecount>=5)
			end = 5;
		else
			end = pagecount;
	}
	if(end==pagecount && i!=1){
		if( (end-4)>0 )
			i = end-4;
		else
			i = 1;
	}

	console.log(i)
	console.log(end)
	console.log(pagecount)
	console.log(page)
	
    document.querySelectorAll('.page > a').forEach(e => e.remove());;
    var pageDiv = document.querySelector('.page');
    for(var i; i<=end; i++){
	    var link = document.createElement("a")
	    link.href = window.location.origin + "/search/" + encodeURIComponent(searchTextValue) + "/" + (i)
	    node = document.createTextNode(i);
		link.appendChild(node);
	    
	    if(page == i){
	    	link.href = "javascript:return false;";
	    	link.classList.add("currentPage");
	    }
	    pageDiv.appendChild(link);
	}


    for (i=start; i<result.length && i<start+pageSize; i++){
    	//console.log(result[i]['_source']['title'])
    	//console.log(result[i]['_source']['content'])
    	//console.log(result[i]['_source']['URL'])

    	var para = document.createElement("div");
    	para.classList.add("resultHtmlList");
    	var br = document.createElement("br");

    	var link = document.createElement("a");
    	if(result[i]['_source']['URL'].length > 65)
    		RESULTURL = result[i]['_source']['URL'].slice(0, 65) + ' ...'
    	else
    		RESULTURL = result[i]['_source']['URL']
    	var node = document.createTextNode(RESULTURL);
    	link.appendChild(node);
    	link.href = result[i]['_source']['URL'];
    	para.appendChild(link);
    	para.appendChild(br);

    	var p = document.createElement("p");
    	if(result[i]['_source']['title'].length > 78)
    		RESULTTITLE = result[i]['_source']['title'].slice(0, 78) + ' ...'
    	else
    		RESULTTITLE = result[i]['_source']['title']
    	node = document.createTextNode(RESULTTITLE);
    	link = document.createElement("a");
    	link.href = result[i]['_source']['URL'];
    	link.classList.add("titleStyle");
    	link.appendChild(node);
    	p.appendChild(link);
		para.appendChild(p);

		//console.log(result[i]['highlight']['content'][0])
		p = document.createElement("p");
		if(typeof(result[i]['highlight']['content']) == 'undefined'){
			if(result[i]['_source']['content'].length > 125)
	    		RESULTCONTENT = result[i]['_source']['content'].slice(0, 125) + ' ...'
	    	else
	    		RESULTCONTENT = result[i]['_source']['content']
			p.innerHTML = RESULTCONTENT;
		}
		else{
			if(result[i]['highlight']['content'][0].length > 125)
	    		RESULTCONTENT = result[i]['highlight']['content'][0].slice(0, 125) + ' ...'
	    	else
	    		RESULTCONTENT = result[i]['highlight']['content'][0]
			p.innerHTML = RESULTCONTENT;
		}

		para.appendChild(p);

		para.classList.add("fadeInUp");
		element.appendChild(para);
    }

    if(json['hits']['hits'].length==0){
    	var para = document.createElement("div");
    	para.classList.add("resultHtmlList");
    	p = document.createElement("p");
    	p.innerHTML = ("無法找到匹配的結果");
    	para.appendChild(p);
    	para.classList.add("fadeInUp");
		element.appendChild(para);
    }

    if(pageContent == '')
    	window.history.pushState(null, null, window.location.origin + "/search/" + encodeURIComponent(searchTextValue) + "/" + 1);
    else
    	window.history.pushState(null, null, window.location.origin + "/search/" + encodeURIComponent(searchTextValue) + "/" + pageContent);
}

