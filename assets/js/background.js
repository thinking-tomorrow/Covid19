$(document).ready(function (){
    cases = $("#cases").text()

    if(cases > 100000){
        $('#data').css("background-size", "cover")
        $("#data").css("color", "white")
    
        $('#data').css('background-image', 'url(../static/images/background_1.jpg)')
    }
    // else if(cases > 50000)
    //     $('body').css('background-image', 'url(../static/images/background_2.png)')
    // else if(total > 10000)
    //     $('body').css('background-image', 'url(../static/images/background_3.png)') 
    // else if(total > 5000)
    //   $(row).css("background-color", "rgba(255, 255, 0, 0.3)")
    // else if(total > 1000)
    //   $(row).css("background-color", "rgba(255, 255, 0, 0.1)")
    // else
    //   $(row).addClass('table-success')
});