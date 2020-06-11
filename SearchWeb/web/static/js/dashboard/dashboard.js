
const csrf_token = document.querySelector('#csrfmiddlewaretoken');

fetch('http://127.0.0.1:8000/getcsrf/', {}).then((response) => {
    console.log(response);
    return response.json(); 
  }).then((data) => {
      console.log(data);
      csrf_token.value =data['csrf_token'];
  }).catch((err) => {
    console.log('錯誤:', err);
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
        //console.log(allRows)
        let i=0
        for (i = 0; i < 4; i++) {
            data = allRows[i].split(',');
            threadIps[i].innerHTML = data[0]
            threadURLs[i].herf = data[1]
            threadURLs[i].innerHTML=data[1]
            threadLevels[i].innerHTML=data[2]
            threadSpeeds[i].innerHTML=data[3]
            threadPasstimes[i].innerHTML = data[4]
            threadTotalfetchcnts[i].innerHTML = data[5]
            threadQueuecnts[i].innerHTML=data[6]
            threadSuccesscnts[i].innerHTML=data[7]
            threadFailcnts[i].innerHTML=data[8]
            threadRedundancyURLcnts[i].innerHTML = data[9]
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
    


function doUpdate()   
{
    getbatchcsv_ajax('getbatchcsv/');
    MU_csv_ajax('getMutualState/')
    window.setTimeout("doUpdate()", 4000);
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
