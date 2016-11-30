$(document).ready(function(){
    $.get("/api/profile/auth",function(data){
        if("0" == data.errno){
            $(".auth-warn").hide();
        }
    })
    
})
