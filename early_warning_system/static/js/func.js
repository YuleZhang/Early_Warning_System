    //读取规则信息
    function loadRulesInfo(){
        var httpRequest = new XMLHttpRequest();//第一步：创建需要的对象
        httpRequest.open('POST', '/searchRules', true); //第二步：打开连接
        httpRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
        httpRequest.send('');//use file path as parameter
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
            if (httpRequest.readyState == 4 && httpRequest.status == 200) {//验证请求是否发送成功
                var json = JSON.parse(httpRequest.responseText);//获取到服务端返回的数据
                console.log(json);
                for(var idx in json){
                    addRow(json[idx][0],json[idx][3],json[idx][4],json[idx][5],json[idx][6],json[idx][7],json[idx][8]);
                    // addRow(json[idx]['fileID'],json[idx]['fileName'],json[idx]['fileUrl'],json[idx]['fileDate']);
                }
                
            }
        };
    }
    
    // //读取CSV文件
    // function buildRules(){
    //         //get the file path and send it to flask
    //         // var file = document.getElementById("file").files[0];
    //         var sIndex = document.getElementById('support').selectedIndex;
    //         var cIndex = document.getElementById('confidence').selectedIndex;
    //         var support = document.getElementById('support').options[sIndex].value;
    //         var confidence = document.getElementById('confidence').options[cIndex].value;
    //         // if (file == undefined) return;
    //         // console.log(file)
    //         //generate HTTPXML Request
    //         var httpRequestProgress = new XMLHttpRequest();//第一步：创建需要的对象
    //         var sitv = setInterval(function(){
    //             httpRequestRules.setRequestHeader("Content-type","application/x-www-form-urlencoded");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
    //             httpRequestProgress.open('POST','/buildRuleProgress',true);
    //             httpRequestRules.onreadystatechange = function () {
    //                 if (httpRequestRules.readyState == 4 && httpRequestRules.status == 200) {
    //                     var res = JSON.parse(httpRequestRules.responseText);
    //                     console.log(res)
    //                     $('#prog_in').width(res + '%');     // 改变进度条进度，注意这里是内层的div， res是后台返回的进度
    //                 }
    //             }
    //         }, 1000);                                 // 每1秒查询一次后台进度
    //         var httpRequestRules = new XMLHttpRequest();
    //         httpRequestRules.open('POST', '/generateRules', true);
    //         httpRequestRules.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    //         httpRequestRules.send('support='+support+'&confidence='+confidence);
    //         httpRequestRules.onreadystatechange = function () {
    //             if (httpRequestRules.readyState == 4 && httpRequestRules.status == 200) {
    //                 var json = JSON.parse(httpRequestRules.responseText);
    //                 clearInterval(sitv);
    //                 $('#prog_out').attr("class", "progress progress-bar-success");
    //                 for(var idx in json){
    //                     addRow(json[idx][0],json[idx][3],json[idx][4],json[idx][5],json[idx][6],json[idx][7],json[idx][8]);
    //                     // addRow(json[idx]['fileID'],json[idx]['fileName'],json[idx]['fileUrl'],json[idx]['fileDate']);
    //                 }
                    
    //             }
    //         };
    //         alert("生成完毕");
    // };
    function buildRules(){
        var sIndex = document.getElementById('support').selectedIndex;
        var cIndex = document.getElementById('confidence').selectedIndex;
        var support = document.getElementById('support').options[sIndex].value;
        var confidence = document.getElementById('confidence').options[cIndex].value;
        var sitv = setInterval(function(){
            var prog_url = '/buildRuleProgress'                   // prog_url指请求进度的url，后面会在django中设置
            $.getJSON(prog_url, function(res){ 
                $('#prog_in').width(res + '%');     // 改变进度条进度，注意这里是内层的div， res是后台返回的进度
                console.log(res)
            });
        }, 1000);                                 // 每1秒查询一次后台进度
        var this_url = '/generateRules'                        // 指当前页面的url
        var yourjson = {"support":support,'confidence':confidence}
        $.getJSON(this_url, {"support":support,'confidence':confidence}, function(res){ 
            // ...
            clearInterval(sitv);                   // 此时请求成功返回结果了，结束对后台进度的查询
            $('#prog_out').attr("class", "progress progress-bar-success"); // 修改进度条外层div的class, 改为完成形态
        });
    }
    //添加一行
    function addRow(idx,...info){ 
            var result="";
            result +="<tr>";
            result +="<td style='text-align: left;'>"+idx+"</td>";
            for(let item of info){
                result +="<td style='text-align: left;'>"+item+"</td>";
            }
            result +="</tr>";
            $("#rulesTB tbody").append(result);
        };
    function freshDefault(){
        // document.getElementById("file").addEventListener("change",function () {
                
  //      });
        var files = document.getElementById("file").files;
        var file;
        if(files.length) {
            file = files[0];
        }
        var input = document.getElementById("curFile");
        input.setAttribute("placeholder", String(file.name));
        input.setAttribute('class', 'form-control');
        console.log("changessss");
    }
    //清空table
    function clearTB(){ 
        tableObj = document.getElementById("tbTop10");
        rowcount = tableObj.rows.length;
        for(i=rowcount  - 1;i > 0; i--){
           tableObj.deleteRow(i);
        }
    };