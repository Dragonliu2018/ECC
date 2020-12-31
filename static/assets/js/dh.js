$(document).ready(function(){ 
    //清空明文密文
    $("#dh-clear").click(function(){
        document.getElementById("messageA").value="";
        document.getElementById("ciphertextA").value="";
        document.getElementById("messageB").value="";
    });
    //清空密钥
    $("#dh-clearkey").click(function(){
        document.getElementById("public_keyA").value="";
        document.getElementById("private_keyA").value="";
        document.getElementById("public_keyB").value="";
        document.getElementById("private_keyB").value="";
        document.getElementById("keyAB").value="";
    });
    //生成密钥
    $("#dh-genkey").click(function(){
        var data = {
            "type":"genkey",
            "private_keyA":"", 
            "public_keyA":"", 
            "private_keyB":"", 
            "public_keyB":"", 
            "keyAB":"", 
        };
        //前后端交互
        $.ajax({
            url: '/dh-data',
            type:'POST',
            data: data,
            dataType:'json',
            success:function(data){ //后端返回的json数据（此处data为json对象）
                document.getElementById("private_keyA").value=data["private_keyA"];
                document.getElementById("public_keyA").value=data["public_keyA"];
                document.getElementById("private_keyB").value=data["private_keyB"];
                document.getElementById("public_keyB").value=data["public_keyB"];
                document.getElementById("keyAB").value=data["keyAB"];
            },
            error:function () {
                alert("生成密钥失败！！！！");
            }
        });
    });
    //测试传输信息
    $("#dh-test").click(function(){
        var data = {
            "type":"test",
            "keyAB":document.getElementById("keyAB").value, 
            "messageA":document.getElementById("messageA").value, 
            "ciphertextA":"", 
            "messageB":"", 
        };
        //前后端交互
        $.ajax({
            url: '/dh-data',
            type:'POST',
            data: data,
            dataType:'json',
            success:function(data){ //后端返回的json数据（此处data为json对象）
                document.getElementById("ciphertextA").value=data["ciphertextA"];
                document.getElementById("messageB").value=data["messageB"];
            },
            error:function () {
                alert("测试出现问题，请检查密钥及明文！！！！");
            }
        });
    });
}); 