
const csrf_token = document.querySelector('#csrfmiddlewaretoken');

fetch('http://127.0.0.1:8000/getcsrf/', {}).then((response) => {
    console.log(response);
    return response.json(); 
  }).then((data) => {
      console.log(data);
      csrf_token.value =data['csrf_token'];
  }).catch((err) => {
    console.log('éŒ¯èª¤:', err);
});


threadIps = document.querySelectorAll('.thread-ip');
threadURLs = document.querySelectorAll('.thread-URL');
threadLevels = document.querySelectorAll('.thread-level');
threadSpeeds = document.querySelectorAll('.thread-speed');
threadPasstimes = document.querySelectorAll('.thread-passtime');
threadTotalfetchcnts = document.querySelectorAll('.thread-totalfetchcnt');
threadQueuecnts = document.querySelectorAll('.thread-queuecnt');
threadSuccesscnts = document.querySelectorAll('.thread-successcnt');
threadFailcnts = document.querySelectorAll('.thread-failcnt');
threadRedundancyURLcnts = document.querySelectorAll('.thread-redundancyURLcnt');

function getbatchcsv_ajax(url, success, fail){
// 1. ????
    var xhr = null;
    xhr = new XMLHttpRequest()
// 2. ?????
    xhr.open('get', url, true)
// 3. ????
    xhr.send(null);
// 4. ????
    xhr.onload = function () {
        //console.log(xhr.responseText);
        var allRows = xhr.responseText.split(/\r?\n|\r/);
        //console.log(allRows)IP,????,????,???,????,???,???,??URL?,??,????
        let i=0
        for (i = 0; i < 4; i++) {
            data = allRows[i].split(',');
            threadIps[i].innerHTML = data[0]
            threadURLs[i].href = data[1]
            threadURLs[i].innerHTML=data[1]
            threadLevels[i].innerHTML=data[2]
            threadTotalfetchcnts[i].innerHTML=data[3]
            threadQueuecnts[i].innerHTML = data[4]
            threadFailcnts[i].innerHTML = data[5]
            threadSuccesscnts[i].innerHTML=data[6]
            threadRedundancyURLcnts[i].innerHTML=data[7]
            threadSpeeds[i].innerHTML=data[8]
            threadPasstimes[i].innerHTML = data[9]
        }
        console.log(data)
        if(xhr.status == 200){
        }else{
            console.log("????");
        }
    }
}

operatingStatuses = document.querySelectorAll('.operating-status');
seedUrls = document.querySelectorAll('.seed-url');
levels = document.querySelectorAll('.level');
waitTimes = document.querySelectorAll('.wait-time');
isThreadRunning=document.querySelector('#is-thread-running')
function MU_csv_ajax(url, success, fail){
    // 1. ????
        var xhr = null;
        xhr = new XMLHttpRequest()
    // 2. ?????
        xhr.open('get', url, true)
    // 3. ????
        xhr.send(null);
    // 4. ????
        xhr.onload = function () {
            //console.log(xhr.responseText);
            var allRows = xhr.responseText.split(/\r?\n|\r/);
            console.log(allRows)
            let i=0
            for (i = 0; i < 4; i++) {
                data = allRows[i+1].split(',');
                operatingStatuses[i].innerHTML = data[1]
                seedUrls[i].innerHTML=data[2]
                levels[i].innerHTML=data[3]
                waitTimes[i].innerHTML=data[4]
            }
            isThreadRunning.innerHTML=allRows[5][0]
            document.querySelector('#thread-operating-status-1').innerHTML=operatingStatuses[0].innerHTML;
            document.querySelector('#thread-operating-status-2').innerHTML=operatingStatuses[1].innerHTML;
            document.querySelector('#thread-operating-status-3').innerHTML=operatingStatuses[2].innerHTML;
            document.querySelector('#thread-operating-status-4').innerHTML=operatingStatuses[3].innerHTML;

            if(xhr.status == 200){
            }else{
                console.log("????");
            }
        }
}

function BanDB_ajax(url, success, fail){
        // 1. ????
            var xhr = null;
            xhr = new XMLHttpRequest()
        // 2. ?????
            xhr.open('get', url, true)
        // 3. ????
            xhr.send(null);
        // 4. ????
            xhr.onload = function () {
                //console.log(xhr.responseText);
                var allRows = xhr.responseText.split(/\r?\n|\r/);
                console.log(allRows)
                screen = '<div class="row" id="ban-ip-screen">'
                for (i = 0; i < allRows.length; i++){
                    screen+= '<div class="col-3" >'+allRows[i]+'</div>'
                }
                screen+= '</div>'
                document.getElementById('ban-ip-screen').outerHTML = screen
                
                if(xhr.status == 200){
                }else{
                    console.log("????");
                }
            }
}

function insertBanIp(url, success, fail){
    // 1. ????
    var xhr = null;
    k=document.getElementById('insert-ban-ip').value
    console.log(k);
        xhr = new XMLHttpRequest()
    // 2. ?????
        xhr.open('get', 'insertbanindb/?insertBanIp='+k, true)
    // 3. ????

        xhr.send(null);
    // 4. ????
        xhr.onload = function () {
            //console.log(xhr.responseText);
            if(xhr.status == 200){
            }else{
                console.log("????");
            }
        }
}

function deleteBanIp(url, success, fail){
    // 1. ????
    var xhr = null;
    k=document.getElementById('delete-ban-ip').value
    console.log(k);
        xhr = new XMLHttpRequest()
    // 2. ?????
        xhr.open('get', 'deletebanindb/?deleteBanIp='+k, true)
    // 3. ????

        xhr.send(null);
    // 4. ????
        xhr.onload = function () {
            //console.log(xhr.responseText);
            if(xhr.status == 200){
            }else{
                console.log("????");
            }
        }
}

function getURLQueue(thread, success, fail){
    // 1. ????
        var xhr = null;
        xhr = new XMLHttpRequest()
    // 2. ?????
        console.log('getURLQueue');

        xhr.open('get', 'geturlqueue/?thread=' + thread, true)
    // 3. ????
        xhr.send(null);
    // 4. ????
        xhr.onload = function () {
            //console.log(xhr.responseText);
            var allRows = xhr.responseText.split(/\r?\n|\r/);
            //console.log(allRows)IP,????,????,???,????,???,???,??URL?,??,????
            let i = 0
            screen = '<div class="row" id="url-queue"' + thread + ' >'
            screen+='<table class="table table-bordered table-dark" style="word-break:break-all"><thead><tr><th scope="col">#</th><th scope="col">URL</th><th scope="col">Level</th><th scope="col">ParentUrl</th></tr></thead><tbody>'
            for (i = 0; i < allRows.length-1; i++){
                data = allRows[i].split(',');
                console.log(data)
                screen += '<tr><th scope="row">' + i + '</th>'
                screen += '<td class="queue-URL">' + data[0] + '</td>'
                screen += '<td class="queue-Level">' + data[1] + '</td>'
                screen += '<td class="queue-ParentURL">' + data[2] + '</td></tr>'
            }
            screen += '</tbody></table></div>'
            document.getElementById('url-queue-'+thread).outerHTML = screen

            if(xhr.status == 200){
            }else{
                console.log("????");
            }
        }
    }

    function getFailURL(thread, success, fail){
        // 1. ????
            var xhr = null;
            xhr = new XMLHttpRequest()
        // 2. ?????
    
            xhr.open('get', 'getfailurl/?thread=' + thread, true)
        // 3. ????
            xhr.send(null);
        // 4. ????
            xhr.onload = function () {
                //console.log(xhr.responseText);
                var allRows = xhr.responseText.split(/\r?\n|\r/);
                //console.log(allRows)IP,????,????,???,????,???,???,??URL?,??,????
                let i = 0

                screen = '<div class="row" id="fail-url-1"'+thread+' >'
                screen+='<table class="table table-bordered table-dark" style="word-break:break-all"><thead><tr><th scope="col">#</th><th scope="col">URL</th><th scope="col">ParentURL</th><th scope="col">Errorcode</th></tr></thead><tbody>'
                for (i = allRows.length-2; i > 0; i--){
                    data = allRows[i].split(',');
                    console.log(data)
                    screen += '<tr><th scope="row">' + i + '</th>'
                    screen += '<td class="fail-URL">' + data[0] + '</td>'
                    screen += '<td class="fail-ParentURL">' + data[1] + '</td>'
                    screen += '<td class="fail-Errorcode">' + data[2] + '</td></tr>'
                }
                screen += '</tbody></table></div>'
                document.getElementById('fail-url-'+thread).outerHTML = screen
    
                if(xhr.status == 200){
                }else{
                    console.log("????");
                }
            }
        }
    
    function getFilter( success, fail){
            // 1. ????
                var xhr = null;
                xhr = new XMLHttpRequest()
            // 2. ?????
        
                xhr.open('get', 'getfilter/' , true)
            // 3. ????
                xhr.send(null);
            // 4. ????
                xhr.onload = function () {
                    //console.log(xhr.responseText);
                    var allRows = xhr.responseText.split(/\r?\n|\r/);
                    //console.log(allRows)IP,????,????,???,????,???,???,??URL?,??,????
                    let i = 0
    
                    screen = '<div class="row" id="filt-string-screen" >'
                    for (i = 0; i < allRows.length-1; i++){
                        data = allRows[i].split(',');
                        console.log(data)
                        screen += '<div class="col-4">' + data[0] + '</div>'
                    }
                    screen += '</div>'
                    document.getElementById('filt-string-screen').outerHTML = screen
                    if(xhr.status == 200){
                    }else{
                        console.log("????");
                    }
                }
            }
            function deleteFilter( success, fail){
                // 1. ????
                    var xhr = null;
                    xhr = new XMLHttpRequest()
                // 2. ?????
                data = document.getElementById('delete-filt-string').value 
                console.log(data)
                    xhr.open('get', 'deletefilter/?data='+data , true)
                // 3. ????
                    xhr.send(null);
                // 4. ????
                    xhr.onload = function () {
                        //console.log(xhr.responseText);
                        if (xhr.status == 200) {
                            
                        }else{
                            console.log("????");
                        }
                    }
            }
    function insertFilter( success, fail){
        // 1. ????
        var xhr = null;
        xhr = new XMLHttpRequest()
    // 2. ?????
        data = document.getElementById('insert-filt-string').value 

        xhr.open('get', 'insertfilter/?data='+data , true)
    // 3. ????
        xhr.send(null);
    // 4. ????
        xhr.onload = function () {
            //console.log(xhr.responseText);
            if (xhr.status == 200) {
                
            }else{
                console.log("????");
            }
        }
    }

    function getAllIPData(searchText){

        data = {
            "sort" : [
                {
                    "beConnectedCount": { "order": "desc" },
                    'fetchCount':{ "order": "desc" },
                }
                
            ],
            'size':5000,
            "query": {
                "match": {
                    "for_fetch": "1"
                }
            }
        }
        //console.log(data)
        url = 'http://127.0.0.1:9200/ipdb/_search'

        fetch(url, {
                headers: {
                  'content-type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify(data)
                })
                .then(_onAllIPDataResponse)
                .then(_onAllIPDataJsonReady);
    
    }
    
    function _onAllIPDataResponse(response) {
        console.log(response)
        return response.json();
    }
    
    function _onAllIPDataJsonReady(json) {
        console.log(json);
        data = json['hits']['hits']

        let i = 0
        screen = '<div class="card-body main-ctrl " id="IP-control-screen">'
        screen+='<table class="table table-bordered table-dark" style="word-break:break-all"><thead><tr><th scope="col">#</th><th scope="col">ip</th><th scope="col">被連結數量</th><th scope="col">此IP下網頁數量</th></tr></thead><tbody>'
        for (i = 0; i < data.length-1; i++){
            console.log(data)   
            screen += '<tr><th scope="row">' + i + '</th>'
            screen += '<td class="ipData-ip_addr">' + data[i]['_source']['ip_addr'] + '</td>'
            screen += '<td class="ipData-beConnectedCount">' + data[i]['_source']['beConnectedCount'] + '</td>'
            screen += '<td class="ipData-fetchCount">' + data[i]['_source']['fetchCount'] + '</td></tr>'
        }
        screen += '</tbody></table></div>'
        document.getElementById('IP-control-screen').outerHTML = screen
    
    }


    function getAllredundancyUrlData(searchText){

        data = {
            "sort" : [
                {
                    "fetchCount": { "order": "desc" },
                }
                
            ],
            'size':5000,
            "query" : {
                "range" : {
                    "fetchCount" : {
                        "gt" :1,
                    }
                }
            }
        }
        //console.log(data)
        url = 'http://127.0.0.1:9200/sitedb/_search'

        fetch(url, {
                headers: {
                  'content-type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify(data)
                })
                .then(_onAllRedundancyUrlDataResponse)
                .then(_onAllRedundancyUrlDataJsonReady);
    
    }
    
    function _onAllRedundancyUrlDataResponse(response) {
        console.log(response)
        return response.json();
    }
    
    function _onAllRedundancyUrlDataJsonReady(json) {
        console.log(json);
        data = json['hits']['hits']

        let i = 0
        screen = '<div class="card-body main-ctrl " id="redundancyUrl-screen">'
        screen+='<table class="table table-bordered table-dark" style="word-break:break-all"><thead><tr><th scope="col">#</th><th scope="col">URL</th><th scope="col">重複次數</th><th scope="col">ip_addr</th><th scope="col">title</th><th scope="col">lastFetchTime</th><th scope="col">content</th></tr></thead><tbody>'
        for (i = 0; i < data.length-1; i++){
            console.log(data)   
            screen += '<tr><th scope="row">' + i + '</th>'
            screen += '<td class="redundancyUrl-URL">' + data[i]['_source']['URL'] + '</td>'
            screen += '<td class="redundancyUrl-fetchCount">' + data[i]['_source']['fetchCount'] + '</td>'
            screen += '<td class="redundancyUrl-ip_addr">' + data[i]['_source']['ip_addr'] + '</td>'
            screen += '<td class="redundancyUrl-title">' + data[i]['_source']['title'] + '</td>'
            screen += '<td class="redundancyUrl-lastFetchTime">' + data[i]['_source']['lastFetchTime'] + '</td>'
            screen += '<td class="redundancyUrl-content">' + data[i]['_source']['content'].substr(0,25) + '</td></tr>'
        }
        screen += '</tbody></table></div>'
        document.getElementById('redundancyUrl-screen').outerHTML = screen
}
    
function doUpdate()   
{
    getbatchcsv_ajax('getbatchcsv/');
    MU_csv_ajax('getMutualState/');
    BanDB_ajax('getbanindb/')
    //getFailURL('getfailurl/')

    window.setTimeout("doUpdate()", 5000);
}
doUpdate();

// <div class="col-6" >
// <span>??IP:<span id='thread-ip-1'></span></span>
// <br>
// <span>????:<span id='thread-level-1'></span></span>
// <br>
// <span>????:<span id='thread-speed-1'></span></span>
// <br>
// <span>????:<span id='thread-passtime-1'></span></span>
// <br>
// </div>
// <div class="col-6 " >
// <span>???:<span id='thread-totalfetchcnt-1'></span></span>
// <br>                                        
// <span>????:<span id='thread-queuecnt-1'></span></span>
// <br>                                    
// <span>???:<span id='thread-successcnt-1'></span></span>
// <br>
// <span>???:<span id='thread-failcnt-1'></span></span>
// <br>
// <span>??URL?:<span id='thread-redundancyURLcnt-1'></span></span>
// <br>
// </div>
