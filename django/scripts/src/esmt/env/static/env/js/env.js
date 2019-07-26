function check_any_services_down(services){
    var bool = false;
    $.each(services, function(service, status){
        if (status == "stopped"){
            bool = true;
            return false;
        }
    });
    if (bool){
        return true;
    }else{
        return false;
    }

}
// Update the current service status read from the JSON file
function updateTabServiceStatus(store, data){
    var env = store.split("-")[0];
    //var clients = data[Object.keys(data)];
    $.each(data, function(client, services){
        if ( env == "solar7"){
             var id = "#" + store + "-panel";
        }else{
            var id = "#" + store + "-" + client;
        }
        $.each(services, function(service, status){
            if (service == "ping"){
                if( status == "up" ){
                     if (check_any_services_down(services)){
                        $("[href='" + id + "'] span").removeClass("glyphicon-triangle-bottom glyphicon-triangle-top text-danger text-success").addClass("glyphicon-resize-horizontal text-warning")
                     }else{
                        $("[href='" + id + "'] span").removeClass("glyphicon-triangle-bottom glyphicon-resize-horizontal text-warning text-danger").addClass("glyphicon-triangle-top text-success")
                     }
                     if (client == "server" || env == "solar7"){
                         $("[href='#" + store  + "']").removeClass("btn-danger").addClass("btn-success").html("Service Details");
                     }
                }else if( status == "down"){
                     $("[href='" + id + "'] span").removeClass("glyphicon-triangle-top text-success").addClass("glyphicon-triangle-bottom text-danger")
                     if (client == "server" || env == "solar7"){
                         $("[href='#" + store  + "']").removeClass("btn-success").addClass("btn-danger").html("Server Down");
                     }
                }
            }
            //console.log(service);
            //console.log(status);
            if ( status == "running" ){
                $(id + " ." + service + " .status").removeClass("btn-danger  bgYellow progress-bar-striped").addClass("btn-success").attr("aria-status","running");
                $(id + " ." + service + " .action span").removeClass("glyphicon-play text-success glyphicon-ban-circle text-warning").addClass("glyphicon-stop text-danger").attr("data-original-title","stop");
                $(id + " ." + service + " .action").attr("ng-disabled","false").attr("data-original-title","stop");
            } else if ( status == "stopped" ){
                $(id + " ." + service + " .status").removeClass("btn-success  bgYellow progress-bar-striped").addClass("btn-danger").attr("aria-status","stopped");
                $(id + " ." + service + " .action span").removeClass("glyphicon-stop text-danger glyphicon-ban-circle text-warning").addClass("glyphicon-play text-success");
                $(id + " ." + service + " .action").attr("ng-disabled","false").attr("data-original-title","start");
            }else if ( status == "starting" ){
                $(id + " ." + service + " .status").removeClass("btn-danger bgYellow progress-bar-striped").addClass("btn-success  progress-bar-striped").attr("aria-status","starting");;
                $(id + " ." + service + " .action span").removeClass("glyphicon-play text-success glyphicon-stop text-danger").addClass("glyphicon-ban-circle text-warning");
                $(id + " ." + service + " .action").attr("ng-disabled","true").attr("data-original-title","starting");
            }else if ( status == "stopping" ){
                $(id + " ." + service + " .status").removeClass("btn-success bgYellow progress-bar-striped").addClass("btn-danger  progress-bar-striped").attr("aria-status","stopping");
                $(id + " ." + service + " .action span").removeClass("glyphicon-play text-success glyphicon-stop text-danger").addClass("glyphicon-ban-circle text-warning");
                $(id + " ." + service + " .action").attr("ng-disabled","true").attr("data-original-title","starting");
            }else{
                $(id + " ." + service + " .status").removeClass("btn-danger  btn-success progress-bar-striped").addClass("bgYellow").attr("aria-status","unrecognized_service");;
                $(id + " ." + service + " .action span").removeClass("glyphicon-play text-success glyphicon-stop text-danger").addClass("glyphicon-ban-circle text-warning");
                $(id + " ." + service + " .action").attr("data-original-title","unrecognized_service");;
            }
        });

    });

}

var handleClick;
$(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

