
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



threadIp1 = document.querySelector('#thread-ip-1');
threadURL1 = document.querySelector('#thread-URL-1');
threadLevel1 = document.querySelector('#thread-level-1');
threadSpeed1 = document.querySelector('#thread-speed-1');
threadPasstime1 = document.querySelector('#thread-passtime-1');
threadTotalfetchcnt1 = document.querySelector('#thread-totalfetchcnt-1');
threadQueuecnt1 = document.querySelector('#thread-queuecnt-1');
threadSuccesscnt1 = document.querySelector('#thread-successcnt-1');
threadFailcnt1 = document.querySelector('#thread-failcnt-1');
threadRedundancyURLcnt1 = document.querySelector('#thread-redundancyURLcnt-1');
var threadDate1 = [threadIp1,threadURL1,threadLevel1,threadTotalfetchcnt1,threadQueuecnt1,threadFailcnt1,threadSuccesscnt1,threadRedundancyURLcnt1,threadSpeed1,threadPasstime1]

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
        data = allRows[1].split(',');
        console.log(data)
        let i;
        for (i = 0; i < threadDate1.length; i++) {
            threadDate1[i].innerHTML=data[i]
        }
        threadDate1[1].herf=data[1]
        if(xhr.status == 200){
        }else{
            console.log("????");
        }
    }
}

operatingStatuses = document.querySelectorAll('.operating-status');
seedUrls = document.querySelectorAll('.seed-url');
lastUrls = document.querySelectorAll('.last-url');
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
            for (i = 0; i < 4; i++) {
                data = allRows[i+1].split(',');
                operatingStatuses[i].innerHTML = data[1]
                seedUrls[i].innerHTML=data[2]
                lastUrls[i].innerHTML=data[3]
                levels[i].innerHTML=data[4]
                waitTimes[i].innerHTML=data[5]
            }

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
