var serviceMapping = {
    "progress_to_rj_bridge" : "progress_to_rj_bridge",
    "rj_to_soa_bridge" : "rj_to_soa_bridge",
    "backoffice" : "backoffice",
    "tomcat6" : "tomcat6",
    "httpd" : "httpd",
    "mysqld" : "mysqld",
    "mysql": "mysql",
    "lolsgmb" : "lolsgmb",
    "ntpd" : "ntpd",
    "specseodd" : "specseodd",
    "xmlexport" : "xmlexport",
    "sgmb" : "sgmb",
    "ccApp" : "ccApp",
    "vnc" : "vnc",
    "transitionComponentContainer": "transitionComponentContainer",
    "aristotleContainer": "aristotleContainer",
    "aristotleBroker": "aristotleBroker"
};

var envMapping = {
    "server": "1",
    "testroom": "80",
    "dispense": "13",
    "till": "50",
    "lop": "69"
};

function sendStartStopRequest(url_val){
    //url_val = "/service/" + service + "/" + action + "/" + domain + "/" + third_octet + "/" + env
    var serviceStatusResponse = $.ajax({cache: false, url: url_val , dataType: "text"});
}

function handleClick(domain, third_octet, env, service){
    selector = "#" + domain + third_octet + envMapping[env]
    var value = $(selector + " ." + service + " .action").text();
    if( value == "stop" ){
        $(selector + " ." + service + " .action").text("stopping");
        $(selector + " ." + service + " .status").text("stopping").removeClass("bgred bggreen").addClass("bgyellow");;
        url_val = "/service/socrates/" + service + "/stop/" + domain + "/" + third_octet + "/" + env
        sendStartStopRequest(url_val);
    }else if(value == "start"){
        $(selector + " ." + service + " .action").text("starting");
        $(selector + " ." + service + " .status").text("starting").removeClass("bgred bggreen").addClass("bgyellow");
        url_val = "/service/socrates/" + service + "/start/" + domain + "/" + third_octet + "/" + env
        sendStartStopRequest(url_val);
    }
}
// Aristotle click handler
function handleAristoClick(domain, service){
    selector = "#" + domain
    var value = $(selector + " ." + service + " .action").text();
    if( value == "stop" ){
        $(selector + " ." + service + " .action").text("stopping");
        $(selector + " ." + service + " .status").text("stopping").removeClass("bgred bggreen").addClass("bgyellow");;
        url_val = "/service/aristotle/" + service + "/stop/49"
        sendStartStopRequest(url_val);
    }else if(value == "start"){
        $(selector + " ." + service + " .action").text("starting");
        $(selector + " ." + service + " .status").text("starting").removeClass("bgred bggreen").addClass("bgyellow");
        url_val = "/service/aristotle/" + service + "/start/49"
        sendStartStopRequest(url_val);
    }
}

//function updatePingStatus(status){
//    var i = 0;
//    var value = '';
//    var env = ['soc29', 'soc2980', 'soc2913', 'soc2950', 'soc2969', 'plato25','aristotle','solar7sok'];
//    while(env[i]){
//        value = env[i];
//        curStatus = status[value]
//        if (curStatus == "up"){
//            $("#" + value ).removeClass("bgred").addClass("bggreen");
//            if(value == 'soc29'){
//                $("." + value ).removeClass("bgred").addClass("bggreen");
//            }
//        } else if (curStatus == "down"){
//            $("#" + value ).removeClass("bggreen").addClass("bgred");
//            if(value == 'soc29'){
//                $("." + value ).removeClass("bggreen").addClass("bgred");
//            }
//        }
//        i++;
//    }
//
//}

// Update the current service status read from the JSON file
function updateServiceStatus(id, status, env){
    var i = 0;
    var curStatus = "";
    var service = "";
    switch (env) {
    case "server":
        var services = ["progress_to_rj_bridge","rj_to_soa_bridge","backoffice", "tomcat6","httpd","mysqld","lolsgmb","ntpd","specseod","xmlexport","sgmb","ccApp"];
        break;
    case "testroom":
    case "dispense":
        var services = ["backoffice"];
        break;
    case "till":
        var services = ["backoffice","mysqld"];
        break;
    case "lop":
        var services = ["tomcat6","mysql","winvnc4"];
        break;
    case "activemq":
        var services = ["transitionComponentContainer","aristotleContainer","aristotleBroker"];
        break;
    }

    while (services[i]) {
        value = services[i];
        service = serviceMapping[value];
        cur_env = status[env]
        curStatus =  cur_env[value]; // Get the current status value from JSON
        if (curStatus == "running"){
            $(id + " ." + service + " .status").text("running").removeClass("bgred bgyellow").addClass("bggreen");
            $(id + " ." + service + " .action").text("stop");
        } else if (curStatus == "stopped"){
            $(id + " ." + service + " .status").text("stopped").removeClass("bggreen bgyellow").addClass("bgred");
            $(id + " ." + service + " .action").text("start");
        }else if ( curStatus == "starting" || curStatus == "stopping" ){
            $(id + " ." + service + " .status").text(curStatus).removeClass("bggreen bgred").addClass("bgyellow");
            $(id + " ." + service + " .action").text(curStatus);
        }else{
            $(id + " ." + service + " .status").text("NA").removeClass("bggreen bgred").addClass("bgyellow");
            $(id + " ." + service + " .action").text("NA");
            }
        i++;
    }
}
$(function(){

    // Handling clicks
    // server - 10.34.29.1
    $("#soc29 .progress_to_rj_bridge .action").click(function(){handleClick("soc","29", "server", "progress_to_rj_bridge");});
    $("#soc29 .rj_to_soa_bridge .action").click(function(){handleClick("soc","29", "server", "rj_to_soa_bridge");});
    $("#soc29 .backoffice .action").click(function(){handleClick("soc","29", "server", "backoffice");});
    $("#soc29 .tomcat6 .action").click(function(){handleClick("soc","29", "server", "tomcat6");});
    $("#soc29 .httpd .action").click(function(){handleClick("soc","29", "server", "httpd");});
    $("#soc29 .mysqld .action").click(function(){handleClick("soc","29", "server", "mysqld");});
    $("#soc29 .lolsgmb .action").click(function(){handleClick("soc","29", "server", "lolsgmb");});
    $("#soc29 .ntpd .action").click(function(){handleClick("soc","29", "server", "ntpd");});
    $("#soc29 .specseodd .action").click(function(){handleClick("soc","29", "server", "specseodd");});
    $("#soc29 .xmlexport .action").click(function(){handleClick("soc","29", "server", "xmlexport");});
    $("#soc29 .sgmb .action").click(function(){handleClick("soc","29", "server", "sgmb");});
    $("#soc29 .ccApp .action").click(function(){handleClick("soc","29", "server", "ccApp");});
    $("#soc29 .progress .action").click(function(){handleClick("soc","29", "server", "progress");});
    // Testroom - 10.34.29.80
    $("#soc2380 .backoffice .action").click(function(){handleClick("soc", "29" , "testroom", "backoffice");});
    // dispense - 10.34.29.13
    $("#soc2313 .backoffice .action").click(function(){handleClick("soc", "29" , "dispense", "backoffice");});
    // Till - 10.34.29.50
    $("#soc2350 .backoffice .action").click(function(){handleClick("soc", "29" , "till", "backoffice");});
    $("#soc2350 .mysqld .action").click(function(){handleClick("soc", "29" , "till", "mysqld");});
    // lop - 10.34.29.69
    $("#soc2969 .mysql .action").click(function(){handleClick("soc", "29" , "lop", "mysql");});
    $("#soc2969 .tomcat6 .action").click(function(){handleClick("soc", "29" , "lop", "tomcat6");});
    $("#soc2969 .vnc .action").click(function(){handleClick("soc", "29" , "lop", "vnc");});
    // Handle Aristotle click events
    //$("#aristotle .transitionComponentContainer .action").click(function(){handleAristoClick("aristotle", "transitionComponentContainer");});
    //$("#aristotle .aristotleContainer .action").click(function(){handleAristoClick("aristotle", "aristotleContainer");});
    //$("#aristotle .aristotleBroker .action").click(function(){handleAristoClick("aristotle", "aristotleBroker");});
    // Refreshing the status
    setInterval(function() {
        var pingStatusResponse = $.ajax({cache: false, url: '../static/data/ping.json', dataType: "text"});
        var socServiceStatusResponse = $.ajax({cache: false, url: '../static/data/soc29.json', dataType: "text"});
        var aristotleServiceStatusResponse = $.ajax({cache: false, url: '../static/data/aristotle49.json', dataType: "text"});
        pingStatusResponse.done(function(data) {
            var status = $.parseJSON(data);
            updatePingStatus(status);
            }
        );
        socServiceStatusResponse.done(function(data) {
            var status = $.parseJSON(data);
            updateServiceStatus("#soc29", status, "server");
            updateServiceStatus("#soc2980", status, "testroom");
            updateServiceStatus("#soc2913", status, "dispense");
            updateServiceStatus("#soc2950", status, "till");
            updateServiceStatus("#soc2969", status, "lop");
            }
        );
        aristotleServiceStatusResponse.done(function(data) {
            var status = $.parseJSON(data);
            updateServiceStatus("#aristotle", status, "activemq");
            }
        );
    },1000000);

});
