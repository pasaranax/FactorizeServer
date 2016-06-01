function request(number){
    // Отправляет запрос на сервер через ajax. session id берет из куки или он генерируется сервером
    // number: обработать число и получить данные

    if(number === undefined){
        number = 0;
    }
    
    var query = "/factorize?number=" + number;
    $.getJSON(query, function(data){
        var answer = "";
        if(data[0] !== undefined){
            $.cookie("sid", data[0][0], {path: "/"});
            for(var i=0; i<data.length; i++) {
                answer += data[i][1] + ": " + data[i][2] + " (" + data[i][3] + " s)\n";
            }
            $(".answer").text(answer);
        }
    }).done(function(){
        $(".loading").hide();
    });
}
