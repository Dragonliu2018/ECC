var differentindex = 999;
$(document).ready(function(){ 
    //清空明文密文
    $(".teacher").hover(function() {
        // alert("666");
        openMsg();
    }, function() {
        layer.close(differentindex);
    });
}); 
function openMsg() {
    differentindex = layer.tips('点击分类内容项，可查看下一级机构账户统计情况', '.name', {
      tips: [1, '#3595CC'],
      time: 30000
    });
}