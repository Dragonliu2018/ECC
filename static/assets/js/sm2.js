$(document).ready(function(){ 
    //表单检查
    // $("#form-check").bootstrapValidator({
    //     message:'This value is not valid',
    //     //   定义未通过验证的状态图标
    //     feedbackIcons: {/*输入框不同状态，显示图片的样式*/
    //         valid: 'glyphicon glyphicon-ok',
    //         invalid: 'glyphicon glyphicon-remove',
    //         validating: 'glyphicon glyphicon-refresh'
    //     },
    //     //   字段验证
    //     fields:{
    //         //   用户名
    //         par_a1:{
    //             message:'用户名非法',
    //             validators:{
    //                 // 非空
    //                 notEmpty:{
    //                     message:'用户名不能为空'
    //                 },
    //                 //限制字符串长度
    //                 stringLength:{
    //                     min:3,
    //                     max:20,
    //                     message:'用户名长度必须位于3到20之间'
    //                 },
    //                 //基于正则表达是的验证
    //                 regexp:{
    //                     regexp:/^[a-zA-Z0-9_\.]+$/,
    //                     message:'用户名由数字字母下划线和.组成'
    //                 }
    //             }
    //         },
    //     }
    // });   
    //模态框钩子
    $('#staticBackdrop2').on('show.bs.modal', function () {
        // 执行一些动作...
        document.getElementById("demo2").innerHTML="666";
    })
    //生成密钥
    $("#sm2-genkey").click(function(){
        document.getElementById("public_key").value="B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207";
        document.getElementById("private_key").value="00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5"; 
    });
    //清空密钥
    $("#sm2-clearkey").click(function(){
        document.getElementById("public_key").value="";
        document.getElementById("private_key").value="";
    });
    //清空明文密文
    $("#sm2-clear").click(function(){
        document.getElementById("message1").value="";
        document.getElementById("ciphertext").value="";
        document.getElementById("message2").value="";
    });
    //算法过程
    $("#sm2-detail").click(function(){
        var data = {
            "type":"detail",
            "public_key": document.getElementById("public_key").value,
            "private_key": document.getElementById("private_key").value,
            "message": document.getElementById("message1").value,
            "ret_message":"",
        };
        // layer.alert("6666");
        $.ajax({
            url: '/sm2-data',
            type:'POST',
            data: data,
            dataType:'json',
            success:function(data){ //后端返回的json数据（此处data为json对象）
                // layer.alert(data["ret_message"]);
                // alert(data["ret_message"]);
                document.getElementById('carouselExampleIndicators').hidden = false;
                document.getElementById("demo").innerHTML=data["ret_message"];
            },
            error:function () {
                // alert("算法求解过程出现问题，请检查密钥及明文！！！！");
                document.getElementById("demo").innerHTML="算法求解过程出现问题，请检查密钥及明文！！！！";
                document.getElementById('carouselExampleIndicators').hidden = true;
            }
        });
    });
    //加密
    $("#sm2-encode").click(function(){
        // $("#form-check").bootstrapValidator('validate');//提交验证
        // if ($("#form-check").data('bootstrapValidator').isValid()) {//获取验证结果，如果成功，执行下面代码
        //     alert("yes");//验证成功后的操作，如ajax
        // }
        // else{
        //     alert("no");//验证成功后的操作，如ajax
        // }
        var data = {
            "type":"encode",
            "public_key": document.getElementById("public_key").value,
            "private_key": document.getElementById("private_key").value,
            "message": document.getElementById("message1").value,
            "ciphertext1":"" 
        };
        // alert(data["par_a"]);
        //前后端交互
        $.ajax({
            url: '/sm2-data',
            type:'POST',
            data: data,
            dataType:'json',
            success:function(data){ //后端返回的json数据（此处data为json对象）
                // document.getElementById('staticBackdrop2').hidden = true;
                document.getElementById("ciphertext").value=data["ciphertext1"]; 
            },
            error:function () {
                // document.getElementById('staticBackdrop2').hidden = false;
                // document.getElementById("ciphertext").value="error";
                alert("加密出现问题，请检查密钥及明文！！！！");
                // $('.alert').alert("加密出现问题，请检查密钥及明文！！！！")
                // document.getElementById("demo2").innerHTML="加密出现问题，请检查密钥及明文！！！！";
            }
        });
    });
    //解密
    $("#sm2-decode").click(function(){
        // $("#form-check").bootstrapValidator('validate');//提交验证
        // if ($("#form-check").data('bootstrapValidator').isValid()) {//获取验证结果，如果成功，执行下面代码
        //     alert("yes");//验证成功后的操作，如ajax
        // }
        // else{
        //     alert("no");//验证成功后的操作，如ajax
        // }
        var data = {
            "type":"decode",
            "public_key": document.getElementById("public_key").value,
            "private_key": document.getElementById("private_key").value,
            "message": "",
            "ciphertext1":document.getElementById("ciphertext").value, 
        };
        // alert(data["par_a"]);
        //前后端交互
        $.ajax({
            url: '/sm2-data',
            type:'POST',
            data: data,
            dataType:'json',
            success:function(data){ //后端返回的json数据（此处data为json对象）
                document.getElementById("message2").value=data["message"];
            },
            error:function () {
                // document.getElementById("message2").value="error"
                alert("解密出现问题，请检查密钥及密文！！！！");
                // document.getElementById("demo2").innerHTML="解密出现问题，请检查密钥及明文！！！！";
            }
        });
    });
}); 
//算法效率
var chart_23850920fbc84b4dbd149238e7d75d4b = echarts.init(
    document.getElementById('23850920fbc84b4dbd149238e7d75d4b'), 'light', {renderer: 'canvas'});
var option_23850920fbc84b4dbd149238e7d75d4b = {
"animation": true,
"animationThreshold": 2000,
"animationDuration": 1000,
"animationEasing": "cubicOut",
"animationDelay": 0,
"animationDurationUpdate": 300,
"animationEasingUpdate": "cubicOut",
"animationDelayUpdate": 0,
"series": [
{
    "type": "bar",
    "name": "RSA",
    "legendHoverLink": true,
    "data": [
        182.57926,
        3.23636,
        106.98003,
        1.89631,
        53.49002,
        0.94815
    ],
    "showBackground": false,
    "barMinHeight": 0,
    "barCategoryGap": "20%",
    "barGap": "30%",
    "large": false,
    "largeThreshold": 400,
    "seriesLayoutBy": "column",
    "datasetIndex": 0,
    "clip": true,
    "zlevel": 0,
    "z": 2,
    "label": {
        "show": true,
        "position": "top",
        "margin": 8
    }
},
{
    "type": "bar",
    "name": "SM2",
    "legendHoverLink": true,
    "data": [
        45.36191,
        45.25977,
        26.57925,
        26.5194,
        13.28962,
        13.2597
    ],
    "showBackground": false,
    "barMinHeight": 0,
    "barCategoryGap": "20%",
    "barGap": "30%",
    "large": false,
    "largeThreshold": 400,
    "seriesLayoutBy": "column",
    "datasetIndex": 0,
    "clip": true,
    "zlevel": 0,
    "z": 2,
    "label": {
        "show": true,
        "position": "top",
        "margin": 8
    }
}
],
"legend": [
{
    "data": [
        "RSA",
        "SM2"
    ],
    "selected": {
        "RSA": true,
        "SM2": true
    },
    "show": true,
    "padding": 5,
    "itemGap": 10,
    "itemWidth": 25,
    "itemHeight": 14
}
],
"tooltip": {
"show": true,
"trigger": "item",
"triggerOn": "mousemove|click",
"axisPointer": {
    "type": "line"
},
"showContent": true,
"alwaysShowContent": false,
"showDelay": 0,
"hideDelay": 100,
"textStyle": {
    "fontSize": 14
},
"borderWidth": 0,
"padding": 5
},
"xAxis": [
{
    "show": true,
    "scale": false,
    "nameLocation": "end",
    "nameGap": 15,
    "gridIndex": 0,
    "inverse": false,
    "offset": 0,
    "splitNumber": 5,
    "minInterval": 0,
    "splitLine": {
        "show": false,
        "lineStyle": {
            "show": true,
            "width": 1,
            "opacity": 1,
            "curveness": 0,
            "type": "solid"
        }
    },
    "data": [
        "1MB\u52a0\u5bc6(min)",
        "1MB\u89e3\u5bc6(min)",
        "10KB\u52a0\u5bc6(s)",
        "10KB\u89e3\u5bc6(s)",
        "5\u5b57\u8282\u52a0\u5bc6(ms)",
        "5\u5b57\u8282\u89e3\u5bc6(ms)"
    ]
}
],
"yAxis": [
{
    "show": true,
    "scale": false,
    "nameLocation": "end",
    "nameGap": 15,
    "gridIndex": 0,
    "inverse": false,
    "offset": 0,
    "splitNumber": 5,
    "minInterval": 0,
    "splitLine": {
        "show": false,
        "lineStyle": {
            "show": true,
            "width": 1,
            "opacity": 1,
            "curveness": 0,
            "type": "solid"
        }
    }
}
],
"title": [
{
    "text": "\u0053\u004d\u0032\u4e0e\u0052\u0053\u0041\u6548\u7387\u5bf9\u6bd4\u000d\u000a",
    "padding": 5,
    "itemGap": 10
}
]
};
chart_23850920fbc84b4dbd149238e7d75d4b.setOption(option_23850920fbc84b4dbd149238e7d75d4b);
//sm2&elgamal
var chart_794d3ce7349e4717a3b47565cfb7fea2 = echarts.init(
    document.getElementById('794d3ce7349e4717a3b47565cfb7fea2'), 'light', {renderer: 'canvas'});
var option_794d3ce7349e4717a3b47565cfb7fea2 = {
"animation": true,
"animationThreshold": 2000,
"animationDuration": 1000,
"animationEasing": "cubicOut",
"animationDelay": 0,
"animationDurationUpdate": 300,
"animationEasingUpdate": "cubicOut",
"animationDelayUpdate": 0,
"series": [
{
    "type": "bar",
    "name": "ELGamal",
    "legendHoverLink": true,
    "data": [
        170.27231,
        0.35886,
        99.76893,
        0.21027,
        49.88446,
        0.10513
    ],
    "showBackground": false,
    "barMinHeight": 0,
    "barCategoryGap": "20%",
    "barGap": "30%",
    "large": false,
    "largeThreshold": 400,
    "seriesLayoutBy": "column",
    "datasetIndex": 0,
    "clip": true,
    "zlevel": 0,
    "z": 2,
    "label": {
        "show": true,
        "position": "top",
        "margin": 8
    }
},
{
    "type": "bar",
    "name": "SM2",
    "legendHoverLink": true,
    "data": [
        44.84356,
        44.75841,
        26.27552,
        26.22563,
        13.13776,
        13.11281
    ],
    "showBackground": false,
    "barMinHeight": 0,
    "barCategoryGap": "20%",
    "barGap": "30%",
    "large": false,
    "largeThreshold": 400,
    "seriesLayoutBy": "column",
    "datasetIndex": 0,
    "clip": true,
    "zlevel": 0,
    "z": 2,
    "label": {
        "show": true,
        "position": "top",
        "margin": 8
    }
}
],
"legend": [
{
    "data": [
        "ELGamal",
        "SM2"
    ],
    "selected": {
        "ELGamal": true,
        "SM2": true
    },
    "show": true,
    "padding": 5,
    "itemGap": 10,
    "itemWidth": 25,
    "itemHeight": 14
}
],
"tooltip": {
"show": true,
"trigger": "item",
"triggerOn": "mousemove|click",
"axisPointer": {
    "type": "line"
},
"showContent": true,
"alwaysShowContent": false,
"showDelay": 0,
"hideDelay": 100,
"textStyle": {
    "fontSize": 14
},
"borderWidth": 0,
"padding": 5
},
"xAxis": [
{
    "show": true,
    "scale": false,
    "nameLocation": "end",
    "nameGap": 15,
    "gridIndex": 0,
    "inverse": false,
    "offset": 0,
    "splitNumber": 5,
    "minInterval": 0,
    "splitLine": {
        "show": false,
        "lineStyle": {
            "show": true,
            "width": 1,
            "opacity": 1,
            "curveness": 0,
            "type": "solid"
        }
    },
    "data": [
        "1MB\u52a0\u5bc6(min)",
        "1MB\u89e3\u5bc6(min)",
        "10KB\u52a0\u5bc6(s)",
        "10KB\u89e3\u5bc6(s)",
        "5\u5b57\u8282\u52a0\u5bc6(ms)",
        "5\u5b57\u8282\u89e3\u5bc6(ms)"
    ]
}
],
"yAxis": [
{
    "show": true,
    "scale": false,
    "nameLocation": "end",
    "nameGap": 15,
    "gridIndex": 0,
    "inverse": false,
    "offset": 0,
    "splitNumber": 5,
    "minInterval": 0,
    "splitLine": {
        "show": false,
        "lineStyle": {
            "show": true,
            "width": 1,
            "opacity": 1,
            "curveness": 0,
            "type": "solid"
        }
    }
}
],
"title": [
{
    "text": "\u0053\u004d\u0032\u4e0e\u0045\u006c\u0047\u0061\u006d\u0061\u006c\u6548\u7387\u5bf9\u6bd4\u000d\u000a",
    "padding": 5,
    "itemGap": 10
}
]
};
chart_794d3ce7349e4717a3b47565cfb7fea2.setOption(option_794d3ce7349e4717a3b47565cfb7fea2);