$(document).ready(function(){ 
    //生成密钥
    $("#elgamal-genkey").click(function(){
        var data = {
            "type":"genkey",
            "par_d":"", 
        };
        //前后端交互
        $.ajax({
            url: '/elgamal-data',
            type:'POST',
            data: data,
            dataType:'json',
            success:function(data){ //后端返回的json数据（此处data为json对象）
                document.getElementById("par_d").value=data["par_d"];
            },
            error:function () {
                alert("生成密钥失败！！！！");
            }
        });
    });
    //清空密钥
    $("#elgamal-clearkey").click(function(){
        document.getElementById("par_d").value="";
    });
    //清空明文密文
    $("#elgamal-clear").click(function(){
        document.getElementById("message1").value="";
        document.getElementById("ciphertext").value="";
        document.getElementById("message2").value="";
    });
    //加密
    $("#elgamal-encode").click(function(){
        var data = {
            "type":"encode",
            "par_d": document.getElementById("par_d").value,
            "message": document.getElementById("message1").value,
            "ciphertext1":"" 
        };
        //前后端交互
        $.ajax({
            url: '/elgamal-data',
            type:'POST',
            data: data,
            dataType:'json',
            success:function(data){ //后端返回的json数据（此处data为json对象）
                document.getElementById("ciphertext").value=data["ciphertext1"];
            },
            error:function () {
                // document.getElementById("ciphertext").value="error";
                alert("加密出现问题，请检查密钥及明文！！！！");
            }
        });
    });
    //解密
    $("#elgamal-decode").click(function(){
        var data = {
            "type":"decode",
            "par_d": document.getElementById("par_d").value,
            "message": "",
            "ciphertext1":document.getElementById("ciphertext").value, 
        };
        // alert(data["par_d"]);
        //前后端交互
        $.ajax({
            url: '/elgamal-data',
            type:'POST',
            data: data,
            dataType:'json',
            success:function(data){ //后端返回的json数据（此处data为json对象）
                document.getElementById("message2").value=data["message"];
            },
            error:function () {
                // document.getElementById("message1").value="error"
                alert("解密出现问题，请检查密钥及密文！！！！");
            }
        });
    });
}); 