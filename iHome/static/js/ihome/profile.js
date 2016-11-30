function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get("/api/profile",function(data){
      if("4101" == data.errno){
        location.href = "/login.html"
      }
      else if ("0" == data.errno){
          $("#user-name").val(data.data.name);
          if (data.data.avatar_url){
              $("#user-avatar").attr("src",data.data.avatar_url);
        }
      }
    });

    $("#form-avatar").submit(function(event){
        event.preventDefault();
        $('.image_uploading').fadeIn('fast');
        $(this).ajaxSubmit({
            url:"/api/profile/avatar",
            type:"post",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success:function(data){
                if ("0" == data.errno){
                    $('.image_uploading').fadeOut('fast');
                    $("#user-avatar").attr("src", data.data.pic_url);
                }
                else if ("4101" == data.errno){
                    location.href = "/login.html";
                }
            }
        });
    });
    $("#form-name").submit(function(event){
        event.preventDefault();
        var data = {};
        $(this).serializeArray().map(function(x){data[x.name] = x.value;});
        var json_data = JSON.stringify(data);
        $.ajax({
            url:"/api/profile/name",
            type:"post",
            data:json_data,
            contentType: "application/json",
            dataType:"json",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success:function(data){
                if ("4101" == data.errno){
                    lacation.href = "/login.html"
                }
                else if ("0" == data.errno){
                    $(".error-msg").hide()
                    $("#user-name").prop("disabled", true);
                    $("#form-name>input[type=submit]").prop("disabled", true);
                    showSuccessMsg();
                }
                else if ("4001" == data.errno || "4103" == data.errno){
                    $(".error-msg").show()
                    $(".error-msg").html(data.errmsg)
                }
            }
        })

    })
});
