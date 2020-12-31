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
                document.getElementById("ciphertext").value=data["ciphertext1"];
            },
            error:function () {
                document.getElementById("ciphertext").value="error";
                alert("加密出现问题，请检查密钥及明文！！！！");
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
                document.getElementById("message1").value=data["message"];
            },
            error:function () {
                document.getElementById("message1").value="error"
                alert("解密出现问题，请检查密钥及密文！！！！");
            }
        });
    });
}); 