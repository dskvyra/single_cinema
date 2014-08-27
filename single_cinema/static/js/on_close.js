    $(window).unload(function() {
        $.get("/stop", function(){
           alert("success");
        });
    });
